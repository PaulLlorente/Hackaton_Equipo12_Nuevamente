"""Prompts v1.0 del Issue #15 y contrato propuesto para el orquestador.

El servidor debe autorizar tenant/documento ANTES de recuperar evidencia.
Estas comprobaciones de alcance son una segunda barrera, no autenticación.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator

from backend.src.api.models.schemas import Flashcards, Guion, Quiz, Resumen

PROMPT_VERSION = "1.0"
Profile = Literal["principiante", "avanzado"]
OutputFormat = Literal["resumen", "flashcard", "quiz", "guion"]
_MODELS = {"resumen": Resumen, "flashcard": Flashcards, "quiz": Quiz, "guion": Guion}
_TEMPLATES = Path(__file__).with_name("templates")


class PromptRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["1.0"] = "1.0"
    documento_titulo: str = Field(min_length=1, max_length=500)
    perfil_destinatario: Profile
    formato_salida: OutputFormat
    nicho_sector: str | None = Field(default=None, min_length=1, max_length=200)
    nivel_detalle: Literal["breve", "detallado"] = "breve"
    objetivo: str = Field(min_length=1, max_length=2000)
    tenant_id: str = Field(min_length=1, max_length=200)
    document_id: str = Field(min_length=1, max_length=200)


class EvidenceChunk(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    chunk_id: str = Field(min_length=1, max_length=500)
    tenant_id: str = Field(min_length=1, max_length=200)
    document_id: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1)
    section_title: str | None = None
    page_start: int | None = Field(default=None, ge=1, strict=True)
    page_end: int | None = Field(default=None, ge=1, strict=True)

    @model_validator(mode="after")
    def validate_pages(self) -> EvidenceChunk:
        if (self.page_start is None) != (self.page_end is None):
            raise ValueError("Las páginas deben estar ambas presentes o ambas ausentes")
        if self.page_start is not None and self.page_end < self.page_start:
            raise ValueError("page_end debe ser mayor o igual a page_start")
        return self


class AdaptationRequest(PromptRequest):
    """Contrato INTERNO backend → prompts; los IDs ya deben estar autorizados."""

    evidencia: list[EvidenceChunk]


def build_from_contract(
    value: str | Mapping[str, Any] | AdaptationRequest,
    *,
    max_context_chars: int = 24000,
    max_chunks: int = 20,
) -> PromptBundle:
    """Valida el contrato v1.0 completo y prepara mensajes sin llamar al LLM."""
    contract = (
        value if isinstance(value, AdaptationRequest)
        else AdaptationRequest.model_validate_json(value) if isinstance(value, str)
        else AdaptationRequest.model_validate(value)
    )
    request = PromptRequest.model_validate(contract.model_dump(exclude={"evidencia"}))
    return build_prompt(request, contract.evidencia,
                        max_context_chars=max_context_chars, max_chunks=max_chunks)


def evidence_from_record(record: Mapping[str, Any]) -> EvidenceChunk:
    """Acepta registros JSONL o resultados de search_index, sin perder alcance.

    Rechaza duplicados contradictorios entre los campos superiores y metadata.
    Para un Document de LangChain: pasar {**doc.metadata, 'text': doc.page_content}.
    El retriever debe conservar chunk_id en metadata.
    """
    if not isinstance(record, Mapping):
        raise ValueError("Cada chunk debe ser un objeto")
    metadata = record.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise ValueError("metadata debe ser un objeto")
    fields = ("chunk_id", "tenant_id", "document_id", "section_title", "page_start", "page_end")
    values = {}
    for field in fields:
        if field in record and field in metadata and record[field] != metadata[field]:
            raise ValueError(f"Metadatos contradictorios: {field}")
        if field in record or field in metadata:
            values[field] = record[field] if field in record else metadata[field]
    return EvidenceChunk(text=record.get("text"), **values)


class _ResponseBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version_prompt: Literal["1.0"]
    perfil: Profile
    estado: Literal["ok", "evidencia_insuficiente"]
    fuentes_usadas: list[str]
    advertencias: list[str]


@lru_cache(maxsize=4)
def response_model(output_format: OutputFormat) -> type[BaseModel]:
    """Reutiliza los cuatro modelos existentes del backend en contenido."""
    return create_model(
        f"Respuesta_{output_format}_v1",
        __base__=_ResponseBase,
        contenido=(_MODELS[output_format] | None, ...),
    )


@dataclass(frozen=True)
class PromptBundle:
    request: PromptRequest
    system_prompt: str
    user_prompt: str
    evidence: tuple[EvidenceChunk, ...]

    @property
    def output_model(self) -> type[BaseModel]:
        return response_model(self.request.formato_salida)

    def insufficient_response(self, reason: str = "No hay evidencia recuperada suficiente.") -> BaseModel:
        """Permite al orquestador abstenerse sin una llamada al proveedor."""
        return self.validate_response({
            "version_prompt": PROMPT_VERSION,
            "perfil": self.request.perfil_destinatario,
            "estado": "evidencia_insuficiente",
            "fuentes_usadas": [],
            "advertencias": [reason],
            "contenido": None,
        })

    @property
    def sources(self) -> dict[str, dict[str, Any]]:
        """Mapa del servidor para convertir referencias F1... en citas reales."""
        return {
            f"F{i}": chunk.model_dump(exclude={"text"})
            for i, chunk in enumerate(self.evidence, 1)
        }

    def validate_response(self, value: str | Mapping[str, Any] | BaseModel) -> BaseModel:
        """Comprueba estructura y referencias; no demuestra fidelidad factual."""
        if isinstance(value, BaseModel):
            value = value.model_dump()
        result = (
            self.output_model.model_validate_json(value)
            if isinstance(value, str)
            else self.output_model.model_validate(value)
        )
        if result.perfil != self.request.perfil_destinatario:
            raise ValueError("El perfil de salida no coincide con la solicitud")
        sources = result.fuentes_usadas
        if len(set(sources)) != len(sources) or not set(sources) <= set(self.sources):
            raise ValueError("La salida contiene fuentes inexistentes o repetidas")
        if result.estado == "evidencia_insuficiente":
            if result.contenido is not None or not result.advertencias or any(
                not warning.strip() for warning in result.advertencias
            ):
                raise ValueError("Sin evidencia: contenido=null y advertencia explicativa obligatorios")
            return result
        if not self.evidence or not sources or result.contenido is None:
            raise ValueError("Una salida ok necesita evidencia, fuentes y contenido")
        content = result.contenido.model_dump()
        _validate_nonempty(content)
        citations = set(re.findall(r"\[(F\d+)\]", json.dumps(content, ensure_ascii=False)))
        if citations != set(sources):
            raise ValueError("Las citas del contenido deben coincidir con fuentes_usadas")
        if "tiempo_estudio" in content and content["tiempo_estudio"] < 1:
            raise ValueError("tiempo_estudio debe ser positivo")
        if self.request.formato_salida == "guion":
            if [scene["numero_escena"] for scene in content["escenas"]] != list(
                range(1, len(content["escenas"]) + 1)
            ):
                raise ValueError("Las escenas deben numerarse consecutivamente desde 1")
        return result


def _validate_nonempty(value: Any) -> None:
    if isinstance(value, str) and not value.strip():
        raise ValueError("El contenido no puede contener texto vacío")
    if isinstance(value, (dict, list)):
        if not value:
            raise ValueError("El contenido no puede contener colecciones vacías")
        for child in value.values() if isinstance(value, dict) else value:
            _validate_nonempty(child)


def build_prompt(
    request: PromptRequest,
    evidence: Sequence[EvidenceChunk],
    *,
    max_context_chars: int = 24000,
    max_chunks: int = 20,
) -> PromptBundle:
    """Prepara mensajes sin inferencia, descargas ni truncamiento silencioso.

    El presupuesto cuenta caracteres del JSON de evidencia, NO tokens.
    El orquestador debe ajustar además su presupuesto al tokenizer del LLM.
    """
    if max_context_chars <= 0 or max_chunks <= 0:
        raise ValueError("Los presupuestos deben ser positivos")
    chunks = tuple(evidence)
    if len(chunks) > max_chunks:
        raise ValueError("Demasiados chunks: ajustar la recuperación antes de generar")
    ids = set()
    payload = []
    for index, chunk in enumerate(chunks, 1):
        if chunk.tenant_id != request.tenant_id or chunk.document_id != request.document_id:
            raise ValueError("La evidencia pertenece a otro tenant o documento")
        if chunk.chunk_id in ids:
            raise ValueError("chunk_id duplicado")
        ids.add(chunk.chunk_id)
        payload.append({"fuente": f"F{index}", **chunk.model_dump(exclude={"tenant_id"})})
    serialized = json.dumps(payload, ensure_ascii=False)
    if len(serialized) > max_context_chars:
        raise ValueError("Contexto demasiado largo: ajustar recuperación o presupuesto explícitamente")
    system = "\n\n".join(
        (_TEMPLATES / name).read_text(encoding="utf-8")
        for name in ("base.md", f"{request.perfil_destinatario}.md",
                     f"detalle_{request.nivel_detalle}.md", "formatos.md")
    )
    system += (f"\n\nPerfil solicitado: {request.perfil_destinatario}. "
               f"Formato solicitado: {request.formato_salida}. "
               f"Detalle solicitado: {request.nivel_detalle}.")
    system += "\nEsquema JSON obligatorio:\n" + json.dumps(
        response_model(request.formato_salida).model_json_schema(), ensure_ascii=False
    )
    user = json.dumps(
        {"documento_titulo": request.documento_titulo, "nicho_sector": request.nicho_sector,
         "objetivo": request.objetivo, "evidencia": payload}, ensure_ascii=False, indent=2
    )
    return PromptBundle(request=request, system_prompt=system, user_prompt=user, evidence=chunks)

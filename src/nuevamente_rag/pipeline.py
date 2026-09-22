"""Pipeline local: contrato de texto limpio, chunking y embeddings.

El módulo mantiene separados los metadatos/textos (JSONL) y la matriz densa
(NPY). La fila N de ``embeddings.npy`` corresponde a la línea N de
``chunks.jsonl``. Este contrato se puede adaptar a ChromaDB sin recalcular los
vectores.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, Sequence

import jsonschema
import numpy as np


DEFAULT_MODEL = "intfloat/multilingual-e5-small"
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_HYPHENATED_LINE_BREAK = re.compile(
    r"(?<=[a-záéíóúüñ])-\n(?=[a-záéíóúüñ])", re.IGNORECASE
)
_SPACE_RUN = re.compile(r"[^\S\n]+")
_BLANK_LINE_RUN = re.compile(r"\n{3,}")
_BOUNDARY_END = re.compile(r"(?:\n\n|[.!?;:][\"'»”’)]*)$")


class Tokenizer(Protocol):
    def __call__(self, text: str, **kwargs: Any) -> dict[str, Any]: ...


class Embedder(Protocol):
    model_name: str
    tokenizer: Tokenizer
    dimension: int

    def embed_documents(self, texts: Sequence[str]) -> np.ndarray: ...

    def embed_query(self, text: str) -> np.ndarray: ...


@dataclass(frozen=True)
class DocumentSection:
    section_index: int
    heading_level: int
    section_title: str | None
    page_start: int
    page_end: int
    text: str


@dataclass(frozen=True)
class CleanDocument:
    document_id: str
    tenant_id: str
    title: str
    language: str
    sections: tuple[DocumentSection, ...]
    source: dict[str, Any]
    extraction: dict[str, Any]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    tenant_id: str
    title: str
    language: str
    chunk_index: int
    section_index: int
    section_title: str | None
    heading_level: int
    page_start: int
    page_end: int
    token_start: int
    token_end: int
    token_count: int
    char_start: int
    char_end: int
    text: str

    def to_record(self) -> dict[str, Any]:
        record = asdict(self)
        metadata: dict[str, str | int] = {
            "tenant_id": self.tenant_id,
            "document_id": self.document_id,
            "title": self.title,
            "language": self.language,
            "section_index": self.section_index,
            "heading_level": self.heading_level,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "chunk_index": self.chunk_index,
        }
        if self.section_title is not None:
            metadata["section_title"] = self.section_title
        record["metadata"] = metadata
        return record


def normalize_extracted_text(text: str) -> str:
    """Normaliza ruido técnico sin destruir párrafos ni referencias de página."""

    normalized = unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n")
    normalized = _CONTROL_CHARS.sub("", normalized)
    normalized = _HYPHENATED_LINE_BREAK.sub("", normalized)
    normalized = "\n".join(_SPACE_RUN.sub(" ", line).strip() for line in normalized.split("\n"))
    normalized = _BLANK_LINE_RUN.sub("\n\n", normalized)
    return normalized.strip()


def _required_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"El campo '{key}' es obligatorio y debe ser texto no vacío")
    return value.strip()


def load_clean_document(input_path: str | Path) -> CleanDocument:
    """Carga TXT o el contrato v1.0 estructurado del módulo de ingestión."""

    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo de entrada: {path}")

    if path.suffix.lower() == ".txt":
        text = normalize_extracted_text(path.read_text(encoding="utf-8"))
        if not text:
            raise ValueError("El archivo TXT no contiene texto útil")
        digest = _sha256_bytes(path.read_bytes())[:16]
        return CleanDocument(
            document_id=f"txt-{digest}",
            tenant_id="default",
            title=path.stem,
            language="es",
            sections=(
                DocumentSection(
                    section_index=0,
                    heading_level=0,
                    section_title=None,
                    page_start=1,
                    page_end=1,
                    text=text,
                ),
            ),
            source={"file_name": path.name, "content_type": "text/plain"},
            extraction={"parser": "external", "advertencias": []},
        )

    if path.suffix.lower() != ".json":
        raise ValueError("La entrada debe ser .json o .txt")

    data = json.loads(path.read_text(encoding="utf-8-sig"))
    contract_path = Path(__file__).resolve().parents[2] / "contracts" / "clean_document.schema.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(
            instance=data,
            schema=contract,
            format_checker=jsonschema.FormatChecker(),
        )
    except jsonschema.ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path) or "$"
        raise ValueError(f"El JSON no cumple el contrato v1.0 en '{location}': {exc.message}") from exc

    metadata_source = data["metadata_origen"]
    total_pages = int(metadata_source["total_paginas"])
    sections: list[DocumentSection] = []
    for section_index, raw_section in enumerate(data["contenido_estructurado"]):
        page_start = int(raw_section["pagina_inicio"])
        page_end = int(raw_section["pagina_fin"])
        if page_end < page_start:
            raise ValueError(
                f"La sección {section_index} tiene pagina_fin menor que pagina_inicio"
            )
        if page_end > total_pages:
            raise ValueError(
                f"La sección {section_index} referencia la página {page_end}, "
                f"pero total_paginas es {total_pages}"
            )

        raw_title = raw_section["titulo_seccion"]
        section_title = (
            normalize_extracted_text(raw_title)
            if isinstance(raw_title, str) and raw_title.strip()
            else None
        )
        body = normalize_extracted_text(raw_section["texto"])
        text = "\n\n".join(part for part in (section_title, body) if part)
        if not text:
            continue
        sections.append(
            DocumentSection(
                section_index=section_index,
                heading_level=int(raw_section["nivel_encabezado"]),
                section_title=section_title,
                page_start=page_start,
                page_end=page_end,
                text=text,
            )
        )

    if not sections:
        raise ValueError("contenido_estructurado no contiene texto útil para indexar")

    return CleanDocument(
        document_id=_required_string(data, "document_id"),
        tenant_id=_required_string(data, "tenant_id"),
        title=_required_string(data, "titulo"),
        language=_required_string(data, "idioma"),
        sections=tuple(sections),
        source={
            "file_name": metadata_source["nombre_archivo"],
            "content_type": data["tipo_origen"],
            "sha256": metadata_source["sha256"],
            "total_pages": total_pages,
            "ingested_at": data["fecha_ingesta"],
        },
        extraction=data["extraccion"],
    )


class TokenAwareChunker:
    """Crea ventanas por tokens y prefiere cerrar en límites de párrafo/oración."""

    def __init__(
        self,
        tokenizer: Tokenizer,
        *,
        chunk_tokens: int = 350,
        overlap_tokens: int = 50,
        boundary_window_ratio: float = 0.25,
    ) -> None:
        if chunk_tokens < 32:
            raise ValueError("chunk_tokens debe ser al menos 32")
        if overlap_tokens < 0 or overlap_tokens >= chunk_tokens:
            raise ValueError("overlap_tokens debe estar entre 0 y chunk_tokens - 1")
        if not 0.0 <= boundary_window_ratio <= 0.5:
            raise ValueError("boundary_window_ratio debe estar entre 0.0 y 0.5")
        self.tokenizer = tokenizer
        self.chunk_tokens = chunk_tokens
        self.overlap_tokens = overlap_tokens
        self.boundary_window_ratio = boundary_window_ratio

    def split(self, document: CleanDocument) -> list[Chunk]:
        chunks: list[Chunk] = []
        for section in document.sections:
            offsets = self._token_offsets(section.text)
            start = 0
            while start < len(offsets):
                hard_end = min(start + self.chunk_tokens, len(offsets))
                end = self._preferred_end(section.text, offsets, start, hard_end)
                char_start = offsets[start][0]
                char_end = offsets[end - 1][1]
                chunk_text = section.text[char_start:char_end].strip()
                if chunk_text:
                    chunk_index = len(chunks)
                    fingerprint = hashlib.sha256(
                        (
                            f"{document.document_id}|{section.section_index}|"
                            f"{section.page_start}|{start}|{chunk_text}"
                        ).encode("utf-8")
                    ).hexdigest()[:12]
                    chunks.append(
                        Chunk(
                            chunk_id=f"{document.document_id}:{chunk_index:05d}:{fingerprint}",
                            document_id=document.document_id,
                            tenant_id=document.tenant_id,
                            title=document.title,
                            language=document.language,
                            chunk_index=chunk_index,
                            section_index=section.section_index,
                            section_title=section.section_title,
                            heading_level=section.heading_level,
                            page_start=section.page_start,
                            page_end=section.page_end,
                            token_start=start,
                            token_end=end,
                            token_count=end - start,
                            char_start=char_start,
                            char_end=char_end,
                            text=chunk_text,
                        )
                    )
                if end >= len(offsets):
                    break
                start = max(start + 1, end - self.overlap_tokens)

        if not chunks:
            raise ValueError("No se generaron chunks a partir del documento")
        return chunks

    def _token_offsets(self, text: str) -> list[tuple[int, int]]:
        encoded = self.tokenizer(
            text,
            add_special_tokens=False,
            return_offsets_mapping=True,
            truncation=False,
        )
        offsets = encoded.get("offset_mapping")
        if offsets and isinstance(offsets[0], list):
            offsets = offsets[0]
        if not isinstance(offsets, list):
            raise TypeError("El tokenizer no devolvió offset_mapping")
        clean_offsets = [(int(start), int(end)) for start, end in offsets if int(end) > int(start)]
        if not clean_offsets:
            raise ValueError("El tokenizer no produjo tokens para una sección con texto")
        return clean_offsets

    def _preferred_end(
        self,
        text: str,
        offsets: Sequence[tuple[int, int]],
        start: int,
        hard_end: int,
    ) -> int:
        if hard_end >= len(offsets):
            return hard_end
        lookback = max(1, int(self.chunk_tokens * self.boundary_window_ratio))
        minimum = max(start + 1, hard_end - lookback)
        for candidate in range(hard_end, minimum - 1, -1):
            char_start = offsets[start][0]
            char_end = offsets[candidate - 1][1]
            if _BOUNDARY_END.search(text[char_start:char_end].rstrip()):
                return candidate
        return hard_end


class SentenceTransformerEmbedder:
    """Embeddings locales normalizados con prefijos compatibles con E5."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        *,
        device: str = "cpu",
        local_files_only: bool = False,
        batch_size: int = 16,
    ) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - depende del entorno local
            raise RuntimeError(
                "Falta sentence-transformers. Instala requirements.txt en un entorno virtual."
            ) from exc
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = SentenceTransformer(
            model_name,
            device=device,
            local_files_only=local_files_only,
        )
        self.tokenizer = self._model.tokenizer
        get_dimension = getattr(self._model, "get_embedding_dimension", None)
        dimension = (
            get_dimension()
            if callable(get_dimension)
            else self._model.get_sentence_embedding_dimension()
        )
        if not isinstance(dimension, int) or dimension < 1:
            raise RuntimeError("No fue posible determinar la dimensión del modelo")
        self.dimension = dimension

    def embed_documents(self, texts: Sequence[str]) -> np.ndarray:
        prepared = [f"passage: {text}" for text in texts]
        return self._encode(prepared)

    def embed_query(self, text: str) -> np.ndarray:
        return self._encode([f"query: {text}"])[0]

    def _encode(self, texts: Sequence[str]) -> np.ndarray:
        vectors = self._model.encode(
            list(texts),
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(vectors, dtype=np.float32)


def build_index(
    document: CleanDocument,
    output_dir: str | Path,
    embedder: Embedder,
    *,
    chunk_tokens: int = 350,
    overlap_tokens: int = 50,
) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    chunker = TokenAwareChunker(
        embedder.tokenizer,
        chunk_tokens=chunk_tokens,
        overlap_tokens=overlap_tokens,
    )
    chunks = chunker.split(document)
    vectors = np.asarray(embedder.embed_documents([chunk.text for chunk in chunks]), dtype=np.float32)
    _validate_vectors(vectors, expected_rows=len(chunks), expected_dimension=embedder.dimension)

    chunks_path = output / "chunks.jsonl"
    embeddings_path = output / "embeddings.npy"
    manifest_path = output / "manifest.json"

    with chunks_path.open("w", encoding="utf-8", newline="\n") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk.to_record(), ensure_ascii=False) + "\n")
    np.save(embeddings_path, vectors, allow_pickle=False)

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "document": {
            "document_id": document.document_id,
            "tenant_id": document.tenant_id,
            "title": document.title,
            "language": document.language,
            "page_count": int(document.source.get("total_pages", 1)),
            "section_count": len(document.sections),
            "source_sha256": document.source.get("sha256"),
            "extraction_warning_count": len(
                document.extraction.get("advertencias", [])
            ),
        },
        "chunking": {
            "strategy": "token_window_with_natural_boundaries",
            "chunk_tokens": chunk_tokens,
            "overlap_tokens": overlap_tokens,
            "chunk_count": len(chunks),
            "section_boundaries_preserved": True,
            "source_page_ranges_preserved": True,
        },
        "embeddings": {
            "model": embedder.model_name,
            "dimension": embedder.dimension,
            "dtype": "float32",
            "normalized": True,
            "similarity": "cosine_or_dot_product",
            "document_prefix": "passage: ",
            "query_prefix": "query: ",
            "shape": [int(vectors.shape[0]), int(vectors.shape[1])],
        },
        "files": {
            "chunks": {
                "path": chunks_path.name,
                "sha256": _sha256_file(chunks_path),
            },
            "embeddings": {
                "path": embeddings_path.name,
                "sha256": _sha256_file(embeddings_path),
            },
        },
        "vector_store_mapping": {
            "ids": "chunks.jsonl[].chunk_id",
            "documents": "chunks.jsonl[].text",
            "metadatas": "chunks.jsonl[].metadata",
            "embeddings": "embeddings.npy[row_index]",
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def search_index(
    index_dir: str | Path,
    query: str,
    embedder: Embedder,
    *,
    top_k: int = 3,
    tenant_id: str | None = None,
) -> list[dict[str, Any]]:
    if not query.strip():
        raise ValueError("La consulta no puede estar vacía")
    if top_k < 1:
        raise ValueError("top_k debe ser al menos 1")

    root = Path(index_dir)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    model_config = manifest["embeddings"]
    if model_config["model"] != embedder.model_name:
        raise ValueError(
            "El modelo de consulta no coincide con el usado para crear el índice: "
            f"{model_config['model']}"
        )

    chunks = [
        json.loads(line)
        for line in (root / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    vectors = np.load(root / "embeddings.npy", allow_pickle=False)
    _validate_vectors(
        vectors,
        expected_rows=len(chunks),
        expected_dimension=int(model_config["dimension"]),
    )
    query_vector = np.asarray(embedder.embed_query(query), dtype=np.float32)
    if query_vector.shape != (vectors.shape[1],):
        raise ValueError("La dimensión del vector de consulta es incompatible")

    scores = vectors @ query_vector
    candidates: list[tuple[int, float]] = []
    for index, score in enumerate(scores):
        if tenant_id is not None and chunks[index]["tenant_id"] != tenant_id:
            continue
        candidates.append((index, float(score)))
    candidates.sort(key=lambda item: item[1], reverse=True)

    results: list[dict[str, Any]] = []
    for index, score in candidates[:top_k]:
        chunk = chunks[index]
        results.append(
            {
                "rank": len(results) + 1,
                "score": round(score, 6),
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "tenant_id": chunk["tenant_id"],
                "section_index": chunk["section_index"],
                "section_title": chunk["section_title"],
                "heading_level": chunk["heading_level"],
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "text": chunk["text"],
            }
        )
    return results


def _validate_vectors(
    vectors: np.ndarray, *, expected_rows: int, expected_dimension: int
) -> None:
    if vectors.ndim != 2:
        raise ValueError(f"La matriz de embeddings debe ser 2D; recibido {vectors.shape}")
    if vectors.shape != (expected_rows, expected_dimension):
        raise ValueError(
            "Forma incompatible de embeddings: "
            f"esperada {(expected_rows, expected_dimension)}, recibida {vectors.shape}"
        )
    if not np.isfinite(vectors).all():
        raise ValueError("Los embeddings contienen NaN o infinito")
    norms = np.linalg.norm(vectors, axis=1)
    if not np.allclose(norms, 1.0, atol=1e-3):
        raise ValueError("Los embeddings deben estar normalizados a norma L2 = 1")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

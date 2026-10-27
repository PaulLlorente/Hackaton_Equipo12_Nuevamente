import logging
import os
from fastapi import APIRouter, HTTPException, Depends
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.src.api.models.schemas_salida import (
    AdaptarRequest,
    AdaptarResponse,
    FuenteCitada,
    Resumen,
    Flashcards,
    Quiz,
    Guion,
    Tutorial,
)
from backend.src.nuevamente_rag.vector_store import MotorVectorialRAG

from backend.database.schema_db import Users
from backend.src.administrar_usuarios.gestionar_usuario import obtener_usuario

logger = logging.getLogger("GenerarContenidoRouter")
router = APIRouter(tags=["Generación LLM"])

# Instancia global del motor RAG
motor_rag = MotorVectorialRAG()

MAPA_ESQUEMAS = {
    "resumen": Resumen,
    "flashcard": Flashcards,
    "quiz": Quiz,
    "guion": Guion,
    "tutorial": Tutorial,
}

SYSTEM_PROMPT = """Eres un Diseñador Instruccional Senior y Pedagogo Experto en IA.
Tu objetivo es transformar el material técnico provisto en un recurso pedagógico adaptado, riguroso y de alto valor de estudio.

Reglas obligatorias:
1. Apégate estrictamente al contexto técnico provisto; no inventes datos fuera de él.
2. Perfil pedagógico objetivo: {perfil}
   - principiante: Conceptos explicados con lenguaje claro y accesible, analogías intuitivas y definiciones guiadas.
   - intermedio: Balance práctico-teórico, profundidad funcional y análisis de casos de uso.
   - avanzado: Rigor técnico exhaustivo, arquitectura profunda, trade-offs, patrones y mejores prácticas.
3. Formato requerido: {formato}. Debes estructurar la salida exactamente bajo el esquema asignado.
4. Reglas estrictas de extensión y profundidad según el formato:
    - Si el formato es una colección (flashcards, quiz, guion, tutorial): debes generar exactamente {cantidad_items} elementos en su lista, sin omitir ninguno.
    - Si el formato es **resumen**: **ESTÁ PROHIBIDO generar un simple párrafo corto**. Debes redactar un documento de estudio extenso y exhaustivo (diseñado para una lectura profunda de 15 minutos). Es obligatorio estructurarlo mediante secciones con subtítulos en Markdown:
        * **Introducción y Contexto:** Planteamiento general del tema basado en el material.
        * **Desarrollo Técnico / Core Concepts:** Explicación detallada de los conceptos clave, arquitectura o procesos involucrados.
        * **Implicaciones Prácticas:** Análisis de su aplicación real según el nivel pedagógico.
        * **Conclusiones:** Síntesis final de los puntos críticos a recordar.
"""


@router.post("/adaptar", response_model=AdaptarResponse)
async def adaptar_contenido(peticion: AdaptarRequest, usuario_actual: Users = Depends(obtener_usuario)):
    """
    Recupera fragmentos relevantes desde ChromaDB y genera la adaptación pedagógica requerida.
    """
    try:
        # 1. Recuperar contexto desde el motor RAG
        documentos = motor_rag.recuperar_contexto(
            query=peticion.query,
            tenant_id=peticion.tenant_id,
            k=peticion.top_k,
        )

        if not documentos:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró información para el tema '{peticion.query}' en el tenant '{peticion.tenant_id}'.",
            )

        contexto_unificado = "\n\n".join(
            [
                f"[Fuente: {doc.metadata.get('origen', 'Desconocido')}]\n{doc.page_content}"
                for doc in documentos
            ]
        )

        # 2. Configurar LLM con salida estructurada según el formato (Fijado a gemini-3.5-flash)
        esquema_salida = MAPA_ESQUEMAS[peticion.formato]
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0.2,
        )
        extractor = llm.with_structured_output(esquema_salida)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """Contexto Técnico Recuperado:
---------------------
{contexto}
---------------------

Genera la adaptación pedagógica para la consulta: {query}""",
                ),
            ]
        )

        cadena = prompt | extractor

        resultado_raw = await cadena.ainvoke(
            {
                "perfil": peticion.perfil,
                "formato": peticion.formato,
                "contexto": contexto_unificado,
                "query": peticion.query,
                "cantidad_items": peticion.cantidad_items,
            }
        )

        # --- APLANAMIENTO DEFENSIVO (Pydantic / Streamlit safety) ---
        if not isinstance(resultado_raw, esquema_salida):
            try:
                if hasattr(esquema_salida, "model_validate"):
                    resultado = esquema_salida.model_validate(resultado_raw)
                else:
                    resultado = resultado_raw
            except Exception:
                resultado = resultado_raw
        else:
            resultado = resultado_raw
        # -------------------------------------------------------------

        fuentes_unicas = []
        ids_vistos = set()

        for doc in documentos:
            meta = doc.metadata or {}
            doc_id = meta.get("document_id", "No disponible")

            if doc_id not in ids_vistos:
                ids_vistos.add(doc_id)
                fuentes_unicas.append(
                    FuenteCitada(
                        origen=meta.get("origen", "Documento sin nombre"),
                        document_id=doc_id,
                        tenant_id=meta.get("tenant_id", peticion.tenant_id),
                    )
                )

        resultado.fuentes = fuentes_unicas

        return resultado

    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Fallo en endpoint /adaptar: {error}")
        raise HTTPException(
            status_code=500, detail=f"Error interno procesando adaptación: {str(error)}"
        )

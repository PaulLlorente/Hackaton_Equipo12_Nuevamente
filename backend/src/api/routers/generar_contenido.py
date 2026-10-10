import logging
import os
from fastapi import APIRouter, HTTPException, Depends
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.src.api.models.schemas_salida import (
    AdaptarRequest,
    AdaptarResponse,
    Resumen,
    Flashcards,
    Quiz,
    Guion,
)
from backend.src.nuevamente_rag.vector_store import MotorVectorialRAG

logger = logging.getLogger("GenerarContenidoRouter")
router = APIRouter(tags=["Generación LLM"])

# Instancia global del motor RAG
motor_rag = MotorVectorialRAG()

MAPA_ESQUEMAS = {
    "resumen": Resumen,
    "flashcard": Flashcards,
    "quiz": Quiz,
    "guion": Guion,
}

SYSTEM_PROMPT = """Eres un Diseñador Instruccional Senior y Pedagogo Experto en IA.
Tu objetivo es transformar el material técnico provisto en un recurso pedagógico adaptado.

Reglas obligatorias:
1. Apégate estrictamente al contexto técnico provisto; no inventes datos fuera de él.
2. Perfil pedagógico objetivo: {perfil}
   - principiante: Conceptos explicados con lenguaje claro y accesible, analogías intuitivas.
   - intermedio: Balance práctico-teórico, profundidad funcional.
   - avanzado: Rigor técnico exhaustivo, arquitectura, trade-offs y mejores prácticas.
3. Formato requerido: {formato}. Debes estructurar la salida exactamente bajo el esquema asignado.
"""


@router.post("/adaptar", response_model=AdaptarResponse)
async def adaptar_contenido(peticion: AdaptarRequest):
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

        contexto_unificado = "\n\n".join([doc.page_content for doc in documentos])

        # 2. Configurar LLM con salida estructurada según el formato
        esquema_salida = MAPA_ESQUEMAS[peticion.formato]
        llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
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

        resultado = await cadena.ainvoke(
            {
                "perfil": peticion.perfil,
                "formato": peticion.formato,
                "contexto": contexto_unificado,
                "query": peticion.query,
            }
        )

        return resultado

    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Fallo en endpoint /adaptar: {error}")
        raise HTTPException(
            status_code=500, detail=f"Error interno procesando adaptación: {str(error)}"
        )
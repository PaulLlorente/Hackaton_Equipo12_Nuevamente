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
Tu objetivo es transformar el material técnico provisto en un recurso pedagógico adaptado.

Reglas obligatorias:
1. Apégate estrictamente al contexto técnico provisto; no inventes datos fuera de él.
2. Perfil pedagógico objetivo: {perfil}
   - principiante: Conceptos explicados con lenguaje claro y accesible, analogías intuitivas.
   - intermedio: Balance práctico-teórico, profundidad funcional.
   - avanzado: Rigor técnico exhaustivo, arquitectura, trade-offs y mejores prácticas.
3. Formato requerido: {formato}. Debes estructurar la salida exactamente bajo el esquema asignado.
4. Cantidad de elementos:
    - Si el formato es una colección (tarjetas en flashcards, preguntas en quiz, escenas en guion o pasos en tutorial):
        debes generar exactamente {cantidad_items} elementos en su lista.
    - Si el formato es resumen: ignora esta cantidad y genera una síntesis fluida y coherente.
"""


@router.post("/adaptar", response_model=AdaptarResponse)
async def adaptar_contenido(peticion: AdaptarRequest,usuario_actual: Users = Depends(obtener_usuario)):
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

        # 2. Configurar LLM con salida estructurada según el formato
        esquema_salida = MAPA_ESQUEMAS[peticion.formato]
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            temperature=0.2,
            max_retries=6,
            timeout=120
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
                "cantidad_items": peticion.cantidad_items,
            }
        )


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

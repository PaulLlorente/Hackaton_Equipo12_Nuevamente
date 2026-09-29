import sys
import json
from pathlib import Path
import logging

# Agregamos la raíz del proyecto al sistema para poder importar la carpeta src
directorio_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(directorio_raiz))

from src.nuevamente_rag.vector_store import MotorVectorialRAG

logger = logging.getLogger("TestLocal")


def ejecutar_prueba():
    try:
        motor = MotorVectorialRAG()

        # Ruta dinámica al mock de datos
        ruta_mock = directorio_raiz / "data" / "mock" / "chunks_mock.jsonl"

        # Ejecutar Indexación
        logger.info("Iniciando prueba de indexación (Archivo Físico)...")
        motor.vectorizar_e_indexar(str(ruta_mock))

        # Ejecutar Recuperación
        logger.info("Iniciando prueba de recuperación (Retriever)...")
        resultados = motor.recuperar_contexto(
            query="¿Qué es una VCN?",
            tenant_id="oracle_hackathon_test"
        )

        # Mostrar Resultados
        print("\n" + "=" * 50)
        print("RESULTADOS DE LA BÚSQUEDA (ARCHIVO FÍSICO)")
        print("=" * 50)
        for i, res in enumerate(resultados, 1):
            print(f"--- Documento {i} ---")
            print(f"Metadatos : {res.metadata}")
            print(f"Contenido : {res.page_content[:150]}...\n")

    except Exception as e:
        logger.critical(f"La prueba local falló: {e}")


def ejecutar_prueba_memoria():
    """Prueba del método en memoria usando el archivo chunks_mock.jsonl"""
    try:
        motor = MotorVectorialRAG()
        tenant_prueba = "oracle_hackathon_memoria"
        ruta_mock = directorio_raiz / "data" / "mock" / "chunks_mock.json"

        # 1. Leemos tu JSONL y lo convertimos en una lista en RAM (Simulando a la API)
        mock_chunks_memoria = []
        with open(ruta_mock, 'r', encoding='utf-8') as archivo_jsonl:
            for linea in archivo_jsonl:
                if linea.strip():
                    mock_chunks_memoria.append(json.loads(linea))

        # Ejecutar Ingesta en Memoria pasándole tu lista
        logger.info(f"Iniciando prueba PLUS (Indexación en Memoria) con {len(mock_chunks_memoria)} chunks...")
        motor.ingestar_y_vectorizar_memoria(
            chunks_data=mock_chunks_memoria,
            tenant_id=tenant_prueba
        )

        # Ejecutar Recuperación
        logger.info("Iniciando recuperación (Retriever Memoria)...")
        resultados = motor.recuperar_contexto(
            query="¿Qué seguridad ofrece OCI para las VCN?",
            tenant_id=tenant_prueba
        )

        # Mostrar Resultados
        print("\n" + "=" * 50)
        print("RESULTADOS DE LA BÚSQUEDA (EN MEMORIA)")
        print("=" * 50)
        for i, res in enumerate(resultados, 1):
            print(f"--- Documento {i} ---")
            print(f"Metadatos : {res.metadata}")
            print(f"Contenido : {res.page_content[:150]}...\n")

    except Exception as e:
        logger.critical(f"La prueba en memoria falló: {e}")


if __name__ == "__main__":
    # Ejecutamos prueba original validada
    ejecutar_prueba()

    print("\n\n" + "*" * 50)
    print("INICIANDO PRUEBA DE NUEVO MÉTODO PLUS EN MEMORIA")
    print("*" * 50 + "\n")

    # Ejecutamos la nueva prueba en memoria
    ejecutar_prueba_memoria()
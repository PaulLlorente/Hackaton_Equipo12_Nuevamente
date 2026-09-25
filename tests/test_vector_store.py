import sys
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
        logger.info("Iniciando prueba de indexación...")
        motor.vectorizar_e_indexar(str(ruta_mock))

        # Ejecutar Recuperación
        logger.info("Iniciando prueba de recuperación (Retriever)...")
        resultados = motor.recuperar_contexto(
            query="¿Qué es una VCN?",
            tenant_id="oracle_hackathon_test"
        )

        # Mostrar Resultados
        print("\n" + "=" * 50)
        print("RESULTADOS DE LA BÚSQUEDA EN CHROMADB")
        print("=" * 50)
        for i, res in enumerate(resultados, 1):
            print(f"--- Documento {i} ---")
            print(f"Metadatos : {res.metadata}")
            print(f"Contenido : {res.page_content[:150]}...\n")

    except Exception as e:
        logger.critical(f"La prueba local falló: {e}")


if __name__ == "__main__":
    ejecutar_prueba()
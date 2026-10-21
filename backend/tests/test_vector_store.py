# test_vector_store.py
import json
import logging
from backend.src.nuevamente_rag.vector_store import MotorVectorialRAG

logging.basicConfig(level=logging.INFO)

def probar_motor():
    print("\n--- 1. INICIALIZANDO MOTOR VECTORIAL ---")
    motor = MotorVectorialRAG(persist_directory="./chroma_db_test")

    tenant_prueba = "tenant_demo_123"
    doc_id = "doc_prueba_001"

    # --- PRUEBA 1: JSON ESTRUCTURADO (Flujo Ingestión) ---
    print("\n--- 2. PRUEBA: INGESTA JSON CON SHA-256 ---")
    json_ingestion = {
        "metadata_origen": {
            "sha256": "hash_ficticio_123456789_abc"
        },
        "contenido_estructurado": [
            {
                "texto": "Este es el primer párrafo con información confidencial sobre la póliza.",
                "pagina_inicio": 1,
                "nivel_encabezado": 1,
                "titulo_seccion": "Introducción"
            }
        ]
    }

    # Ingestar por primera vez
    motor.ingestar_y_vectorizar_memoria(
        texto_crudo=json.dumps(json_ingestion),
        tenant_id=tenant_prueba,
        document_id=doc_id
    )

    # --- PRUEBA 2: IDEMPOTENCIA (Intentar subir el mismo hash) ---
    print("\n--- 3. PRUEBA: IDEMPOTENCIA (Documento Duplicado) ---")
    # Debería mostrar en logs: "Documento duplicado detectado... Omitiendo vectorización"
    motor.ingestar_y_vectorizar_memoria(
        texto_crudo=json.dumps(json_ingestion),
        tenant_id=tenant_prueba,
        document_id=doc_id
    )

    # --- PRUEBA 3: FALLBACK A TEXTO PLANO ---
    print("\n--- 4. PRUEBA: FALLBACK A TEXTO PLANO ---")
    texto_plano = "Este es un texto libre sin formato JSON que un usuario pegó directamente en el chat."
    motor.ingestar_y_vectorizar_memoria(
        texto_crudo=texto_plano,
        tenant_id=tenant_prueba,
        document_id="doc_plano_002"
    )

    # --- PRUEBA 4: RECUPERACIÓN DE CONTEXTO ---
    print("\n--- 5. PRUEBA: RECUPERAR CONTEXTO ---")
    resultados = motor.recuperar_contexto(
        query="póliza confidencial",
        tenant_id=tenant_prueba,
        k=2
    )

    print(f"\nResultados encontrados: {len(resultados)}")
    for doc in resultados:
        print(f"- Texto: {doc.page_content}")
        print(f"  Metadatos: {doc.metadata}\n")

if __name__ == "__main__":
    probar_motor()
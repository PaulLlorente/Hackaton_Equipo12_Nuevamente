import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("VectorStoreRAG")

class Config:
    """Validador de variables de entorno."""
    load_dotenv()

    @classmethod
    def obtener_google_api_key(cls) -> SecretStr:
        api_key: str | None = os.getenv("GOOGLE_API_KEY")
        if not api_key or len(api_key) < 20:
            logger.critical("Configuración inválida o faltante: GOOGLE_API_KEY.")
            raise ValueError("La API Key no existe o es demasiado corta.")
        return SecretStr(api_key)

class MotorVectorialRAG:
    """Motor principal para manejo de ChromaDB y Gemini."""

    def __init__(self, persist_directory: str | None = None):
        try:
            self.api_key = Config.obtener_google_api_key()
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-2", #Modelo vigente
                google_api_key=self.api_key
            )

            if persist_directory:
                self.persist_directory = persist_directory
            else:
                directorio_base = Path(__file__).resolve().parent.parent.parent
                self.persist_directory = str(directorio_base / "chroma_db")

            logger.info(f"Motor RAG inicializado. BD en: {self.persist_directory}")

        except Exception as error_init:
            logger.error(f"Fallo en la inicialización: {error_init}")
            raise

    def vectorizar_e_indexar(self, ruta_jsonl: str) -> Chroma:
        ruta_path = Path(ruta_jsonl)
        if not ruta_path.exists():
            logger.error(f"Archivo no encontrado: {ruta_path}")
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_path}")

        documentos_langchain = []
        ids_chunks = []

        logger.info(f"Procesando chunks desde: {ruta_path.name}")

        try:
            with open(ruta_path, 'r', encoding='utf-8') as archivo_jsonl:
                for linea in archivo_jsonl:
                    if not linea.strip():
                        continue
                    chunk_data = json.loads(linea)
                    doc = Document(
                        page_content=chunk_data["text"],
                        metadata=chunk_data["metadata"]
                    )
                    documentos_langchain.append(doc)
                    ids_chunks.append(chunk_data["chunk_id"])

            logger.info(f"Vectorizando {len(documentos_langchain)} chunks...")

            vectorstore = Chroma.from_documents(
                documents=documentos_langchain,
                embedding=self.embeddings,
                ids=ids_chunks,
                persist_directory=self.persist_directory
            )
            logger.info("Indexación completada.")
            return vectorstore

        except json.JSONDecodeError as error_json:
            logger.error(f"Error de formato JSONL: {error_json}")
            raise
        except Exception as error_vectorizacion:
            logger.error(f"Error crítico en vectorización: {error_vectorizacion}")
            raise

    def recuperar_contexto(self, query: str, tenant_id: str, k: int = 3):
        logger.info(f"Ejecutando Retriever | Query: '{query}' | Tenant: {tenant_id}")
        try:
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return vectorstore.similarity_search(
                query=query,
                k=k,
                filter={"tenant_id": tenant_id}
            )
        except Exception as error_retriever:
            logger.error(f"Fallo al recuperar contexto: {error_retriever}")
            raise
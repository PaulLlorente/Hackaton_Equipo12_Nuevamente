import os
import json
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
                model="models/gemini-embedding-2",
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

        try:
            with open(ruta_path, 'r', encoding='utf-8') as archivo_jsonl:
                for linea in archivo_jsonl:
                    if not linea.strip():
                        continue
                    chunk_data = json.loads(linea)
                    doc = Document(page_content=chunk_data["text"], metadata=chunk_data["metadata"])
                    documentos_langchain.append(doc)
                    ids_chunks.append(chunk_data["chunk_id"])

            vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )

            self._ingestar_con_throttling(documentos_langchain, ids_chunks, vectorstore)
            return vectorstore

        except json.JSONDecodeError as error_json:
            logger.error(f"Error de formato JSONL: {error_json}")
            raise
        except Exception as error_vectorizacion:
            logger.error(f"Error crítico en vectorización: {error_vectorizacion}")
            raise

    def recuperar_contexto(self, query: str, tenant_id: str, k: int = 3):
        try:
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return vectorstore.similarity_search(query=query, k=k, filter={"tenant_id": tenant_id})
        except Exception as error_retriever:
            logger.error(f"Fallo al recuperar contexto: {error_retriever}")
            raise

    def ingestar_y_vectorizar_memoria(self, texto_crudo, tenant_id: str, document_id: str = "doc_desconocido",
                                      origen: str = "origen_desconocido") -> Chroma:
        if not texto_crudo:
            raise ValueError("No hay datos para vectorizar.")

        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

        try:
            datos_documento = texto_crudo if isinstance(texto_crudo, dict) else json.loads(str(texto_crudo))
            sha256_hash = datos_documento.get("metadata_origen", {}).get("sha256")

            if sha256_hash:
                hash_str = str(sha256_hash)
                existentes = vectorstore.get(where={"$and": [{"tenant_id": tenant_id}, {"sha256": hash_str}]})
                if existentes and existentes.get("ids"):
                    logger.info("Documento duplicado detectado. Omitiendo vectorización.")
                    return vectorstore

            secciones = datos_documento.get("contenido_estructurado", [])
            documentos_langchain, ids_chunks = [], []

            for indice, seccion in enumerate(secciones):
                fragmento = seccion.get("texto", "").strip()
                if not fragmento:
                    continue

                metadatos = {
                    "tenant_id": tenant_id,
                    "document_id": document_id,
                    "origen": origen,
                    "sha256": str(sha256_hash) if sha256_hash else "desconocido",
                    "pagina_inicio": seccion.get("pagina_inicio", 1),
                    "nivel_encabezado": seccion.get("nivel_encabezado", 0),
                    "titulo_seccion": seccion.get("titulo_seccion", "Sin titulo")
                }
                documentos_langchain.append(Document(page_content=fragmento, metadata=metadatos))
                ids_chunks.append(f"{document_id}_chunk_{indice}_{str(hash(fragmento))}")

            if documentos_langchain:
                self._ingestar_con_throttling(documentos_langchain, ids_chunks, vectorstore)
            return vectorstore

        except (json.JSONDecodeError, TypeError, AttributeError):
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,
                                                           separators=["\n\n", "\n", ".", " ", ""])
            fragmentos_texto = text_splitter.split_text(str(texto_crudo))
            documentos_langchain, ids_chunks = [], []

            for indice, fragmento in enumerate(fragmentos_texto):
                metadatos = {"tenant_id": tenant_id, "document_id": document_id, "origen": origen}
                documentos_langchain.append(Document(page_content=fragmento, metadata=metadatos))
                ids_chunks.append(f"{document_id}_chunk_plano_{indice}_{str(hash(fragmento))}")

            if documentos_langchain:
                self._ingestar_con_throttling(documentos_langchain, ids_chunks, vectorstore)
            return vectorstore

    def _ingestar_con_throttling(self, documentos_langchain, ids_chunks, vectorstore):
        """Procesa lotes calculando el peso en tokens para evitar Error 429 de Gemini."""
        tamano_lote = 5
        total_chunks = len(documentos_langchain)
        limite_caracteres_minuto = 85000  # Límite seguro (~22,000 tokens)
        caracteres_actuales = 0

        for i in range(0, total_chunks, tamano_lote):
            lote_docs = documentos_langchain[i: i + tamano_lote]
            lote_ids = ids_chunks[i: i + tamano_lote]

            caracteres_lote = sum(len(doc.page_content) for doc in lote_docs)

            if caracteres_actuales + caracteres_lote > limite_caracteres_minuto:
                logger.warning("Límite de cuota Gemini próximo. Pausa obligatoria de 65 segundos...")
                time.sleep(65)
                caracteres_actuales = 0

            vectorstore.add_documents(documents=lote_docs, ids=lote_ids)
            caracteres_actuales += caracteres_lote
            logger.info(f"Progreso: {min(i + tamano_lote, total_chunks)}/{total_chunks} chunks indexados.")

            time.sleep(2)
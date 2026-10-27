import os
import json
import time
import logging
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
                model="models/gemini-embedding-2",  # Modelo vigente
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

            logger.info(f"Vectorizando {len(documentos_langchain)} chunks por lotes...")

            vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )

            tamano_lote = 3
            total_chunks = len(documentos_langchain)

            for i in range(0, total_chunks, tamano_lote):
                lote_docs = documentos_langchain[i : i + tamano_lote]
                lote_ids = ids_chunks[i : i + tamano_lote]
                vectorstore.add_documents(documents=lote_docs, ids=lote_ids)
                logger.info(f"Lote JSONL indexado: {min(i + tamano_lote, total_chunks)}/{total_chunks}")
                if i + tamano_lote < total_chunks:
                    time.sleep(12)

            logger.info("Indexación completada exitosamente por lotes.")
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

    def ingestar_y_vectorizar_memoria(self, texto_crudo, tenant_id: str, document_id: str = "doc_desconocido",
                                      origen: str = "origen_desconocido") -> Chroma:
        """Recibe el texto crudo en memoria, aplica chunking semántico y lo indexa."""
        if not texto_crudo:
            logger.error("El texto recibido está vacío.")
            raise ValueError("No hay datos para vectorizar.")

        logger.info(f"Procesando entrada para el tenant {tenant_id}...")

        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

        try:
            # INTENTO 1: Validar si es JSON estructurado (Diccionario o String JSON)
            if isinstance(texto_crudo, dict):
                datos_documento = texto_crudo
            else:
                datos_documento = json.loads(str(texto_crudo))

            # IDEMPOTENCIA: Verificar hash SHA-256
            metadata_origen = datos_documento.get("metadata_origen", {})
            sha256_hash = metadata_origen.get("sha256")

            if sha256_hash:
                hash_str = str(sha256_hash)  # Forzamos el tipado estricto a string para calmar al linter

                existentes = vectorstore.get(
                    where={
                        "$and": [
                            {"tenant_id": tenant_id},
                            {"sha256": hash_str}
                        ]
                    }
                )

                if existentes and existentes.get("ids"):
                    logger.info(
                        f"Documento duplicado detectado (Hash: {hash_str}). Omitiendo vectorización en Gemini.")
                    return vectorstore

            secciones = datos_documento.get("contenido_estructurado", [])
            documentos_langchain = []
            ids_chunks = []

            logger.info(f"Vectorizando {len(secciones)} chunks estructurados en memoria...")

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

                doc = Document(page_content=fragmento, metadata=metadatos)
                documentos_langchain.append(doc)
                chunk_id = f"{document_id}_chunk_{indice}_{str(hash(fragmento))}"
                ids_chunks.append(chunk_id)

            if documentos_langchain:
                vectorstore.add_documents(documents=documentos_langchain, ids=ids_chunks)
                logger.info("Indexación estructurada completada exitosamente.")
            return vectorstore

        except (json.JSONDecodeError, TypeError, AttributeError) as e:
            # INTENTO 2: Fallback si es texto plano crudo
            logger.warning(f"Formato JSON no detectado, aplicando fallback a texto plano. Detalle: {e}")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", " ", ""]
            )

            fragmentos_texto = text_splitter.split_text(str(texto_crudo))
            documentos_langchain = []
            ids_chunks = []

            logger.info(f"Vectorizando {len(fragmentos_texto)} chunks en texto plano...")

            for indice, fragmento in enumerate(fragmentos_texto):
                metadatos = {
                    "tenant_id": tenant_id,
                    "document_id": document_id,
                    "origen": origen
                }

                doc = Document(page_content=fragmento, metadata=metadatos)
                documentos_langchain.append(doc)
                chunk_id = f"{document_id}_chunk_plano_{indice}_{str(hash(fragmento))}"
                ids_chunks.append(chunk_id)

            if documentos_langchain:
                vectorstore.add_documents(documents=documentos_langchain, ids=ids_chunks)
                logger.info("Indexación de texto plano completada exitosamente.")
            return vectorstore

        except Exception as error_vectorizacion:
            logger.error(f"Error crítico en vectorización en memoria: {error_vectorizacion}")
            raise
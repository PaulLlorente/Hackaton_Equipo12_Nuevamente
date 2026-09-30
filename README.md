# 🎓 NuevaMente – Sistema Inteligente de Adaptación y Generación de Contenido Educativo

<div align="center">

**Hackathon ONE G10 (Oracle Next Education & Alura)**  
*G10-LATAM-equipo-12*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OCI Object Storage](https://img.shields.io/badge/Oracle_Cloud-OCI_Always_Free-F80000?style=for-the-badge&logo=oracle&logoColor=white)](https://www.oracle.com/cloud/free/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.python.org/)

</div>

---

## 🚀 Descripción del Proyecto

**NuevaMente** es una solución inteligente de tecnología educativa (EdTech) diseñada para ingestar manuales y documentaciones técnicas densas y transformarlas automáticamente en contenidos didácticos personalizados. 

El sistema adapta el material técnico original según el **perfil del destinatario** (Principiante, Junior, Arquitecto, Ejecutivo), la **industria de aplicación** (Fintech, Salud, E-commerce, General) y el **formato pedagógico de salida** (Flashcards, Guías Prácticas, Quizzes Interactivos, Resúmenes TL;DR o Guiones de Clase), garantizando fidelidad absoluta gracias a un pipeline avanzado de RAG.

---

## 🏛️ Arquitectura de la Solución y Flujo RAG

El flujo técnico del MVP se compone de las siguientes fases:

1. **Ingestión y Extracción:** Recepción de archivos técnicos en formato PDF, Markdown o texto plano (`PyPDF` / extractores nativos).
2. **Pipeline de RAG (Retrieval-Augmented Generation):** Segmentación del texto en fragmentos (*chunking*), generación de embeddings vectoriales y almacenamiento en un Vector Store para evitar alucinaciones y asegurar el anclaje en las fuentes originales.
3. **Orquestación con LLMs y Prompts Estructurados:** Uso de cadenas inteligentes para planificar, redactar y estructurar el contenido didáctico con tipado estricto (`Pydantic`).
4. **Persistencia en la Nube (OCI Always Free):** Integración obligatoria con **Oracle Cloud Infrastructure Object Storage** para almacenar de forma segura los documentos técnicos originales y los paquetes educativos generados en formato JSON.

```mermaid
graph TD
    A[Documento Técnico PDF/MD] --> B[Extracción y Chunking]
    B --> C[Generación de Embeddings & Vector Store]
    C --> D[Orquestación LLM + RAG]
    D --> E[Validación de Fidelidad y Esquema JSON]
    E --> F[Interfaz Interactiva Streamlit]
    E --> G[(OCI Object Storage Always Free)]
## 🚀 API de Ingestión y Búsqueda Semántica (RAG)

El backend expone una API REST construida sobre **FastAPI** que encapsula el pipeline de normalización, chunking consciente de tokens y recuperación densa basada en representaciones vectoriales multilingües.

### Documentación Interactiva
Con el servidor levantado, la documentación OpenAPI interactiva está disponible en:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Endpoints Disponibles

#### 1. `GET /health`
Verificación de disponibilidad operativa del servicio.
* **Respuesta (`200 OK`)**:
  ```json
  {
    "status": "ok",
    "service": "NuevaMente API"
  }

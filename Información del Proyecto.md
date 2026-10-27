# Proyecto NuevaMente \- Documentación Técnica y de Gestión Integral (Equipo 12 \- Hackathon ONE G10-LATAM)

## 1\. Introducción y Visión General (README)

**NuevaMente** es una solución tecnológica integral basada en IA y un motor RAG (*Retrieval-Augmented Generation*) optimizado para la transformación y adaptación inteligente de contenidos educativos y documentales. Resuelve la necesidad de adaptar material de estudio complejo a diversos niveles (*principiante, avanzado, resúmenes, quizzes y guiones*) con trazabilidad y cumplimiento de arquitectura moderna.

- **Colección Postman**: `docs/postman_collection.json` para pruebas de la API REST.  
- **Contratos**: Disponibles en `docs/contracts/` para validación JSON y Pydantic.

## 2\. Arquitectura del Sistema

Diseño modular limpio y desacoplado:

- **`backend/`**: Núcleo lógico.  
  - **API REST (`src/api/`)**: Routers FastAPI (`generar_contenido.py`, `usuarios.py`) y modelos Pydantic.  
  - **Pipeline RAG (`src/nuevamente_rag/`)**: Recuperación vectorial y orquestación de contexto.  
  - **Ingestión (`src/ingestion/`)**: Extractores PDF (`extractorPDF.py`) y Markdown (`extractorMD.py`), normalización y control de *hashing*.  
  - **IA (`src/nuevamente_ai/`)**: Prompts multinivel y contratos de salida.  
- **`frontend/`**: Interfaz interactiva en Streamlit. Vistas modulares (`auth.py`, `carga.py`, `consulta.py`, `cuenta.py`) con estilos CSS en `frontend/styles/`.  
- **`docs/`**: Contratos, especificaciones y referencias.  
- **`project_management/`**: Bitácoras, actividades y tableros de gestión.

## 3\. Stack Tecnológico Oficial

- **Python**: Lenguaje principal de procesamiento e IA.  
- **FastAPI & Uvicorn**: Framework web asíncrono y servidor ASGI de alto rendimiento.  
- **Google Gemini & LangChain**: LLM principal y orquestador de componentes/agentes.  
- **ChromaDB**: Base de datos vectorial local (*Vector Store*) de alta velocidad y cero costo.  
- **Pydantic**: Validación y contratos estrictos de datos.  
- **Streamlit & CSS**: Interfaz visual interactiva y adaptada.  
- **Postman & Pytest**: Validación de endpoints y pruebas unitarias.

## 4\. Infraestructura y Despliegue en la Nube (OCI)

- **OCI**: Capa *Always Free* y nodos especializados para estabilidad del MVP.  
- **Portales MCP (Model Context Protocol)**: Centralización, auditoría y protección *Zero Trust* de herramientas y recursos para modelos y agentes (Claude Desktop, Gemini, RAG), evitando exposición de credenciales.  
- **Alta Disponibilidad y DRP (Disaster Recovery Plan)**: Nodo adicional con función DRP y balanceo *Round Robin* para resiliencia continua.  
- **Object Storage**: Gestión centralizada de documentos y respaldos.  
- **Compute Instances & VCN**: Servidores Linux con listas de seguridad para FastAPI y Streamlit.

## 5\. Cronograma y Bitácora (Semanas 1 a 4\)

### Semana 1: Planificación y Arquitectura Base

- **Actividades**: Definición modular (FastAPI/Streamlit), repositorio GitHub, *GitHub Flow* y distribución equilibrada de roles.  
- **Entregables**: Estructura de carpetas base y asignación de flujos.

### Semana 2: Ingestión y Pipeline RAG

- **Actividades**: Desarrollo de extractores PDF/Markdown, normalización, control de *hashing* e integración de **ChromaDB**.  
- **Entregables**: Módulo de ingestión funcional y pruebas unitarias iniciales.

### Semana 3: Backend, Endpoints y Contratos de IA

- **Actividades**: Routers asíncronos en FastAPI, integración de prompts dinámicos (`nuevamente_ai`) multinivel y esquemas Pydantic.  
- **Entregables**: API REST operativa y conexión con prompts.

### Semana 4 (Cierre Hackathon): Integración Final y Despliegue MVP

- **Actividades**: Interfaz en Streamlit, despliegue en **OCI**, servidores MCP, nodo DRP con *Round Robin* y pruebas E2E.  
- **Entregables**: MVP desplegado en OCI bajo alta disponibilidad y documentación completa para jueces.

## 6\. Guía de Configuración y Ejecución

1. **Clonar repositorio**: `git clone <URL_REPOSITORIO> && cd nuevamente && git checkout main`  
2. **Entorno virtual y dependencias backend**: `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`  
3. **Variables de entorno (`.env`) en `backend/`**: `ENVIRONMENT=development`, `DEBUG=True`, `DATABASE_URL=sqlite:///./nuevamente.db`, `GOOGLE_API_KEY=<tu_clave>`, `UPLOAD_DIR=backend/data/uploads`  
4. **Ejecutar Backend**: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`  
5. **Ejecutar Frontend (Streamlit)**: `cd frontend && streamlit run app.py`
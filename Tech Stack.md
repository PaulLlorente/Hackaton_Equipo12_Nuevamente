# Stack Tecnológico - Proyecto NuevaMente (Team 12)

Este documento detalla las tecnologías, librerías, componentes del pipeline y la infraestructura en la nube integrados en el proyecto NuevaMente.

## 1. Backend & API REST
* **Python**: Lenguaje principal de desarrollo y procesamiento lógico.
* **FastAPI**: Framework web asíncrono para la construcción de los routers de la API y endpoints de generación.
* **Uvicorn**: Servidor ASGI para la ejecución y despliegue del backend.

## 2. Pipeline RAG & Procesamiento de Datos (Ingestión)
* **Pipeline RAG Integral (`nuevamente_rag`)**: Módulo avanzado de recuperación y generación aumentada conectado con los vectores y plantillas.
* **Extractores Especializados (`ingestion`)**:
  * `extractorPDF.py`: Procesamiento y extracción inteligente de documentos PDF.
  * `extractorMD.py`: Manejo y parseo de archivos en formato Markdown.
  * `structurer.py` & `hashing.py`: Estructuración, normalización y control de huellas digitales de los fragmentos (*chunks*).
* **Vector Store (`vector_store.py`)**: Gestión y consulta de la base de datos vectorial utilizando **ChromaDB** como motor local optimizado para garantizar almacenamiento eficiente sin costos fuera de la capa *Always Free*.

## 3. Inteligencia Artificial & Orquestación (`nuevamente_ai`)
* **Google Gemini**: Modelo de Lenguaje Grande (LLM) principal empleado para la generación de respuestas e inteligencia del sistema.
* **LangChain**: Framework orquestador de agentes y componentes para el manejo del flujo del pipeline RAG.
* **Gestión de Prompts (`prompts.py`)**: Plantillas dinámicas estructuradas en múltiples niveles de complejidad (principiante, avanzado, resúmenes, guiones, quizzes).
* **Esquemas de Validación**: Contratos definidos mediante modelos Pydantic para asegurar la consistencia en las respuestas de la IA.

## 4. Frontend & Interfaz de Usuario
* **Streamlit**: Framework interactivo para la interfaz gráfica del usuario.
* **Módulos de Vistas**: Arquitectura dividida en vistas de autenticación, carga de documentos, consultas interactivas y gestión de cuentas.
* **Estilos UI**: Hojas de estilo personalizadas en CSS.

## 5. Nube & Infraestructura (OCI)
* **Oracle Cloud Infrastructure (OCI)**: Despliegue en la nube utilizando la capa *Always Free* de Oracle para asegurar sostenibilidad y cumplimiento de los requisitos del hackathon.
* **Object Storage**: Almacenamiento en la nube de OCI para la gestión centralizada de documentos y respaldos del sistema.
* **Compute Instances & VCN**: Máquinas virtuales en la nube configuradas con reglas de red seguras para la ejecución de los servicios.

## 6. Control de Versiones & Gestión de Proyecto
* **Git y GitHub**: Control de versiones mediante ramas, flujos de trabajo (*GitHub Flow*) y resolución de *pull requests*.
* **Seguridad y Entorno**: Configuración de variables de entorno mediante `.env` protegido por `.gitignore`.
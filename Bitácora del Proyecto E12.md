# Bitácora de Proyecto - NuevaMente (Team 12)

## Programación Semanal y Entregables

### Semana 1: Planificación, Conceptualización y Arquitectura Base
* **Objetivos de la Semana**: Establecer las bases del proyecto, definir el alcance del pipeline RAG para el hackathon y configurar el entorno colaborativo del equipo.
* **Actividades Realizadas**:
  * Definición de la arquitectura modular (FastAPI para backend y Streamlit para frontend).
  * Creación del repositorio en GitHub, configuración de ramas y establecimiento del flujo de trabajo (GitHub Flow).
  * Distribución equilibrada de roles y tareas entre los integrantes del equipo.
* **Entregables de la Semana**:
  * Repositorio inicializado con la estructura de carpetas base (backend/, frontend/, docs/, project_management/).
  * Documento inicial de asignación de roles y flujos de trabajo.

### Semana 2: Desarrollo del Módulo de Ingestión y Pipeline RAG
* **Objetivos de la Semana**: Implementar la lógica central de procesamiento de documentos y almacenamiento vectorial.
* **Actividades Realizadas**:
  * Desarrollo de los extractores especializados para formatos PDF (extractorPDF.py) y Markdown (extractorMD.py).
  * Creación de los componentes de normalización, estructuración y control de huellas digitales (hashing) de los fragmentos (chunks).
  * Configuración del motor de almacenamiento vectorial (vector_store.py).
* **Entregables de la Semana**:
  * Módulo de ingestión funcional capaz de parsear y estructurar documentos educativos.
  * Pruebas unitarias iniciales para la validación del pipeline RAG y almacenamiento vectorial.

### Semana 3: Consolidación del Backend, Endpoints y Contratos de IA
* **Objetivos de la Semana**: Conectar el procesamiento de datos con la API y estructurar los contratos de inteligencia artificial.
* **Actividades Realizadas**:
  * Construcción de los routers asíncronos en FastAPI para la gestión de usuarios y generación de contenido.
  * Integración de las plantillas de prompts dinámicos (nuevamente_ai) orientadas a la adaptación de contenidos en múltiples niveles.
  * Implementación de esquemas de validación mediante Pydantic.
* **Entregables de la Semana**:
  * API REST operativa con endpoints de generación y validación de esquemas.
  * Conexión inicial del backend con el pipeline de prompts multinivel.

### Semana 4 (Cierre Hackathon): Integración Final y Despliegue del MVP
* **Objetivos de la Semana**: Consolidar la interfaz interactiva, validar los formatos de salida y realizar el despliegue del MVP en el entorno de producción.
* **Actividades Realizadas**:
  * Integración final de la interfaz interactiva en Streamlit con los distintos formatos de salida y adaptaciones.
  * Configuración de la infraestructura en Oracle Cloud Infrastructure (OCI) y despliegue del MVP en el entorno de producción (VM y Object Storage).
  * Pruebas integrales de extremo a extremo y validación de cumplimiento de la rúbrica del hackathon.
* **Entregables de la Semana**:
  * MVP desplegado y funcional en la nube de OCI.
  * Documentación técnica completa (Tech Stack, Bitácora y README) lista para la evaluación final de los jueces.
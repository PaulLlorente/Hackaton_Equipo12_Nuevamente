# 📂 Bitácora de Proyecto – G10-LATAM-equipo-12
**Proyecto:** 🎓 NuevaMente – Sistema Inteligente de Adaptación y Generación de Contenido Educativo  
**Rol PM:** Paul Enrique Llorente Gilbert  

Este documento registra el historial de avances, acuerdos de reuniones (Dailys/Sprints), decisiones técnicas y resolución de bloqueos durante el ciclo de desarrollo del MVP.

---

## 📅 Semana 1: Setup, Arquitectura y Pruebas de Concepto (PoC)
**Fechas:** [Insertar Fechas]  
**Estado:** En curso / Completado  

### 🎯 Objetivos de la Semana
- Configuración inicial del repositorio y tableros de trabajo.
- Pruebas aisladas de ingestión de documentos (PDF/MD) y conexión a OCI Object Storage.
- Levantamiento de interfaces base (Streamlit/Gradio) y estructura de API.

### 📝 Registro de Avances y Decisiones
- **Infraestructura & Git:** Se configuró el repositorio con protección de ramas (`main`) y se asignaron roles y accesos al equipo.
- **Backend / Ingestión:** Validación de librerías (`PyPDF`) para la extracción limpia de texto técnico.
- **Cloud (OCI):** Conexión exitosa al Bucket en la capa *Always Free* de Oracle Cloud Infrastructure.
- **Frontend / API:** Estructuras iniciales desplegadas localmente para pruebas de integración.

### 🚧 Bloqueos y Soluciones
- *Ninguno reportado hasta el momento.* / *(Ej: Demora menor en la asignación de credenciales de OCI, resuelta mediante documentación oficial).*

### 🤝 Acuerdos Clave
- Se utilizará `Pydantic` para asegurar el tipado estricto del JSON de salida que se comunicará entre el Backend y el Frontend.

---

## 📅 Semana 2: Desarrollo del Core (Integración Backend - RAG)
**Fechas:** [Insertar Fechas]  
**Estado:** Pendiente  

### 🎯 Objetivos de la Semana
- Implementación del pipeline RAG (Chunking, Embeddings y Vector Store).
- Conexión del flujo de ingesta de documentos con la API principal.
- Integración de la subida automática de archivos originales a OCI.

### 📝 Registro de Avances y Decisiones
- *(Espacio para documentar al finalizar la semana)*

### 🚧 Bloqueos y Soluciones
- *(Espacio para documentar bloqueos)*

---

## 📅 Semana 3: Orquestación LLM y Conexión Frontend
**Fechas:** [Insertar Fechas]  
**Estado:** Pendiente  

### 🎯 Objetivos de la Semana
- Conexión del LLM con los prompts estructurados según perfiles y formatos pedagógicos.
- Integración de la interfaz de Streamlit con los endpoints de la API.
- Persistencia de los paquetes JSON generados en OCI Object Storage.

### 📝 Registro de Avances y Decisiones
- *(Espacio para documentar al finalizar la semana)*

---

## 📅 Semana 4: Testing, Refinamiento y Demo Day
**Fechas:** [Insertar Fechas]  
**Estado:** Pendiente  

### 🎯 Objetivos de la Semana
- Pruebas de estrés y mitigación de alucinaciones en el pipeline RAG.
- Validación del checklist obligatorio del Hackathon (OCI, RAG, JSON, UI).
- Redacción final del `README.md` y grabación de la demo con 3 escenarios.

### 📝 Registro de Avances y Decisiones
- *(Espacio para documentar al finalizar la semana)*

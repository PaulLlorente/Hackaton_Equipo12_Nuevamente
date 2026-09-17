# 👥 Asignación de Roles y Cronograma de 30 Días – NuevaMente

Este documento detalla la distribución equitativa de la carga operativa por integrante según su perfil técnico, junto con el cronograma semanal de desarrollo (*Sprints*) enfocado en cumplir con todos los requerimientos del MVP.

---

## 👥 Asignación de Roles y Distribución de Carga (Equilibrada)

Equipo de 8 personas (1 AI Engineer, 1 Frontend, 3 Backend y 2 Full Stack), la carga se ha estructurado para que todos trabajen en paralelo hacia el MVP:  

* 👨‍💼 **Paul Enrique (Project Manager):**  
  * **Funciones:** Gestión del tablero en GitHub Projects, facilitador de Dailys (15 min diarios), asegurar que se cumpla la restricción de OCI "Always Free", redacción del README.md final, preparación del *Pitch* para el Demo Day y remoción de bloqueos (ej. conseguir credenciales).  

* 👨‍💻 **Cristhian Pereira (AI Engineer):**  
  * **Funciones:** Diseño del pipeline RAG, *Prompt Engineering* (perfiles, formatos de salida), y orquestación principal con LangChain/LangGraph y el LLM elegido.  

* 👩‍💻 **Angiee Auqui (Frontend Developer):**  
  * **Funciones:** Creación de la interfaz interactiva con Streamlit o Gradio, diseño de la carga de archivos y visualización del JSON final transformado en una UI amigable.  

* 👨‍💻 **Héctor Roberto (Full Stack Developer):**  
  * **Funciones:** Puente entre la UI de Angiee y el Backend. Validará los esquemas de entrada y salida con *Pydantic* (tipado estricto) para asegurar que la UI reciba el JSON perfectamente estructurado.  

* 💻 **Brayan Camilo (Full Stack Developer):**  
  * **Funciones:** Módulo de Ingestión de documentos. Codificará la extracción de texto de PDFs y Markdown (`PyPDF`, etc.) y lo preparará para que el AI Engineer lo procese.  

* 👩‍💻 **Cristhian Vanessa (Backend Developer - RAG Data):**  
  * **Funciones:** Implementación de la base de datos vectorial (*Vector Store* como ChromaDB o FAISS). Se encargará del *chunking* (segmentación) y la generación de embeddings. 

* ⚙️ **Edgar Moreno (Backend Developer - Cloud OCI):**  
  * **Funciones:** Integración exclusiva con OCI Object Storage. Crear los scripts (OCI SDK) para subir el PDF original y descargar el JSON final en el Bucket Always Free.  

* ⚙️ **Erick Hernandez (Backend Developer - API Core):**  
  * **Funciones:** Creación del servidor local o API (FastAPI o Flask) que una el módulo de ingestión, la base de datos vectorial, el LLM y OCI en un solo *Endpoint* que consumirá el Frontend.  

---

## 📅 Cronograma de 30 Días (Sprints Semanales)

### 🚀 Semana 1: Setup, Arquitectura y Pruebas de Concepto (PoC)
* **Objetivo:** Tener la infraestructura lista y scripts básicos funcionando aislados.
* **Paul (PM):** Configurar repositorio de GitHub, crear tablero Kanban, definir `.gitignore`, `.env.example` y crear la cuenta de OCI.
* **Brayan (FS):** Script en Python que lea un PDF técnico de prueba y extraiga el texto limpio.
* **Cristhian P. (AI) & Vanessa (Backend):** Script de prueba que tome el texto de Brayan, lo fragmente (*chunking*) y genere un embedding local.
* **Edgar (Backend):** Conectarse al Bucket de OCI con un script en Python y lograr subir un archivo de texto de prueba.  
* **Angiee (Front) & Héctor (FS):** Levantar un "Hola Mundo" en Streamlit/Gradio con un botón de subida de archivos.  
* **Erick (Backend):** Levantar la estructura base de FastAPI/Flask con endpoints vacíos.

### ⚙️ Semana 2: Desarrollo del Core (Integración Backend - RAG)
* **Objetivo:** El pipeline de datos debe procesar un archivo hasta la base vectorial y la API debe estar conectada.
* **Paul (PM):** Revisar que no se generen costos en OCI. Monitorear PRs rezagados en GitHub.  
* **Cristhian P. (AI):** Crear los prompts de sistema (roles: Principiante, Avanzado) y conectarlos al LLM.  
* **Vanessa (Backend):** Configurar ChromaDB/FAISS para buscar similitudes basándose en los embeddings.  
* **Erick (Backend) & Brayan (FS):** Conectar el módulo de ingestión con la API. Cuando se haga un `POST`, el documento debe enviarse al flujo de Vanessa.
* **Edgar (Backend):** Integrar la subida del archivo original a OCI dentro del flujo de la API.  

### 🧠 Semana 3: Orquestación LLM y Conexión Frontend
* **Objetivo:** Generar el primer JSON de salida correcto y mostrarlo en la interfaz.  
* **Cristhian P. (AI) & Héctor (FS):** Forzar al LLM (con *Pydantic* u outputs estructurados) a devolver estrictamente el JSON con metadatos, perfil, conceptos clave y contenido adaptado.  
* **Angiee (Front):** Conectar Streamlit al endpoint creado por Erick. Mostrar indicadores de carga mientras la IA procesa.
* **Edgar (Backend):** Tomar el JSON generado por el LLM y guardarlo en OCI Object Storage.  
* **Paul (PM):** Iniciar la preparación de la presentación (Demo Day). Testear la aplicación como usuario final con 2 documentos distintos.  

### 🎯 Semana 4: Testing, Refinamiento y Demo Day
* **Objetivo:** MVP estable, prevención de alucinaciones y entrega final.
* **Todo el equipo Técnico:** Resolución de bugs.
* **Cristhian P. (AI) & Vanessa (Backend):** Ajustar la temperatura del LLM y el *retrieval* de la base vectorial para evitar alucinaciones y asegurar fidelidad técnica.  
* **Angiee (Front) & Héctor (FS):** Mejorar el UX/UI, manejar mensajes de error (ej. si el PDF está corrupto o la API de LLM falla).  
* **Paul (PM):**
  * Validar que el MVP cumpla el *Checklist* obligatorio: PDF ingest, RAG, Outputs JSON, OCI Always Free.  
  * Completar la documentación del `README.md` en GitHub con diagrama de arquitectura.  
  * Grabar la demostración práctica con al menos 3 escenarios de adaptación.
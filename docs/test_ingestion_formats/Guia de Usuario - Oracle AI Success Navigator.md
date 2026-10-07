## Oracle® Customer Success: Guía de Usuario de Oracle AI Success Navigator para OCI

Versión de la Versión: 26.1.3

Código de Documento: G48003-08

Fecha de Publicación Oficial: Agosto 2026

Oracle Cloud Infrastructure Documentation

## Tabla de Contenidos Analítica

1. Descripción General de Oracle AI Success Navigator para OCI
- 1.1 Obtener Ayuda en la Plataforma
- 1.2 Canales de Soporte y Comunidad
- 1.3 Requisitos de Navegadores Web Compatibles
- 1.4 Accesibilidad de la Documentación
2. Primeros Pasos (Get Started)
- 2.1 Acerca de Oracle AI Success Navigator para OCI
- 2.2 Objetivos Principales del Sistema
- 2.3 Características y Capacidades de la Plataforma
- 2.4 Configuración Inicial para Administradores
- 2.5 Recorrido por la Página Principal (Home Page)
- 2.6 Inicio de Sesión y Autenticación
3. Ask Oracle en Success Navigator para OCI
- 3.1 Uso Operativo de Ask Oracle
- 3.2 Gestión de Conversaciones e Historial
- 3.3 Trucos y Mejores Prácticas de Prompting para OCI
- 3.4 Especificación del Endpoint de Inferencia OpenAI Compatible
- 3.5 Uso y Operación de la Biblioteca de Prompts (Prompt Library)
4. Uso de Herramientas y Recursos de Success Navigator
- 4.1 Cloud Migration Advisor (CMA)
- 4.2 Exploración de Journeys: Plantillas Base vs. Workload Journeys
- 4.3 Herramientas de Descubrimiento: Oracle Estate Explorer (OEE) y CPAT
- 4.4 Centro de Incorporación (Onboarding Center) y Rutas de Aprendizaje
- 4.5 Gestión Integral de Cargas de Trabajo (Workloads)
- 4.6 Catálogo de Arquitecturas de Referencia de OCI
- 4.7 Asistencia Generativa con AI Assist
- 4.8 Well-Architected Tool (WAT) y Evaluación por Pilares
5. Administración y Gobernanza de la Plataforma
- 5.1 Gestión de Miembros del Equipo (My Team)
- 5.2 Matriz de Privilegios por Nivel de Acceso (Access Level Privileges)
- 5.3 Gestión y Asignación de Socios de Implementación (Partners)
- 5.4 Repositorio Documental Centralizado (My Documents)
6. Notas de la Versión (Release Notes)
- 6.1 Registro de Cambios: Versión 26.1 (Mayo 2026)
- 6.2 Registro de Cambios: Versión 25.2.2 (2025)
- 6.3 Registro de Cambios: Versión 25.2.1 (2025)
7. Glosario Técnico de Términos de OCI

## Prefacio

Este prefacio describe las características de accesibilidad del documento y las convenciones adoptadas en el programa Success Navigator de Oracle.

## Declaración de Propósito

La Guía de Usuario de Oracle AI Success Navigator para OCI describe cómo utilizar Success Navigator para OCI para gestionar los viajes (journeys) de adopción de la nube de los clientes, integrando las mejores prácticas de la industria y orientación operativa paso a paso.

## Accesibilidad de la Documentación

Para obtener información detallada sobre el compromiso de Oracle con la accesibilidad en entornos digitales y software empresarial, visite el sitio web del Programa de Accesibilidad de Oracle en http://www.oracle.com/pls/topic/lookup?ctx=acc&amp;id=docacc.

## 1. Descripción General de Oracle AI Success Navigator para OCI

Success Navigator para OCI es una plataforma digital interactiva diseñada para guiar a su organización a través del ciclo de vida de sus cargas de trabajo (workloads) en Oracle Cloud Infrastructure. Success Navigator proporciona una consola unificada para supervisar el avance de las implementaciones, acceder a guías de despliegue paso a paso y utilizar herramientas diagnósticas avanzadas como el OCI Learning Center, el Cloud Migration Advisor (CMA) y la Well-Architected Tool (WAT).

┌───────────────────────────────────────────────────────────

─────────────┐

│

Oracle AI Success Navigator Workspace

│

├──────────────────┬───────────────────┬────────────────────

─────────────┤

│ Workloads Hub │ Guided Journeys │ Enterprise Tools

│

- │ · DB Migration │ · Discover │ · Cloud Migration Advisor │

- │ · Generative AI │ · Design │ · Well-Architected Tool (WAT) │
- │ · Multicloud │ · Implement │ · OCI Learning Center
- │

└──────────────────┴───────────────────┴────────────────────

─────────────┘

## 1.1 Obtener Ayuda en la Plataforma

Existen múltiples canales para profundizar en las capacidades de Success Navigator para OCI, recibir asistencia técnica especializada e interactuar con especialistas de producto:

- Menú de Asistencia: En el extremo superior derecho de la interfaz, el menú de ayuda consolida enlaces directos a la documentación oficial, las notas de lanzamiento, canales de tickets y módulos de retroalimentación.
- Buscador Integrado: La función de búsqueda del panel de ayuda permite indexar temas de soporte, manuales y notas de versión sin alterar la página activa de la aplicación.
- Lectura de Documentación: Incluye manuales de usuario detallados para cada módulo y registros de cambios funcionales de cada versión liberada.

## 1.2 Canales de Soporte y Comunidad

- Compartir Comentarios: Puede responder encuestas de satisfacción periódicas o enviar propuestas de mejora directamente al laboratorio de ideas (Idea Lab), donde la comunidad vota las características que se integrarán en futuras versiones de OCI.
- Cloud Customer Connect: Foro oficial de clientes de Oracle para debatir con ingenieros de soporte, arquitectos certificados y socios de canal autorizados.

## 1.3 Requisitos de Navegadores Web Compatibles

Para garantizar la compatibilidad con los estándares web modernos, la aceleración por hardware y la seguridad mediante cifrado TLS 1.3, Success Navigator para OCI admite los siguientes navegadores:

| Navegador Web         | Versión Mínima Requerida          | Estado de Certificación   |
|-----------------------|-----------------------------------|---------------------------|
| Versión 80 o superior | Certificado / Recomendado         | Google Chrome             |
| Apple Safari          | Certificado                       | Versión 13 o superior     |
| Versión 80 o superior | Certificado / Recomendado         | Microsoft Edge            |
| Mozilla Firefox       | Versión 68 o superior Certificado |                           |

## 2. Primeros Pasos (Get Started)

## 2.1 Acerca de Oracle AI Success Navigator para OCI

Success Navigator para OCI unifica los procesos de adopción tecnológica mediante rutas de trabajo guiadas y estructuradas. Reduce la fricción operativa al conectar la toma de decisiones inicial con la fase de ingeniería, apoyándose en plantillas validadas por los comités de arquitectura de Oracle.

## Objetivos Principales:

1. Proporcionar soporte guiado para iniciativas estratégicas como migración de bases de datos, despliegue de soluciones de IA Generativa y proyectos Multicloud enlazados con AWS, Azure o Google Cloud Platform.
2. Fomentar la colaboración segura entre el cliente, Oracle Consulting y socios de implementación a través de repositorios de archivos compartidos por proyecto con control de acceso por roles.
3. Habilitar la evaluación continua de posturas de seguridad y arquitectura utilizando la herramienta Well-Architected Tool.
4. Integrar el aprendizaje técnico continuo mediante rutas formativas oficiales embebidas directamente en la interfaz.

## 2.2 Características y Capacidades de la Plataforma

- Gestión Centralizada de Workloads: Tablero de control con métricas de distribución por tipo de proyecto, historial cronológico de actualizaciones y estado de ejecución.
- Rutas Guiadas (Guided Journeys): Fases estructuradas de Descubrimiento (Discover), Diseño (Design) e Implementación (Implement), equipadas con listas de verificación, cuestionarios y herramientas automatizadas.
- Integración Nativa con Herramientas OCI: Acceso directo a Cloud Migration Advisor, repositorios de arquitecturas de referencia y laboratorios de formación.

## 2.3 Configuración Inicial para Administradores

Si ha recibido la invitación de administrador del inquilino (tenant), debe completar el siguiente flujo de aprovisionamiento:

1. Localice el correo de bienvenida oficial de Oracle y seleccione el hipervínculo Log In, o acceda directamente a https://navigator.oracle.com/.
2. Lea detenidamente y acepte los Términos y Condiciones del Servicio. El acceso a las funciones operativas permanecerá bloqueado hasta que se confirme esta acción.
3. Diríjase a la sección Members (Miembros) en el menú principal para registrar los correos corporativos de los ingenieros y arquitectos que conformarán el equipo de trabajo.
4. Cree las primeras cargas de trabajo (workloads) asignándoles los tipos correspondientes (Database Migration, Gen AI o Multicloud).

Recomendación Operativa: No es necesario ingresar todos los parámetros técnicos y de infraestructura durante la creación inicial de la carga de trabajo; la configuración puede ajustarse progresivamente según avance el diseño técnico.

## 2.4 Recorrido por la Página Principal (Home Page)

La consola principal de Success Navigator se estructura en cuatro componentes visuales:

1. Manage Your Workloads (Administre sus Cargas de Trabajo): Gráficos de distribución de recursos, resumen de actividad reciente y accesos directos de edición.
2. Explore Journeys and Resources (Explorar Rutas y Recursos): Catálogo de rutas de adopción en modo plantilla para revisión conceptual previa al despliegue.
3. Encabezado de la Aplicación (Application Header): Barra superior con menú de navegación global, selector de organizaciones, buzón de notificaciones y panel de perfil.
4. Asistente Flotante Ask Oracle / AI Assist: Interfaz de lenguaje natural lista para responder consultas de arquitectura y generar planes de acción sobre la vista actual.

## 3. Ask Oracle en Success Navigator para OCI

Ask Oracle es un agente inteligente impulsado por IA Generativa que reside dentro de la plataforma para acelerar el análisis técnico, resumir requisitos de implementación y priorizar tareas operativas según dependencias y plazos.

<!-- image -->

─────────────┘

## 3.1 Uso Operativo de Ask Oracle

- Iniciar una Conversación: Abra el asistente desde cualquier página, seleccione un prompt sugerido o formule una consulta personalizada en lenguaje natural.
- Solicitar Salidas Estructuradas: Puede exigir que el modelo entregue sus respuestas como tablas comparativas, listas de verificación o diagramas cronológicos de tareas.
- Historial de Interacciones: Las conversaciones se nombran y respaldan de forma
- automática según la temática tratada. Puede renombrarlas o eliminarlas desde el menú contextual (...).
- Calificación y Retroalimentación: Cada respuesta dispone de controles de evaluación (pulgar arriba / pulgar abajo) y un cuadro para observaciones, lo que optimiza la precisión de las inferencias futuras.
- Seguridad y Confidencialidad: Está estrictamente prohibido introducir credenciales privadas, claves API o información de identificación personal (PII) en los campos de entrada de Ask Oracle.

## 3.2 Dieciséis Técnicas y Consejos para Interactuar con Ask Oracle

1. Claridad y Especificidad: Incluya siempre la carga de trabajo exacta, la etapa del proyecto y las restricciones de tiempo.
- Ejemplo: "Identifique las brechas de preparación para migrar una base de datos Oracle local a OCI. Priorice las cinco acciones críticas a completar en los próximos 30 días explicando su justificación técnica."
2. Descomposición de Solicitudes Complejas: Divida proyectos extensos en solicitudes secuenciales estructuradas en fases de identificación, diagnóstico y recomendación.
3. Definición de Formatos Estrictos: Ordene explícitamente a la IA generar resúmenes ejecutivos, tablas Markdown, listas con casillas de verificación o matrices de decisión.
4. Definición de Rol y Audiencia Objetivo: Indique la perspectiva profesional que debe asumir el modelo (ej.: "Como arquitecto de infraestructura..." o "Para una presentación ante el Director de Finanzas...").
5. Aclaración y Filtrado de Alcance: Aplique restricciones contextuales para excluir entornos de prueba, herramientas obsoletas o servicios fuera del presupuesto Always Free.
6. Preguntas de Seguimiento Iterativas: Mantenga una conversación activa para indagar sobre mitigación de riesgos, alternativas de alta disponibilidad o costos de almacenamiento.
7. Solicitud de Procedimientos Paso a Paso: Exija listas numeradas con prerrequisitos de red, políticas de identidad requeridas y criterios de validación exitosa.
8. Segmentación por Conversaciones Nuevas: Inicie un hilo de chat limpio cuando cambie radicalmente de carga de trabajo para evitar la contaminación de contexto en el LLM.
9. Mantenimiento del Hilo Contextual: Conserve el mismo chat mientras refine un artefacto específico (por ejemplo, al pedir ajustes sobre una tabla de migración generada previamente).
10. Inyección del Contexto Organizacional: Señale si su sistema requiere soporte para conexiones FastConnect privadas, límites máximos de caída (downtime) o compatibilidad multicloud.
11. Priorización por Retorno y Esfuerzo: Solicite que las recomendaciones se clasifiquen según su impacto en el negocio frente a las horas-hombre de desarrollo requeridas.
12. Seguimiento del Estado del Proyecto: Utilice el agente para cotejar el avance de una lista de tareas e identificar hitos atrasados o dependencias circulares.
13. Protección Rigurosa de Datos Sensibles: Emplee nombres genéricos (ej.

BaseDeDatos\_A, Servidor\_Web\_01) para proteger la topología real de su centro de datos.

14. Validación Cruzada contra Documentación Oficial: Verifique los parámetros obligatorios de servicios OCI contrastándolos con las notas de lanzamiento vigentes.
15. Generación de Representaciones Visuales en Texto: Ordene la creación de diagramas de flujo ASCII o cronogramas tipo Gantt en texto para insertarlos en documentos técnicos.
16. Salidas Multilingües y Adaptadas: Solicite explicaciones bilingües (inglés/español) o redacciones en lenguaje desprovisto de jerga técnica compleja para stakeholders no técnicos.

## 3.3 Especificación del Endpoint de Inferencia OpenAI Compatible

Ask Oracle utiliza un punto de enlace de inferencia de IA Generativa administrado por OCI, compatible con la especificación de API de OpenAI. Esto permite enlazar clientes estandarizados utilizando las siguientes coordenadas de red:

| Parámetro de Red                     | Valor de Configuración Oficial                                                         |
|--------------------------------------|----------------------------------------------------------------------------------------|
| Realm de Infraestructura             | OC1                                                                                    |
| Ubicación del Data Center            | US Midwest (Chicago)                                                                   |
| Identificador de Región (Region ID)  | us-chicago-1                                                                           |
| Ubicación Geográfica del Endpoint    | Estados Unidos                                                                         |
| URL de Acceso (Acciones de Chat)     | https://inference.generativeai.us-chicago-1. oci.oraclecloud.com/20231130/actions/chat |
| URL de Acceso (OpenAI v1 Compatible) | https://inference.generativeai.us-chicago-1. oci.oraclecloud.com/openai/v1             |

Nota de Seguridad de Red: Estos endpoints de servicio son invocados internamente por los componentes autorizados de Oracle. Los clientes gestionan su acceso mediante mecanismos de autorización basados en tokens de firma de OCI IAM.

## 3.4 Operación de la Biblioteca de Prompts (Prompt Library)

La Biblioteca de Prompts contiene plantillas validadas por ingenieros de Oracle para acelerar casos de uso frecuentes:

- Exploración: Filtre por categorías como Database Migration, Generative AI o Multicloud Deployments.
- Ejecución Directa: Seleccione Use this prompt para cargar la plantilla con sus parámetros en la ventana de chat activa.
- Comandos Slash (/): Si una plantilla cuenta con un identificador de barra, escriba / seguido del nombre clave (por ejemplo: /review-release-schedule) en el campo de texto

para ejecutarla de inmediato.

- Marcadores y Evaluaciones: Puede calificar la utilidad de los prompts, escribir reseñas internas y marcarlos como favoritos para consulta posterior.

## 4. Uso de Herramientas y Recursos de Success Navigator

## 4.1 Cloud Migration Advisor (CMA)

El Cloud Migration Advisor simplifica la complejidad de migrar bases de datos locales hacia OCI. Mediante su Modo Guiado (Guided Mode), la herramienta examina las versiones, esquemas, tipos de datos y conjuntos de caracteres de su entorno relacional para determinar la compatibilidad con Oracle Autonomous Database (Serverless o Dedicated) y proponer la metodología de migración más conveniente (Data Pump, Zero Downtime Migration o RMAN).

## 4.2 Exploración de Rutas (Journeys)

Un journey representa la secuencia metodológica recomendada por Oracle para ejecutar proyectos de nube sin contratiempos.

<!-- image -->

─────────────┘

## Comparativa entre Plantillas Base y Cargas de Trabajo Activas:

| Característica Funcional   | Base Journey (Plantilla)   | Workload Journey (Proyecto Activo)   |
|----------------------------|----------------------------|--------------------------------------|

| Propósito Principal     | Exploración conceptual y planificación        | Gestión técnica, ejecución y seguimiento        |
|-------------------------|-----------------------------------------------|-------------------------------------------------|
| Nivel de Acceso         | Público para todos los usuarios del inquilino | Restringido exclusivamente a miembros asignados |
| Capacidad de Edición    | Solo Lectura (Inmutable)                      | Totalmente editable y colaborativo              |
| Subida de Archivos      | No permitida                                  | Habilitada mediante módulo de Shared Files      |
| Seguimiento de Progreso | Inhabilitado                                  | Monitoreo porcentual por fases y tareas         |

## 4.3 Herramientas de Descubrimiento de Bases de Datos

En la etapa de Descubrimiento (Discover), el sistema integra utilidades especializadas que recopilan metadatos técnicos sin comprometer datos confidenciales:

- Oracle Estate Explorer (OEE): Evalúa el catálogo corporativo de bases de datos para estimar la preparación técnica, costos estimados de operación y dimensionamiento en Autonomous Database.
- Cloud Premigration Advisor Tool (CPAT): Analiza la base de datos de origen en busca de incompatibilidades técnicas, estructuras obsoletas o restricciones de almacenamiento antes de iniciar la transferencia de datos hacia OCI.

## 4.4 Centro de Incorporación (Onboarding Center)

El OCI Onboarding Center ofrece rutas formativas modulares adaptadas a diferentes roles:

- Getting Started with OCI: Fundamentos de computación, redes VCN, almacenamiento en bloques y Object Storage.
- Learn by Services: Entrenamientos enfocados en servicios individuales (Autonomous Database, OCI Generative AI, Streaming, etc.).
- Learn by Roles: Especializaciones para administradores de sistemas, desarrolladores de aplicaciones y arquitectos de seguridad en la nube.

## 4.5 Gestión de Cargas de Trabajo (Workloads)

Una carga de trabajo agrupa los recursos lógicos y físicos de OCI orientados a un fin empresarial específico. Actualmente, el sistema soporta cinco tipologías de proyecto:

1. Migración de Bases de Datos (Database Migration)
2. Implementación de IA Generativa (Generative AI)
3. Despliegues Multicloud: Microsoft Azure
4. Despliegues Multicloud: Amazon Web Services (AWS)
5. Despliegues Multicloud: Google Cloud Platform (GCP)

## Pasos para Crear una Carga de Trabajo:

1. En la consola principal, despliegue el menú de opciones y elija Add Workload.
2. Rellene los atributos solicitados: Nombre del Proyecto, Estado Actual, Socio de Implementación (Partner), Descripción Técnica, Notas Operativas y Tipo de Carga de Trabajo.
3. Presione el botón Submit.
4. Agregue los ingenieros y analistas responsables. Los miembros deben haber sido registrados previamente en el directorio global del equipo (My Team).
5. Seleccione Submit para finalizar la creación del espacio de trabajo y habilitar el viaje estructurado asociado.

## 4.6 Catálogo de Arquitecturas de Referencia de OCI

Colección de patrones de diseño aprobados por el comité de ingeniería de Oracle, los cuales mitigan riesgos en la interconexión de nubes y bases de datos críticas. Diseños destacados:

- Oracle ZDM - Logical Offline Migration to ADB-S on Oracle Database@Azure: Patrón que detalla cómo utilizar Zero Downtime Migration para migrar bases de datos on-premises hacia instancias de Oracle Autonomous Database Serverless alojadas dentro de la infraestructura compartida con Microsoft Azure.
- Oracle ZDM - Logical Offline Migration to ExaDB-D on Oracle Database@Azure: Arquitectura técnica para orquestar la migración de esquemas complejos hacia entornos dedicados de Exadata Database Service en Azure.

## 4.7 Asistencia Operativa con AI Assist

Complemento de productividad que permite interactuar con la consola mediante instrucciones conversacionales. Posee atajos para expandir la ventana al modo de pantalla completa, explorar el archivo histórico de interacciones, copiar esquemas directamente al portapapeles y reutilizar prompts preconstruidos según la vista activa.

## 4.8 Well-Architected Tool (WAT)

Herramienta diagnóstica que contrasta la infraestructura de una carga de trabajo frente a los cuatro pilares del marco de excelencia de Oracle:

┌────────────────────────────────────┐

<!-- image -->

<!-- image -->

└──────────────────┘

1. Seguridad y Cumplimiento: Políticas de identidad y acceso (IAM), cifrado de datos en reposo y en tránsito con claves maestras (KMS) y auditoría continua con Cloud Guard.
2. Confiabilidad y Resiliencia: Redundancia interregional, diseños multizona en dominios de disponibilidad (AD) y recuperación ante desastres (DR) con tiempos de recuperación objetivos (RTO/RPO) reducidos.
3. Rendimiento y Optimización de Costos: Dimensionamiento elástico de formas de cómputo GPU/CPU, particionamiento de almacenamiento y aprovechamiento de la capa Always Free.
4. Eficiencia Operativa: Automatización de despliegues mediante Terraform/Resource Manager, observabilidad con OCI Monitoring y gobernanza de recursos.

## Ciclo de Vida de una Evaluación:

- Creación: Se inicia un cuestionario asociándolo a una carga de trabajo en ejecución.
- Estados:
- In Progress: Cuestionario parcialmente completado; editable en cualquier momento.
- Completed: Respuestas consolidadas; la herramienta genera un informe de brechas y una calificación porcentual de apego a mejores prácticas.
- Retake (Reevaluación): Permite repetir el diagnóstico para medir el impacto de las modificaciones aplicadas a la infraestructura.

## 5. Administración y Gobernanza de la Plataforma

## 5.1 Gestión de Miembros del Equipo (My Team)

El panel My Team permite asignar ingenieros, consultores externos y especialistas de Oracle a proyectos determinados, definiendo su ámbito de visibilidad.

## Atributos de Cada Miembro:

- Nombre y Correo Electrónico: Credenciales de identidad corporativa.
- Relación (Relationship): Naturaleza contractual del usuario:
- Team Member: Personal directo del cliente.
- Partner: Integrador o consultor tecnológico autorizado.
- Oracle: Ingeniero de soporte o arquitecto oficial de Oracle.
- Nivel de Acceso (Access Level): Nivel jerárquico de control asignado.
- Cargas de Trabajo Vinculadas (Associated Workloads): Proyectos a los que el miembro puede acceder y en los que puede colaborar.

## 5.2 Matriz de Privilegios por Nivel de Acceso (Access Level Privileges)

Success Navigator cuenta con un sistema de autorización granular distribuido en tres niveles:

| Acción Funcional / Privilegio Operativo       | Viewer (Visualizador)   | Contributor (Colaborador)   | Admin (Administrador)   |
|-----------------------------------------------|-------------------------|-----------------------------|-------------------------|
| Visualizar la Consola Principal (Home)        | Sí                      | Sí                          | Sí                      |
| Consultar Plantillas de Rutas (Base Journeys) | Sí                      | Sí                          | Sí                      |
| Consultar Listado de Miembros del Equipo      | Sí                      | Sí                          | Sí                      |
| Registrar y Modificar Miembros del Equipo     | No                      | No                          | Sí                      |
| Visualizar Cargas de Trabajo (Workloads)      | Sí                      | Sí                          | Sí                      |
| Crear Nuevas Cargas de Trabajo                | No                      | No                          | Sí                      |
| Modificar Cargas de Trabajo Asignadas         | No                      | Sí                          | Sí                      |
| Acceder al Cloud                              | Sí                      | Sí                          | Sí                      |

| Migration Advisor (CMA)                             |    |    |    |
|-----------------------------------------------------|----|----|----|
| Explorar Documentación de Rutas Técnicas            | Sí | Sí | Sí |
| Descargar Recursos y Guías de un Journey            | Sí | Sí | Sí |
| Subir Archivos y Documentos a un Journey            | No | Sí | Sí |
| Navegar en el Centro de Formación (Learning Center) | Sí | Sí | Sí |
| Explorar Arquitecturas de Referencia                | Sí | Sí | Sí |
| Consultar la Herramienta Well-Architected (WAT)     | Sí | Sí | Sí |
| Iniciar Nuevas Evaluaciones de Arquitectura         | No | Sí | Sí |
| Actualizar Respuestas de Evaluaciones               | No | Sí | Sí |
| Visualizar Repositorio Central de Documentos        | Sí | Sí | Sí |
| Subir Archivos al                                   | No | Sí | Sí |

| Repositorio de Documentos                     |    |    |    |
|-----------------------------------------------|----|----|----|
| Consultar Planes de Versiones y Release Notes | Sí | Sí | Sí |

Regla de Resolución de Permisos: En caso de que un usuario posea múltiples roles superpuestos a través de grupos de identidad, el sistema aplicará los privilegios más permisivos (jerarquía: Admin &gt; Contributor &gt; Viewer).

## 5.3 Gestión y Asignación de Socios de Implementación (Partners)

Para garantizar la gobernanza del proyecto, los administradores pueden homologar los socios consultores que tendrán autorización para colaborar en el desarrollo de soluciones:

1. Haga clic en su perfil en el encabezado y elija Partner Management.
2. Seleccione la opción Add Partner.
3. Localice en el directorio corporativo el nombre de la firma consultora (por ejemplo, Accenture, Deloitte, Infosys o consultoría directa de Oracle) y confirme la selección.
4. Una vez aprobado, el socio figurará en los menús desplegables durante la creación o edición de cargas de trabajo.

## 5.4 Repositorio Documental Centralizado (My Documents)

El módulo My Documents funciona como una biblioteca de artefactos técnicos compartidos. Permite subir diagramas, guías operativas, especificaciones funcionales y enlaces web, controlando la audiencia destinataria.

## Formatos Compatibles y Restricciones de Tamaño:

- Límite de Tamaño Máximo por Archivo: 20 Megabytes (20 MB).
- Documentos Ofimáticos: PDF (.pdf), Microsoft Word (.doc, .docx), Excel (.xls, .xlsx), PowerPoint (.ppt, .pptx), Texto Plano (.txt) y Archivos Comprimidos (.zip).
- Archivos Multimedia de Audio: MP3 (.mp3), WAV (.wav), OGG (.ogg).
- Archivos Multimedia de Video: MP4 (.mp4), WEBM (.webm), OGV (.ogv).
- Archivos Gráficos e Imágenes: PNG (.png), JPG/JPEG (.jpg, .jpeg), GIF (.gif), WEBP (.webp).

## Procedimiento para Cargar Documentos y Enlaces:

1. Ingrese a My Documents desde el menú lateral de la plataforma.
2. Seleccione el botón Upload.
3. Ingrese el título descriptivo del archivo o la dirección URL del enlace externo.
4. Asigne los tipos de relación autorizados para visualizar el documento (Team Member, Partner o Oracle).
5. Arrastre el archivo hacia la zona de carga interactiva o ingrese la URL correspondiente.
6. Incluya etiquetas o comentarios explicativos para facilitar la indexación semántica en el buscador.
7. Asocie el artefacto a una carga de trabajo, una ruta (journey), una fase del ciclo de vida o una tarea técnica específica.
8. Presione Submit para completar la publicación.

## 6. Notas de la Versión (Release Notes)

## 6.1 Registro de Cambios: Versión 26.1 (Mayo 2026)

- Renombramiento Oficial: La plataforma adopta el nombre Oracle AI Success Navigator for OCI, reflejando la integración de agentes generativos en todas sus herramientas operativas.
- Modelo de Roles y Permisos Granulares: Rediseño del esquema de autorización con la incorporación del rol Contributor (en reemplazo del antiguo rol Member), permitiendo delegar la gestión técnica sin otorgar permisos globales de administración del inquilino.
- Expansión del Repositorio Multimedia (My Documents): Soporte oficial para archivos de presentación PowerPoint (.ppt, .pptx) y formatos de video (.mp4, .webm, .ogv) de hasta 20 MB por archivo.
- Nuevas Cargas de Trabajo (Workload Journeys):
- AI Services: Rutas guiadas y cuestionarios de arquitectura para capacidades cognitivas preentrenadas (OCI Vision, OCI Language, OCI Speech y OCI Document Understanding).
- Core Infrastructure: Diagnósticos para cómputo Bare Metal, redes elásticas, topologías de almacenamiento y esquemas de identidad corporativa.
- Oracle Integration Cloud (OIC): Procedimientos y flujos para plataformas de integración como servicio (iPaaS), conectores SaaS/on-premise y gestión de APIs.
- VMware Migration: Mejores prácticas y hojas de ruta para migrar entornos virtualizados hacia OCI VMware Solution (OCVS) manteniendo las herramientas operativas vSphere nativas.

## 6.2 Registro de Cambios: Versión 25.2.2 (2025)

- Lanzamiento de AI Assist: Incorporación del asistente conversacional con modelos de lenguaje fundacionales para resolver consultas técnicas de despliegue en tiempo real.
- Evolución del OCI Learning Center: Reorganización de las rutas de capacitación en categorías basadas en roles y servicios, con tarjetas modulares que exhiben el estado de avance en tiempo real.

## 6.3 Registro de Cambios: Versión 25.2.1 (2025)

- Lanzamiento Limitado (Limited Availability): Presentación inicial de la consola de Success Navigator para OCI, integrando los módulos fundacionales de Workloads, Journeys, Well-Architected Tool, Cloud Migration Advisor y Reference Architectures.
- Incidencia Conocida Documentada (Journeys &amp; My Documents): Debido a
- reestructuraciones en el esquema de la base de datos de rutas guiadas, algunos archivos asociados a journeys creados en versiones previas pueden perder su vinculación. Se instruye a los administradores a desvincular y volver a cargar los archivos afectados para restablecer los enlaces relacionales.

## 7. Glosario Técnico de Términos de OCI

- Autonomous Database (ADB): Base de datos relacional en la nube totalmente gestionada que utiliza aprendizaje automático para realizar ajustes de rendimiento, parches de seguridad, copias de respaldo y escalado de forma automática y sin tiempo de inactividad.
- Cloud Migration Advisor (CMA): Herramienta integrada en Success Navigator que analiza las características técnicas de bases de datos locales y genera recomendaciones para su migración hacia la nube de Oracle.
- Cloud Premigration Advisor Tool (CPAT): Utilidad basada en scripts y APIs que examina bases de datos Oracle de origen para validar que no existan objetos incompatibles antes de la migración.
- FastConnect: Servicio de conectividad de red dedicado y privado que conecta directamente el centro de datos local del cliente con Oracle Cloud Infrastructure sin transitar por la red pública de Internet.
- Identity and Access Management (IAM): Servicio que permite administrar quién tiene acceso a los recursos en la nube, qué nivel de privilegios posee y en qué compartimentos específicos puede operar.
- Oracle Estate Explorer (OEE): Solución de evaluación automatizada que cataloga y clasifica inventarios masivos de bases de datos relacionales para planificar su transición hacia arquitecturas autónomas.
- Oracle Zero Downtime Migration (ZDM): Mecanismo de migración automatizado desarrollado por Oracle que permite trasladar bases de datos hacia OCI con un tiempo de inactividad prácticamente nulo utilizando Oracle GoldenGate y Data Guard.
- Pilar Well-Architected: Cada una de las cuatro dimensiones de evaluación (Seguridad, Confiabilidad, Rendimiento/Costos y Operaciones) sobre las cuales se diagnostica la madurez técnica de una arquitectura en OCI.
- Virtual Cloud Network (VCN): Red privada definida por software (SDN) configurada en un centro de datos de Oracle, compuesta por subredes, tablas de enrutamiento y fire
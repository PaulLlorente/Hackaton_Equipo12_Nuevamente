# Formatos del backend

Solo genera el formato solicitado:

- resumen: conceptos_clave y contenido_adaptado son texto; tiempo_estudio es un
  entero positivo en minutos estimados; evaluacion_calidad describe cobertura.
- flashcard: contenido_adaptado es una lista no vacía de objetos pregunta/respuesta;
  cada tarjeta evalúa una idea respaldada. Los otros campos siguen Resumen.
- quiz: contenido_adaptado es una lista no vacía de preguntas. Conserva opciones
  como UN string, con etiquetas "A) ...; B) ...; C) ...". respuesta_correcta incluye
  etiqueta, justificación y referencia. Los distractores son alternativas de
  evaluación, no afirmaciones verdaderas; solo una opción debe ser correcta según
  las fuentes. No crees preguntas sobre datos ausentes. Los otros campos siguen Resumen.
- guion: usa titulo, tiempo_estimado como texto que indique duración estimada, y
  escenas no vacías. Cada escena tiene marca_tiempo, numero_escena consecutivo
  desde 1 y narrador como texto con referencias. Las marcas de tiempo deben
  seguir el orden del relato. No uses los campos exclusivos de Resumen.

No fuerces una cantidad fija de tarjetas, preguntas ni escenas: depende de la
evidencia disponible. Para un objetivo sin evidencia suficiente, contenido=null
y estado="evidencia_insuficiente" tienen prioridad sobre completar un formato.

# Prompts por perfil — Issue #15

## Entrega

Prompts base v1.0 para **principiante** y **avanzado**, con `resumen`, `flashcard`,
`quiz` y `guion`. Reutiliza los modelos de salida existentes del backend.
Admite título, objetivo, sector opcional y nivel de detalle `breve`/`detallado`.
El perfil controla complejidad; el detalle controla extensión. Ambos conservan
los hechos y límites de las fuentes.

El módulo prepara mensajes y valida respuestas. No hace llamadas a un proveedor.
Los ejemplos son sintéticos y escritos a mano, no respuestas reales de un LLM.
La conexión a `/adaptar` corresponde al backend. El contrato está implementado
como **propuesta de interfaz interna**, pendiente de acuerdo con Héctor; no es
el cuerpo HTTP público ni modifica el contrato de ingestión v1.0.

La rama parte del commit `7dc6ff8` de `chore/nuevamenteE12` (PR #23), que contiene
la organización nueva del equipo. Los archivos propios de esta entrega están
en `backend/src/nuevamente_ai`, `backend/scripts`, `backend/tests`,
`backend/data/samples` y `docs/contracts`.

## Instalación y prueba

Ejecutar desde la **raíz del repositorio**:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements-ai.txt
python -m pytest -q backend/tests/test_ai_prompts.py
```

Python 3.11+; también verificado con Python 3.12. Las únicas dependencias para
esta entrega son Pydantic, pytest y jsonschema. No necesita modelos descargados,
LangChain, Gemini ni claves. Este manifiesto no reemplaza las dependencias del
backend completo.

Las pruebas comprueban el contrato, sus ejemplos, ambos perfiles y cuatro
formatos, referencias permitidas, consistencia de páginas, aislamiento por
tenant/documento, presupuesto de contexto, abstención y CLI.
No evalúan el comportamiento ni la fidelidad factual de un LLM. Las pruebas de
ingestión y vector store del PR base tienen pendientes propios; ejecutar estas
pruebas no certifica todo ese PR.

## Vista previa sin consumir una API

```powershell
python backend/scripts/preview_prompts.py --input backend/data/samples/adaptation_request.example.json --output artifacts/prompts/ejemplo.json
```

El resultado contiene `system_prompt`, `user_prompt`, `sources` y
`response_schema`. Son mensajes preparados, no contenido educativo generado.
Para cambiar perfil, formato o detalle, editar una copia del JSON de entrada.
El CLI rechaza flags que sobrescriban un contrato completo.

También se pueden usar los chunks JSON/JSONL seleccionados por el retriever:

```powershell
python backend/scripts/preview_prompts.py --input backend/data/samples/prompt_context.example.json --tenant-id equipo-12-demo --document-id manual-demo --documento-titulo "Manual de prueba" --perfil avanzado --formato quiz --objetivo "Explicar los reintentos" --sector tecnologia --detalle detallado --output artifacts/prompts/avanzado.json
```

Seleccionar los chunks pertinentes antes de llamar al módulo. No enviar
automáticamente un PDF completo. Los artefactos de usuarios van en `artifacts/`,
ignorado por Git; los ejemplos versionados contienen únicamente datos sintéticos.

## Interfaz interna backend → prompts

El ejemplo completo es `backend/data/samples/adaptation_request.example.json`.

| Campo | Regla |
| --- | --- |
| `schema_version` | `1.0`; valor predeterminado si se omite |
| `tenant_id`, `document_id` | Alcance autorizado por el servidor |
| `documento_titulo` | Texto no vacío, hasta 500 caracteres |
| `perfil_destinatario` | `principiante` o `avanzado` |
| `formato_salida` | `resumen`, `flashcard`, `quiz`, `guion` |
| `nicho_sector` | Opcional, `null` o texto no vacío de hasta 200 caracteres |
| `nivel_detalle` | `breve` (predeterminado) o `detallado` |
| `objetivo` | Texto no vacío de hasta 2.000 caracteres |
| `evidencia` | Lista de chunks con IDs, texto, sección y páginas |

El tenant se deriva de la identidad autenticada y se autoriza el documento
**antes** de recuperar. Validar IDs en este módulo no demuestra autenticación.
No se permite mezclar tenants/documentos, repetir chunk IDs ni enviar datos
desconocidos en el contrato.

Cada chunk conserva `chunk_id`, `tenant_id`, `document_id`, `text`,
`section_title`, `page_start` y `page_end`. Las dos páginas pueden ser `null`
si no están disponibles; nunca se inventan. Cuando existan son el rango de la
sección/chunk, no una localización recalculada de cada frase.

En esta interfaz, `evidencia` sustituye al texto plano `documento_contenido`:
permite conservar atribución y páginas. Si `/adaptar` ya recibe texto plano,
Héctor puede mantener ese cuerpo HTTP y convertirlo a evidencia con origen
autorizado. No debe pasar dos textos contradictorios al módulo.

### Uso desde Python

```python
from backend.src.nuevamente_ai import build_from_contract

# payload ya incluye tenant y documento autorizados y los chunks recuperados.
bundle = build_from_contract(payload)

if not bundle.evidence:
    result = bundle.insufficient_response().model_dump()
else:
    # El backend configura y llama al LLM con estos dos mensajes.
    messages = [("system", bundle.system_prompt), ("human", bundle.user_prompt)]
    schema = bundle.output_model.model_json_schema()
    # raw_response = llamada_real_del_backend(messages, schema)
    # result = bundle.validate_response(raw_response).model_dump()

sources = bundle.sources  # Mapa del servidor para resolver F1, F2... a citas.
```

`validate_response` acepta JSON como string, un mapping o un modelo Pydantic.
No es un cliente de inferencia. Si el proveedor permite salida estructurada,
el backend puede usar `bundle.output_model`; esa compatibilidad debe probarse
con el modelo y SDK que adopte el equipo.

Para registros JSONL o resultados del PoC:

```python
from backend.src.nuevamente_ai import (
    PromptRequest, build_prompt, evidence_from_record,
)

request = PromptRequest(
    documento_titulo="Manual autorizado", perfil_destinatario="principiante",
    formato_salida="resumen", objetivo="Explicar los reintentos",
    tenant_id="empresa_autorizada", document_id="doc_autorizado",
    nicho_sector="tecnologia", nivel_detalle="detallado",
)
bundle = build_prompt(request, [evidence_from_record(r) for r in records])
```

El adaptador acepta metadatos superiores o en `metadata`, rechazando valores
contradictorios. Para un Document de LangChain se puede pasar
`{**doc.metadata, "text": doc.page_content}`. El retriever debe conservar
`chunk_id` en metadata, además del alcance; no se presume que Chroma lo incluya
automáticamente por haberlo usado como ID al indexar.

## Salida y referencias

El ejemplo es `backend/data/samples/adaptation_response.example.json`.

- `version_prompt`: `1.0`.
- `perfil`: el perfil solicitado.
- `estado`: `ok` o `evidencia_insuficiente`.
- `fuentes_usadas`: referencias permitidas, como `F1`.
- `advertencias`: limitaciones y estimaciones reales.
- `contenido`: Resumen/Flashcards/Quiz/Guion existente, o `null` si falta evidencia.

El campo `contenido_adaptado` permanece dentro de los modelos existentes de
resumen, flashcards y quiz; guion mantiene su propia lista de escenas. El backend
puede transformar la envoltura al contrato HTTP que acuerde con el frontend.

El validador exige referencias existentes, coincidencia de `[F1]` con las fuentes
declaradas, perfil/formato correctos, contenido no vacío, tiempos de estudio
positivos y numeración consecutiva del guion. No prueba que una afirmación se
derive de la fuente ni que una analogía o respuesta de quiz sea correcta.
Los modelos internos mantienen el comportamiento actual de Pydantic del equipo.

## Schemas para integrar

En `docs/contracts/`:

- `adaptation_prompt.schema.json`: entrada interna.
- `adaptation_response_resumen.schema.json`.
- `adaptation_response_flashcard.schema.json`.
- `adaptation_response_quiz.schema.json`.
- `adaptation_response_guion.schema.json`.

Para regenerarlos después de cambiar los modelos:

```powershell
python backend/scripts/export_prompt_contract.py
```

Los schemas validan la estructura; el módulo agrega comprobaciones de alcance,
duplicados, presupuesto y correspondencia de referencias.

## Evaluación posterior con el proveedor

`backend/data/samples/prompt_eval_cases.json` propone casos de respuesta con
evidencia, dato ausente, contexto vacío, instrucciones dentro del documento y
fuentes contradictorias. Ejecutarlos con ambos perfiles, cuatro formatos y ambos
detalles: **5 × 2 × 4 × 2 = 80 escenarios propuestos**, todavía pendientes.
Registrar versión del prompt, modelo, configuración y revisión humana.

Criterios: fidelidad a cifras/condiciones, diferencia pedagógica entre perfiles,
detalle apropiado, formato válido, citas respaldadas y abstención ante falta o
conflicto de fuentes. Separar datos de instrucciones reduce riesgos, pero no
garantiza resistencia a instrucciones maliciosas dentro de documentos.

El presupuesto predeterminado es 24.000 **caracteres del JSON de evidencia** y
20 chunks; no equivale a tokens. El backend debe medir el prompt entero según
el tokenizer del modelo y reservar espacio para salida. El módulo rechaza el
exceso sin recortar silenciosamente.

## Preparación del PR

Mantener el diff propio separado del PR #23. Mientras ese PR siga abierto, puede
abrirse el PR de prompts con base `chore/nuevamenteE12`. Cuando la reestructuración
esté en `main`, cambiar la base y revisar el diff antes del merge. Comparar con
`main` ahora mostraría también los tres commits previos de reestructuración.

Esta entrega no cierra automáticamente #15: el equipo debe revisar los prompts,
el contrato propuesto y sus pruebas. El endpoint, login, Chroma y OCI mantienen
sus propias tareas de integración.

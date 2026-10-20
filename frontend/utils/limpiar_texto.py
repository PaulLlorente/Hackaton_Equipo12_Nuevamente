import json
import re


def limpiar_texto(texto):
    """
    Limpia y normaliza el contenido recuperado del motor RAG.

    Características:
    - Maneja valores None y textos vacíos.
    - Extrae el campo 'texto' cuando el contenido es un JSON.
    - Convierte los saltos de línea literales (\\n) en saltos reales.
    - Normaliza saltos de línea de Windows, Linux y Mac.
    - Elimina espacios y tabulaciones innecesarios.
    - Conserva párrafos, listas, títulos y bloques de código.
    - Corrige espacios antes de los signos de puntuación.
    - Evita eliminar contenido textual legítimo.
    """

    # --------------------------------------------------------
    # 1. Validar y normalizar el tipo de entrada
    # --------------------------------------------------------
    if texto is None:
        return ""

    if not isinstance(texto, str):
        # Algunas fuentes pueden entregar estructuras JSON.
        try:
            texto = json.dumps(texto, ensure_ascii=False)
        except (TypeError, ValueError):
            texto = str(texto)

    texto = texto.strip()

    if not texto:
        return ""

    # --------------------------------------------------------
    # 2. Intentar interpretar un objeto JSON serializado
    # --------------------------------------------------------
    # Ejemplo:
    # {"texto": "Primera línea\\nSegunda línea"}
    #
    # Solo extraemos el campo "texto" cuando realmente existe.
    if texto.startswith("{") and texto.endswith("}"):
        try:
            datos = json.loads(texto)

            if isinstance(datos, dict):
                for clave in ("texto", "content", "page_content"):
                    if clave in datos:
                        texto = str(datos[clave] or "")
                        break

        except (json.JSONDecodeError, TypeError, ValueError):
            # Si no es JSON válido, se trata como texto normal.
            pass

    # --------------------------------------------------------
    # 3. Eliminar envolturas simples como "texto": "..."
    # --------------------------------------------------------
    texto = re.sub(r'^\s*"?texto"?\s*:\s*', "", texto, flags=re.IGNORECASE).strip()

    # Retirar las comillas exteriores solamente si forman
    # una envoltura completa y no son contenido legítimo.
    if len(texto) >= 2 and texto[0] == texto[-1] == '"':
        texto = texto[1:-1]

    # --------------------------------------------------------
    # 4. Normalizar saltos de línea
    # --------------------------------------------------------
    # Primero convertimos secuencias escapadas de CRLF.
    # Se contemplan una o más barras invertidas:
    # \n, \\n, \\\n, etc.
    texto = re.sub(r"\\+r\\+n", "\n", texto)
    texto = re.sub(r"\\+n", "\n", texto)
    texto = re.sub(r"\\+r(?![A-Za-z])", "\n", texto)

    # Normalizar saltos reales de distintos sistemas.
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")

    # Eliminar caracteres nulos.
    texto = texto.replace("\x00", "")

    # --------------------------------------------------------
    # 5. Normalizar espacios sin destruir el formato
    # --------------------------------------------------------
    lineas = texto.split("\n")
    lineas_limpias = []

    for linea in lineas:
        # Convertir tabulaciones en espacios.
        linea = linea.replace("\t", " ")

        # Compactar espacios consecutivos.
        linea = re.sub(r" {2,}", " ", linea)

        # Eliminar espacios en los extremos.
        linea = linea.strip()

        lineas_limpias.append(linea)

    texto = "\n".join(lineas_limpias)

    # --------------------------------------------------------
    # 6. Reducir saltos de línea excesivos
    # --------------------------------------------------------
    # Máximo una línea vacía entre párrafos.
    texto = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", texto)

    # --------------------------------------------------------
    # 7. Unir líneas partidas sin destruir listas ni bloques
    # --------------------------------------------------------
    # Los documentos Markdown pueden contener:
    # - Títulos: # Título
    # - Listas: - Elemento
    # - Numeración: 1. Elemento
    # - Citas: > Texto
    # - Tablas: | columna |
    # - Código: ```python
    #
    # No unimos automáticamente líneas estructurales.
    lineas = texto.split("\n")
    resultado = []

    en_bloque_codigo = False

    patron_estructura = re.compile(
        r"^(?:"
        r"#{1,6}\s|"  # Títulos Markdown
        r"[-*+]\s|"  # Listas
        r"\d+[.)]\s|"  # Listas numeradas
        r">\s?|"  # Citas
        r"\|.*\||"  # Filas de tablas
        r"```|"  # Bloques de código
        r"~~~|"  # Bloques de código alternativos
        r"<(?:div|p|br|ul|ol|li)\b|"  # HTML básico
        r")",
        flags=re.IGNORECASE,
    )

    for linea in lineas:
        # Detectar bloques de código para preservar su formato.
        if linea.startswith(("```", "~~~")):
            en_bloque_codigo = not en_bloque_codigo
            resultado.append(linea)
            continue

        # Dentro de un bloque de código no modificamos el texto.
        if en_bloque_codigo:
            resultado.append(linea)
            continue

        # Conservar párrafos vacíos.
        if not linea:
            if resultado and resultado[-1] != "":
                resultado.append("")
            continue

        es_estructura = bool(patron_estructura.match(linea))

        if not resultado or not resultado[-1]:
            resultado.append(linea)
            continue

        linea_anterior = resultado[-1]

        # No combinar con líneas que forman estructuras Markdown.
        anterior_es_estructura = bool(patron_estructura.match(linea_anterior))

        if es_estructura or anterior_es_estructura:
            resultado.append(linea)
        else:
            # Unir líneas normales que pertenecen a la misma frase.
            resultado[-1] = linea_anterior + " " + linea

    texto = "\n".join(resultado)

    # --------------------------------------------------------
    # 8. Corregir espacios antes de signos de puntuación
    # --------------------------------------------------------
    texto = re.sub(r"[ \t]+([,.;:!?])", r"\1", texto)

    # --------------------------------------------------------
    # 9. Eliminar líneas vacías en los extremos
    # --------------------------------------------------------
    texto = texto.strip()

    return texto
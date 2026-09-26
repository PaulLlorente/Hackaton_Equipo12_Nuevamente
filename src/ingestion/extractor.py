import pymupdf
from .hashing import calcular_sha256
from pathlib import Path
from .schema import FragmentoTexto, MetadataOrigen


class DocumentExtractor:
    """
    Servicio encargado exclusivamente de interactuar con el documento (se recibe en bytes desde el cliente o servidor). 
    Extrae metadatos y texto crudo.
    """

    # refactorizamos el alcance para recibir el archivo en bytes, evitamos ir a buscarlo en una ruta
    def __init__(self, source: bytes, nombre_archivo: str ):

            # ejecutamos la apertura del documento dentro de un bloque try-except para capturar errores de PyMuPDF                
        try:
            self.documento = pymupdf.open(stream=source, filetype="pdf")
            self.nombre_archivo = nombre_archivo
            self.source = source
                
        except pymupdf.Error as e:
            raise RuntimeError(f"Error de PyMuPDF al abrir el documento: {e}") from e

    # Context manager para asegurar el cierre del documento
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.documento.close()

    # Propiedades para obtener la extensión del archivo y el total de páginas
    @property
    def extension(self) -> str:
        return Path(self.nombre_archivo).suffix[1:]

    @property
    def total_paginas(self) -> int:
        return self.documento.page_count

    # Método para extraer fragmentos de texto del documento
    def extraer_fragmentos(self) -> list[FragmentoTexto]:

        fragmentos = []

        for numero_pagina, pagina in enumerate(self.documento, start=1):

            datos = pagina.get_text("dict")

            for block in datos.get("blocks", []):
                if block["type"] != 0:
                    continue

                textos_block = []
                primer_span = None

                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        texto = span.get("text", "").strip()

                        if primer_span is None and texto:
                            primer_span = span
                        if texto:
                            textos_block.append(texto)

                texto_completo = " ".join(textos_block).strip()

                if not texto_completo or primer_span is None:
                    continue

                fragmentos.append(
                    FragmentoTexto(
                        texto=texto_completo,
                        tamano_fuente=primer_span.get("size", 0.0),
                        pagina=numero_pagina,
                        negrita=bool(primer_span.get("flags", 0) & 16),
                        fuente=primer_span.get("font", None),
                        bbox=tuple(block.get("bbox")),  # ← bbox del BLOQUE completo
                    )
                )

        return fragmentos

    # Método para obtener metadatos del documento
    def get_metadata(self) -> MetadataOrigen:

        return MetadataOrigen(
            nombre_archivo= self.nombre_archivo,
            total_paginas=self.total_paginas,
            sha256=calcular_sha256(self.source),
        )
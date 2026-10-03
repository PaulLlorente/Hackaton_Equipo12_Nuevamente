import pymupdf
from ..hashing import calcular_sha256
from pathlib import Path
from ..schema import FragmentoTexto, MetadataOrigen, ResultadoExtraccion
from ..extractor import DocumentExtractor


class ExtractorPDF(DocumentExtractor):

    @property
    def extension(self) -> str:
        return Path(self.nombre_archivo).suffix[1:]

    @property
    def parser_name(self) -> str:
        return "PyMuPDF"

    @property
    def parser_version(self) -> str:
        return pymupdf.__version__

    def parse(self) -> ResultadoExtraccion:
        fragmentos = []

        try:
            with pymupdf.open(stream=self.source, filetype="pdf") as documento:

                for numero_pagina, pagina in enumerate(documento, start=1):

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
                                bbox=tuple(block.get("bbox")),
                            )
                        )
                metadatos = MetadataOrigen(
                    nombre_archivo=self.nombre_archivo,
                    total_paginas=documento.page_count,
                    sha256=calcular_sha256(self.source),
                    parser="PyMuPDF",
                    version_parser=pymupdf.__version__,
                )

                resultados_extraccion = ResultadoExtraccion(
                    fragmentos=fragmentos, metadata=metadatos
                )

            # Al salir del with, el PDF se cierra automáticamente.
            return resultados_extraccion

        except pymupdf.Error as e:
            raise RuntimeError(f"Error de PyMuPDF al procesar el documento: {e}") from e

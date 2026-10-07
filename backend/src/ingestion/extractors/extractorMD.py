from pathlib import Path
from ..schema import ResultadoExtraccion, MetadataOrigen, FragmentoTexto
from ..extractor import DocumentExtractor
from ..hashing import calcular_sha256


# clase que hereda de DocumentExtractor y se encarga de extraer datos de archivos Markdown
class ExtractorMarkdown(DocumentExtractor):

    @property
    def extension(self) -> str:
        return Path(self.nombre_archivo).suffix[1:]

    @property
    def parser_name(self) -> str:
        return "NativeMarkdown"

    @property
    def parser_version(self) -> str:
        return "1.0"

    def parse(self) -> ResultadoExtraccion:
        fragmentos = []

        try:
            contenido = self.source.decode("utf-8")

            # Recorremos el texto nativamente línea por línea
            for line in contenido.splitlines():
                texto = line.strip()
                if not texto:
                    continue

                # Simulamos el tamaño de fuente y página
                if texto.startswith("# "):
                    tamano = 24.0  # H1
                elif texto.startswith("## "):
                    tamano = 20.0  # H2
                elif texto.startswith("### "):
                    tamano = 16.0  # H3
                else:
                    tamano = 12.0  # Texto normal

                fragmentos.append(
                    FragmentoTexto(texto=texto, tamano_fuente=tamano, pagina=1)
                )

            metadatos = MetadataOrigen(
                nombre_archivo=self.nombre_archivo,
                total_paginas=1,
                sha256=calcular_sha256(self.source),
            )

            return ResultadoExtraccion(fragmentos=fragmentos, metadata=metadatos)

        except UnicodeDecodeError as e:
            raise RuntimeError(f"Error al decodificar el archivo Markdown: {e}")

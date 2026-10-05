"""
Interfaz principal de conversión Markdown a PDF para el proyecto BrainPolitics.
Proporciona la función `convert_md_to_pdf` y ejecutable por CLI.
"""

import sys
import os
import argparse
from typing import Optional
from .pdf_nerve import PDFNerve


def convert_md_to_pdf(
    input_path: str,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
    include_cover: bool = True,
    preset: str = "marxist_editorial"
) -> str:
    """Convierte un archivo Markdown (.md) en un PDF profesional para presentaciones públicas.

    Args:
        input_path: Ruta al archivo Markdown fuente (.md).
        output_path: Ruta del archivo PDF de salida. Si es None, se genera en la misma carpeta con extensión .pdf.
        title: Título personalizado del documento (opcional).
        include_cover: Si es True, incluye portada de presentación pública.
        preset: Estilo visual ("marxist_editorial", "academic_dark").

    Returns:
        str: Ruta absoluta al archivo PDF generado.

    Raises:
        FileNotFoundError: Si el archivo Markdown de entrada no existe.
        RuntimeError: Si ocurre un error durante el proceso de compilación PDF.
    """
    input_abs = os.path.abspath(input_path)
    if not os.path.exists(input_abs):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {input_path}")

    if not output_path:
        base, _ = os.path.splitext(input_abs)
        output_path = f"{base}.pdf"
    else:
        output_path = os.path.abspath(output_path)

    with open(input_abs, "r", encoding="utf-8") as f:
        md_content = f.read()

    nerve = PDFNerve()
    success = nerve.render_pdf(
        md_content=md_content,
        output_path=output_path,
        title=title,
        include_cover=include_cover,
        preset=preset
    )

    if not success:
        raise RuntimeError(f"Fallo en la generación del PDF para el archivo: {input_path}")

    return output_path


def main():
    """Línea de comandos CLI para conversión rápida."""
    parser = argparse.ArgumentParser(
        description="Convertidor profesional de Markdown a PDF (BrainPolitics)."
    )
    parser.add_argument("input_file", help="Ruta al archivo .md")
    parser.add_argument("-o", "--output", help="Ruta del PDF de salida (opcional)")
    parser.add_argument("-t", "--title", help="Título del documento para la portada")
    parser.add_argument("--no-cover", action="store_true", help="Omitir la portada de presentación pública")
    parser.add_argument("--preset", default="marxist_editorial", choices=["marxist_editorial", "academic_dark"], help="Estilo visual")

    args = parser.parse_args()

    try:
        pdf_out = convert_md_to_pdf(
            input_path=args.input_file,
            output_path=args.output,
            title=args.title,
            include_cover=not args.no_cover,
            preset=args.preset
        )
        print(f"✅ PDF generado exitosamente: {pdf_out}")
    except Exception as e:
        print(f"❌ Error al convertir documento: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

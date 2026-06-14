#!/usr/bin/env python3
"""
pdfslice — Recorta un rango de páginas de un PDF.

Uso:
    pdfslice <archivo.pdf> <inicio> [fin] [-o salida.pdf] [--open]

Ejemplos:
    pdfslice informe.pdf 3 7          → informe_p3-p7.pdf (junto al original)
    pdfslice informe.pdf 5            → desde pág 5 hasta el final
    pdfslice informe.pdf 3 7 -o /tmp/recorte.pdf
    pdfslice informe.pdf 3 7 --open   → genera y abre en Preview
"""

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Error: PyMuPDF no está instalado. Ejecuta: pip3 install pymupdf")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="pdfslice",
        description="Recorta un rango de páginas de un PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  pdfslice informe.pdf 3 7\n"
            "  pdfslice informe.pdf 5\n"
            "  pdfslice informe.pdf 3 7 -o /tmp/recorte.pdf\n"
            "  pdfslice informe.pdf 3 7 --open"
        ),
    )
    parser.add_argument("pdf", help="Ruta al archivo PDF de entrada")
    parser.add_argument("start", type=int, help="Página de inicio (base 1)")
    parser.add_argument("end", type=int, nargs="?", help="Página final (base 1, inclusive). Si se omite, va hasta el final.")
    parser.add_argument("-o", "--output", help="Ruta del PDF de salida (opcional)")
    parser.add_argument("--open", action="store_true", dest="open_after", help="Abrir el resultado al terminar")
    return parser.parse_args()


def default_output_path(input_path: Path, start: int, end: int) -> Path:
    stem = input_path.stem
    suffix = input_path.suffix
    name = f"{stem}_p{start}-p{end}{suffix}"
    return input_path.parent / name


def main():
    args = parse_args()

    input_path = Path(args.pdf).expanduser().resolve()
    if not input_path.exists():
        sys.exit(f"Error: no se encontró el archivo '{input_path}'")
    if not input_path.suffix.lower() == ".pdf":
        sys.exit(f"Error: el archivo no tiene extensión .pdf")

    doc = fitz.open(str(input_path))
    total_pages = doc.page_count

    start = args.start
    end = args.end if args.end is not None else total_pages

    # Validaciones
    if start < 1:
        sys.exit(f"Error: la página de inicio debe ser ≥ 1 (recibido: {start})")
    if end < start:
        sys.exit(f"Error: la página final ({end}) no puede ser menor que la de inicio ({start})")
    if start > total_pages:
        sys.exit(f"Error: la página de inicio ({start}) supera el total de páginas del documento ({total_pages})")
    if end > total_pages:
        print(f"Aviso: la página final ({end}) supera el total ({total_pages}). Se usará {total_pages}.")
        end = total_pages

    # Determinar ruta de salida
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = default_output_path(input_path, start, end)

    # Extraer páginas en un documento nuevo (PyMuPDF usa índices 0-based).
    # insert_pdf copia solo los recursos usados por las páginas seleccionadas,
    # evitando que el output herede el peso completo del original.
    out = fitz.open()
    out.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
    out.save(str(output_path), garbage=4, deflate=True)
    out.close()
    doc.close()

    print(f"✓ {total_pages} págs. → recorte p{start}–p{end} ({end - start + 1} págs.)")
    print(f"  {output_path}")

    if args.open_after:
        subprocess.run(["open", str(output_path)])


if __name__ == "__main__":
    main()

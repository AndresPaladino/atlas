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


def _fitz():
    """Importa PyMuPDF perezosamente para que importar este módulo sea barato."""
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:  # pragma: no cover - depende del entorno
        raise RuntimeError(
            "PyMuPDF no está instalado. Ejecutá: pip3 install pymupdf"
        ) from exc
    return fitz


def page_count(pdf: Path) -> int:
    """Cantidad de páginas de un PDF."""
    doc = _fitz().open(str(pdf))
    try:
        return doc.page_count
    finally:
        doc.close()


def slice_pdf(src: Path, start: int, end: int, out: "Path | None" = None) -> Path:
    """Recorta ``src`` a las páginas [start, end] (base 1, inclusive).

    ``insert_pdf`` copia solo los recursos usados por las páginas seleccionadas,
    así el recorte no hereda el peso completo del original. Devuelve la ruta de
    salida (junto al original si ``out`` es None).
    """
    src = Path(src)
    fitz = _fitz()
    doc = fitz.open(str(src))
    try:
        total = doc.page_count
        if start < 1:
            raise ValueError(f"la página de inicio debe ser ≥ 1 (recibido: {start})")
        if start > total:
            raise ValueError(f"la página de inicio ({start}) supera el total ({total})")
        end = min(end, total)
        if end < start:
            raise ValueError(f"la página final ({end}) es menor que la de inicio ({start})")
        if out is None:
            out = default_output_path(src, start, end)
        out = Path(out)
        new = fitz.open()
        try:
            new.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
            new.save(str(out), garbage=4, deflate=True)
        finally:
            new.close()
        return out
    finally:
        doc.close()


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

    total_pages = page_count(input_path)

    start = args.start
    end = args.end if args.end is not None else total_pages

    if end > total_pages:
        print(f"Aviso: la página final ({end}) supera el total ({total_pages}). Se usará {total_pages}.")
        end = total_pages

    output_path = (
        Path(args.output).expanduser().resolve() if args.output else None
    )

    try:
        output_path = slice_pdf(input_path, start, end, output_path)
    except ValueError as exc:
        sys.exit(f"Error: {exc}")

    end = min(end, total_pages)
    print(f"✓ {total_pages} págs. → recorte p{start}–p{end} ({end - start + 1} págs.)")
    print(f"  {output_path}")

    if args.open_after:
        subprocess.run(["open", str(output_path)])


if __name__ == "__main__":
    main()

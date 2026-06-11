"""CLI de atlas:  extract · status · doctor."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import resolve_tier
from .device import detect_device, ollama_available
from .manifest import Manifest, Status

app = typer.Typer(
    add_completion=False,
    help="Atlas CLI — extrae PDFs a markdown (PDF → markdown+LaTeX+captions).",
)
console = Console()


# ── localización del directorio raw/ ──────────────────────────────────────────
def find_raw_dir(explicit: Optional[Path]) -> Path:
    """Resuelve raw/: --raw > $ATLAS_RAW > raíz de Atlas (subiendo desde cwd) > ./raw."""
    if explicit is not None:
        return explicit.expanduser().resolve()
    env = os.environ.get("ATLAS_RAW")
    if env:
        return Path(env).expanduser().resolve()
    cur = Path.cwd().resolve()
    for base in (cur, *cur.parents):
        if (base / "schema").is_dir() and (base / "raw").is_dir():
            return base / "raw"
    return (cur / "raw").resolve()


def _iter_pdfs(raw_dir: Path):
    return sorted(p for p in raw_dir.rglob("*.pdf") if p.is_file())


# ── doctor ──────────────────────────────────────────────────────────────────
@app.command()
def doctor() -> None:
    """Muestra device detectado, tier elegido y disponibilidad de Ollama."""
    device = detect_device()
    tier = resolve_tier(device)
    has_ollama = ollama_available()

    table = Table(title=f"atlas v{__version__} · diagnóstico", show_header=False)
    table.add_row("Device", device.label)
    table.add_row("torch", "disponible" if device.torch_available else "[red]NO instalado[/red]")
    table.add_row("Tier", tier.summary)
    table.add_row(
        "Captions",
        "[green]activables[/green] (--captions)"
        if (tier.captions and has_ollama)
        else ("[yellow]Ollama no instalado[/yellow]" if tier.captions
              else "[dim]no en este tier[/dim]"),
    )
    console.print(table)

    if not device.torch_available:
        console.print("[yellow]torch no está; correrá el fallback markitdown (texto plano). "
                      "Reinstalá con ./install.sh para habilitar marker.[/yellow]")


# ── status ────────────────────────────────────────────────────────────────────
@app.command()
def status(
    raw: Optional[Path] = typer.Option(None, "--raw", help="Directorio raw/ (auto-detectado por defecto)."),
) -> None:
    """Lista los PDFs de raw/ clasificados en converted / stale / pending."""
    raw_dir = find_raw_dir(raw)
    if not raw_dir.is_dir():
        console.print(f"[red]No existe el directorio raw/: {raw_dir}[/red]")
        raise typer.Exit(1)

    manifest = Manifest.load(raw_dir)
    pdfs = _iter_pdfs(raw_dir)

    counts = {Status.CONVERTED: 0, Status.STALE: 0, Status.PENDING: 0}
    table = Table(title=f"raw/ = {raw_dir}")
    table.add_column("estado")
    table.add_column("archivo")
    for pdf in pdfs:
        st = manifest.status_of(pdf)
        counts[st] += 1
        color = {"converted": "green", "stale": "yellow", "pending": "cyan"}[st.value]
        table.add_row(f"[{color}]{st.value}[/{color}]", pdf.relative_to(raw_dir).as_posix())

    console.print(table)
    console.print(
        f"[green]{counts[Status.CONVERTED]} converted[/green] · "
        f"[yellow]{counts[Status.STALE]} stale[/yellow] · "
        f"[cyan]{counts[Status.PENDING]} pending[/cyan] · {len(pdfs)} total"
    )


# ── git push helper ───────────────────────────────────────────────────────────
def _git_push(raw_dir: Path, extracted_pdfs: list[Path]) -> None:
    import subprocess

    repo_root = raw_dir.parent
    md_files = [str(p.with_suffix(".md").relative_to(repo_root)) for p in extracted_pdfs]
    manifest_rel = str((raw_dir / ".atlas-extract.json").relative_to(repo_root))

    def run(cmd: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)

    console.print("\n[cyan]▸ git add …[/cyan]")
    r = run(["git", "add"] + md_files + [manifest_rel])
    if r.returncode != 0:
        console.print(f"[red]git add falló:[/red] {r.stderr.strip()}")
        return

    n = len(md_files)
    names = ", ".join(Path(f).stem for f in md_files)
    msg = f"Extract {n} PDF(s) to markdown via atlas-local [{names}]"
    console.print(f"[cyan]▸ git commit …[/cyan]")
    r = run(["git", "commit", "-m", msg])
    if r.returncode != 0:
        if "nothing to commit" in r.stdout:
            console.print("[yellow]Nada nuevo para commitear (ya estaba up to date).[/yellow]")
        else:
            console.print(f"[red]git commit falló:[/red] {r.stderr.strip()}")
        return

    console.print("[cyan]▸ git push …[/cyan]")
    r = run(["git", "push"])
    if r.returncode == 0:
        console.print("[green]✓ Push exitoso.[/green]")
    else:
        console.print(f"[red]git push falló:[/red] {r.stderr.strip()}")


# ── extract ────────────────────────────────────────────────────────────────────
@app.command()
def extract(
    paths: list[Path] = typer.Argument(None, help="PDFs específicos; vacío = todos los pendientes de raw/."),
    raw: Optional[Path] = typer.Option(None, "--raw", help="Directorio raw/ (auto-detectado por defecto)."),
    captions: bool = typer.Option(False, "--captions", help="Generar captions de figuras (requiere Ollama)."),
    force: bool = typer.Option(False, "--force", help="Re-extraer aunque ya esté converted."),
    push: bool = typer.Option(False, "--push", help="Commit y push de los .md y manifest al terminar."),
) -> None:
    """Convierte PDFs de raw/ a markdown (sibling .md) y actualiza el manifest."""
    from .extract import Extractor  # import perezoso (arrastra torch/marker)

    raw_dir = find_raw_dir(raw)
    if not raw_dir.is_dir():
        console.print(f"[red]No existe el directorio raw/: {raw_dir}[/red]")
        raise typer.Exit(1)

    device = detect_device()
    tier = resolve_tier(device)
    manifest = Manifest.load(raw_dir)

    # Selección de targets.
    if paths:
        targets = [p.expanduser().resolve() for p in paths]
    else:
        targets = [
            p for p in _iter_pdfs(raw_dir)
            if force or manifest.status_of(p) in (Status.PENDING, Status.STALE)
        ]

    if not targets:
        console.print("[green]Nada para extraer: todo está converted.[/green] "
                      "(Usá --force para re-extraer.)")
        return

    do_captions = captions and tier.captions and ollama_available()
    if captions and not do_captions:
        console.print("[yellow]--captions ignorado: el tier no lo soporta o falta Ollama.[/yellow]")

    console.print(f"[cyan]Device:[/cyan] {device.label}  ·  [cyan]Tier:[/cyan] {tier.name}  ·  "
                  f"[cyan]Captions:[/cyan] {'sí' if do_captions else 'no'}")
    console.print(f"[cyan]A extraer:[/cyan] {len(targets)} PDF(s)\n")

    extractor = Extractor(tier, device)
    ok = 0
    extracted = []
    for pdf in targets:
        rel = pdf.relative_to(raw_dir).as_posix() if raw_dir in pdf.parents or pdf.parent == raw_dir else pdf.name
        try:
            console.print(f"▸ {rel} …", end=" ")
            result = extractor.extract(pdf)

            if do_captions and result.images:
                from .caption import caption_images, inline_captions

                caps = caption_images(result.images, tier.caption_model)
                result.markdown = inline_captions(result.markdown, caps)

            md_path = pdf.with_suffix(".md")
            header = (
                f"<!-- atlas-local: extraído de {rel} con {result.extractor} "
                f"v{result.extractor_version} en {device.kind}. No editar a mano. -->\n\n"
            )
            md_path.write_text(header + result.markdown, encoding="utf-8")

            # Imágenes locales junto al .md (gitignored); habilitan render local de refs.
            for name, data in result.images.items():
                (pdf.parent / name).write_bytes(data)

            manifest.record(
                pdf, md_path=md_path, extractor=result.extractor,
                extractor_version=result.extractor_version, device=device.kind,
                n_pages=result.n_pages, n_figs=result.n_figs,
            )
            ok += 1
            extracted.append(pdf)
            console.print(f"[green]✓[/green] {result.n_pages}p / {result.n_figs} figs")
        except Exception as exc:  # noqa: BLE001 — un PDF roto no debe frenar el batch
            console.print(f"[red]✗ {exc}[/red]")

    manifest.save()
    console.print(f"\n[green]Listo:[/green] {ok}/{len(targets)} extraídos. "
                  f"Manifest: {manifest.path.relative_to(raw_dir.parent)}")

    if push and extracted:
        _git_push(raw_dir, extracted)


@app.command()
def render(
    file: Optional[Path] = typer.Argument(None, help="Archivo .md/.txt; vacío = lee stdin."),
) -> None:
    """Filtro LaTeX→Unicode best-effort para leer mate en terminal cruda."""
    import sys

    from .render import render_text

    text = file.read_text(encoding="utf-8") if file else sys.stdin.read()
    sys.stdout.write(render_text(text))


if __name__ == "__main__":
    app()

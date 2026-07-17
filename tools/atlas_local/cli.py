"""CLI de atlas:  extract · status · doctor."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

# Referencia de imagen generada por marker: ![](_page_N_Kind_idx.ext)
# sin prefijo de directorio (i.e. bare, sibling al .md).
_BARE_IMG_REF_RE = re.compile(r"(!\[[^\]]*\]\()(_page_[^/)\s]+)(\))")


def _prefix_image_refs(markdown: str, prefix: str) -> str:
    """Reescribe refs de imagen bare (_page_…) → <prefix>/_page_… en el monolítico."""
    return _BARE_IMG_REF_RE.sub(lambda m: f"{m.group(1)}{prefix}/{m.group(2)}{m.group(3)}", markdown)

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from . import segment as seg_mod  # lógica pura, sin torch
from .config import resolve_tier, THROTTLE_PROFILES, DEFAULT_THROTTLE, ThrottleProfile
from .device import detect_device, ollama_available
from .manifest import Manifest, Status

# Tamaño aproximado de los modelos de marker al descargar por primera vez.
_MARKER_MODELS_GB = 8.5


def _resolve_cache_dir(raw_dir: Path) -> Path:
    """Directorio de caché de modelos HF/torch.

    Orden: ATLAS_CACHE env var → misma unidad que raw/ → ~/.atlas-cache.
    Poner la caché en la misma unidad que raw/ evita llenar C: en Windows.
    """
    env = os.environ.get("ATLAS_CACHE")
    if env:
        return Path(env).expanduser().resolve()
    # raw_dir es atlas/raw/, su padre es la raíz del proyecto.
    return raw_dir.parent / ".atlas-cache"


def _apply_throttle(profile: ThrottleProfile) -> None:
    """Aplica nice/ionice al proceso actual. Silencioso si el SO no lo soporta."""
    import sys
    if sys.platform == "win32":
        return
    try:
        os.nice(profile.nice)
    except (OSError, AttributeError):
        pass
    if profile.ionice == 3:
        try:
            import subprocess as _sp
            _sp.run(["ionice", "-c", "3", "-p", str(os.getpid())], capture_output=True)
        except Exception:
            pass  # ionice no disponible → sin efecto


def _preflight(targets: list[Path], cache_dir: Path, raw_dir: Path) -> None:
    """Advierte si el espacio en disco o la RAM disponible son ajustados."""
    import shutil

    warnings_found = []

    # ── Disco en cache_dir (modelos ~8.5 GB en primera descarga) ─────────────
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        du = shutil.disk_usage(cache_dir)
        free_gb = du.free / 1024**3
        hf_hub = cache_dir / "hub"
        already_cached = hf_hub.exists() and any(hf_hub.iterdir())
        if not already_cached and free_gb < _MARKER_MODELS_GB + 2:
            warnings_found.append(
                f"[yellow]⚠  Disco en {cache_dir.drive or str(cache_dir)}: "
                f"{free_gb:.1f} GB libres — primera descarga de modelos ocupa "
                f"~{_MARKER_MODELS_GB:.0f} GB. Puede quedarse sin espacio.[/yellow]"
            )
    except OSError:
        pass

    # ── RAM disponible (marker necesita ~6–8 GB) ──────────────────────────────
    try:
        import psutil  # dep transitiva de varios paquetes del entorno

        free_ram_gb = psutil.virtual_memory().available / 1024**3
        if free_ram_gb < 6:
            warnings_found.append(
                f"[yellow]⚠  RAM disponible: {free_ram_gb:.1f} GB — "
                f"marker carga modelos que ocupan ~6–8 GB. "
                f"Puede quedarse sin memoria.[/yellow]"
            )
    except ImportError:
        pass  # psutil no instalado: saltear el chequeo de RAM

    for w in warnings_found:
        console.print(w)
    if warnings_found:
        console.print()

app = typer.Typer(
    add_completion=False,
    help="Atlas CLI — backend del knowledge graph (validate/lint/index/session) "
         "y extracción de PDFs (extract).",
)
console = Console()


# ── localización del wiki / raíz del repo ─────────────────────────────────────
def _require_wiki(explicit: Optional[Path]) -> Path:
    """Resuelve wiki/ o aborta con mensaje claro."""
    from .wiki.paths import find_wiki_dir

    wiki = find_wiki_dir(explicit)
    if wiki is None or not wiki.is_dir():
        console.print("[red]No encuentro wiki/. Corré el comando dentro del repo "
                      "Atlas o pasá --wiki.[/red]")
        raise typer.Exit(1)
    return wiki


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
def _git_push(raw_dir: Path, extracted_pdfs: list[Path], artifacts_dir: Path) -> None:
    import subprocess

    repo_root = raw_dir.parent
    md_files = [str((artifacts_dir / p.relative_to(raw_dir)).with_suffix(".md").relative_to(repo_root)) for p in extracted_pdfs]
    manifest_rel = str((raw_dir / ".atlas-extract.json").relative_to(repo_root))

    # Artefactos de segmentación (cuando el doc se segmentó): TOC + dir de chunks.
    seg_files: list[str] = []
    for p in extracted_pdfs:
        stem = p.relative_to(raw_dir).as_posix().replace(".pdf", "")
        toc = artifacts_dir / (stem + ".toc.md")
        chunks_dir_p = artifacts_dir / stem
        if toc.exists():
            seg_files.append(str(toc.relative_to(repo_root)))
        if chunks_dir_p.is_dir():
            seg_files.append(str(chunks_dir_p.relative_to(repo_root)))

    def run(cmd: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)

    console.print("\n[cyan]▸ git add …[/cyan]")
    r = run(["git", "add"] + md_files + seg_files + [manifest_rel])
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
    usellm: bool = typer.Option(False, "--usellm", help="Mejorar tablas/ecuaciones/reading-order vía LLM (Ollama, requiere Ollama)."),
    force: bool = typer.Option(False, "--force", help="Re-extraer aunque ya esté converted."),
    push: bool = typer.Option(False, "--push", help="Commit y push de los .md y manifest al terminar."),
    segment: Optional[bool] = typer.Option(None, "--segment/--no-segment", help="Forzar/inhibir la segmentación en chunks+TOC (default: auto por umbral de tamaño)."),
    throttle: str = typer.Option(DEFAULT_THROTTLE, "--throttle", help="Perfil de uso de recursos: low|medium|full-throttle (default: medium)."),
) -> None:
    """Convierte PDFs de raw/ a markdown y actualiza el manifest. Artefactos en extracted/."""
    from .extract import Extractor  # import perezoso (arrastra torch/marker)

    raw_dir = find_raw_dir(raw)
    if not raw_dir.is_dir():
        console.print(f"[red]No existe el directorio raw/: {raw_dir}[/red]")
        raise typer.Exit(1)

    artifacts_dir = raw_dir.parent / "extracted"
    artifacts_dir.mkdir(exist_ok=True)

    cache_dir = _resolve_cache_dir(raw_dir)  # override con $ATLAS_CACHE

    device = detect_device()
    tier = resolve_tier(device)
    manifest = Manifest.load(raw_dir, artifacts_dir)

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

    do_usellm = usellm and tier.captions and ollama_available()
    if usellm and not do_usellm:
        console.print("[yellow]--usellm ignorado: el tier no lo soporta o falta Ollama.[/yellow]")

    profile = THROTTLE_PROFILES.get(throttle)
    if profile is None:
        console.print(f"[red]--throttle debe ser low, medium o full-throttle.[/red]")
        raise typer.Exit(1)

    effective_batch = profile.batch_pages
    _apply_throttle(profile)

    _preflight(targets, cache_dir, raw_dir)

    console.print(f"[cyan]Device:[/cyan] {device.label}  ·  [cyan]Tier:[/cyan] {tier.name}  ·  "
                  f"[cyan]Throttle:[/cyan] {profile.name} (batch={effective_batch})  ·  "
                  f"[cyan]Captions:[/cyan] {'sí' if do_captions else 'no'}  ·  "
                  f"[cyan]LLM:[/cyan] {'sí' if do_usellm else 'no'}")
    console.print(f"[cyan]Caché modelos:[/cyan] {cache_dir}")
    console.print(f"[cyan]A extraer:[/cyan] {len(targets)} PDF(s)\n")

    extractor = Extractor(tier, device, cache_dir=cache_dir, use_llm=do_usellm)
    ok = 0
    extracted = []
    for pdf in targets:
        rel = pdf.relative_to(raw_dir).as_posix() if raw_dir in pdf.parents or pdf.parent == raw_dir else pdf.name
        try:
            console.print(f"▸ {rel} …", end=" ")

            def _on_batch(start: int, end: int, total: int) -> None:
                console.print(f"\n  [dim]lote p{start}-p{end}/{total} …[/dim]", end=" ")

            result = extractor.extract(pdf, batch_pages=effective_batch, on_progress=_on_batch)

            if do_captions and result.images:
                from .caption import caption_images, inline_captions

                caps = caption_images(result.images, tier.caption_model)
                result.markdown = inline_captions(result.markdown, caps)

            # El .md monolítico y sus artefactos van a extracted/, no a raw/.
            pdf_rel = pdf.relative_to(raw_dir)
            md_path = artifacts_dir / pdf_rel.with_suffix(".md")
            md_path.parent.mkdir(parents=True, exist_ok=True)
            header = (
                f"<!-- atlas-local: extraído de {rel} con {result.extractor} "
                f"v{result.extractor_version} en {device.kind}. No editar a mano. -->\n\n"
            )

            # Imágenes al subdirectorio <stem>/ para evitar colisiones entre PDFs.
            # Los chunks viven en ese mismo dir, así sus refs bare resuelven bien.
            # El monolítico vive un nivel arriba y necesita el prefijo.
            img_dir = artifacts_dir / pdf_rel.parent / pdf.stem
            if result.images:
                img_dir.mkdir(exist_ok=True)
                for name, data in result.images.items():
                    (img_dir / name).write_bytes(data)
                md_markdown = _prefix_image_refs(result.markdown, pdf.stem)
            else:
                md_markdown = result.markdown
            md_path.write_text(header + md_markdown, encoding="utf-8")

            # Segmentación: docs grandes → chunks + TOC para ingest selectivo.
            # Usa result.markdown (refs bare) — los chunks viven en img_dir.
            seg = None
            total_tokens = seg_mod.token_est(result.markdown)
            want_segment = segment if segment is not None else seg_mod.should_segment(
                result.n_pages, total_tokens
            )
            if want_segment:
                seg = seg_mod.segment_markdown(
                    result.markdown, md_path=md_path,
                    source_rel=rel, n_pages=result.n_pages,
                    target_tokens=seg_mod.DEFAULT_TARGET_TOKENS,
                    artifacts_base=md_path.parent,
                )

            manifest.record(
                pdf, md_path=md_path, extractor=result.extractor,
                extractor_version=result.extractor_version, device=device.kind,
                n_pages=result.n_pages, n_figs=result.n_figs,
                toc_path=seg.toc_path if seg else None,
                chunks_dir=seg.chunks_dir if seg else None,
                n_chunks=seg.n_chunks if seg else 0,
            )
            ok += 1
            extracted.append(pdf)
            seg_note = f" · {seg.n_chunks} chunks" if seg else ""
            console.print(f"[green]✓[/green] {result.n_pages}p / {result.n_figs} figs{seg_note}")
        except Exception as exc:  # noqa: BLE001 — un PDF roto no debe frenar el batch
            console.print(f"[red]✗ {exc}[/red]")

    manifest.save()
    console.print(f"\n[green]Listo:[/green] {ok}/{len(targets)} extraídos. "
                  f"Manifest: {manifest.path.relative_to(raw_dir.parent)}")

    if push and extracted:
        _git_push(raw_dir, extracted, artifacts_dir)


@app.command()
def render(
    file: Optional[Path] = typer.Argument(None, help="Archivo .md/.txt; vacío = lee stdin."),
) -> None:
    """Filtro LaTeX→Unicode best-effort para leer mate en terminal cruda."""
    import sys

    from .render import render_text

    text = file.read_text(encoding="utf-8") if file else sys.stdin.read()
    sys.stdout.write(render_text(text))


# ── validate ────────────────────────────────────────────────────────────────────
@app.command()
def validate(
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
) -> None:
    """Valida el contrato de frontmatter de todas las páginas. Exit ≠ 0 si hay errores."""
    from .wiki.loader import load_wiki
    from .wiki.schema import validate_page

    wiki_dir = _require_wiki(wiki)
    pages = load_wiki(wiki_dir)
    n_err = 0
    n_warn = 0
    for p in pages:
        for msg in validate_page(p):
            if msg.startswith("warn:"):
                n_warn += 1
                console.print(f"[yellow]warn[/yellow]  {p.rel_path}: {msg.removeprefix('warn: ')}")
            else:
                n_err += 1
                console.print(f"[red]error[/red] {p.rel_path}: {msg}")
    console.print(
        f"\n{len(pages)} páginas · [red]{n_err} errores[/red] · [yellow]{n_warn} warnings[/yellow]"
    )
    if n_err:
        raise typer.Exit(1)


# ── lint ──────────────────────────────────────────────────────────────────────
@app.command(name="lint")
def lint_cmd(
    scope: Optional[str] = typer.Argument(None, help="Carpeta del wiki (concepts, theorems, …)."),
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
    as_json: bool = typer.Option(False, "--json", help="Salida JSON (para los modos LLM)."),
) -> None:
    """Audita la consistencia del wiki (orphans, links/aristas rotos, simetría, …)."""
    import json as _json

    from .wiki.lint import lint

    wiki_dir = _require_wiki(wiki)
    raw_dir = wiki_dir.parent / "raw"
    findings = lint(wiki_dir, scope=scope, raw_dir=raw_dir if raw_dir.is_dir() else None)

    if as_json:
        console.print_json(_json.dumps({"findings": [f.as_dict() for f in findings]}))
        return

    if not findings:
        console.print("[green]✓ Sin findings.[/green]")
        return

    from collections import Counter
    counts = Counter(f.check for f in findings)
    table = Table(title=f"lint · wiki/ ({'/'+scope if scope else 'completo'})")
    table.add_column("sev")
    table.add_column("check")
    table.add_column("ubicación")
    table.add_column("detalle")
    for f in findings:
        color = "red" if f.severity == "error" else "yellow"
        table.add_row(f"[{color}]{f.severity}[/{color}]", f.check, f.location, f.message)
    console.print(table)
    summary = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    console.print(f"\n{len(findings)} findings — {summary}")


# ── index ──────────────────────────────────────────────────────────────────────
@app.command(name="index")
def index_cmd(
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
) -> None:
    """Regenera wiki/index.md y los MOCs de área desde el filesystem."""
    from .wiki.index import generate

    wiki_dir = _require_wiki(wiki)
    changed = generate(wiki_dir)
    if changed:
        console.print("[green]Regenerado:[/green]")
        for c in changed:
            console.print(f"  • {c}")
    else:
        console.print("[green]Índice y MOCs ya estaban al día.[/green]")


# ── forget ──────────────────────────────────────────────────────────────────────
@app.command()
def forget(
    source: str = typer.Argument(..., help="Slug de la fuente a olvidar (wiki/sources/<slug>)."),
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Aplicar sin confirmar."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Solo reportar el plan, no tocar nada."),
) -> None:
    """Olvida una fuente: quita su link de cada página y borra las que quedan sin fuentes.

    Preserva entidades compartidas: una página con otra fuente sobrevive (solo
    pierde este link); se borra solo la que quedaba sostenida por esta sola fuente.
    """
    from .wiki.forget import apply_forget, plan_forget
    from .wiki.index import generate
    from .wiki.loader import load_wiki

    wiki_dir = _require_wiki(wiki)
    plan = plan_forget(load_wiki(wiki_dir), source)
    if plan.is_empty:
        console.print(f"[yellow]No encontré la fuente '{source}' ni páginas que la citen.[/yellow]")
        return

    if plan.source_page:
        console.print(f"[cyan]Página de fuente a borrar:[/cyan] {plan.source_page}")
    console.print(f"[cyan]Páginas que solo pierden el link ({len(plan.unlinked)}):[/cyan] "
                  + (", ".join(plan.unlinked) or "—"))
    console.print(f"[red]Páginas a borrar (quedan sin fuente) ({len(plan.deleted)}):[/red] "
                  + (", ".join(plan.deleted) or "—"))

    if dry_run:
        console.print("[dim]--dry-run: nada modificado.[/dim]")
        return
    if not yes and not typer.confirm("¿Aplicar?"):
        console.print("Cancelado.")
        return

    touched = apply_forget(wiki_dir.parent, plan)
    generate(wiki_dir)
    console.print(f"[green]✓[/green] {len(touched)} archivos afectados. Índice regenerado.")


# ── ingest-status / ingest-stamp (manifest raw→wiki) ─────────────────────────────
@app.command(name="ingest-status")
def ingest_status_cmd(
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
    raw: Optional[Path] = typer.Option(None, "--raw", help="Directorio raw/ (auto-detectado)."),
    as_json: bool = typer.Option(False, "--json", help="Salida JSON (para --compile)."),
    freshness: bool = typer.Option(False, "--freshness", help="Vista de frescura (new/stale/current por page)."),
) -> None:
    """Inventario de PDFs en raw/ y su cobertura en wiki/sources/.

    Por defecto muestra una fila por PDF: pending / partial (N/M chunks) / ingested.
    Con --freshness muestra la vista legacy por page: new / stale / current / missing-raw.
    """
    import json as _json

    from .wiki.ingest import ingest_status, raw_ingest_status
    from .wiki.loader import load_wiki

    wiki_dir = _require_wiki(wiki)
    pages = load_wiki(wiki_dir)

    if freshness:
        statuses = ingest_status(pages, wiki_dir.parent)
        if as_json:
            console.print_json(_json.dumps({"sources": [s.as_dict() for s in statuses]}))
            return
        if not statuses:
            console.print("[green]No hay páginas de fuente todavía.[/green]")
            return
        color = {"current": "green", "new": "cyan", "stale": "yellow", "missing-raw": "red"}
        table = Table(title="ingest-status --freshness (wiki/sources/ → raw/)")
        table.add_column("estado")
        table.add_column("fuente")
        table.add_column("raw")
        for s in statuses:
            table.add_row(f"[{color.get(s.status, 'white')}]{s.status}[/]", s.slug, s.raw_path or "—")
        console.print(table)
        return

    raw_dir = find_raw_dir(raw)
    if not raw_dir.is_dir():
        console.print(f"[red]No existe el directorio raw/: {raw_dir}[/red]")
        raise typer.Exit(1)

    artifacts_dir_is = raw_dir.parent / "extracted"
    statuses = raw_ingest_status(pages, raw_dir, wiki_dir.parent, artifacts_dir_is)

    if as_json:
        console.print_json(_json.dumps({"raw": [s.as_dict() for s in statuses]}))
        return

    if not statuses:
        console.print("[yellow]No hay entradas en raw/.atlas-extract.json todavía.[/yellow]")
        return

    color = {"pending": "red", "partial": "yellow", "ingested": "green"}
    table = Table(title="ingest-status (raw/ → wiki/sources/)")
    table.add_column("estado")
    table.add_column("PDF")
    table.add_column("chunks", justify="right")
    table.add_column("sources")
    table.add_column("pendientes")
    for s in statuses:
        if s.n_chunks:
            chunks_cell = f"{len(s.covered_chunks)}/{s.n_chunks}"
            if s.status == "partial":
                chunks_dir_p = artifacts_dir_is / s.pdf_key.replace(".pdf", "")
                all_chunks = sorted(
                    p.name for p in chunks_dir_p.iterdir()
                    if p.is_file() and p.suffix == ".md"
                ) if chunks_dir_p.exists() else []
                missing = [c for c in all_chunks if c not in s.covered_chunks]
                pending_cell = ", ".join(missing) if missing else "—"
            else:
                pending_cell = "—"
        else:
            chunks_cell = "—"
            pending_cell = "—"
        sources_cell = ", ".join(s.sources) if s.sources else "—"
        table.add_row(
            f"[{color.get(s.status, 'white')}]{s.status}[/]",
            s.pdf_key,
            chunks_cell,
            sources_cell,
            pending_cell,
        )
    console.print(table)


@app.command(name="ingest-stamp")
def ingest_stamp_cmd(
    source: Optional[str] = typer.Argument(None, help="Slug de la fuente recién ingerida (omitir con --all)."),
    all_sources: bool = typer.Option(False, "--all", help="Sella todas las fuentes ingestables de una."),
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
) -> None:
    """Sella hash + lista de chunks en el frontmatter de la fuente (idempotente).

    Con un slug sella esa fuente; con --all sella cada source/assessment ingestable.
    """
    from .wiki.ingest import _INGESTABLE_FOLDERS, stamp_source
    from .wiki.loader import load_wiki

    wiki_dir = _require_wiki(wiki)
    pages = load_wiki(wiki_dir)

    if all_sources:
        targets = [p for p in pages if p.folder in _INGESTABLE_FOLDERS]
    elif source:
        targets = [p for p in pages if p.folder in _INGESTABLE_FOLDERS and p.slug == source]
        if not targets:
            console.print(f"[red]No existe fuente ingestable con slug '{source}'[/red]")
            raise typer.Exit(1)
    else:
        console.print("[red]Pasá un slug o usá --all.[/red]")
        raise typer.Exit(1)

    stamped = skipped = 0
    for page in targets:
        digest = stamp_source(wiki_dir.parent, page)
        if digest is None:
            skipped += 1
            if not all_sources:
                console.print(f"[yellow]No encontré el archivo raw de '{page.slug}' (path/extracted). Sin sellar.[/yellow]")
                raise typer.Exit(1)
            continue
        stamped += 1
        console.print(f"[green]✓[/green] {page.slug} sellada · ingested_sha256={digest[:12]}…")
    if all_sources:
        console.print(f"[bold]{stamped} sellada(s), {skipped} sin raw.[/bold]")


# ── log ──────────────────────────────────────────────────────────────────────
@app.command(name="log")
def log_cmd(
    limit: int = typer.Option(30, "--limit", "-n", help="Cantidad de commits a mostrar."),
    wiki: Optional[Path] = typer.Option(None, "--wiki", help="Directorio wiki/ (auto-detectado)."),
) -> None:
    """Muestra el log de mutaciones del wiki, derivado de git."""
    from .wiki.gitlog import render_log

    wiki_dir = _require_wiki(wiki)
    console.print(render_log(wiki_dir.parent, limit=limit))


# ── session (firewall) ──────────────────────────────────────────────────────────
session_app = typer.Typer(help="Estado de sesión / firewall del modo practice.")
app.add_typer(session_app, name="session")


def _session_root(wiki: Optional[Path]) -> Path:
    return _require_wiki(wiki).parent


@session_app.command("set")
def session_set(
    topic: str = typer.Argument(..., help="Tema T de la sesión practice."),
    wiki: Optional[Path] = typer.Option(None, "--wiki"),
) -> None:
    """Arranca una sesión practice sobre T y calcula los slugs bloqueados (grafo)."""
    from .wiki.session import set_practice

    root = _session_root(wiki)
    s = set_practice(root, root / "wiki", topic)
    console.print(f"[cyan]practice[/cyan] · T = {s.topic}")
    console.print(f"Bloqueados ({len(s.blocked_slugs)}): {', '.join(s.blocked_slugs) or '—'}")


@session_app.command("mode")
def session_mode(
    mode: str = typer.Argument(..., help="query | practice | ingest | lint"),
    wiki: Optional[Path] = typer.Option(None, "--wiki"),
) -> None:
    """Cambia el modo. Cualquier modo ≠ practice levanta el firewall."""
    from .wiki.session import set_mode

    s = set_mode(_session_root(wiki), mode)
    console.print(f"[cyan]modo:[/cyan] {s.mode}")


@session_app.command("reveal")
def session_reveal(wiki: Optional[Path] = typer.Option(None, "--wiki")) -> None:
    """Válvula de escape: permite la próxima lectura bloqueada (queda logueada)."""
    from .wiki.session import set_reveal

    set_reveal(_session_root(wiki), True)
    console.print("[yellow]reveal ON[/yellow] — el firewall permite leer; recordá /practice para re-armarlo.")


@session_app.command("clear")
def session_clear(wiki: Optional[Path] = typer.Option(None, "--wiki")) -> None:
    """Resetea la sesión (modo query, sin bloqueos)."""
    from .wiki.session import clear

    clear(_session_root(wiki))
    console.print("[green]Sesión reseteada (modo query).[/green]")


@session_app.command("show")
def session_show(wiki: Optional[Path] = typer.Option(None, "--wiki")) -> None:
    """Muestra el estado de sesión actual."""
    from .wiki.session import load_session

    s = load_session(_session_root(wiki))
    console.print(f"modo={s.mode} · T={s.topic} · reveal={s.reveal}")
    console.print(f"bloqueados ({len(s.blocked_slugs)}): {', '.join(s.blocked_slugs) or '—'}")


@session_app.command("check")
def session_check(
    path: Path = typer.Argument(..., help="Archivo que se quiere leer."),
    wiki: Optional[Path] = typer.Option(None, "--wiki"),
) -> None:
    """Decide si el firewall permite leer un archivo. Exit 2 = denegado (para el hook)."""
    from .wiki.session import check_read

    root = _session_root(wiki)
    allowed, reason = check_read(root, path)
    if allowed:
        raise typer.Exit(0)
    # markup=False: el mensaje lleva [[slug]] y va al hook / a Claude tal cual.
    console.print(reason, markup=False)
    raise typer.Exit(2)


if __name__ == "__main__":
    app()

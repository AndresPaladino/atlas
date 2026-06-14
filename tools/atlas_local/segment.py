"""Segmentación de markdowns extraídos en chunks + índice (TOC).

Un PDF grande produce un markdown monolítico que cuesta una fortuna de tokens
leer entero en `/ingest`. Este módulo lo parte en **chunks por sección de
heading** (sin cortar un tema a la mitad) más un **TOC compacto** que Claude lee
primero para cargar solo los chunks relevantes.

Lógica pura: no importa torch/marker, así corre y se testea en cualquier entorno.

Heurísticas:
- Páginas: se infieren del separador de paginación de marker (`{N}----…`) si está
  presente, o del ref de imagen más cercano (`_page_N_…`, que codifica la página
  0-indexada). Si no hay ninguno, se omiten. En la salida se muestran 1-indexadas.
- Tokens: estimación barata `len(texto) // 4`, suficiente para presupuestar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# ── Umbral de segmentación ──────────────────────────────────────────────────
SEGMENT_MIN_PAGES = 40
SEGMENT_MIN_TOKENS = 25_000

# ── Defaults de chunking ────────────────────────────────────────────────────
DEFAULT_TARGET_TOKENS = 3000   # tamaño objetivo de un chunk
DEFAULT_MAX_TOKENS = 4500      # por encima, una sección hoja se hard-splitea

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
# Separador de página de marker con paginate_output: línea tipo "{0}--------…".
_PAGE_MARKER_RE = re.compile(r"^\{(\d+)\}-{3,}\s*$")
# Ref de imagen extraída por marker: _page_<N>_<Kind>_<idx>. N es 0-indexado.
_IMG_PAGE_RE = re.compile(r"_page_(\d+)_[A-Za-z]+_\d+")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")


def token_est(text: str) -> int:
    """Estimación barata de tokens (~4 chars/token)."""
    return len(text) // 4


def slugify(text: str, *, max_len: int = 48) -> str:
    """kebab-case ASCII para nombres de archivo, alineado con el wiki."""
    text = text.lower()
    # Quitar tildes comunes sin arrastrar unicodedata.
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
                 ("ñ", "n"), ("ü", "u")):
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if len(text) > max_len:
        text = text[:max_len].rstrip("-")
    return text or "seccion"


def _clean_title(raw: str) -> str:
    """Saca énfasis/markup de un título de heading para mostrarlo y sluggear."""
    t = raw.strip().strip("#").strip()
    t = t.replace("**", "").replace("`", "")
    t = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", t)  # *énfasis*
    t = re.sub(r"\s+", " ", t).strip()
    return t or "Sección"


@dataclass
class Block:
    """Una sección atómica: la línea de heading y su cuerpo hasta el próximo
    heading (de cualquier nivel). El preámbulo (antes del 1er heading) es
    ``level == 0``."""

    level: int
    title: str
    parents: list[str]            # títulos de headings ancestros
    text: str                     # incluye la línea de heading
    page_start: int | None = None  # 0-indexado interno
    page_end: int | None = None

    @property
    def tokens(self) -> int:
        return token_est(self.text)


@dataclass
class Chunk:
    index: int
    blocks: list[Block]

    @property
    def title(self) -> str:
        for b in self.blocks:
            if b.title:
                return b.title
        return "preámbulo"

    @property
    def parents(self) -> list[str]:
        return self.blocks[0].parents if self.blocks else []

    @property
    def text(self) -> str:
        return "".join(b.text for b in self.blocks)

    @property
    def tokens(self) -> int:
        return token_est(self.text)

    @property
    def page_start(self) -> int | None:
        pages = [b.page_start for b in self.blocks if b.page_start is not None]
        return min(pages) if pages else None

    @property
    def page_end(self) -> int | None:
        pages = [b.page_end for b in self.blocks if b.page_end is not None]
        return max(pages) if pages else None

    @property
    def filename(self) -> str:
        return f"{self.index:02d}-{slugify(self.title)}.md"


# ── parsing ──────────────────────────────────────────────────────────────────
def parse_blocks(markdown: str) -> list[Block]:
    """Parte el markdown en bloques atómicos por límite de heading."""
    lines = markdown.splitlines(keepends=True)
    fence = False
    cur_page: int | None = None
    page_at_line: list[int | None] = []
    heading_at: list[tuple[int, str] | None] = []  # (level, title) o None

    for line in lines:
        if _FENCE_RE.match(line):
            fence = not fence
            page_at_line.append(cur_page)
            heading_at.append(None)
            continue
        if not fence:
            pm = _PAGE_MARKER_RE.match(line.strip())
            if pm:
                cur_page = int(pm.group(1))
            for im in _IMG_PAGE_RE.finditer(line):
                cur_page = int(im.group(1))
            hm = _HEADING_RE.match(line)
            heading_at.append((len(hm.group(1)), _clean_title(hm.group(2))) if hm else None)
        else:
            heading_at.append(None)
        page_at_line.append(cur_page)

    # Índices donde arranca un bloque: 0 (preámbulo) + cada línea de heading.
    starts = [0] + [i for i, h in enumerate(heading_at) if h is not None]
    starts = sorted(set(starts))

    blocks: list[Block] = []
    stack: list[tuple[int, str]] = []  # (level, title) de ancestros vigentes
    for k, start in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        if start == end:
            continue
        text = "".join(lines[start:end])
        h = heading_at[start]
        if h is None:  # preámbulo
            level, title, parents = 0, "", []
        else:
            level, title = h
            while stack and stack[-1][0] >= level:
                stack.pop()
            parents = [t for _, t in stack]
            stack.append((level, title))
        pages = [page_at_line[i] for i in range(start, end) if page_at_line[i] is not None]
        blocks.append(Block(
            level=level, title=title, parents=parents, text=text,
            page_start=min(pages) if pages else None,
            page_end=max(pages) if pages else None,
        ))
    return blocks


def _hard_split(block: Block, target_tokens: int) -> list[Block]:
    """Parte un bloque sobre-budget por párrafos (líneas en blanco)."""
    paras = re.split(r"(\n\s*\n)", block.text)  # conserva separadores
    pieces: list[Block] = []
    buf = ""
    part = 1

    def flush() -> None:
        nonlocal buf, part
        if not buf.strip():
            buf = ""
            return
        suffix = "" if part == 1 else f" (parte {part})"
        pieces.append(Block(
            level=block.level, title=block.title + suffix, parents=block.parents,
            text=buf, page_start=block.page_start, page_end=block.page_end,
        ))
        part += 1
        buf = ""

    for seg in paras:
        if buf and token_est(buf + seg) > target_tokens:
            flush()
        buf += seg
    flush()
    return pieces or [block]


def plan_chunks(
    blocks: list[Block],
    *,
    target_tokens: int = DEFAULT_TARGET_TOKENS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> list[Chunk]:
    """Agrupa bloques consecutivos en chunks ≤ target_tokens, hard-splitando
    los bloques individuales que exceden max_tokens."""
    chunks: list[Chunk] = []
    cur: list[Block] = []
    cur_tok = 0

    def flush() -> None:
        nonlocal cur, cur_tok
        if cur:
            chunks.append(Chunk(index=len(chunks), blocks=cur))
            cur, cur_tok = [], 0

    for block in blocks:
        if block.tokens > max_tokens:
            flush()
            for piece in _hard_split(block, target_tokens):
                chunks.append(Chunk(index=len(chunks), blocks=[piece]))
            continue
        if cur and cur_tok + block.tokens > target_tokens:
            flush()
        cur.append(block)
        cur_tok += block.tokens
    flush()
    return chunks


# ── escritura de artefactos ──────────────────────────────────────────────────
def _page_label(start: int | None, end: int | None) -> str:
    """Rango de páginas 1-indexado para mostrar (interno es 0-indexado)."""
    if start is None:
        return "—"
    if end is None or end == start:
        return str(start + 1)
    return f"{start + 1}–{end + 1}"


def write_chunks(chunks: list[Chunk], dest_dir: Path, source_rel: str) -> list[Path]:
    """Escribe cada chunk como un .md auto-descriptivo en dest_dir.

    Limpia chunks previos del directorio: una re-extracción puede producir
    otra cantidad de chunks o slugs distintos, y los viejos quedarían huérfanos.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    for old in dest_dir.glob("*.md"):
        old.unlink()
    written: list[Path] = []
    total = len(chunks)
    for ch in chunks:
        crumb = " › ".join([*ch.parents, ch.title]) if ch.title else "(preámbulo)"
        header = (
            f"<!-- atlas-local chunk {ch.index + 1}/{total} · fuente: {source_rel} "
            f"· págs {_page_label(ch.page_start, ch.page_end)} · {crumb}. "
            f"No editar a mano. -->\n\n"
        )
        path = dest_dir / ch.filename
        path.write_text(header + ch.text.lstrip("\n"), encoding="utf-8")
        written.append(path)
    return written


def render_toc(
    blocks: list[Block],
    chunks: list[Chunk],
    *,
    source_rel: str,
    chunks_dirname: str,
    n_pages: int,
) -> str:
    """Genera el índice markdown: resumen + tabla heading → chunk."""
    block_to_chunk: dict[int, Chunk] = {}
    for ch in chunks:
        for b in ch.blocks:
            block_to_chunk[id(b)] = ch

    total_tokens = sum(b.tokens for b in blocks)
    lines = [
        f"<!-- atlas-local TOC de {source_rel}. No editar a mano. -->",
        "",
        f"# Índice — {source_rel}",
        "",
        f"- Páginas: {n_pages or '—'} · Tokens estimados: ~{total_tokens:,} · "
        f"Chunks: {len(chunks)}",
        f"- Leé este índice primero; cargá solo los chunks que necesites desde "
        f"`{chunks_dirname}/`.",
        "",
        "| Sección | Págs | ~tok | Chunk |",
        "|---|---|---|---|",
    ]
    for b in blocks:
        if b.level == 0 and not b.title:
            label = "_(preámbulo)_"
        else:
            indent = "&nbsp;&nbsp;" * max(0, b.level - 1)
            label = f"{indent}{b.title}"
        ch = block_to_chunk.get(id(b))
        chunk_cell = f"`{ch.filename}`" if ch else "—"
        lines.append(
            f"| {label} | {_page_label(b.page_start, b.page_end)} "
            f"| {b.tokens:,} | {chunk_cell} |"
        )
    return "\n".join(lines) + "\n"


def should_segment(n_pages: int, total_tokens: int) -> bool:
    """¿Conviene segmentar? Sí si el doc supera páginas o tokens de umbral."""
    return n_pages >= SEGMENT_MIN_PAGES or total_tokens >= SEGMENT_MIN_TOKENS


@dataclass
class SegmentResult:
    toc_path: Path
    chunks_dir: Path
    chunk_paths: list[Path] = field(default_factory=list)

    @property
    def n_chunks(self) -> int:
        return len(self.chunk_paths)


def segment_markdown(
    markdown: str,
    *,
    md_path: Path,
    source_rel: str,
    n_pages: int,
    target_tokens: int = DEFAULT_TARGET_TOKENS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> SegmentResult:
    """Segmenta un markdown ya escrito: produce `<stem>.toc.md` y `<stem>/`.

    ``md_path`` es la ruta del monolítico (p.ej. raw/Notas.md); los artefactos
    quedan como hermanos: raw/Notas.toc.md y raw/Notas/."""
    blocks = parse_blocks(markdown)
    chunks = plan_chunks(blocks, target_tokens=target_tokens, max_tokens=max_tokens)

    chunks_dir = md_path.with_suffix("")  # raw/Notas
    chunk_paths = write_chunks(chunks, chunks_dir, source_rel)

    toc_path = md_path.with_suffix(".toc.md")
    toc = render_toc(
        blocks, chunks, source_rel=source_rel,
        chunks_dirname=chunks_dir.name, n_pages=n_pages,
    )
    toc_path.write_text(toc, encoding="utf-8")

    return SegmentResult(toc_path=toc_path, chunks_dir=chunks_dir, chunk_paths=chunk_paths)

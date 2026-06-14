"""Estado de conversión, versionado en ``raw/.atlas-extract.json``.

Llaveado por la ruta del PDF relativa a ``raw/`` (así el manifest es portable:
el desktop convierte, commitea, y el Mac hace pull y ve qué ya está hecho).
Una entrada queda ``stale`` si el sha256 del PDF cambió respecto a lo registrado.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path

MANIFEST_NAME = ".atlas-extract.json"
_CHUNK = 1 << 20  # 1 MiB


class Status(str, Enum):
    CONVERTED = "converted"  # .md existe y el hash coincide
    STALE = "stale"          # el PDF cambió desde la última extracción
    PENDING = "pending"      # nunca se extrajo (o el .md falta)


@dataclass
class Entry:
    sha256: str
    extractor: str
    extractor_version: str
    device: str
    extracted_at: str
    md_path: str          # relativo a raw/
    n_pages: int = 0
    n_figs: int = 0
    toc_path: str | None = None     # relativo a raw/, si se segmentó
    chunks_dir: str | None = None   # relativo a raw/, si se segmentó
    n_chunks: int = 0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


class Manifest:
    def __init__(self, raw_dir: Path, entries: dict[str, Entry]):
        self.raw_dir = raw_dir
        self.path = raw_dir / MANIFEST_NAME
        self._entries = entries

    # ── carga / guardado ─────────────────────────────────────────────────────
    @classmethod
    def load(cls, raw_dir: Path) -> "Manifest":
        path = raw_dir / MANIFEST_NAME
        entries: dict[str, Entry] = {}
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            for key, val in data.get("entries", {}).items():
                entries[key] = Entry(**val)
        return cls(raw_dir, entries)

    def save(self) -> None:
        payload = {
            "version": 1,
            "entries": {k: asdict(v) for k, v in sorted(self._entries.items())},
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    # ── consultas ────────────────────────────────────────────────────────────
    def _key(self, pdf: Path) -> str:
        return pdf.relative_to(self.raw_dir).as_posix()

    def status_of(self, pdf: Path) -> Status:
        entry = self._entries.get(self._key(pdf))
        if entry is None:
            return Status.PENDING
        md = self.raw_dir / entry.md_path
        if not md.exists():
            return Status.PENDING
        if entry.sha256 != sha256_file(pdf):
            return Status.STALE
        return Status.CONVERTED

    def get(self, pdf: Path) -> Entry | None:
        return self._entries.get(self._key(pdf))

    # ── mutación ─────────────────────────────────────────────────────────────
    def record(self, pdf: Path, *, md_path: Path, extractor: str,
               extractor_version: str, device: str, n_pages: int = 0,
               n_figs: int = 0, toc_path: "Path | None" = None,
               chunks_dir: "Path | None" = None, n_chunks: int = 0) -> Entry:
        entry = Entry(
            sha256=sha256_file(pdf),
            extractor=extractor,
            extractor_version=extractor_version,
            device=device,
            extracted_at=now_iso(),
            md_path=md_path.relative_to(self.raw_dir).as_posix(),
            n_pages=n_pages,
            n_figs=n_figs,
            toc_path=toc_path.relative_to(self.raw_dir).as_posix() if toc_path else None,
            chunks_dir=chunks_dir.relative_to(self.raw_dir).as_posix() if chunks_dir else None,
            n_chunks=n_chunks,
        )
        self._entries[self._key(pdf)] = entry
        return entry

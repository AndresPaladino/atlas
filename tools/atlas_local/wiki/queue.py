"""Cola de ingest persistente.

Vive en ``.atlas/ingest-queue.json`` (gitignored junto con session.json).
Registra qué PDFs están en vuelo, cuántos chunks se procesaron, y permite
reanudar sesiones cortadas sin perder progreso.

Estados de un item:
- pending    : encolado pero no iniciado
- in-progress: sesión activa procesando chunks
- done       : todos los chunks procesados y sellados
- failed     : sesión abortada con error (retomable manualmente)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

QUEUE_REL = ".atlas/ingest-queue.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class QueueItem:
    pdf_key: str                              # rel a raw/, ej. "DDSE.pdf"
    status: str = "pending"                   # pending | in-progress | done | failed
    chunks_total: int = 0                     # 0 si no hay carpeta de chunks
    chunks_done: list[str] = field(default_factory=list)  # nombres de chunk procesados
    source_slug: str | None = None            # slug de wiki/sources/ una vez creado
    started_at: str | None = None
    updated_at: str | None = None

    @property
    def progress(self) -> str:
        if not self.chunks_total:
            return "—"
        return f"{len(self.chunks_done)}/{self.chunks_total}"

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Queue:
    version: int = 1
    items: list[QueueItem] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"version": self.version, "items": [i.as_dict() for i in self.items]}

    def get(self, pdf_key: str) -> QueueItem | None:
        for item in self.items:
            if item.pdf_key == pdf_key:
                return item
        return None

    def in_progress(self) -> list[QueueItem]:
        return [i for i in self.items if i.status == "in-progress"]

    def pending(self) -> list[QueueItem]:
        return [i for i in self.items if i.status == "pending"]


def _queue_path(root: Path) -> Path:
    return root / QUEUE_REL


def load_queue(root: Path) -> Queue:
    path = _queue_path(root)
    if not path.exists():
        return Queue()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return Queue()
    items = [
        QueueItem(
            pdf_key=i["pdf_key"],
            status=i.get("status", "pending"),
            chunks_total=i.get("chunks_total", 0),
            chunks_done=list(i.get("chunks_done", [])),
            source_slug=i.get("source_slug"),
            started_at=i.get("started_at"),
            updated_at=i.get("updated_at"),
        )
        for i in data.get("items", [])
    ]
    return Queue(version=data.get("version", 1), items=items)


def save_queue(root: Path, queue: Queue) -> None:
    path = _queue_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(queue.as_dict(), indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def add_item(root: Path, pdf_key: str, chunks_total: int = 0) -> QueueItem:
    """Agrega un PDF a la cola (pending). Idempotente: no duplica si ya existe."""
    queue = load_queue(root)
    existing = queue.get(pdf_key)
    if existing:
        return existing
    item = QueueItem(pdf_key=pdf_key, chunks_total=chunks_total)
    queue.items.append(item)
    save_queue(root, queue)
    return item


def start_item(root: Path, pdf_key: str) -> QueueItem | None:
    """Marca un item como in-progress. Devuelve None si no existe."""
    queue = load_queue(root)
    item = queue.get(pdf_key)
    if item is None:
        return None
    item.status = "in-progress"
    item.started_at = item.started_at or _now()
    item.updated_at = _now()
    save_queue(root, queue)
    return item


def update_item(root: Path, pdf_key: str, chunk: str, source_slug: str | None = None) -> QueueItem | None:
    """Registra un chunk como procesado. Devuelve None si el item no existe."""
    queue = load_queue(root)
    item = queue.get(pdf_key)
    if item is None:
        return None
    if chunk not in item.chunks_done:
        item.chunks_done.append(chunk)
    if source_slug:
        item.source_slug = source_slug
    item.updated_at = _now()
    save_queue(root, queue)
    return item


def done_item(root: Path, pdf_key: str) -> QueueItem | None:
    """Cierra un item (done). Devuelve None si no existe."""
    queue = load_queue(root)
    item = queue.get(pdf_key)
    if item is None:
        return None
    item.status = "done"
    item.updated_at = _now()
    save_queue(root, queue)
    return item


def fail_item(root: Path, pdf_key: str) -> QueueItem | None:
    """Marca un item como failed. Devuelve None si no existe."""
    queue = load_queue(root)
    item = queue.get(pdf_key)
    if item is None:
        return None
    item.status = "failed"
    item.updated_at = _now()
    save_queue(root, queue)
    return item


def clear_done(root: Path) -> int:
    """Elimina items done y failed. Devuelve cuántos se eliminaron."""
    queue = load_queue(root)
    before = len(queue.items)
    queue.items = [i for i in queue.items if i.status not in ("done", "failed")]
    save_queue(root, queue)
    return before - len(queue.items)
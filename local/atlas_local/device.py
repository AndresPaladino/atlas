"""Detección de hardware: resuelve el backend de cómputo disponible.

Única "capa de portabilidad" propia del proyecto. marker y Ollama auto-detectan
el resto. La detección es defensiva: si torch no está instalado o falla, cae a
CPU en vez de explotar (así `doctor` siempre corre).
"""

from __future__ import annotations

import platform
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    kind: str          # "cuda" | "mps" | "cpu"
    name: str          # nombre legible del acelerador
    memory_gb: float   # VRAM dedicada (cuda) o RAM unificada estimada (mps); 0.0 si desconocido
    torch_available: bool

    @property
    def label(self) -> str:
        mem = f"{self.memory_gb:.0f}GB" if self.memory_gb else "memoria desconocida"
        return f"{self.kind} · {self.name} · {mem}"


def _unified_memory_gb() -> float:
    """RAM total del sistema en GB (proxy de la memoria unificada en Apple Silicon)."""
    import os

    # Linux y la mayoría de los Unix.
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024**3)
    except (ValueError, OSError, AttributeError):
        pass
    # macOS: SC_PHYS_PAGES no existe → usar sysctl hw.memsize.
    try:
        import subprocess

        out = subprocess.run(["sysctl", "-n", "hw.memsize"],
                             capture_output=True, text=True, check=True)
        return int(out.stdout.strip()) / (1024**3)
    except Exception:
        return 0.0


def detect_device() -> Device:
    """Resuelve el mejor backend disponible: CUDA > MPS > CPU."""
    try:
        import torch
    except ImportError:
        return Device(kind="cpu", name=platform.processor() or "CPU", memory_gb=0.0,
                      torch_available=False)

    # NVIDIA / CUDA (Windows, Linux) ─ p.ej. la 3080 Ti.
    if torch.cuda.is_available():
        props = torch.cuda.get_device_properties(0)
        return Device(kind="cuda", name=props.name,
                      memory_gb=props.total_memory / (1024**3), torch_available=True)

    # Apple Silicon / Metal (MPS). Usa memoria unificada → aproximamos con RAM total.
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        chip = platform.processor() or "Apple Silicon"
        return Device(kind="mps", name=f"Apple GPU ({chip})",
                      memory_gb=_unified_memory_gb(), torch_available=True)

    # Fallback: CPU.
    return Device(kind="cpu", name=platform.processor() or "CPU",
                  memory_gb=_unified_memory_gb(), torch_available=True)


def ollama_available() -> bool:
    """True si el binario de Ollama está en PATH (requisito para captions)."""
    return shutil.which("ollama") is not None

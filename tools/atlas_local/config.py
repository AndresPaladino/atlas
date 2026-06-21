"""Tiers de procesamiento según el hardware detectado.

Mapea un :class:`~atlas_local.device.Device` a una configuración concreta:
qué extractor usar, si los captions de figuras están disponibles, qué modelo
de visión y qué tamaño de batch. El rate no importa (corre en background), así
que los tiers chicos priorizan no quedarse sin memoria por sobre la velocidad.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .device import Device

CAPTION_MODEL = "qwen2.5vl:7b"


@dataclass(frozen=True)
class Tier:
    name: str            # etiqueta legible del tier
    extractor: str       # "marker" | "markitdown"
    captions: bool       # ¿se pueden generar captions de figuras?
    caption_model: str   # modelo de visión (Ollama) si captions=True
    batch_multiplier: int  # hint de batch para marker (1 = conservador)

    @property
    def summary(self) -> str:
        cap = f"captions ({self.caption_model})" if self.captions else "sin captions"
        return f"{self.name} · extractor={self.extractor} · {cap}"


@dataclass(frozen=True)
class ThrottleProfile:
    name: str
    batch_pages: int
    nice: int   # Unix process priority (0=normal, 19=lowest); ignorado en Windows
    ionice: int  # 0=none, 3=idle (Linux ionice clase idle)


THROTTLE_PROFILES: Dict[str, ThrottleProfile] = {
    "low":           ThrottleProfile("low",           batch_pages=10, nice=19, ionice=3),
    "medium":        ThrottleProfile("medium",        batch_pages=20, nice=10, ionice=0),
    "full-throttle": ThrottleProfile("full-throttle", batch_pages=40, nice=0,  ionice=0),
}

DEFAULT_THROTTLE = "medium"


def resolve_tier(device: Device) -> Tier:
    """Elige el tier para el device dado.

    - cuda ≥12GB  → marker full + captions, batch holgado.
    - cuda 8–12GB → marker + captions, batch chico.
    - mps         → marker + captions (si hay Ollama), batch chico.
    - cpu         → solo extracción de texto (markitdown), sin captions.
    """
    if device.kind == "cuda":
        if device.memory_gb >= 12:
            return Tier("cuda-full", "marker", True, CAPTION_MODEL, batch_multiplier=2)
        return Tier("cuda-lite", "marker", True, CAPTION_MODEL, batch_multiplier=1)

    if device.kind == "mps":
        return Tier("mps", "marker", True, CAPTION_MODEL, batch_multiplier=1)

    # CPU: marker es lentísimo y sin GPU no vale la pena; texto plano con markitdown.
    return Tier("cpu", "markitdown", False, CAPTION_MODEL, batch_multiplier=1)

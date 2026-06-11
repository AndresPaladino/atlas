"""atlas-local — capa de extracción local para Atlas.

Convierte PDFs de ``raw/`` a markdown (con LaTeX y captions de figuras) usando
la GPU disponible (CUDA / Apple MPS / CPU). Claude consume el ``.md`` cacheado
en vez de la imagen de cada página, ahorrando tokens sin perder fidelidad.
"""

__version__ = "0.1.0"

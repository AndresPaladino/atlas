# atlas (CLI)

Convierte los PDFs de `raw/` a markdown con LaTeX y captions de figuras, usando la GPU disponible (CUDA/MPS/CPU). Así Claude lee texto en vez de imágenes → menos tokens, misma fidelidad.

## Instalación

```bash
./install.sh        # macOS / Linux
.\install.ps1       # Windows (PowerShell)
```

Solo necesitás Python. El script instala `uv` si falta y configura el backend de torch automáticamente.

**Captions de figuras (opcional):** requiere [Ollama](https://ollama.com/download) + `ollama pull qwen2.5vl:7b`. Sin esto la extracción funciona igual pero sin describir imágenes.

## Uso

```bash
atlas doctor                   # hardware detectado y captions disponibles
atlas status                   # PDFs pendientes / convertidos / desactualizados
atlas extract                  # convierte todos los PDFs pendientes de raw/
atlas extract raw/foo.pdf      # un PDF puntual
atlas extract --captions       # + describe figuras (necesita Ollama)
atlas extract --force          # re-extrae todo
```

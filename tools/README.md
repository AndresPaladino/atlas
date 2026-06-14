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
atlas extract --no-segment     # no segmentar aunque el doc sea grande
atlas extract --chunk-tokens 4000  # tamaño objetivo de cada chunk (default 3000)
```

## Segmentación de docs grandes

Un libro de cientos de páginas extrae a un markdown gigante que Claude no puede procesar de una sola lectura. Por eso, para docs grandes (**≥40 páginas** o **≥25k tokens** estimados), `atlas extract` produce además un índice + chunks, y `/ingest` lee el índice primero y solo los chunks que necesita.

Para `raw/Notas.pdf` se generan:

```
raw/Notas.md            # monolítico (se sigue escribiendo siempre; fallback y render)
raw/Notas.toc.md        # índice: árbol de headings + páginas + tokens estimados + chunk que lo contiene
raw/Notas/              # chunks por sección (.md), nunca cortando un tema a la mitad
  00-introduccion.md
  01-preliminares.md
  ...
```

- Cada chunk arranca con un breadcrumb (fuente, rango de páginas, ruta de headings) para ser legible en aislamiento.
- Los docs chicos (exámenes, papers cortos) no se segmentan: queda solo el `.md`, como antes.
- El TOC y los chunks **se versionan en git** (igual que el `.md` y el manifest): se extrae en una máquina y se hace `pull` en otra sin re-extraer. Las imágenes siguen siendo locales.
- Flags: `--segment` fuerza la segmentación, `--no-segment` la inhibe, `--chunk-tokens N` ajusta el tamaño objetivo.

La página `wiki/sources/<slug>.md` deriva su "Mapa de coverage" directo del TOC, así que el grafo apunta a las secciones exactas sin recargar el documento entero.

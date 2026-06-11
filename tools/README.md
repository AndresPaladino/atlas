# atlas-local

Capa de extracción local para Atlas. Convierte los PDFs de `raw/` a markdown
(`raw/<nombre>.md`) **con LaTeX y captions de figuras**, usando la GPU disponible
— NVIDIA/CUDA, Apple Silicon/MPS, o CPU como fallback.

Así Claude deja de leer cada página como **imagen** (caro en tokens) y pasa a leer
**texto barato**, sin perder la fidelidad matemática. El procesamiento corre en
batch, en background; la velocidad no importa.

```
raw/*.pdf  ──[atlas-local, GPU]──►  raw/*.md  ──[Claude /ingest]──►  wiki/
```

## Instalación

Requiere solo tener Python disponible (uv instala lo demás, incluso su propio
Python aislado — no usa tu conda).

### macOS / Linux
```bash
cd atlas/local
./install.sh
```

### Windows (PowerShell)
```powershell
cd atlas\local
.\install.ps1
```

El bootstrap: instala `uv` si falta, corre `uv sync` con el backend de torch
correcto (`UV_TORCH_BACKEND=auto`: CUDA en Win/Linux con NVIDIA, MPS en Apple
Silicon, CPU si no hay GPU), chequea Ollama, y corre `atlas-local doctor`.

### Captions de figuras (opcional)
Requieren [Ollama](https://ollama.com/download) y el modelo de visión:
```bash
ollama pull qwen2.5vl:7b
```
Sin Ollama, la extracción funciona igual pero sin describir figuras.

## Uso

```bash
uv run atlas-local doctor                 # device, tier, captions disponibles
uv run atlas-local status                 # PDFs converted / stale / pending
uv run atlas-local extract                # convierte todos los pendientes de raw/
uv run atlas-local extract --captions     # + describe figuras (necesita Ollama)
uv run atlas-local extract raw/foo.pdf    # un PDF puntual
uv run atlas-local extract --force        # re-extrae todo
uv run atlas-local render respuesta.md     # filtro LaTeX→Unicode (terminal cruda)
```

Los `.md` y `raw/.atlas-extract.json` (manifest) **se versionan en git**: el
desktop con GPU hace el batch pesado, commitea, y otra máquina hace `pull` y los
reutiliza sin re-convertir. Las imágenes que extrae marker quedan locales
(gitignored); su contenido viaja como caption-texto dentro del `.md`.

## Tiers por hardware

| Device           | Extractor   | Captions |
|------------------|-------------|----------|
| CUDA ≥12GB       | marker      | sí       |
| CUDA 8–12GB / MPS| marker      | sí (batch chico) |
| CPU              | markitdown  | no (texto plano) |

## Para hablar con el wiki (la parte de Claude)

`atlas-local` **no** llama a Claude ni maneja credenciales. Para consultar/practicar:
abrí la carpeta `atlas/` en **Claude Code** y logueate ahí (suscripción o
`ANTHROPIC_API_KEY`). Para que la matemática se renderice, leé las respuestas en un
cliente con render de KaTeX: app desktop, web (`claude.ai/code`), o extensión de
IDE (VS Code + KaTeX-for-Claude). Detalle en `../schema/output-conventions.md`.

## Troubleshooting

- **`doctor` dice "torch NO instalado"** → corré `./install.sh` de nuevo; revisá
  que `uv sync` haya terminado sin error.
- **Reporta `cpu` teniendo GPU** → en NVIDIA, verificá drivers CUDA; en Mac,
  necesitás Apple Silicon (los Intel no tienen MPS). Forzá re-sync:
  `UV_TORCH_BACKEND=auto uv sync --reinstall-package torch`.
- **conda interfiere** → uv usa su propio `.venv`; no hace falta `conda activate`.
  Si algo se cruza, desactivá conda (`conda deactivate`) antes de correr.
- **VRAM insuficiente / OOM** → el tier ya ajusta el batch; si igual falla, corré
  sin `--captions` (la extracción pesa menos que el VLM).
- **Captions no salen** → falta Ollama o el modelo: `ollama pull qwen2.5vl:7b`.

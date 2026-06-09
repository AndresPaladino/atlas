#!/usr/bin/env bash
# atlas-local bootstrap (macOS / Linux)
# Uso:  cd atlas/local && ./install.sh
#
# Idempotente: instala uv si falta, sincroniza el entorno con el backend de
# torch correcto (CUDA/MPS/CPU), avisa sobre Ollama (opcional, solo captions)
# y corre `atlas-local doctor` para confirmar el device detectado.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

say()  { printf '\033[1;36m▸ %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m⚠ %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m✓ %s\033[0m\n' "$*"; }

# ── 1. uv ────────────────────────────────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  say "uv no encontrado; instalando (instalador oficial de Astral)…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # El instalador deja uv en ~/.local/bin (o ~/.cargo/bin en versiones viejas).
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
command -v uv >/dev/null 2>&1 || { warn "uv sigue sin estar en PATH. Abrí una terminal nueva y reintentá."; exit 1; }
ok "uv $(uv --version | awk '{print $2}')"

# ── 2. Sync con backend de torch automático ──────────────────────────────────
# uv detecta CUDA en Win/Linux, usa el wheel MPS en Apple Silicon, y CPU si no
# hay GPU. Si tu conda está activo, uv igual crea su propio venv aislado en .venv.
say "Sincronizando entorno (uv sync, torch-backend auto)…"
UV_TORCH_BACKEND=auto uv sync --extra render
ok "Entorno listo en $HERE/.venv"

# ── 3. Ollama (opcional, solo para captions de figuras) ──────────────────────
if command -v ollama >/dev/null 2>&1; then
  ok "Ollama detectado — captions de figuras disponibles (--captions)."
else
  warn "Ollama no instalado. La extracción funciona igual; los captions de figuras"
  warn "quedan deshabilitados. Para habilitarlos: https://ollama.com/download"
  warn "y luego:  ollama pull qwen2.5vl:7b"
fi

# ── 4. Fix editable install (conda interference workaround) ──────────────────
# uv instala atlas-local como editable via .pth, pero el Python de conda no
# procesa ese .pth al arrancar desde el shebang del entrypoint. Lo reemplazamos
# por un wrapper bash que inyecta PYTHONPATH directamente.
ENTRYPOINT="$HERE/.venv/bin/atlas-local"
cat > "$ENTRYPOINT" << 'WRAPPER'
#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHONPATH="$DIR/../.." exec "$DIR/python3" -m atlas_local.cli "$@"
WRAPPER
chmod +x "$ENTRYPOINT"
ok "Entrypoint corregido ($ENTRYPOINT)"

# ── 5. Doctor ─────────────────────────────────────────────────────────────────
say "Diagnóstico de hardware:"
uv run atlas-local doctor

echo
ok "Instalación completa. Probá:  uv run atlas-local status"

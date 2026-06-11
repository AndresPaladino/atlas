#!/usr/bin/env bash
# atlas bootstrap (macOS / Linux)
# Uso:  cd atlas/tools && ./install.sh
#
# Instala el comando global `atlas` via uv tool.
# Idempotente: instala uv si falta, luego instala/reinstala atlas.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

say()  { printf '\033[1;36m▸ %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m⚠ %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m✓ %s\033[0m\n' "$*"; }

# ── 1. uv ────────────────────────────────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  say "uv no encontrado; instalando (instalador oficial de Astral)…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
command -v uv >/dev/null 2>&1 || { warn "uv sigue sin estar en PATH. Abrí una terminal nueva y reintentá."; exit 1; }
ok "uv $(uv --version | awk '{print $2}')"

# ── 2. Instalar atlas globalmente ─────────────────────────────────────────────
say "Instalando atlas como comando global (uv tool install)…"
UV_TORCH_BACKEND=auto uv tool install "${HERE}[render]"
ok "atlas instalado en PATH"

# ── 3. Ollama (opcional, solo para captions de figuras) ──────────────────────
if command -v ollama >/dev/null 2>&1; then
  ok "Ollama detectado — captions de figuras disponibles (--captions)."
else
  warn "Ollama no instalado. La extracción funciona igual; los captions de figuras"
  warn "quedan deshabilitados. Para habilitarlos: https://ollama.com/download"
  warn "y luego:  ollama pull qwen2.5vl:7b"
fi

# ── 4. Doctor ─────────────────────────────────────────────────────────────────
say "Diagnóstico de hardware:"
atlas doctor

echo
ok "Instalación completa. Probá desde cualquier directorio:  atlas status"

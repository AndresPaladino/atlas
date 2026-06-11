#!/usr/bin/env bash
# Atlas setup script
# Run once after cloning: bash setup.sh

set -e

ATLAS_PATH="$(cd "$(dirname "$0")" && pwd)"
SETTINGS_FILE="$ATLAS_PATH/.claude/settings.local.json"

echo "🗂  Atlas path: $ATLAS_PATH"

# ── 1. Crear .claude/settings.local.json desde el ejemplo ────────────────────
SETTINGS_EXAMPLE="$ATLAS_PATH/.claude/settings.local.json.example"
if [ ! -f "$SETTINGS_FILE" ]; then
  if [ -f "$SETTINGS_EXAMPLE" ]; then
    echo "⚙️  Creando .claude/settings.local.json desde el ejemplo…"
    cp "$SETTINGS_EXAMPLE" "$SETTINGS_FILE"
    echo "   ✓ Creado"
  else
    echo "   ⚠️  settings.local.json.example no encontrado, salteando"
  fi
else
  echo "   ✓ .claude/settings.local.json ya existe, salteando"
fi

# ── 2. Crear estructura de wiki/ ──────────────────────────────────────────────
for d in wiki/concepts wiki/theorems wiki/methods wiki/examples wiki/comparisons wiki/sources; do
  mkdir -p "$ATLAS_PATH/$d"
  [ ! -f "$ATLAS_PATH/$d/.gitkeep" ] && touch "$ATLAS_PATH/$d/.gitkeep"
done
echo "🧠  Wiki estructurado: wiki/{concepts,theorems,methods,examples,comparisons,sources}/"

# ── 3. Instalar CLI atlas (PDF → markdown) ────────────────────────────────────
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "$WINDIR" ]]; then
  echo "⚙️  Instalando atlas (Windows)…"
  powershell.exe -ExecutionPolicy Bypass -File "$ATLAS_PATH\\tools\\install.ps1"
else
  echo "⚙️  Instalando atlas…"
  bash "$ATLAS_PATH/tools/install.sh"
fi

# ── 4. Listo ──────────────────────────────────────────────────────────────────
echo ""
echo "✅  Atlas listo. Abrí Claude Code en este directorio para empezar."
echo "   → Tirá PDFs en raw/ y corré /ingest para poblar el wiki."

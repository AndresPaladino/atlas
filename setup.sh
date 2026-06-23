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

# ── 2b. Hook pre-push: bloquea pushear datos personales al repo público ───────
HOOK_SRC="$ATLAS_PATH/tools/pre-push-guard.sh"
HOOK_DST="$ATLAS_PATH/.git/hooks/pre-push"
if [ -d "$ATLAS_PATH/.git" ] && [ -f "$HOOK_SRC" ]; then
  ln -sf ../../tools/pre-push-guard.sh "$HOOK_DST"
  chmod +x "$HOOK_SRC"
  echo "🛡  Hook pre-push instalado (anti-leak hacia upstream)"
fi

# ── 3. Instalar CLI atlas (PDF → markdown) ────────────────────────────────────
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "$WINDIR" ]]; then
  echo "⚙️  Instalando atlas (Windows)…"
  powershell.exe -ExecutionPolicy Bypass -File "$ATLAS_PATH\\tools\\install.ps1"
else
  echo "⚙️  Instalando atlas…"
  bash "$ATLAS_PATH/tools/install.sh"
fi

# ── 4. Configurar cliente MCP (Claude Desktop, si está instalado) ─────────────
python3 - "$ATLAS_PATH" <<'PYEOF'
import json, os, sys
from pathlib import Path

atlas_root = sys.argv[1]
entry = {"command": "atlas-mcp", "env": {"ATLAS_ROOT": atlas_root}}

candidates = [
    Path.home() / "Library/Application Support/Claude/claude_desktop_config.json",  # macOS
    Path.home() / ".config/Claude/claude_desktop_config.json",                       # Linux
]
cfg_path = next((p for p in candidates if p.parent.exists()), None)
if cfg_path is None:
    print("   ℹ  Claude Desktop no detectado. Config MCP manual:")
    print(f'      {{"mcpServers": {{"atlas": {json.dumps(entry)}}}}}')
    sys.exit(0)

cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
cfg.setdefault("mcpServers", {})
if cfg["mcpServers"].get("atlas") == entry:
    print("   ✓ Claude Desktop MCP ya configurado")
    sys.exit(0)

cfg["mcpServers"]["atlas"] = entry
cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
print(f"   ✓ Claude Desktop MCP configurado en {cfg_path}")
PYEOF

# ── 5. Listo ──────────────────────────────────────────────────────────────────
echo ""
echo "✅  Atlas listo. Abrí Claude Code en este directorio para empezar."
echo "   → Tirá PDFs en raw/ y corré /ingest para poblar el wiki."

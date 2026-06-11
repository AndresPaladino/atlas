#!/usr/bin/env bash
# Atlas setup script
# Run once after cloning: bash setup.sh

set -e

ATLAS_PATH="$(cd "$(dirname "$0")" && pwd)"
SETTINGS_FILE="$ATLAS_PATH/.claude/settings.local.json"

echo "🗂  Atlas path: $ATLAS_PATH"

# ── 1. Create .claude/settings.local.json from example ───────────────────────
SETTINGS_EXAMPLE="$ATLAS_PATH/.claude/settings.local.json.example"
if [ ! -f "$SETTINGS_FILE" ]; then
  if [ -f "$SETTINGS_EXAMPLE" ]; then
    echo "⚙️  Creating .claude/settings.local.json from example..."
    cp "$SETTINGS_EXAMPLE" "$SETTINGS_FILE"
    echo "   ✓ Created"
  else
    echo "   ⚠️  settings.local.json.example not found, skipping"
  fi
else
  echo "   ✓ .claude/settings.local.json already exists, skipping"
fi

# ── 2. Scaffold wiki/ (LLM-owned knowledge graph) ────────────────────────────
for d in wiki/concepts wiki/theorems wiki/methods wiki/examples wiki/comparisons wiki/sources; do
  mkdir -p "$ATLAS_PATH/$d"
  [ ! -f "$ATLAS_PATH/$d/.gitkeep" ] && touch "$ATLAS_PATH/$d/.gitkeep"
done
echo "🧠  Wiki directory scaffolded: wiki/{concepts,theorems,methods,examples,comparisons,sources}/"

# ── 3. Install atlas-local (PDF → markdown pipeline) ─────────────────────────
if [ -f "$ATLAS_PATH/local/install.sh" ]; then
  echo "⚙️  Installing atlas-local (PDF extraction pipeline)..."
  bash "$ATLAS_PATH/local/install.sh"
else
  echo "   ⚠️  local/install.sh not found, skipping atlas-local install"
fi

# ── 4. Done ───────────────────────────────────────────────────────────────────
echo ""
echo "✅  Atlas ready. Open Claude Code in this directory to start a session."
echo "   → Drop PDFs into raw/ and run /ingest to populate the wiki."

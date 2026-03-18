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

# ── 2. Create current month log directory ─────────────────────────────────────
MONTH_DIR="$ATLAS_PATH/logs/$(date +%Y-%m)"
mkdir -p "$MONTH_DIR"
echo "📅  Log directory created: logs/$(date +%Y-%m)/"

# ── 3. Done ───────────────────────────────────────────────────────────────────
echo ""
echo "✅  Atlas ready. Open Claude Code in this directory to start a session."
echo "   → Read profile/student_profile.md and update your active subjects."
echo "   → Copy subjects/_template/index.md to add a new subject."

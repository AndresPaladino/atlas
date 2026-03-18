#!/usr/bin/env bash
# Atlas setup script
# Run once after cloning: bash setup.sh

set -e

ATLAS_PATH="$(cd "$(dirname "$0")" && pwd)"
SETTINGS_FILE="$ATLAS_PATH/.claude/settings.local.json"

echo "🗂  Atlas path: $ATLAS_PATH"

# ── 1. Update hardcoded paths in .claude/settings.local.json ─────────────────
if [ -f "$SETTINGS_FILE" ]; then
  echo "⚙️  Updating .claude/settings.local.json with local path..."
  # Replace any absolute path that looks like a home directory Atlas install
  sed -i.bak "s|/Users/[^/]*/[^\"]*Atlas|$ATLAS_PATH|g" "$SETTINGS_FILE"
  rm -f "$SETTINGS_FILE.bak"
  echo "   ✓ Paths updated"
else
  echo "   ⚠️  settings.local.json not found, skipping path update"
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

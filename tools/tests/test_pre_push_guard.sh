#!/usr/bin/env bash
# Self-check del guardrail anti-leak. Corre en un repo git temporal.
# Uso: bash tools/tests/test_pre_push_guard.sh
set -euo pipefail

GUARD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/pre-push-guard.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$TMP"

git init -q
git config user.email t@t.t; git config user.name t
git commit -q --allow-empty -m base
git branch -q upstream-main          # simula upstream/main como el base limpio
git update-ref refs/remotes/upstream/main upstream-main

z40="0000000000000000000000000000000000000000"
fail=0
run() { # url, stdin → espera exit_code $1
  local want=$1 url=$2; shift 2
  local got=0
  printf '%s' "$1" | bash "$GUARD" remote "$url" >/dev/null 2>&1 || got=$?
  if [ "$got" != "$want" ]; then echo "FALLO: url=$url want=$want got=$got"; fail=1; fi
}

base=$(git rev-parse HEAD)

# commit de funcionalidad (tools/)
mkdir -p tools; echo x > tools/foo.py; git add .; git commit -q -m func
func=$(git rev-parse HEAD)

# commit personal (wiki/)
mkdir -p wiki; echo y > wiki/page.md; git add .; git commit -q -m personal
pers=$(git rev-parse HEAD)

stdin_func="refs/heads/main $func refs/heads/main $base"
stdin_pers="refs/heads/main $pers refs/heads/main $base"

# 1. público + solo funcionalidad → permite (0)
run 0 "git@github.com:AndresPaladino/atlas.git" "$stdin_func"
# 2. público + datos personales → bloquea (1)
run 1 "git@github.com:AndresPaladino/atlas.git" "$stdin_pers"
# 3. privado (atlas-personal) + datos personales → permite (0)
run 0 "git@github.com:AndresPaladino/atlas-personal.git" "$stdin_pers"
# 4. público sin .git en url + personal → bloquea (1)
run 1 "git@github.com:AndresPaladino/atlas" "$stdin_pers"

[ "$fail" = 0 ] && echo "OK — 4/4 casos del guardrail" || { echo "TESTS FALLARON"; exit 1; }

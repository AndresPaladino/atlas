#!/usr/bin/env bash
# Guardrail anti-leak: bloquea pushear datos personales al repo PÚBLICO (upstream/atlas).
#
# git invoca el hook como:  pre-push <remote-name> <remote-url>
# y pasa por stdin una línea por ref:  <local-ref> <local-sha> <remote-ref> <remote-sha>
#
# Solo actúa si el remote es el público "atlas" (no atlas-personal). Si algún commit
# a enviar toca wiki/ raw/ o extracted/, rechaza el push.
#
# Instalado por setup.sh como symlink en .git/hooks/pre-push.

set -euo pipefail

remote_url="${2:-}"

# Solo el repo público. atlas-personal (privado) puede recibir todo.
# Match: termina en /atlas o /atlas.git (pero NO atlas-personal).
case "$remote_url" in
  *[/:]atlas|*[/:]atlas.git) ;;   # público → seguir chequeando
  *) exit 0 ;;                      # cualquier otro remote → permitir
esac

z40="0000000000000000000000000000000000000000"
leaked=""

while read -r local_ref local_sha remote_ref remote_sha || [ -n "$local_ref" ]; do
  [ -z "$local_sha" ] && continue                  # línea vacía / última sin newline
  [ "$local_sha" = "$z40" ] && continue           # borrado de rama, nada que revisar

  if [ "$remote_sha" = "$z40" ]; then
    # rama nueva en el remoto: revisar todo lo que no esté ya en upstream/main
    range="upstream/main..$local_sha"
  else
    range="$remote_sha..$local_sha"
  fi

  personal=$(git diff --name-only "$range" -- wiki/ raw/ extracted/ 2>/dev/null || true)
  [ -n "$personal" ] && leaked="$leaked$personal"$'\n'
done

if [ -n "$leaked" ]; then
  echo "✋ pre-push BLOQUEADO: estás por pushear datos personales al repo PÚBLICO ($remote_url)" >&2
  echo "   Archivos bajo wiki/ raw/ extracted/ no pueden ir a upstream:" >&2
  printf '%s' "$leaked" | sort -u | sed 's/^/     /' >&2
  echo "   → Pushea solo commits de funcionalidad (tools/ schema/ .claude/). Ver .claude/WORKFLOW.md" >&2
  exit 1
fi

exit 0

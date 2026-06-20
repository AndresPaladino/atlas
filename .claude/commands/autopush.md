---
description: Commitear cambios pendientes, push a origin, y si hay commits de funcionalidad también a upstream (atlas público) vía diff limpio + PR
---

Sos el ejecutor del flujo de sync de Atlas. Tu trabajo es: armar commits de los cambios pendientes, push a origin siempre, y detectar si hay commits que van también a upstream.

## Argumento opcional

El usuario puede pasar un nombre de feature: `$ARGUMENTS`. Si no lo pasa, inferilo del contenido de los cambios.

---

## Paso 0 — armar commits de cambios pendientes

Antes de pushear, revisá si hay cambios sin commitear:

```bash
git status --short
git diff --name-only HEAD
```

Si hay archivos modificados o sin trackear (excluí `.obsidian/` y archivos temporales), agrupalos en commits semánticamente coherentes:

**Regla de agrupación:**
- Un commit puede mezclar `tools/` + `schema/` + `.claude/` (todo funcionalidad)
- Un commit puede mezclar `wiki/` + `raw/` (todo contenido personal)
- **Nunca** un mismo commit mezcla funcionalidad con `raw/`/`wiki/`
- `.obsidian/` va en su propio commit o se ignora (es ruido de UI)

**Para cada grupo**, generá un mensaje de commit descriptivo en español con el formato:
```
<tipo>(<scope>): <qué cambió y por qué>
```
donde `tipo` es: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`.

Ejemplo de flujo con múltiples grupos:
```bash
# grupo 1: funcionalidad
git add tools/atlas_local/cli.py schema/modes.md .claude/commands/ingest.md
git commit -m "feat(cli): ..."

# grupo 2: contenido
git add wiki/concepts/foo.md raw/bar.md
git commit -m "ingest: ..."
```

Si no hay nada que commitear, continuá al Paso 1.

---

## Paso 1 — push a origin

```bash
git push origin main
```

Si falla (divergencia), avisá y detenete. No sigas al Paso 2.

---

## Paso 2 — detectar commits candidatos para upstream

Un commit es candidato para upstream si y solo si **ninguno** de sus archivos modificados está bajo `raw/` o `wiki/`. Los commits que mezclan zonas **no son candidatos** (avisalo si pasa).

```bash
git fetch upstream
git log upstream/main..HEAD --oneline
```

Para cada commit, chequeá sus archivos:

```bash
git diff-tree --no-commit-id -r --name-only <hash>
```

Separalos en:
- **candidatos**: solo tocan `tools/`, `schema/`, `.claude/`, u otros archivos de funcionalidad
- **solo-personales**: tocan `raw/` o `wiki/` (van únicamente a origin, ya pusheados)
- **mixtos**: mezclan zonas (reportá cuáles son y sugerí que el usuario los separe en el futuro)

Si no hay candidatos, avisá "No hay commits de funcionalidad nuevos para upstream" y terminá.

---

## Paso 3 — upstream: diff acumulado en vez de cherry-pick por commit

El cherry-pick commit-a-commit produce commits vacíos cuando upstream ya tiene esos cambios. Usá el **diff acumulado**:

1. Determiná el nombre de rama: usá `$ARGUMENTS` si existe, sino inferilo del contenido.

2. Stash si hay cambios sin commitear residuales (no debería haberlos después del Paso 0):

```bash
git stash   # solo si git status muestra cambios
```

3. Creá la rama desde upstream/main:

```bash
git checkout -b upstream-sync upstream/main
```

4. Identificá qué archivos de funcionalidad difieren entre `main` y `upstream/main`:

```bash
git diff upstream/main..main --name-only -- tools/ schema/ .claude/ CLAUDE.md README.md setup.sh
```

5. Traé esos archivos desde `main`:

```bash
git checkout main -- <archivo1> <archivo2> ...
```

6. Verificá que no se filtre nada personal — el staging debe contener SOLO archivos de funcionalidad:

```bash
git status
```

Si aparece cualquier archivo bajo `raw/` o `wiki/`, **detenete** y avisá antes de continuar.

7. Commiteá y pusheá:

```bash
git commit -m "feat: sync funcionalidad desde atlas-personal

<lista de archivos y qué cambia cada uno>"

git push upstream upstream-sync:feat/<nombre>
gh pr create --repo AndresPaladino/atlas --base main --head feat/<nombre> \
  --title "feat: <nombre>" \
  --body "Sync de funcionalidad desde atlas-personal.

Archivos incluidos:
<lista>"
```

8. Limpieza:

```bash
git checkout main
git branch -D upstream-sync
git stash pop   # si hiciste stash en el paso 2
```

9. Mostrá el link del PR al usuario.

---

## Errores comunes

- Si `upstream` no está configurado: `git remote add upstream git@github.com:AndresPaladino/atlas.git`
- Si `gh` no está disponible: pusheá la rama igual y mostrá la URL para abrir el PR manualmente
- Si `upstream-sync` ya existe: `git branch -D upstream-sync` antes de recrearla
- Si hay cambios sin commitear al hacer checkout: `git stash` antes, `git stash pop` al final

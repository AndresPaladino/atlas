# Workflow de sync — Atlas personal

## Repos

| Remote | Repo | Para qué |
|---|---|---|
| `origin` | `atlas-personal` (privado) | trabajo diario, wiki, raw |
| `upstream` | `atlas` (público) | template limpio, sin contenido personal |

## Comandos diarios

```bash
git pull origin main          # al arrancar (sync desde otra máquina)
git push origin main          # al terminar (o después de cada sesión de estudio)
```

## Cuando mejorás schema/ o tools/

**Regla base:** separá los cambios en commits distintos. Un commit que va a
`upstream` **no puede tocar `raw/`, `extracted/` ni `wiki/`** (datos personales). Mantené la
funcionalidad (`tools/`, `schema/`, `.claude/`) y los datos personales en
commits separados desde el principio.

> ⚠️ **No uses `git push upstream <hash>:main`.** `main` (atlas-personal) y
> `upstream/main` (atlas público) **divergieron**: el público se creó borrando
> `wiki/`/`raw/`, así que el *árbol* de cualquier commit de `main` todavía
> contiene tus datos personales. Pushear un hash de `main` al público
> arrastraría tu wiki (o git lo rechaza por non-fast-forward; forzarlo = leak).

La forma segura es **cherry-pick sobre `upstream/main` + PR**:

```bash
git fetch upstream
git checkout -b upstream-sync upstream/main      # arranca del árbol LIMPIO del público
git cherry-pick <commits de funcionalidad>       # en orden; NUNCA los de raw/wiki

# Si un cherry-pick choca en un archivo de funcionalidad, tomá la versión de main
# (es el estado final correcto y no tiene datos personales):
#   git checkout main -- <archivo> && git add <archivo> && git cherry-pick --continue

# Verificá que NO se cuele nada personal antes de pushear:
git diff --name-only upstream/main HEAD          # debe ser solo tools/ schema/ .claude/

git push upstream upstream-sync:feat/<nombre>    # rama revisable, NO main directo
# → abrí el PR con el link que imprime git y mergealo en GitHub
#   (o: gh pr create --repo AndresPaladino/atlas --base main --head feat/<nombre>)

git checkout main && git branch -D upstream-sync # limpieza
```

Después, `git pull origin main` en la otra máquina trae la funcionalidad (y los
datos personales) por el repo privado. El público es solo para compartir
funcionalidad hacia afuera.

> **Nota de layout:** `raw/` contiene solo PDFs + `.atlas-extract.json`. Los artefactos de extracción (`.md`, `.toc.md`, carpetas de chunks) viven en `extracted/`. Tanto `raw/` como `extracted/` son datos personales — nunca van a `upstream`.

## Setup en Mac (primera vez)

```bash
git clone git@github.com:AndresPaladino/atlas-personal.git atlas
cd atlas/tools && ./install.sh    # instala el comando `atlas` globalmente
```

## Extracción de PDFs

```bash
# Agregar PDF a raw/, luego:
atlas extract                 # extrae todos los pending (auto-detecta raw/)
atlas extract --push          # extrae + commit + push de los .md en un paso
atlas status                  # ver qué hay pending/converted/stale
```

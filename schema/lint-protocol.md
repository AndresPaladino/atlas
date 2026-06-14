---
type: schema
updated: 2026-06-10
---

# Protocolo: modo `/lint`

Auditar consistencia del wiki. Reportar problemas accionables y ofrecer fix interactivo. No modifica nada sin confirmación del usuario.

> **La detección es código, no prompt.** Corré `atlas lint [scope] --json`: los
> checks de abajo están implementados de forma determinística en el CLI
> (`tools/atlas_local/wiki/lint.py`). El agente **no** los reimplementa leyendo
> archivos — consume el JSON y se dedica al juicio: presentar, priorizar y aplicar
> fixes. La lista de abajo es la **especificación** de lo que el comando detecta.

---

## Apertura

1. Anunciar `[modo: lint]`.
2. Determinar scope (sin argumento = todo `wiki/`; con argumento = carpeta).
3. Correr `atlas lint $SCOPE --json` y parsear los findings.

---

## Checks (especificación del comando)

El comando aplica todos. Cada check produce 0..N findings.

### 1. Orphans

Páginas sin ningún wikilink entrante ni arista (`requires`/`unlocks`/`sources`/`illustrates`/`compares`/`covers_*`) que las referencie desde otra página. (El índice y los MOCs se generan, así que no cuentan como "referencia".)

Excepción: páginas tipo `area` y `source` son raíces, no son orphans por definición.

**Finding**: `orphan | wiki/<tipo>/<slug>.md`

**Fix sugerido**: borrar, o agregar a `wiki/index.md`, o agregar inbound link desde la página más afín (detectar por tags).

### 2. Wikilinks rotos

Wikilinks `[[slug]]` o `[[carpeta/slug]]` que no resuelven a ningún archivo existente.

**Finding**: `broken-link | <archivo-origen>:<línea> → [[<slug>]]`

**Fix sugerido**: corregir el slug (si hay match aproximado por alias), crear stub, o borrar el wikilink.

### 3. `requires` / `unlocks` rotos

Wikilinks en frontmatter `requires:` o `unlocks:` que no apuntan a archivos existentes.

**Finding**: `broken-edge | <archivo>.<requires|unlocks> → [[<slug>]]`

**Fix sugerido**: corregir, crear stub, o borrar la arista.

### 4. Consistencia bidireccional de aristas

Si `A.requires` incluye `[[B]]`, entonces `B.unlocks` debe incluir `[[A]]`.

**Finding**: `edge-asymmetric | [[A]] requires [[B]] pero [[B]] no tiene [[A]] en unlocks`

**Fix sugerido**: agregar la arista faltante en B.

### 5. Fuentes huérfanas en `raw/`

Archivos bajo `raw/` (PDFs) que no tienen ningún `wiki/sources/*.md` cuyo `path:` apunte a ellos.

Excepción: archivos `.md` y `.jpeg`/`.jpg`/`.png` en `raw/` son extracciones y figuras producidas por `atlas-local` — no son fuentes primarias, se omiten de este check.

**Finding**: `source-not-ingested | raw/<path>`

**Fix sugerido**: ofrecer correr `/ingest` sobre la fuente.

### 6. Teoremas sin `statement_form`

Páginas `type: theorem` cuyo frontmatter no tiene `statement_form:` definido.

**Finding**: `theorem-no-statement | [[<slug>]]`

**Fix sugerido**: pedir al usuario el `statement_form` (formato "if A then B") y completarlo.

### 7. Métodos sin `when_to_use` / `fails_when`

Páginas `type: method` sin uno o ambos campos en frontmatter.

**Finding**: `method-no-applicability | [[<slug>]] falta <campo>`

**Fix sugerido**: pedir al usuario los campos y completarlos.

### 8. Conceptos mencionados sin página propia

Términos que aparecen ≥3 veces en wikilinks de otras páginas (`[[término]]`) pero no resuelven a ningún archivo existente y no son aliases conocidos.

**Finding**: `concept-implicit | "<término>" mencionado en N páginas, sin página propia`

**Fix sugerido**: crear stub o agregar como alias de una página existente.

### 9. Frontmatter incompleto

Páginas wiki donde falta algún campo obligatorio según `schema/wiki-conventions.md` (`type`, `title`, `areas`, `created`, `updated`).

**Finding**: `frontmatter-incomplete | [[<slug>]] falta <campo>`

**Fix sugerido**: completar con el usuario.

### 10. `updated:` rancio

Páginas wiki cuyo `updated:` es anterior a la fecha del último commit de git que tocó el archivo (`git log -1 --format=%cs -- <file>`).

**Finding**: `updated-stale | <file> updated=<fecha> pero el último commit es <fecha-mayor>`

**Fix sugerido**: actualizar `updated:` a la fecha del último commit.

---

## Reporte

Presentar al usuario:

```markdown
# Lint report — YYYY-MM-DD

Scope: <wiki/ o sub-scope>
Archivos analizados: N

## Resumen
- orphan: 3
- broken-link: 1
- edge-asymmetric: 2
- source-not-ingested: 4
- theorem-no-statement: 0
- method-no-applicability: 1
- concept-implicit: 2
- frontmatter-incomplete: 0
- updated-stale: 0

Total findings: 13
```

Después, ofrecer:

> "¿Querés que abordemos los findings uno por uno? Empiezo por los más impactantes (broken-link, edge-asymmetric) y seguimos."

---

## Fix interactivo

Para cada finding aceptado por el usuario:

1. Mostrar el contexto: archivo, línea, contenido relevante.
2. Proponer el fix exacto (qué texto cambia).
3. Esperar `sí` / `no` / `editá` (si el usuario quiere ajustar el fix).
4. Aplicar.
5. Si el fix tocó el catálogo, correr `atlas index`. El log se deriva de git:
   dejar (o sugerir) un commit `lint: <breve>` al cerrar la tanda de fixes.

Si el usuario dice "no" a un finding: no aplicar, pasar al siguiente.

---

## Cierre

Resumen final:

> "Lint completo. Findings procesados: ⟨aplicados⟩ / ⟨rechazados⟩ / ⟨pendientes⟩. Cambios registrados en `wiki/log.md`."

---

## Reglas de calidad

- **Read-only por default**: el lint nunca modifica archivos sin confirmación explícita del usuario por cada finding.
- **No spam**: si el wiki tiene 50 findings, agrupar por tipo y procesar tipo-por-tipo. No abrumar.

---

## Notas de portabilidad

El protocolo describe checks estáticos sobre frontmatter y wikilinks. Cualquier script (Python, Node, shell con grep + jq) puede implementarlo. El fix interactivo necesita un agente LLM para discutir con el usuario, pero los checks puros son código.

---
type: schema
updated: 2026-06-02
---

# Convenciones del wiki

Contrato de forma para todo archivo bajo `wiki/`. Cualquier modo que cree o modifique páginas wiki debe respetar este archivo.

---

## Taxonomía — tipos de página

| Tipo | Carpeta | Qué es |
|---|---|---|
| `concept` | `wiki/concepts/` | Una idea / objeto matemático / entidad. Ej: gradiente, proceso, autómata finito. |
| `theorem` | `wiki/theorems/` | Enunciado formal con hipótesis y conclusión. Ej: TFI, lema de Arden, teorema de Green. |
| `method` | `wiki/methods/` | Procedimiento operativo. Ej: criterio de la Hessiana, análisis de Kleene. |
| `example` | `wiki/examples/` | Caso resuelto que ilustra un concepto/teorema/método. Ej: parametrización de la cicloide. |
| `comparison` | `wiki/comparisons/` | Página que contrasta 2+ entidades. Ej: TFI vs teorema de la función inversa. |
| `source` | `wiki/sources/` | Resumen estructurado de una fuente externa con mapa de coverage. |
| `area` | `wiki/areas/` | MOC (map of content) de un área. Listado vía Dataview o manual. |

Regla: cada página tiene **un solo tipo**. La pertenencia a múltiples áreas (`math` + `signals`) se declara en el frontmatter, no replicando el archivo.

---

## Frontmatter común

Todo archivo wiki empieza con bloque YAML:

```yaml
---
type: concept | theorem | method | example | comparison | source | area
title: "Título legible"
aliases: ["nombre alt", "símbolo", "EN name"]
areas: [math, signals]
tags: [calculus/vector, integration]
requires: ["[[gradient]]"]
unlocks: ["[[greens-theorem]]"]
bloom: 2
sources: ["[[marsden-ch5]]", "[[teorico-calc-vec-clase07#p12]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---
```

Campos obligatorios para todo tipo (excepto `area`): `type`, `title`, `areas`, `created`, `updated`.

Campos extra por tipo:

- **`theorem`**: `statement_form: "if A and B then C"` — esqueleto lógico.
- **`method`**: `when_to_use: "..."`, `fails_when: "..."` — selección del método.
- **`example`**: `illustrates: ["[[concept-or-theorem]]"]`, `difficulty: 1|2|3`, `session_ref: "subjects/<materia>/index.md#<fecha>"`.
- **`source`**: `source_kind: lecture|book|paper|notes`, `path: "raw/lectures/.../foo.pdf"`, `pages: "12-34"`, `covers_concepts: [[...]]`, `covers_theorems: [[...]]`, `covers_methods: [[...]]`.
- **`comparison`**: `compares: ["[[A]]", "[[B]]"]`.
- **`area`**: `tag_prefix: "math"` — prefijo de tag que captura sus miembros.

### Validez de campos

- `bloom`: entero 0–6. **0** = aún no trabajado (default al crear). 1–6 = niveles de la tabla en `CLAUDE.md` / `schema/practice-protocol.md`.
- `requires` / `unlocks`: arrays de wikilinks `[[slug]]`. Definen el DAG de dependencias.
- `aliases`: incluir variantes (símbolo, EN, ES, abreviatura). Sirve para el firewall y para resolver `[[wikilinks]]` ambiguos.
- `tags`: kebab con `/` para jerarquía. Ej: `calculus/vector/integration`.
- `seen_in_subjects`: slugs de carpetas bajo `subjects/`. Permite Dataview proyectar.

---

## Notación matemática

- Sintaxis: **KaTeX**.
- Inline: `$...$`. Display: `$$...$$`.
- **Prohibido**: `\(...\)` y `\[...\]` — incompatibles con varios renderers.
- Variables vectoriales: `\vec{v}` o `\mathbf{v}`. Mantener consistencia dentro de la página.
- Operadores: `\nabla`, `\partial`, `\mathrm{d}`. Para diferenciales preferir `\mathrm{d}x` sobre `dx`.

---

## Wikilinks y rutas

- Dentro de `wiki/`: usar `[[slug]]` (Obsidian-style). El slug es el filename sin `.md` ni carpeta.
- Para wikilinks ambiguos (mismo slug en dos carpetas) usar `[[concepts/gradient]]`.
- Para cruzar a `subjects/`: ruta relativa, ej `[ver sesión](../subjects/calculo-vectorial/index.md)`.
- **No usar URLs**, ni paths absolutos, ni `~/`.

---

## Citas de fuentes

Toda afirmación fuerte (enunciado formal, número, fecha histórica, atribución) requiere cita inline.

Forma canónica:

> Por el TFI [[apostol-vol2-ch13]] §13.4 p. 376, si $\partial F / \partial y \neq 0$ entonces...

Reglas:
- `[[source-slug]]` apunta a una página en `wiki/sources/`.
- Sección y número de página son **obligatorios** para libros y papers.
- Para clases teóricas: `[[teorico-calc-vec-clase07]] p. 12` o `#p12`.
- Para afirmaciones informales / desarrollo intuitivo: no requiere cita.

---

## File naming (slugs)

- **kebab-case** siempre. Ej: `implicit-function-theorem.md`, no `ImplicitFunctionTheorem.md`.
- **Inglés** para términos internacionales (matemática, física, CS estándar).
- **Español** para términos curso-específicos sin equivalente neutro (ej: `analisis-de-kleene.md` si el curso lo trata como bloque didáctico unitario).
- El `aliases:` del frontmatter cierra el gap idiomático.
- Nunca incluir el tipo en el nombre del archivo (no `gradient-concept.md`) — el tipo vive en el frontmatter y la carpeta.

---

## Bloom — fuente única de verdad

El nivel de Bloom de un concepto vive **únicamente** en el frontmatter de su página wiki (`bloom:`). Las materias proyectan vía Dataview o lectura manual de `seen_in_subjects:`.

Razón: un concepto presente en dos materias = un solo número, sin drift entre archivos.

La sección "Bloom actual" de `subjects/[materia]/index.md` queda como referencia humana legible pero **no es la verdad ejecutable**. Cuando los dos archivos divergen, la wiki gana.

Esto lo verifica `schema/lint-protocol.md` (chequeo "Bloom desincronizado").

---

## Sección de contenido (cuerpo)

Estructura sugerida (no obligatoria — adaptar al tipo):

```markdown
## Definición
...

## Intuición
...

## Enunciado formal  (solo para theorem)
**Hipótesis:** ...
**Conclusión:** ...

## Cuándo usarlo  (solo para method)
...

## Cuándo falla  (solo para method)
...

## Ejemplos
- [[ejemplo-1]]
- [[ejemplo-2]]

## Conexiones
- Requiere: [[...]], [[...]]
- Habilita: [[...]], [[...]]
- Relacionado: [[...]]

## Fuentes
- [[apostol-vol2-ch13]] §13.4 p. 376
- [[teorico-calc-vec-clase07]] pp. 8-15
```

El frontmatter es lo no-negociable. El cuerpo debe ser legible pero su estructura es discrecional.

---

## Updates — actualización de páginas existentes

Cuando un modo modifica una página:

1. Actualizar `updated:` en el frontmatter.
2. Si se agrega una fuente nueva: append a `sources:` (no reemplazar).
3. Si se agrega área nueva: append a `areas:`.
4. Si `bloom:` cambia: registrar el cambio en `wiki/log.md` con motivo.
5. Si `requires:` o `unlocks:` cambian: verificar que los wikilinks existan (o se vayan a crear en la misma operación).

---

## Notas de portabilidad

Todas las convenciones acá son estándares de markdown extendido (YAML frontmatter, wikilinks Obsidian-style, KaTeX). Cualquier parser de markdown con soporte de frontmatter (gray-matter, remark, pandoc) las procesa sin extensiones específicas. Es decir: el wiki es válido fuera de Atlas.

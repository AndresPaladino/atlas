---
type: schema
updated: 2026-06-10
---

# Protocolo: modo `/ingest`

Tomar una fuente cruda (PDF, notas, libro, paper) y poblar/actualizar el wiki con su contenido conceptual. La fuente queda inmutable en `raw/`; el wiki captura la síntesis.

---

## Apertura

1. Leer `schema/purpose.md`: define el alcance (qué entra al wiki y qué se descarta). Filtrar los candidatos contra esto durante todo el análisis.
2. Identificar la fuente:\
   - Si el comando trae ruta: `Read` directo sobre el archivo en `raw/`.
   - Si trae descripción ("estas notas pegadas"): pedir el contenido.
   - Si trae solo nombre ambiguo o directamente no trae nada: usar `atlas ingest-status` en cli y preguntar cuál.
3. Clasificar la fuente — bifurca el resto del protocolo:
   - **Material de estudio** (libro, paper, notas, clase) → página `type: source` en `wiki/sources/`. Confirmar `source_kind` (book / paper / notes / lecture) si no es inferible del nombre.
   - **Evaluación** (examen, parcial, práctico — típicamente slug `*-exam-*` / `*-parcial-*`) → página `type: assessment` en `wiki/assessments/`. Confirmar `assessment_kind` (exam / parcial / practica) y `course` (sigla). Un examen **no** es fuente de conocimiento: usa `evaluates:` (no `covers_*`) y cada concepto evaluado recibe `assessed_by:` apuntando de vuelta (relación bidireccional, ver `wiki-conventions.md`).

El ingest es en **dos fases**: primero se analiza (Fase 1, no se escribe nada), recién después se genera (Fase 2). La separación mejora la calidad —reflexionar antes de escribir— y evita reescrituras.

---

# Fase 1 — Análisis (no se escribe nada)

## Paso 1 — Leer y mapear

Elegir la fuente más barata disponible, en este orden de preferencia:

1. **TOC + chunks (docs grandes).** Si existe `raw/<mismo-nombre>.toc.md` (lo produce `atlas extract` al segmentar libros/apuntes grandes, ver `tools/`), leer **primero el TOC**: es un índice compacto (árbol de headings + página + tokens estimados + qué chunk contiene cada sección). A partir del TOC se arma el mapa de conceptos **sin leer el cuerpo entero**. Para profundizar en una sección, leer **solo** el chunk correspondiente de `raw/<mismo-nombre>/` (p.ej. `raw/<nombre>/02-extremos.md`). **Nunca** leer el monolítico `raw/<nombre>.md` cuando hay TOC: anula el ahorro de tokens. Si el usuario pide un rango de páginas, mapearlo a chunks vía la columna de páginas del TOC.
2. **Markdown monolítico (docs chicos).** Si **no** hay `.toc.md` pero sí `raw/<mismo-nombre>.md`, leerlo completo: para exámenes y papers cortos el costo es bajo y trae LaTeX + captions de figuras.
3. **PDF visual (fallback).** Si no hay `.md`, hacer `Read` visual sobre el PDF — fiel pero caro en tokens.

- Construir un mapa interno: para cada sección listar los conceptos / teoremas / métodos / ejemplos que aparecen (con el TOC, esto sale casi directo de los headings).
- No escribir nada todavía.

---

## Paso 2 — Analizar contra el wiki existente

Para cada candidato del mapa, hacer lookup en `wiki/index.md` (por título / alias / slug) y armar el **artefacto de análisis** — todavía sin tocar ningún archivo:

- **Estado**: ¿ya existe como página, o es nuevo?
- **Conexiones**: con qué páginas existentes engancha (`requires` / `unlocks` plausibles).
- **Contradicciones**: si la fuente afirma algo que choca con una página actual, marcarlo (no resolverlo todavía).
- **Estructura propuesta**: qué páginas crear, cuáles actualizar, y bajo qué tipo / área.

---

## Paso 3 — Discutir con el usuario

Presentar el análisis de forma compacta:

> "Analicé la fuente:
> - Nuevos: ⟨candidatos con tipo entre paréntesis⟩
> - Ya cubiertos (solo agrego la fuente): ⟨...⟩
> - Contradicciones / a revisar: ⟨...⟩
>
> ¿Cuáles enfatizo? ¿Confirmás la estructura propuesta?"

Esperar respuesta del usuario. El usuario puede:
- Pedir focus en un subconjunto.
- Marcar conceptos como "ya existe" → solo actualizar.
- Indicar que se cree todo.
- Resolver una contradicción detectada.

---

# Fase 2 — Generación

Recién acá se crean / modifican archivos, según lo acordado en Fase 1.

## Paso 4 — Crear página de fuente

Crear `wiki/sources/<slug>.md`.

Slug:
- Para libros o capítulos: `<autor-apellido>-<libro-abrev>` o `<autor>-ch<NN>`.
- Para papers: `<primer-autor>-<año>-<tema-corto>`.
- Para apuntes o notas: `<tema-corto>-notes` o `<autor-o-curso>-<tema>`.
- Para teóricos: `<tema>-lecture` o `<curso>-clase<NN>`.

No codificar el origen en el slug — el slug describe el contenido, no el contexto de uso.

Frontmatter: seguir el **frontmatter común** de `schema/wiki-conventions.md` (single source of truth) con `type: source` y los campos propios del tipo:

- `source_kind: book | paper | notes | lecture`
- `path: "raw/<archivo>.pdf"` — ruta al `.pdf` (fuente inmutable). Campo de tracking: `atlas ingest-status` lo usa para saber qué PDFs ya tienen coverage.
- `chunks: ["raw/<nombre>/01-intro.md", "raw/<nombre>/03-svd.md"]` — lista de chunks de `raw/<nombre>/` que Claude leyó para producir esta source. Permite calcular cobertura parcial cuando el libro es grande y se ingresa en varias pasadas. Omitir si el PDF no tiene carpeta de chunks.
- `extracted: "raw/<archivo>.md"` — legacy: markdown monolítico (solo para docs sin chunks). No usar en docs segmentados; preferir `chunks:`.
- `toc: "raw/<archivo>.toc.md"` — opcional: índice de segmentación, si el doc se segmentó.
- `pages: "1-24"` — rango de páginas cubierto, opcional.
- `covers_concepts` / `covers_theorems` / `covers_methods` — wikilinks a lo que la fuente cubre.

Cuerpo:

```markdown
## Mapa de coverage

Si el doc tiene `raw/<nombre>.toc.md`, esta tabla se deriva casi directo de él: cada fila del TOC (sección + página) ya trae el heading; basta anotar el concepto wiki que le corresponde y, opcionalmente, el chunk donde vive.

| Sección / diapositiva | Página | Concepto wiki |
|---|---|---|
| §13.4 enunciado | 376 | [[implicit-function-theorem]] |
| §13.5 caso vectorial | 381 | [[implicit-function-theorem]] |
| Ej 2 | 384 | [[jacobian]] |

## Notas
(opcional — peculiaridades de notación de la fuente, errata conocida, etc.)
```

---

## Paso 4-bis — Si la fuente es una evaluación

En vez de `wiki/sources/`, crear `wiki/assessments/<slug>.md` con `type: assessment`.

- Slug: `<curso>-<kind><fecha>`, p.ej. `sistop-exam-dic2024`, `gal2-parcial-may2019`.
- Frontmatter propio del tipo (ver `wiki-conventions.md`): `assessment_kind`, `course`, `path`, `evaluates` (en lugar de `covers_*`), `extracted`/`ingested_sha256` opcionales.
- Cuerpo: mismo "Mapa de coverage" pero por problema (`| Problema | Concepto wiki |`).
- En el Paso 5, cada concepto evaluado se trata por **Caso A-assessment** (abajo): no toca `sources:`, append a `assessed_by:`.

## Paso 5 — Para cada concepto del mapa

Según el estado ya determinado en el análisis (Paso 2):

### Caso A: existe (fuente de conocimiento)

- Leer la página existente.
- Append la fuente nueva a `sources:` del frontmatter.
- Si la fuente trae detalles que la página no tenía (ej: enunciado más preciso, ejemplo nuevo, observación) → agregar al cuerpo con cita explícita.
- Actualizar `updated:`.

### Caso A-assessment: existe (evaluación)

- Leer la página existente.
- Append el assessment a `assessed_by:` (no a `sources:`). El lado `evaluates:` del assessment ya apunta acá → simetría (la verifica `atlas lint`).
- Actualizar `updated:`.

### Caso B: no existe

- Crear `wiki/<tipo>/<slug>.md` con frontmatter completo según `schema/wiki-conventions.md`.
- `sources:` arranca con la fuente recién creada.
- Cuerpo: definición + intuición + (si aplica) enunciado/cuándo-usar. Mínimo un párrafo legible — no stubs vacíos.

---

## Paso 6 — Actualizar aristas

Para cada página tocada (creada o modificada):

- Revisar `requires:` — agregar prerrequisitos faltantes. Si el prerrequisito no existe como página, crearlo en stub (frontmatter + 1 línea de definición) con nota "Pendiente de desarrollar".
- Revisar `unlocks:` — agregar páginas que dependen de esta. Asegurar que las páginas listadas tengan a esta en sus `requires:` (consistencia bidireccional).

Aristas son del DAG conceptual, no de la fuente. La fuente solo aporta la oportunidad de detectarlas.

---

## Paso 7 — Sellar el hash de ingestión

Por cada fuente ingerida, correr `atlas ingest-stamp <slug>`: registra en su
frontmatter el hash del raw (`ingested_sha256`) y la lista `chunks:` cuando el PDF
tiene carpeta de chunks. Es lo que permite a `--compile` saltear después las
fuentes sin cambios (cero re-ingesta redundante) y lo que cierra el coverage de
`ingest-status` (sin `chunks:` reporta `partial 0/N`). Determinístico — el LLM no
calcula el hash, solo invoca el comando.

En `--compile`, en vez de una llamada por fuente, correr `atlas ingest-stamp --all`
una sola vez al final: sella toda fuente ingestable (idempotente, no pisa `chunks:`
ya declarados).

---

## Paso 8 — Regenerar índice y áreas

Correr `atlas index`. Regenera `wiki/index.md` y los MOCs de `wiki/areas/*.md`
desde el filesystem (entre marcadores `<!-- atlas:auto -->`, preservando las
descripciones humanas). **No** editar esas listas a mano — driftan.

Después, `atlas validate` para confirmar que el frontmatter de las páginas nuevas
cumple el contrato (`schema/wiki-conventions.md`).

---

## Paso 9 — Commit (= log)

El log de mutaciones se deriva de git: la mutación real *es* el commit. No editar
`wiki/log.md` a mano. Dejar (o sugerir) un commit con la convención:

```
ingest: <título de la fuente> — N páginas creadas, M actualizadas
```

`atlas log` lo renderiza después (`git log -- wiki/`).

---

## Cierre

Resumen al usuario:

> "Ingest completo. Archivos tocados:
> - Fuente: `wiki/sources/<slug>.md`
> - Creadas: ⟨N⟩ páginas
> - Actualizadas: ⟨M⟩ páginas
> - Log: `wiki/log.md`
>
> Si querés verificar el grafo: abrir Obsidian → graph view."

---

## Reglas de calidad

- **No stubs vacíos**: toda página creada tiene al menos un párrafo de contenido. Si no se puede escribir un párrafo útil, mejor no crearla y dejar el concepto mencionado en `sources/`.
- **Citas obligatorias** en claims fuertes: el primer párrafo de una página nueva debe llevar al menos una cita a la fuente que la originó.
- **Idioma según `wiki-conventions.md`**: slug en inglés para términos internacionales; español para específicos.
- **No duplicar**: antes de crear, buscar por aliases en `wiki/index.md`. Si hay ambigüedad, preguntar al usuario.

---

## Modo compile

Activado con `/ingest --compile`. Escanea `raw/` en busca de archivos no registrados y los ingiere en secuencia.

### Paso C1 — Detectar archivos nuevos

1. Listar las **fuentes** de `raw/`:
   - Los **`.pdf`** (unidad primaria de una fuente).
   - Los `.txt`/`.md` **nativos**: los que no tienen un PDF homónimo **y** no son artefactos de extracción.

   **Excluir siempre los artefactos que produce `atlas extract`** — no son fuentes: el `.md` monolítico, el `<nombre>.toc.md`, y **todo** lo que viva dentro de un directorio de chunks `raw/<nombre>/`. La forma fiable de identificarlos es leer `raw/.atlas-extract.json` y descartar todo `md_path`, `toc_path` y cualquier archivo bajo un `chunks_dir`. **Un documento segmentado es una sola fuente = su `.pdf`**; sus chunks y su TOC nunca se enumeran como fuentes separadas (al ingerir esa fuente, el Paso 1 ya lee el TOC y solo los chunks relevantes).
2. Leer los frontmatters de todos los archivos bajo `wiki/sources/` y extraer el campo `path:` de cada uno.
3. Construir la lista de **archivos no registrados**: fuentes en `raw/` cuyo path no aparece en ningún `path:` de `wiki/sources/`.
   Además, correr `atlas ingest-status --json`: las fuentes ya registradas con estado `stale` (su raw cambió desde la última ingesta) son candidatas a **re-ingestión**; las `current` se saltean (cero llamadas LLM). Sumar las `stale` a la lista a procesar.
4. Para cada fuente nueva, chequear si existe su `.md` cacheado (mismo nombre, extensión `.md`). Si **falta**, avisar y sugerir correr la extracción local antes de ingerir (no convertir el PDF desde Claude):
   > "`<archivo>.pdf` no tiene markdown extraído. Corré `atlas extract` (o `atlas extract raw/<archivo>.pdf`) y volvé a `/ingest --compile`. Si querés ingerirlo igual ahora, lo leo visualmente del PDF (más caro en tokens)."

Si no hay archivos nuevos:
> "No hay archivos nuevos en `raw/`. Tirá un PDF ahí y volvé a correr `/ingest --compile`."

### Paso C2 — Presentar al usuario

Mostrar la lista de archivos nuevos con su nombre y, si se puede inferir del nombre, el tipo probable:

> "Encontré N archivos nuevos en `raw/`:
> 1. `nombre-archivo.pdf` — (paper / libro / apunte, inferido del nombre)
> 2. ...
>
> ¿Los ingiero todos, o querés elegir cuáles?"

Esperar respuesta. El usuario puede:
- Confirmar todos → ingerir en secuencia.
- Indicar un subconjunto → ingerir solo esos.
- Posponer alguno → excluirlo de esta sesión (no se procesa; en la próxima aparecerá de nuevo).

### Paso C3 — Ingerir en secuencia

Para cada archivo seleccionado, ejecutar el flujo normal de ingest completo (Fase 1 análisis → Fase 2 generación) antes de pasar al siguiente. Al terminar cada uno, informar brevemente:

> "✓ `nombre-archivo.pdf` → fuente `[[slug]]`, N páginas creadas, M actualizadas."

En compile, **omitir el Paso 7 (stamp) por fuente**: al terminar la secuencia, correr `atlas ingest-stamp --all` una sola vez. Sella todo lo ingerido (hash + `chunks:`) en un paso.

### Paso C4 — Resumen final

Al terminar todos:

> "Compile completo.
> - Archivos procesados: N
> - Páginas wiki creadas: X (total)
> - Páginas wiki actualizadas: Y (total)
> - Archivos ignorados / pospuestos: Z"

---

## Notas de portabilidad

El protocolo describe acciones sobre filesystem (leer fuente, crear/actualizar archivos markdown). Cualquier agente con file-IO y un LLM detrás puede implementarlo. No depende de tools específicos del runtime.

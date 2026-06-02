---
type: schema
updated: 2026-06-02
---

# Protocolo: modo `/ingest`

Tomar una fuente cruda (PDF, notas, libro, paper) y poblar/actualizar el wiki con su contenido conceptual. La fuente queda inmutable en `raw/`; el wiki captura la síntesis.

---

## Apertura

1. Anunciar `[modo: ingest]`.
2. Identificar la fuente:
   - Si el comando trae ruta: `Read` directo sobre el archivo en `raw/`.
   - Si trae descripción ("estas notas pegadas"): pedir el contenido.
   - Si trae solo nombre ambiguo: listar `raw/` y preguntar cuál.
3. Confirmar `source_kind` (book / paper / notes / lecture) con el usuario si no es inferible del nombre del archivo. No asumir materia — la fuente puede no pertenecer a ninguna materia activa.

---

## Paso 1 — Leer y mapear

- Leer la fuente completa (o pedir rango de páginas si es muy larga).
- Construir un mapa interno: para cada sección o diapositiva, listar los conceptos / teoremas / métodos / ejemplos que aparecen.
- No escribir nada todavía.

---

## Paso 2 — Discutir con el usuario

Presentar el mapa de forma compacta:

> "Identifiqué N conceptos en la fuente:
> - ⟨lista de candidatos con tipo entre paréntesis⟩
>
> ¿Cuáles enfatizo? ¿Hay alguno que ya cubrimos antes y solo quiero agregar como fuente?"

Esperar respuesta del usuario. El usuario puede:
- Pedir focus en un subconjunto.
- Marcar conceptos como "ya existe" → solo actualizar.
- Indicar que se cree todo.

---

## Paso 3 — Crear página de fuente

Crear `wiki/sources/<slug>.md`.

Slug:
- Para libros o capítulos: `<autor-apellido>-<libro-abrev>` o `<autor>-ch<NN>`.
- Para papers: `<primer-autor>-<año>-<tema-corto>`.
- Para apuntes o notas: `<tema-corto>-notes` o `<autor-o-curso>-<tema>`.
- Para teóricos (si aplica): `<tema>-lecture` o `<materia>-clase<NN>`.

No codificar la materia en el slug — el slug describe el contenido, no el contexto de uso.

Frontmatter:

```yaml
---
type: source
title: "<título legible>"
aliases: ["<variantes>"]
source_kind: book | paper | notes | lecture
path: "raw/<nombre-de-archivo>"   # ruta relativa al repo, sin subcarpetas
pages: "1-24"                     # rango cubierto, opcional
areas: [math, signals]
tags: [calculus/vector]
covers_concepts: ["[[implicit-function-theorem]]", "[[jacobian]]"]
covers_theorems: ["[[implicit-function-theorem]]"]
covers_methods: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Cuerpo:

```markdown
## Mapa de coverage

| Sección / diapositiva | Página | Concepto wiki |
|---|---|---|
| §13.4 enunciado | 376 | [[implicit-function-theorem]] |
| §13.5 caso vectorial | 381 | [[implicit-function-theorem]] |
| Ej 2 | 384 | [[jacobian]] |

## Notas
(opcional — peculiaridades de notación de la fuente, errata conocida, etc.)
```

---

## Paso 4 — Para cada concepto del mapa

Hacer un lookup en `wiki/index.md` por título / alias / slug.

### Caso A: existe

- Leer la página existente.
- Append la fuente nueva a `sources:` del frontmatter.
- Si la fuente trae detalles que la página no tenía (ej: enunciado más preciso, ejemplo nuevo, observación) → agregar al cuerpo con cita explícita.
- Actualizar `updated:`.
- No tocar `bloom:` (se actualiza solo en `/practice`).

### Caso B: no existe

- Crear `wiki/<tipo>/<slug>.md` con frontmatter completo según `schema/wiki-conventions.md`.
- `sources:` arranca con la fuente recién creada.
- `bloom: 0` (no trabajado todavía).
- `seen_in_subjects:` = vacío por defecto. Solo completar si el concepto aparece explícitamente en una de las materias activas del perfil (verificar `profile/student_profile.md`). La fuente no determina la materia — el uso en práctica sí.
- Cuerpo: definición + intuición + (si aplica) enunciado/cuándo-usar. Mínimo un párrafo legible — no stubs vacíos.

---

## Paso 5 — Actualizar aristas

Para cada página tocada (creada o modificada):

- Revisar `requires:` — agregar prerrequisitos faltantes. Si el prerrequisito no existe como página, crearlo en stub (frontmatter + 1 línea de definición) con nota "Pendiente de desarrollar".
- Revisar `unlocks:` — agregar páginas que dependen de esta. Asegurar que las páginas listadas tengan a esta en sus `requires:` (consistencia bidireccional).

Aristas son del DAG conceptual, no de la fuente. La fuente solo aporta la oportunidad de detectarlas.

---

## Paso 6 — Actualizar índice y áreas

- `wiki/index.md`: append a la sección correspondiente (concepts / theorems / etc.) con un link a la página nueva o modificada. Si el archivo usa Dataview, no requiere edición manual.
- `wiki/areas/<area>.md`: si la página pertenece a un área cuyo MOC no la listaba, append vía Dataview (no manual) o nota manual si Dataview no está disponible.

---

## Paso 7 — Log

Append a `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | <título de la fuente>

- Fuente: [[<slug>]] (`raw/<path>`)
- Páginas wiki creadas: [[a]], [[b]]
- Páginas wiki actualizadas: [[c]] (sources +1), [[d]] (cuerpo expandido)
- Aristas nuevas: [[a]] requires [[x]]; [[b]] unlocks [[y]]
```

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
- **Idioma según `wiki-conventions.md`**: slug en inglés para términos internacionales; español para curso-específicos.
- **No duplicar**: antes de crear, buscar por aliases en `wiki/index.md`. Si hay ambigüedad, preguntar al usuario.

---

## Modo compile

Activado con `/ingest --compile`. Escanea `raw/` en busca de archivos no registrados y los ingiere en secuencia.

### Paso C1 — Detectar archivos nuevos

1. Listar todos los archivos en `raw/` (extensiones `.pdf`, `.md`, `.txt`).
2. Leer los frontmatters de todos los archivos bajo `wiki/sources/` y extraer el campo `path:` de cada uno.
3. Construir la lista de **archivos no registrados**: archivos en `raw/` cuyo path no aparece en ningún `path:` de `wiki/sources/`.

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

Para cada archivo seleccionado, ejecutar el flujo normal de ingest (Pasos 1–7) completo antes de pasar al siguiente. Al terminar cada uno, informar brevemente:

> "✓ `nombre-archivo.pdf` → fuente `[[slug]]`, N páginas creadas, M actualizadas."

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

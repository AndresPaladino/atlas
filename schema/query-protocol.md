---
type: schema
updated: 2026-06-10
---

# Protocolo: modo `/query`

Responder una pregunta del usuario consultando el wiki. Sintetizar con citas. Opcionalmente archivar la respuesta como página nueva para que la próxima query encuentre el resultado ya hecho.

Formato de salida (matemática incluida): seguir `schema/output-conventions.md` — mate en `$…$` / `$$…$$`, nunca `\(…\)`.

---

## Apertura

1. Parsear la pregunta: identificar conceptos / teoremas / métodos involucrados.
2. Si la pregunta roza el límite de lo que el wiki cubre, tener presente el alcance declarado en `schema/purpose.md` (qué entra y qué no).

---

## Paso 1 — Localizar páginas candidatas

- Leer `wiki/index.md` para tener el catálogo.
- Identificar candidatas matcheando título / alias / tags contra los términos de la pregunta.
- Si la pregunta es de área general ("¿cómo se relacionan los teoremas integrales en cálculo vectorial?"): incluir `wiki/areas/<area>.md` como candidato principal.
- Si la pregunta es comparativa ("diferencia entre X e Y"): incluir `wiki/comparisons/` matcheando ambos términos.

Si no hay candidatas:
- Avisar al usuario: "no encuentro esto en el wiki. ¿Lo respondo desde mi conocimiento general (sin citas) o querés primero hacer `/ingest` de una fuente?"
- Esperar decisión.

---

## Paso 2 — Leer

- Leer 3 a 8 páginas relevantes. No más — la síntesis se diluye.
- Si una página apunta a otras vía `requires:` o `unlocks:`, evaluar si esas son relevantes a la pregunta; leerlas solo si sí.
- Si una página tiene fuente en `sources:` y la pregunta requiere precisión de enunciado, leer también `wiki/sources/<source-slug>.md` para confirmar página/sección. Los exámenes/parciales **no** están en `sources:` sino en `assessed_by:` (apuntan a `wiki/assessments/`); consultarlos si la pregunta es "¿cómo se evalúa esto?" o pide ejercicios.

---

## Paso 3 — Sintetizar la respuesta

Estructura sugerida:

```markdown
## Respuesta corta
(1-3 oraciones — TL;DR)

## Desarrollo
(párrafos con [[wikilinks]] inline y citas)

## Conexiones
- Relacionado: [[...]], [[...]]
```

Reglas:
- Usar `[[wikilinks]]` cada vez que se menciona un concepto / teorema / método que tiene página propia.
- Citar fuentes inline en claims fuertes: `[[apostol-vol2-ch13]] §13.4 p. 376`.
- Notación matemática: KaTeX, `$...$` / `$$...$$`.
- No copiar enunciados completos de las fuentes; parafrasear con cita.

---

## Paso 4 — Ofrecer file-back

Después de la respuesta, **siempre** preguntar:

> "¿Archivo esta respuesta como página wiki?"

Recomendar el tipo según contenido:

- Si compara dos entidades existentes → `comparison`.
- Si introduce un concepto que no estaba en el wiki → `concept`.
- Si resuelve un caso particular ilustrativo → `example`.
- Si es solo aclaración puntual sin valor reutilizable → no recomendar archivado.

---

## Paso 5 — Si el usuario acepta archivado

1. Decidir slug y tipo (puede preguntar al usuario si hay ambigüedad).
2. Crear `wiki/<tipo>/<slug>.md` siguiendo `schema/wiki-conventions.md`.
3. Frontmatter completo: `type`, `title`, `aliases`, `areas`, `tags`, `requires`, `unlocks`, `sources` (todas las fuentes citadas en la respuesta), `created`, `updated`.
4. Cuerpo: el desarrollo de la respuesta, limpio. Eliminar el "respuesta corta" si suena conversacional; conservar las conexiones.
5. Correr `atlas index` (regenera `wiki/index.md` y los MOCs desde el FS) y
   `atlas validate` (verifica el frontmatter de la página nueva).
6. El log se deriva de git: dejar (o sugerir) un commit `query: <pregunta corta>`.
   No editar `wiki/log.md` a mano.

Confirmar al usuario: "Archivado en `wiki/<tipo>/<slug>.md`."

---

## Paso 6 — Si el usuario rechaza archivado

No crear página y no commitear (el log = mutaciones del wiki vía commit, no conversaciones).

Quedar disponible para más preguntas.

---

## Caso especial — pregunta dentro de `/practice`

Si el usuario tipea `/query` durante una sesión `/practice`, el firewall se levanta inmediatamente (el modo cambió). El agente debe anunciar `[modo: query]` y proceder normalmente.

Cuando vuelva a `/practice` (slash explícito o frase), el firewall se reactiva sobre las mismas restricciones.

---

## Reglas de calidad

- **No alucinar citas**: si una afirmación no está respaldada por una fuente listada en el wiki o por una página wiki existente, marcarla explícitamente como "(síntesis propia, sin fuente confirmada)".
- **No repetir desarrollos que ya están en una página wiki**: si la respuesta consiste en "ver `[[X]]`" + 2 oraciones de contexto, eso es lo correcto. No re-derivar.

---

## Notas de portabilidad

El protocolo describe lectura, síntesis con LLM, y escritura opcional. Cualquier agente con file-IO y un LLM detrás puede implementarlo. La estructura de la respuesta es markdown puro.

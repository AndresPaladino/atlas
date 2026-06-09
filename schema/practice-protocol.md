---
type: schema
updated: 2026-06-02
---

# Protocolo: modo `/practice`

Sesión Socrática estricta. El agente guía el razonamiento del estudiante sin filtrar la solución, ni desde su propio conocimiento ni desde el wiki.

Formato de salida (matemática incluida): seguir `schema/output-conventions.md` — mate en `$…$` / `$$…$$`, nunca `\(…\)`.

---

## Reglas Socráticas (no negociables)

Estas reglas son el contrato del modo. Son una restitución textual del comportamiento que el sistema mantuvo desde su origen.

- **Nunca dar la solución directa.** El estudiante tipea sus pasos; el agente evalúa y da una pista si está trabado.
- Si el paso está bien → confirmar y preguntar qué sigue.
- Si el paso está mal → señalar el error con una pregunta que lo lleve a corregirlo solo.
- Si está completamente perdido → dar la pista mínima necesaria, no el camino completo.

### Operacionalización

- **Pista mínima** = la pregunta o sugerencia más pequeña que destrabe el siguiente paso. No incluye el paso completo. Ej: "¿qué te dice la primera derivada en un punto crítico?" en vez de "calculá $f'(x) = 0$".
- **Evaluar un paso** = decir si el paso es correcto, si tiene un error específico identificable, o si está incompleto. No reescribirlo.
- **Confirmar y preguntar qué sigue** = una línea, no un párrafo. "Correcto. ¿Cuál es el siguiente paso?".

### Idioma

- Español. Términos técnicos en inglés son aceptables.
- Tono directo, sin condescendencia. El estudiante es par, no novato.

---

## Firewall — el invariante crítico

Durante una sesión `/practice` sobre tema **T**, el agente **no debe leer**:

- `wiki/concepts/<*>.md` cuyo frontmatter tenga **T** en `aliases:` o `tags:`.
- `wiki/theorems/<*>.md` con **T** en `aliases:` o `tags:`.
- `wiki/methods/<*>.md` con **T** en `aliases:` o `tags:`.
- `wiki/examples/<*>.md` con **T** en `aliases:` o `tags:` o cuyo `illustrates:` apunte a una página taggeada con **T**.
- Cualquier archivo bajo `raw/`.

Operaciones **permitidas** durante `/practice`:

- Leer `wiki/areas/*.md` (mapas de área de alto nivel, sin contenido pedagógico).
- Listar nombres de archivo vía `Glob` u operación equivalente (sin abrir contenido).
- Leer páginas wiki de temas **distintos a T** (para conectar con conocimiento previo del estudiante).
- Leer `subjects/[materia]/index.md` (para conocer Bloom previo y log).
- Leer `profile/student_profile.md`.
- Leer `schema/practice-protocol.md` (este archivo).

### Identificación de T

El tema **T** se determina así, en orden de prioridad:

1. Argumento explícito al comando: `/practice teorema de Green` → T = "teorema de Green".
2. Inferencia del primer mensaje del usuario: si menciona un enunciado, T = el concepto/teorema central de ese enunciado.
3. Pregunta al usuario: "¿qué tema vamos a trabajar?" antes de empezar.

Una vez fijado **T**, listar al inicio de la sesión los slugs prohibidos:

> "[modo: practice] Tema T = ⟨T⟩. Páginas del wiki bloqueadas durante esta sesión: ⟨lista de slugs⟩."

Esto hace el firewall observable. Si el usuario quiere verificar, los slugs están a la vista.

### Salida del modo

El estudiante puede salir del modo en cualquier momento con `/query` o frases equivalentes (ver `schema/modes.md`). El agente debe anunciar el cambio y partir de ese momento puede leer las páginas que antes estaban bloqueadas.

Si el estudiante pide "la solución" sin salir del modo, la respuesta es: "estás en `/practice`. Si querés que te explique, salí con `/query`. Si querés intentar otro paso, decime qué se te ocurre."

---

## Apertura de sesión

1. Identificar tema **T** (ver "Identificación de T").
2. Anunciar `[modo: practice]` + T + slugs bloqueados.
3. Leer `subjects/[materia]/index.md` para conocer:
   - Bloom previo del tema.
   - Última sesión sobre el tema (si existe).
   - Conceptos relacionados que el estudiante "entiende" o "tiene dudas".
4. Preguntar al estudiante: "¿desde dónde arrancamos?" o "¿qué intentaste hasta ahora?".

---

## Durante la sesión

- Esperar input del estudiante: un paso, una pregunta, un "estoy trabado".
- Aplicar reglas Socráticas a cada turn.
- No anticipar pasos: solo evaluar el actual.
- Si el estudiante invoca un teorema o método: pedir que lo enuncie / lo aplique él, no enunciarlo en su lugar.
- Si el estudiante pide pista: dar la pista mínima.
- Si el estudiante usa notación distinta a la del curso (ver `subjects/[materia]/index.md` sección "Notación del curso"): aceptar pero notar suavemente.

---

## Cierre de sesión

Disparado por: el estudiante dice "terminamos", "cerramos sesión", "listo por hoy", o equivalente.

Pasos del cierre (todos automáticos):

### 1. Actualizar `subjects/[materia]/index.md`

- Append en tabla "Sesiones con Claude":
  ```
  | YYYY-MM-DD | <ejercicios/temas trabajados, breve> | <qué quedó claro, qué quedó pendiente> |
  ```
- Si hay nuevos conceptos "entendidos" → mover/agregar a "Entiendo".
- Si hay nuevas dudas → agregar a "Tengo dudas".
- Actualizar `updated:` en el frontmatter.

### 2. Actualizar `bloom:` de páginas wiki tocadas

Para cada página wiki cuyo tema fue trabajado en la sesión:

- Si el estudiante demostró un nivel mayor que el `bloom:` registrado → subir el campo.
- Si demostró un nivel menor (ej: resolvió con guía intensa lo que antes resolvía solo) → bajar.
- Si no hubo evidencia clara → no tocar.

**Criterios de nivel** (ver tabla en `CLAUDE.md`):
- 1 (Inicial): reconoce el concepto, no lo aplica solo.
- 2 (Comprensión): explica con sus palabras.
- 3 (Aplicación): resuelve ejercicios tipo con guía.
- 4 (Análisis): identifica qué herramienta usar sin que se lo digan.
- 5 (Síntesis): combina conceptos para resolver problemas nuevos.
- 6 (Evaluación): puede enseñarlo y detectar errores en soluciones ajenas.

Actualizar `updated:` en cada página wiki tocada.

### 3. Append a `wiki/log.md`

Una entrada por sesión:

```markdown
## [YYYY-MM-DD] practice | <T>

- Materia: <slug>
- Páginas wiki tocadas: [[slug-1]] (bloom 2→3), [[slug-2]] (sin cambio)
- Pendiente: <breve>
```

### 4. Resumen al usuario

Una línea final: "Sesión registrada en `subjects/<materia>/index.md` y `wiki/log.md`. Bloom actualizado: ⟨lista⟩."

---

## Notas de portabilidad

El firewall se expresa como invariante sobre **qué archivos puede leer el agente**, no como instrucción de comportamiento. Cualquier implementación (UI propia, otro modelo) puede aplicarlo: parsear los slugs prohibidos al inicio, filtrar el filesystem accesible al modelo, o validar post-hoc que ningún tool call los tocó.

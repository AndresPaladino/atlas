---
type: schema
updated: 2026-07-17
---

# Protocolo: modo `/learn`

Lección expositiva sobre un tema: el agente enseña activamente, con estructura y con ritmo controlado por el usuario. Complementa a `/query` (respuesta puntual a una pregunta) y a `/practice` (Socrático: nunca explica). Acá el agente sí desarrolla el tema completo.

Formato de salida (matemática incluida): seguir `schema/output-conventions.md` — mate en `$…$` / `$$…$$`, nunca `\(…\)`.

Sin estado: el modo no registra progreso entre sesiones ni muta el wiki. No hay commit al cierre.

---

## Apertura

1. Identificar tema **T**, en orden de prioridad:
   1. Argumento explícito al comando: `/learn teorema de Green` → T = "teorema de Green".
   2. Inferencia del primer mensaje del usuario.
   3. Pregunta al usuario: "¿qué tema querés aprender?".
2. Leer `wiki/index.md` y localizar páginas sobre T (título / alias / tags). Si T es un área entera, incluir `wiki/areas/<area>.md`.
3. Evaluar cobertura:
   - **Hay páginas de T** → leer 3 a 8 relevantes (como `/query`; más diluye). Si un claim necesita precisión de enunciado, confirmar contra `wiki/sources/<source-slug>.md`.
   - **No hay nada, o solo stubs** → avisar antes de arrancar: "el wiki no cubre esto (o apenas). ¿Doy la lección desde conocimiento general (sin citas) o hacés `/ingest` de una fuente primero?" y esperar decisión.
4. **Prerequisitos — solo mencionar.** Listar los `requires:` de las páginas de T al abrir: "esto asume que manejás [[a]] y [[b]]". No verificar ni gatear el avance; el usuario decide si los repasa (puede pedir `/learn` del prerequisito y volver).

---

## La lección

Arco default — **adaptable al tema** (un método pide otro arco que un teorema; un concepto puro puede no tener "cuándo falla"):

1. **Motivación** — qué problema resuelve, por qué existe.
2. **Idea central** — la intuición en lenguaje llano. Ejemplo concreto antes de la abstracción (preferencia global del sistema).
3. **Formalización** — definiciones y enunciados precisos, con citas.
4. **Ejemplos trabajados** — al menos uno completo.
5. **Conexiones y limitaciones** — dónde engancha con el grafo (`unlocks`, comparaciones), cuándo no aplica o falla.

Reglas de exposición:

- `[[wikilinks]]` inline al mencionar cualquier entidad con página propia.
- Citar fuentes en claims fuertes: `[[apostol-vol2-ch13]] §13.4 p. 376`.
- Si la lección (o una parte) sale de conocimiento general sin respaldo en el wiki, marcarlo explícitamente: "(síntesis propia, sin fuente en el wiki)".
- No copiar enunciados textuales de las fuentes; parafrasear con cita.
- La lección **puede** desarrollar contenido que ya está en páginas wiki — ese es el punto del modo —, pero debe ser consistente con ellas y citarlas. Si contradice una página, señalarlo como posible error a revisar con `/lint` o `/query`.

---

## Ritmo — por bloques, con check de recuperación

- Dividir la lección en **2 a 4 bloques**, en los cortes naturales del arco.
- Al final de cada bloque, **parar** y cerrar con un **check de recuperación**: una pregunta que pida reconstruir de memoria lo central del bloque recién visto. Recuperación, no comprensión: "enunciá la condición del teorema con tus palabras", "¿cuál era el paso clave del ejemplo?" — nunca "¿se entendió?" ni "¿alguna duda?".
- Evaluar la respuesta en una línea (correcto / qué faltó) y recién ahí ofrecer el avance: "Siguiente: ⟨qué viene⟩. ¿Sigo?".
- **El check es salteable**: si el usuario responde "seguí" directo, avanzar sin insistir. El control del ritmo sigue siendo suyo.
- **No escalar a Socrático**: si la respuesta está mal o incompleta, dar la corrección directa y seguir — esto es `/learn`, no `/practice`. El retrieval fuerte viene después, en el handoff.
- Preguntas intra-lección se responden en el momento, dentro del hilo del bloque. Si la pregunta se va del tema, responder breve y ofrecer retomarla en `/query` al final.

---

## Cierre — handoff a `/practice`

Disparado por: fin del último bloque, o el usuario dice "listo", "basta", "hasta acá".

1. Cierre de una línea: mini-mapa de lo visto (los `[[wikilinks]]` tocados en la lección).
2. Ofrecer el handoff:
   > "¿Ejercitamos esto? `/practice ⟨T⟩` arma el firewall sobre lo que acabamos de ver y saco ejercicios de `wiki/assessments/`."
   Si acepta → activar `/practice` normalmente (protocolo aparte). Que el firewall bloquee justo las páginas de la lección es **deliberado**: en práctica se recuerda, no se relee.
3. Si la lección se dio sin respaldo del wiki: sugerir `/ingest` de una fuente real para consolidar el tema en el grafo — antes o además de practicar.

---

## Reglas de calidad

- **No alucinar citas**: si una afirmación no está respaldada por una fuente listada en el wiki o por una página existente, marcarla como "(síntesis propia, sin fuente confirmada)".
- **No abrumar**: la lección cubre T, no toda su área. Lo adyacente se apunta con `[[wikilink]]` y se deja para otro `/learn`.

---

## Notas de portabilidad

El protocolo es lectura + exposición con LLM: sin escritura, sin estado persistente. `atlas session mode learn` solo marca el modo en `.atlas/session.json` (cualquier modo ≠ practice levanta el firewall); no arma bloqueos. Cualquier agente con file-IO puede implementarlo filtrando nada: el modo es deliberadamente abierto.

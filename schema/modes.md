---
type: schema
updated: 2026-07-17
---

# Modos de Atlas

Atlas opera en **5 modos** explícitos. Cada modo carga un protocolo distinto desde `schema/`. Este archivo es el dispatcher: define qué modo se activa, cómo se cambia, y la regla del firewall.

---

## Los 5 modos

| Modo | Comando | Protocolo | Propósito |
|---|---|---|---|
| Ingest | `/ingest [ruta]` | `schema/ingest-protocol.md` | Leer fuente cruda → poblar/actualizar wiki |
| Query | `/query <pregunta>` | `schema/query-protocol.md` | Responder pregunta consultando wiki; opcional file-back |
| Learn | `/learn [tema]` | `schema/learn-protocol.md` | Lección expositiva por bloques con checks de recuperación; handoff a `/practice` |
| Practice | `/practice [tema]` | `schema/practice-protocol.md` | Sesión Socrática estricta; firewall sobre wiki |
| Lint | `/lint [scope]` | `schema/lint-protocol.md` | Auditar consistencia del wiki |

---

## Modo default (sin slash command)

Si la sesión arranca sin slash command, el agente debe elegir modo a partir del primer mensaje del usuario, aplicando esta heurística:

1. **El mensaje describe un ejercicio o ejercita un tema** → activar `/practice`.
   - Señales: "ejercicio N", "práctico N", "tengo que resolver", "ayudame con (problema)", "está bien si...", "no me sale", "estoy trabado", presencia de enunciado de ejercicio textual.
2. **El mensaje pide una explicación o definición** → activar `/query`.
   - Señales: "explicame", "qué es", "cómo funciona", "diferencia entre X e Y", "para qué sirve", pregunta directa sobre un concepto.
3. **El mensaje pide aprender un tema completo** → activar `/learn`.
   - Señales: "enseñame", "quiero aprender", "dame una clase/lección de", "arranquemos X de cero", "no sé nada de X".
   - Distinción con `/query`: query responde una pregunta puntual y acotada; learn cubre un tema entero con lección estructurada.
4. **El mensaje pide cargar una fuente** → activar `/ingest`.
   - Señales: "subí estas notas", "ingerí este PDF", "leé este apunte", mención explícita de un archivo en `raw/` o `extracted/`.
5. **Ambigüedad** → falla cerrada hacia `/practice`. El modo Socrático es la opción segura: nunca filtra solución; siempre se puede salir explícitamente.

El agente debe **anunciar el modo activado** en su primera respuesta: `"[modo: practice]"` al inicio de la respuesta. Esto es observable y verificable.

---

## Cambio de modo intra-sesión

El usuario puede cambiar de modo en cualquier momento mediante:

- **Slash command explícito**: `/query`, `/learn`, `/practice`, `/ingest`, `/lint`. Es la forma canónica.
- **`/reveal`** — válvula especial (no cambia de modo): permite una lectura puntual bloqueada por el firewall de `/practice`, sin salir de la sesión Socrática. Se re-arma solo después.
- **Frase de salida**:
  - `"salí del modo práctica"`, `"basta de Socrático"`, `"explicame directo"` → cambia a `/query`.
  - `"enseñame X"`, `"quiero aprender X"`, `"dame una clase de X"` → cambia a `/learn`.
  - `"volvé al modo práctica"`, `"hagamos un ejercicio"` → cambia a `/practice`.
  - `"vamos a cargar una fuente"`, `"ingerimos un PDF"` → cambia a `/ingest`.

El agente debe **anunciar el cambio**: `"[modo: query]"` cuando el cambio se efectúa.

---

## El firewall — invariante estructural

Durante una sesión `/practice` sobre tema **T**, el agente no puede leer las
páginas wiki sobre T (ni su vecindario en el grafo) ni `raw/` ni `extracted/`. No es honor system:
está **enforced por un hook `PreToolUse`** que lee el estado de sesión
(`.atlas/session.json`, fijado con `atlas session set "<T>"`) y deniega los `Read`
bloqueados. Válvula de escape deliberada: `/reveal` (lectura puntual, logueada) o
un cambio de modo explícito (`/query`, `/learn`), que lo levanta.

Definición completa, vecindario del grafo y rationale: `schema/practice-protocol.md`.

---

## Cómo se compone una sesión

```
Inicio de sesión
    ↓
Lectura automática de CLAUDE.md (router) → carga este archivo
    ↓
Primer mensaje del usuario
    ↓
¿Hay slash command? ──sí──→ activar modo correspondiente; leer schema/<modo>-protocol.md
    │
    no
    ↓
Aplicar heurística default (sección "Modo default")
    ↓
Anunciar modo: "[modo: X]"
    ↓
Cargar schema/X-protocol.md y aplicarlo
    ↓
... interacción ...
    ↓
¿Cambio de modo? ──sí──→ anunciar nuevo modo; cargar nuevo protocolo
    │
    no
    ↓
Cierre de sesión (rutina del modo activo en ese momento)
```

---

## Notas de portabilidad

Este archivo describe el dispatcher en lenguaje neutral. Una implementación alternativa (UI propia, otro agente) puede aplicar las mismas reglas: parsear el primer mensaje contra la heurística, cargar el protocolo como system prompt, y aplicar el firewall como filtro estático sobre el contenido accesible.

---
type: schema
updated: 2026-06-09
---

# Convenciones de salida

Contrato de formato para las respuestas de Atlas (modos `/query` y `/practice`).
El objetivo es que la matemática se renderice correctamente en la **superficie
canónica de lectura**: un cliente de Claude Code que renderiza KaTeX (app
desktop, web `claude.ai/code`, o extensión de IDE como VS Code + KaTeX-for-Claude).

## Matemática

- **Inline**: `$ … $`. Ejemplo: la derivada es $\frac{df}{dx}$.
- **Bloque**: `$$ … $$` en su propia línea. Ejemplo:
  $$\int_a^b f(x)\,dx = F(b) - F(a)$$
- **No usar** `\( … \)` ni `\[ … \]`: varios renderers (incluido KaTeX por
  defecto) no los reconocen. Tampoco usar bloques de código para ecuaciones.
- Comandos LaTeX estándar de KaTeX: `\frac`, `\int`, `\sum`, `\sqrt`, `\vec`,
  `\partial`, `\nabla`, matrices con `\begin{bmatrix}…\end{bmatrix}`, etc.
- Para variables o símbolos sueltos en medio de prosa, igual usar `$x$`, `$\theta$`
  — no Unicode crudo — para mantener consistencia de render.

## Terminal cruda

Si el usuario lee desde una terminal sin render (no recomendado), la mate sale
como LaTeX literal. Claude Code no expone un hook que reescriba el texto que
muestra, así que no hay render vivo en la terminal. Como paliativo hay un
**filtro standalone** (`atlas render`, ver `tools/README.md`) que convierte
LaTeX→Unicode best-effort sobre texto ya guardado (p.ej. una respuesta archivada
al wiki). La recomendación sigue siendo leer en un cliente con render.

## Notación del wiki

Las páginas del wiki siguen `schema/wiki-conventions.md`. Las mismas reglas de
delimitadores de mate aplican ahí: Obsidian renderiza `$…$` / `$$…$$` con MathJax.

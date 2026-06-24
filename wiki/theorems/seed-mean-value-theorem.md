---
type: theorem
title: "Teorema del valor medio"
aliases: ["mean value theorem", "MVT", "TVM", "teorema de Lagrange", "teorema del valor medio de Lagrange"]
areas: [math]
tags: [calculus/single-variable, examples/seed]
requires: ["[[seed-derivative]]"]
unlocks: []
statement_form: "Si f es continua en [a,b] y derivable en (a,b), entonces existe c en (a,b) tal que f'(c) = (f(b)-f(a))/(b-a)."
sources: []
assessed_by: []
created: 2026-06-23
updated: 2026-06-23
---

# Teorema del valor medio

> Página semilla del template Atlas (contenido de dominio público, autocontenida).
> Sirve para probar `/query` sin ingestar nada. Borrala cuando tengas tu propio wiki.

## Enunciado formal

**Hipótesis:**
- $f$ es continua en el intervalo cerrado $[a,b]$,
- $f$ es derivable en el intervalo abierto $(a,b)$.

**Conclusión:** existe al menos un punto $c \in (a,b)$ tal que

$$f'(c) = \frac{f(b) - f(a)}{b - a}.$$

## Interpretación

El lado derecho es la pendiente de la recta secante que une los extremos $(a, f(a))$ y $(b, f(b))$. El teorema afirma que en algún punto interior la recta tangente tiene **exactamente esa misma pendiente**: hay un instante donde la velocidad instantánea iguala a la velocidad promedio.

## Por qué importan las hipótesis

- Sin continuidad en los extremos, el resultado puede fallar (un salto en $a$ o $b$ rompe la secante).
- Sin derivabilidad en el interior, no hay $f'(c)$ que invocar: $f(x)=|x|$ en $[-1,1]$ tiene velocidad promedio $0$, pero no existe $c$ con $f'(c)=0$ porque $f$ no es derivable en $0$.

El **teorema de Rolle** es el caso particular $f(a)=f(b)$, donde la conclusión es $f'(c)=0$.

## Conexiones

- Requiere: [[seed-derivative]]
- Ejemplo: [[seed-mvt-application]]

---
type: concept
title: "Integral de línea"
aliases: ["line integral", "integral curvilínea", "integral de camino"]
areas: [math]
tags: [calculus/vector, integration, curves]
requires: ["[[curve-parametrization]]", "[[arc-length]]"]
unlocks: ["[[gradient-field]]", "[[greens-theorem]]"]
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

### De un campo escalar

Sea $f: U \subset \mathbb{R}^n \to \mathbb{R}$ continuo y $\alpha: [a,b] \to U$ parametrización de $C$. La integral de línea de $f$ sobre $C$ es [[gonzalez-cvec-2023]] §2.2.1 p. 52:

$$\int_C f\, \mathrm{d}s = \int_a^b f(\alpha(t))\, \|\alpha'(t)\|\, \mathrm{d}t.$$

Interpretación: si $f$ es densidad lineal, $\int_C f\,\mathrm{d}s$ es la masa total del cable $C$.

### De un campo vectorial

Sea $X: U \to \mathbb{R}^n$ continuo. La integral de línea de $X$ sobre $C$ (orientada por $\alpha$) es [[gonzalez-cvec-2023]] §2.2.2 p. 54:

$$\int_C X \cdot \mathrm{d}s = \int_a^b X(\alpha(t)) \cdot \alpha'(t)\, \mathrm{d}t.$$

Notación clásica para $X = (P, Q, R)$: $\int_C P\,\mathrm{d}x + Q\,\mathrm{d}y + R\,\mathrm{d}z$.

Interpretación: si $X$ es un campo de fuerzas, $\int_C X \cdot \mathrm{d}s$ es el trabajo a lo largo de $C$.

## Propiedades clave

- **Linealidad** y **aditividad** respecto a la curva.
- **Independencia de parametrización** (para la integral escalar).
- **Cambio de orientación**: $\int_{C^{op}} X \cdot \mathrm{d}s = -\int_C X \cdot \mathrm{d}s$.

## Conexiones

- Requiere: [[curve-parametrization]], [[arc-length]]
- Habilita: [[gradient-field]], [[greens-theorem]]
- Relacionado: [[surface-integral]] (análogo sobre superficies)

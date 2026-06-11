---
type: concept
title: "Condition Number"
aliases: ["número de condición", "κ(A)", "condition number"]
areas: [linear-algebra, numerical-analysis]
tags: [linear-algebra/numerical, numerical-analysis]
requires: ["[[singular-values]]"]
unlocks: []
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

El **número de condición** de una matriz $\mathbf{A}$ es

$$\kappa(\mathbf{A}) = \frac{\sigma_{\max}(\mathbf{A})}{\sigma_{\min}(\mathbf{A})},$$

el cociente entre el mayor y el menor [[singular-values|valor singular]] no nulo [[brunton-kutz-ch1]] §1.4 p. 48.

## Intuición

El número de condición mide cuánto puede amplificarse el **error relativo** al resolver $\mathbf{A}\mathbf{x} = \mathbf{b}$. Si $\mathbf{x}$ tiene un error $\boldsymbol{\epsilon}_x$ y $\mathbf{b}$ tiene un error $\boldsymbol{\epsilon}_b$, en el peor caso:

$$\frac{\|\mathbf{b}\|}{\|\boldsymbol{\epsilon}_b\|} = \frac{\|\mathbf{x}\|}{\|\boldsymbol{\epsilon}_x\|} \cdot \frac{\sigma_{\min}}{\sigma_{\max}}.$$

La relación señal-ruido de la salida se reduce por un factor $\kappa(\mathbf{A})$ respecto a la entrada [[brunton-kutz-ch1]] §1.4 p. 48.

- $\kappa \approx 1$: matriz bien condicionada, errores pequeños no se amplifican.
- $\kappa \gg 1$: matriz mal condicionada (casi singular), errores pequeños en $\mathbf{b}$ producen errores grandes en $\mathbf{x}$.
- $\kappa = \infty$: matriz singular.

## Mitigación

Truncar la SVD agresivamente (ignorar valores singulares muy pequeños) aumenta el $\sigma_{\min}$ efectivo y reduce $\kappa$, a costa de usar un subespacio $\tilde{\mathbf{U}}$ más pequeño.

## Conexiones

- Requiere: [[singular-values]]
- Relacionado: [[pseudo-inverse]], [[least-squares-regression]], [[spectral-norm]]

## Fuentes

- [[brunton-kutz-ch1]] §1.4 pp. 48–49

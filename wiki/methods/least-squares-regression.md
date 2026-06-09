---
type: method
title: "Least-Squares Regression (via SVD)"
aliases: ["mínimos cuadrados", "least squares", "regresión por mínimos cuadrados", "linear regression SVD"]
when_to_use: "Resolver Ax = b cuando el sistema es sobre-determinado (n ≫ m, más ecuaciones que incógnitas) buscando la solución de mínimo error ‖Ax − b‖₂, o sub-determinado (n ≪ m) buscando la solución de mínima norma ‖x‖₂ con Ax = b."
fails_when: "El sistema tiene un número de condición enorme (κ(A) ≫ 1): la solución puede ser numéricamente inestable. En ese caso conviene truncar la SVD más agresivamente."
areas: [linear-algebra, statistics, data-science]
tags: [linear-algebra/linear-systems, statistics/regression]
requires: ["[[pseudo-inverse]]", "[[four-fundamental-subspaces]]"]
unlocks: []
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Cuándo usarlo

Para resolver $\mathbf{A}\mathbf{x} = \mathbf{b}$ cuando:
- Sistema **sobre-determinado** ($n \gg m$): no existe solución exacta, se minimiza $\|\mathbf{A}\mathbf{x} - \mathbf{b}\|_2^2$.
- Sistema **sub-determinado** ($n \ll m$): hay infinitas soluciones, se elige la de mínima norma $\|\mathbf{x}\|_2$.

## Procedimiento

1. Computar la SVD (economy): $\mathbf{A} = \tilde{\mathbf{U}}\tilde{\boldsymbol{\Sigma}}\tilde{\mathbf{V}}^*$.
2. Aplicar la [[pseudo-inverse|pseudo-inversa]]:

$$\tilde{\mathbf{x}} = \mathbf{A}^\dagger\mathbf{b} = \tilde{\mathbf{V}}\tilde{\boldsymbol{\Sigma}}^{-1}\tilde{\mathbf{U}}^*\mathbf{b}.$$

Esto es equivalente a `pinv(A)*b` en MATLAB o `np.linalg.pinv(A) @ b` en Python [[brunton-kutz-ch1]] §1.4 p. 47.

## Regresión lineal 1D

Para $\mathbf{b} = \mathbf{a} x$ (determinar la pendiente $x$):

$$x = \frac{\mathbf{a}^*\mathbf{b}}{\|\mathbf{a}\|_2^2},$$

que es el producto punto de $\mathbf{b}$ con la dirección normalizada $\mathbf{a}$ [[brunton-kutz-ch1]] §1.4 p. 49.

## Regresión multilineal

Para $\mathbf{A} \in \mathbb{R}^{n \times m}$ con múltiples predictores (ej. precios inmobiliarios con 13 atributos), el procedimiento SVD es idéntico; solo cambia el tamaño de $\mathbf{A}$.

## Cuándo falla

Cuando $\kappa(\mathbf{A}) = \sigma_\mathrm{max}/\sigma_\mathrm{min} \gg 1$: la solución amplifica el ruido en $\mathbf{b}$. Solución: truncar la SVD para aumentar $\sigma_\mathrm{min}$ efectivo (ver [[condition-number]]).

## Conexiones

- Requiere: [[pseudo-inverse]], [[four-fundamental-subspaces]]
- Relacionado: [[condition-number]], [[singular-value-decomposition]]

## Fuentes

- [[brunton-kutz-ch1]] §1.4 pp. 49–53

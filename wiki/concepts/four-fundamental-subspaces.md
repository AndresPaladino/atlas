---
type: concept
title: "Four Fundamental Subspaces"
aliases: ["cuatro subespacios fundamentales", "column space", "null space", "row space", "kernel", "espacio columna", "espacio nulo", "espacio fila"]
areas: [linear-algebra]
tags: [linear-algebra/subspaces]
requires: ["[[singular-value-decomposition]]"]
unlocks: ["[[pseudo-inverse]]", "[[least-squares-regression]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Para una matriz $\mathbf{A} = \tilde{\mathbf{U}}\tilde{\boldsymbol{\Sigma}}\tilde{\mathbf{V}}^*$ de rango $r$, la [[singular-value-decomposition|SVD]] revela los cuatro subespacios fundamentales [[brunton-kutz-ch1]] §1.4 p. 46:

| Subespacio | Definición | Spanneado por |
|---|---|---|
| $\mathrm{col}(\mathbf{A})$ | span de columnas, también llamado *range* | columnas de $\tilde{\mathbf{U}}$ |
| $\ker(\mathbf{A}^*)$ | complemento ortogonal de $\mathrm{col}(\mathbf{A})$ | columnas de $\hat{\mathbf{U}}^\perp$ |
| $\mathrm{row}(\mathbf{A}) = \mathrm{col}(\mathbf{A}^*)$ | span de filas | columnas de $\tilde{\mathbf{V}}$ |
| $\ker(\mathbf{A})$ | *null space*: vectores que $\mathbf{A}$ lleva a $\mathbf{0}$ | columnas de $\hat{\mathbf{V}}^\perp$ |

Se satisfacen las descomposiciones directas:
$$\mathrm{col}(\mathbf{A}) \oplus \ker(\mathbf{A}^*) = \mathbb{R}^n, \qquad \mathrm{col}(\mathbf{A}^*) \oplus \ker(\mathbf{A}) = \mathbb{R}^m.$$

## Intuición

Los cuatro subespacios determinan la **geometría de solubilidad** del sistema $\mathbf{A}\mathbf{x} = \mathbf{b}$:
- Si $\mathbf{b} \in \mathrm{col}(\mathbf{A})$ y $\ker(\mathbf{A}) = \{0\}$: solución única.
- Si $\mathbf{b} \in \mathrm{col}(\mathbf{A})$ y $\dim(\ker(\mathbf{A})) > 0$: infinitas soluciones (sistema sub-determinado).
- Si $\mathbf{b} \notin \mathrm{col}(\mathbf{A})$: no hay solución exacta (sistema sobre-determinado → usar [[least-squares-regression|mínimos cuadrados]]).

## Conexiones

- Requiere: [[singular-value-decomposition]]
- Habilita: [[pseudo-inverse]], [[least-squares-regression]]

## Fuentes

- [[brunton-kutz-ch1]] §1.4 pp. 46–48

---
type: concept
title: "Pseudo-Inverse (Moore-Penrose)"
aliases: ["pseudo-inversa", "Moore-Penrose pseudo-inverse", "A†", "pinv"]
areas: [linear-algebra]
tags: [linear-algebra/matrix-decomposition, linear-algebra/linear-systems]
requires: ["[[singular-value-decomposition]]", "[[four-fundamental-subspaces]]", "[[unitary-matrix]]"]
unlocks: ["[[least-squares-regression]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

La **pseudo-inversa izquierda de Moore-Penrose** de una matriz $\mathbf{A}$ con SVD truncada $\mathbf{A} = \tilde{\mathbf{U}}\tilde{\boldsymbol{\Sigma}}\tilde{\mathbf{V}}^*$ se define como [[brunton-kutz-ch1]] §1.4 p. 47:

$$\mathbf{A}^\dagger \triangleq \tilde{\mathbf{V}}\tilde{\boldsymbol{\Sigma}}^{-1}\tilde{\mathbf{U}}^*, \quad \text{de modo que} \quad \mathbf{A}^\dagger\mathbf{A} = \tilde{\mathbf{V}}\tilde{\mathbf{V}}^*.$$

Note que $\mathbf{A}^\dagger\mathbf{A} = \mathbf{I}_{m \times m}$ solo si la SVD truncada captura todos los valores singulares no nulos (es decir, si el rango es $m$).

## Intuición

La pseudo-inversa "invierte" $\mathbf{A}$ en la medida de lo posible: proyecta $\mathbf{b}$ al espacio columna de $\tilde{\mathbf{U}}$ y luego aplica la inversa en ese subespacio. Esto da la solución $\tilde{\mathbf{x}} = \mathbf{A}^\dagger\mathbf{b}$, que es simultáneamente:
- la solución de **mínimos cuadrados** cuando el sistema es sobre-determinado ($n \gg m$), y
- la solución de **mínima norma** cuando el sistema es sub-determinado ($n \ll m$).

## Error conceptual común

$\tilde{\mathbf{U}}\tilde{\mathbf{U}}^*$ **no es la identidad** para una SVD truncada (solo $\tilde{\mathbf{U}}^*\tilde{\mathbf{U}} = \mathbf{I}_{r \times r}$). $\tilde{\mathbf{U}}\tilde{\mathbf{U}}^*$ es una proyección sobre $\mathrm{col}(\tilde{\mathbf{U}})$ [[brunton-kutz-ch1]] §1.4 p. 48.

## Costo computacional

Invertir $\tilde{\mathbf{U}}$ y $\tilde{\mathbf{V}}$ (matrices unitarias) requiere solo $\mathcal{O}(n^2)$ operaciones (transponer). Invertir $\tilde{\boldsymbol{\Sigma}}$ (diagonal) requiere $\mathcal{O}(r)$. Mucho más barato que invertir una matriz densa: $\mathcal{O}(n^3)$.

## Conexiones

- Requiere: [[singular-value-decomposition]], [[four-fundamental-subspaces]], [[unitary-matrix]]
- Habilita: [[least-squares-regression]]
- Relacionado: [[condition-number]]

## Fuentes

- [[brunton-kutz-ch1]] §1.4 pp. 47–49

---
type: method
title: "Method of Snapshots"
aliases: ["método de snapshots", "Sirovich method", "método de Sirovich"]
when_to_use: "Cuando n ≫ m: calcular los vectores singulares izquierdos U de X a través de la eigendescomposición de X*X (tamaño m×m) en lugar de XX* (tamaño n×n, intratable)."
fails_when: "Cuando m también es grande, el beneficio computacional desaparece. Tampoco aplica si se necesita la SVD completa (todos los valores singulares)."
areas: [linear-algebra, data-science, numerical-analysis]
tags: [linear-algebra/matrix-decomposition, numerical-analysis/algorithms]
requires: ["[[singular-value-decomposition]]"]
unlocks: []
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Cuándo usarlo

Cuando $n \gg m$ (matriz tall-skinny): calcular $\mathbf{X}\mathbf{X}^*$ requiere almacenar una matriz $n \times n$ (potencialmente con billones de entradas), mientras que $\mathbf{X}^*\mathbf{X}$ es solo $m \times m$ [[brunton-kutz-ch1]] §1.3 p. 41.

## Procedimiento

1. Calcular $\mathbf{X}^*\mathbf{X} \in \mathbb{C}^{m \times m}$.
2. Resolver la eigendescomposición: $\mathbf{X}^*\mathbf{X}\mathbf{V} = \mathbf{V}\hat{\boldsymbol{\Sigma}}^2$.
3. Recuperar los primeros $r$ vectores singulares izquierdos:

$$\tilde{\mathbf{U}} = \mathbf{X}\tilde{\mathbf{V}}\tilde{\boldsymbol{\Sigma}}^{-1}.$$

Esto fue introducido por Sirovich en 1987 en el contexto de simulaciones de fluidos [[brunton-kutz-ch1]] §1.3 p. 41.

## Cuándo falla

- Si la magnitud del ruido hace que los valores singulares cercanos a cero sean inestables, $\tilde{\boldsymbol{\Sigma}}^{-1}$ amplifica ese ruido al calcular $\tilde{\mathbf{U}}$.
- No aplica directamente si $m$ también es grande (usar entonces [[randomized-svd|rSVD]]).

## Conexiones

- Requiere: [[singular-value-decomposition]]
- Relacionado: [[principal-component-analysis]], [[randomized-svd]]

## Fuentes

- [[brunton-kutz-ch1]] §1.3 pp. 41–42

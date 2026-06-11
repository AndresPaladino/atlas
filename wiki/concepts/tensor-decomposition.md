---
type: concept
title: "Tensor Decomposition (CP/PARAFAC)"
aliases: ["descomposición tensorial", "CP decomposition", "CANDECOMP", "PARAFAC", "N-way decomposition"]
areas: [linear-algebra, data-science]
tags: [linear-algebra/matrix-decomposition, data-science/multiway]
requires: ["[[singular-value-decomposition]]", "[[low-rank-approximation]]"]
unlocks: []
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

La descomposición **CP (CANDECOMP/PARAFAC)** generaliza la [[singular-value-decomposition|SVD]] a tensores $\mathcal{M}$ de $N$ modos. Para un tensor de tres modos (dos espaciales + tiempo):

$$\mathcal{M} = \sum_{r=1}^{R} \lambda_r \, \mathbf{A}_r \circ \mathbf{B}_r \circ \mathbf{C}_r,$$

donde $\circ$ denota el producto externo, $\mathbf{A}_r$, $\mathbf{B}_r$, $\mathbf{C}_r$ son los factores espaciotemporales del $r$-ésimo componente, y $\lambda_r$ son los pesos [[brunton-kutz-ch1]] §1.9 p. 81.

## Intuición

La [[singular-value-decomposition|SVD]] requiere "aplanar" (vectorizar) los datos en una matriz, lo que destruye las correlaciones multidimensionales naturales. La descomposición tensorial mantiene la estructura original del array y extrae modos de variación en cada dirección independientemente.

**Analogía con SVD:** así como la SVD descompone $\mathbf{X}$ como suma de matrices rango-1 $\sigma_k \mathbf{u}_k \mathbf{v}_k^T$, la CP descompone $\mathcal{M}$ como suma de tensores rango-1 $\lambda_r \mathbf{A}_r \circ \mathbf{B}_r \circ \mathbf{C}_r$.

## Limitaciones

- Para $N$ grande, la CP puede ser computacionalmente intratable (NP-hard en general).
- Métodos aleatorizados están extendiendo la viabilidad a tensores grandes.

## Conexiones

- Requiere: [[singular-value-decomposition]], [[low-rank-approximation]]

## Fuentes

- [[brunton-kutz-ch1]] §1.9 pp. 81–85

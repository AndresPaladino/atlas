---
type: concept
title: "Singular Value Decomposition (SVD)"
aliases: ["SVD", "descomposición en valores singulares"]
areas: [linear-algebra, data-science]
tags: [linear-algebra/matrix-decomposition]
requires: ["[[unitary-matrix]]", "[[singular-values]]"]
unlocks: ["[[low-rank-approximation]]", "[[pseudo-inverse]]", "[[principal-component-analysis]]", "[[four-fundamental-subspaces]]", "[[method-of-snapshots]]", "[[randomized-svd]]"]
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Toda matriz $\mathbf{X} \in \mathbb{C}^{n \times m}$ admite una descomposición única de la forma

$$\mathbf{X} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^*,$$

donde $\mathbf{U} \in \mathbb{C}^{n \times n}$ y $\mathbf{V} \in \mathbb{C}^{m \times m}$ son matrices [[unitary-matrix|unitarias]], y $\boldsymbol{\Sigma} \in \mathbb{R}^{n \times m}$ es diagonal con entradas no negativas ([[singular-values|valores singulares]]) ordenadas $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_m \geq 0$ [[brunton-kutz-ch1]] §1.1 p. 31.

Las columnas de $\mathbf{U}$ se llaman **vectores singulares izquierdos** (left singular vectors) y las de $\mathbf{V}$ son los **vectores singulares derechos** (right singular vectors).

## Intuición

La SVD descompone cualquier transformación lineal $\mathbf{X}$ como: rotar el espacio de entrada ($\mathbf{V}^*$), escalar a lo largo de los ejes ($\boldsymbol{\Sigma}$), y rotar el espacio de salida ($\mathbf{U}$). Geométricamente: una hiperesfera unitaria en $\mathbb{R}^m$ se mapea mediante $\mathbf{X}$ a un elipsoide en $\mathbb{R}^n$; los valores singulares son las longitudes de los semiejes.

Dado que $\boldsymbol{\Sigma}$ es diagonal, $\mathbf{X}$ puede expandirse como suma de matrices rango-1:

$$\mathbf{X} = \sum_{k=1}^{m} \sigma_k \mathbf{u}_k \mathbf{v}_k^*,$$

donde $\mathbf{u}_k$ y $\mathbf{v}_k$ son la $k$-ésima columna de $\mathbf{U}$ y $\mathbf{V}$. Esto se llama **dyadic summation** o expansión en productos externos.

## SVD economy (reducida)

Cuando $n \geq m$, $\boldsymbol{\Sigma}$ tiene a lo sumo $m$ valores no nulos. La **economy SVD** elimina las filas cero:

$$\mathbf{X} = \hat{\mathbf{U}} \hat{\boldsymbol{\Sigma}} \mathbf{V}^*, \quad \hat{\mathbf{U}} \in \mathbb{C}^{n \times m},\; \hat{\boldsymbol{\Sigma}} \in \mathbb{R}^{m \times m}.$$

## Relación con la eigendescomposición

La SVD generaliza la eigendescomposición a matrices no cuadradas. Las columnas de $\mathbf{U}$ son eigenvectores de $\mathbf{X}\mathbf{X}^*$ y las de $\mathbf{V}$ son eigenvectores de $\mathbf{X}^*\mathbf{X}$. Cada valor singular $\sigma_k$ es la raíz cuadrada positiva del eigenvalor correspondiente [[brunton-kutz-ch1]] §1.3 p. 41.

## Conexiones

- Requiere: [[unitary-matrix]], [[singular-values]]
- Habilita: [[low-rank-approximation]], [[pseudo-inverse]], [[principal-component-analysis]], [[four-fundamental-subspaces]], [[method-of-snapshots]], [[randomized-svd]]
- Relacionado: [[eckart-young-theorem]], [[condition-number]]

## Fuentes

- [[brunton-kutz-ch1]] §1.1 pp. 31–34

---
type: concept
title: "Principal Component Analysis (PCA)"
aliases: ["PCA", "análisis de componentes principales", "principal components"]
areas: [linear-algebra, statistics, data-science]
tags: [data-science/dimensionality-reduction, statistics/multivariate]
requires: ["[[singular-value-decomposition]]", "[[covariance-matrix]]"]
unlocks: []
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

**PCA** es la aplicación de la [[singular-value-decomposition|SVD]] a datos con la media substraída. Dado un conjunto de datos $\mathbf{X} \in \mathbb{R}^{n \times m}$ (filas = observaciones, columnas = variables):

1. Calcular la media por columna: $\bar{x}_j = \frac{1}{n}\sum_{i=1}^n X_{ij}$.
2. Substraer la media: $\mathbf{B} = \mathbf{X} - \bar{\mathbf{X}}$.
3. Computar la SVD: $\mathbf{B} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^*$.

Las columnas de $\mathbf{V}$ son los **componentes principales** (PCs) [[brunton-kutz-ch1]] §1.5 p. 55. Son los eigenvectores de la [[covariance-matrix|matriz de covarianza]] $\mathbf{C} = \frac{1}{n-1}\mathbf{B}^*\mathbf{B}$.

## Intuición

PCA encuentra una nueva base de coordenadas en la cual:
- Las variables son **linealmente no correlacionadas** (la covarianza es diagonal en las coordenadas PC).
- La varianza está concentrada en los primeros componentes.
- Proyectar sobre los primeros $r$ PCs es la mejor reducción de dimensionalidad en sentido de mínima varianza perdida.

Diferencia clave con la SVD "raw": PCA resta la media primero, lo que la conecta a la estadística (la covarianza, no la correlación cruda).

## Relación SVD-PCA

$$\mathbf{C} = \frac{1}{n-1}\mathbf{B}^*\mathbf{B} = \frac{1}{n-1}\mathbf{V}\boldsymbol{\Sigma}^2\mathbf{V}^* \implies \mathbf{D} = \frac{1}{n-1}\boldsymbol{\Sigma}^2.$$

La varianza en cada dirección PC es $\lambda_k = \sigma_k^2/(n-1)$ [[brunton-kutz-ch1]] §1.5 p. 55.

## Aplicaciones en la fuente

- **Datos Gaussianos con ruido**: los PCs recuperan la rotación y escala de la distribución.
- **Datos de cáncer ovárico** (4000 genes, 216 pacientes): PCA revela clustering en las primeras 3 PCs.
- **Eigenfaces**: PCA sobre imágenes de rostros produce una base de "caras promedio" reutilizable para clasificación facial.

## Conexiones

- Requiere: [[singular-value-decomposition]], [[covariance-matrix]]
- Relacionado: [[low-rank-approximation]], [[method-of-snapshots]]

## Fuentes

- [[brunton-kutz-ch1]] §1.5 pp. 53–60, §1.6 pp. 61–67

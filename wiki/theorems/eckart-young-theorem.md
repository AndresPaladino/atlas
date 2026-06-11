---
type: theorem
title: "Eckart–Young Theorem"
aliases: ["teorema de Eckart-Young", "Schmidt-Eckart-Young", "optimal low-rank approximation theorem"]
statement_form: "if rank(X̃) = r then ‖X − X̃‖ ≥ ‖X − X_r‖"
areas: [linear-algebra, data-science]
tags: [linear-algebra/matrix-decomposition]
requires: ["[[singular-value-decomposition]]", "[[low-rank-approximation]]", "[[frobenius-norm]]", "[[spectral-norm]]"]
unlocks: ["[[optimal-hard-threshold]]"]
sources: ["[[brunton-kutz-ch1]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Enunciado formal

**Hipótesis:** Sea $\mathbf{X} \in \mathbb{C}^{n \times m}$ y sea $\tilde{\mathbf{X}} = \tilde{\mathbf{U}}\tilde{\boldsymbol{\Sigma}}\tilde{\mathbf{V}}^*$ su [[low-rank-approximation|aproximación de rango $r$]] vía SVD truncada.

**Conclusión:** Para cualquier otra matriz $\hat{\mathbf{X}}$ con $\mathrm{rank}(\hat{\mathbf{X}}) = r$:

$$\underset{\hat{\mathbf{X}},\; \mathrm{rank}(\hat{\mathbf{X}})=r}{\mathrm{argmin}} \|\mathbf{X} - \hat{\mathbf{X}}\|_F = \tilde{\mathbf{U}}\tilde{\boldsymbol{\Sigma}}\tilde{\mathbf{V}}^*, \qquad \text{(Th. 1.1, [[brunton-kutz-ch1]] p. 36)}$$

y el mismo resultado vale en la [[spectral-norm|norma espectral]] $\|\cdot\|_2$.

Los errores exactos son:

$$\|\mathbf{X} - \tilde{\mathbf{X}}\|_F^2 = \sum_{k=r+1}^{m}\sigma_k^2, \qquad \|\mathbf{X} - \tilde{\mathbf{X}}\|_2 = \sigma_{r+1}.$$

## Intuición

No hay ninguna matriz de rango $r$ que aproxime $\mathbf{X}$ mejor que la SVD truncada, en sentido de mínimos cuadrados. Esto convierte a la SVD truncada en la herramienta óptima de compresión y reducción de dimensionalidad para datos de baja dimensión intrínseca.

El resultado fue primero probado por Schmidt (1907) en el contexto de operadores en espacios de funciones, redescubierto por Eckart y Young en 1936 para matrices finitas [[brunton-kutz-ch1]] §1.2 p. 36.

## Consecuencias prácticas

- Justifica el uso de la [[low-rank-approximation|SVD truncada]] como representación óptima de datos.
- El error relativo $\sum_{k=r+1}\sigma_k^2 / \sum_{k=1}\sigma_k^2$ es la fracción de varianza perdida.
- La forma del error $\|\mathbf{X} - \tilde{\mathbf{X}}\|_2 = \sigma_{r+1}$ motiva el [[optimal-hard-threshold|umbral óptimo de Gavish-Donoho]].

## Conexiones

- Requiere: [[singular-value-decomposition]], [[low-rank-approximation]], [[frobenius-norm]], [[spectral-norm]]
- Habilita: [[optimal-hard-threshold]]

## Fuentes

- [[brunton-kutz-ch1]] §1.2 pp. 36–37 (Theorem 1.1)

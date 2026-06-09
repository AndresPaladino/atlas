---
type: method
title: "Optimal Hard Threshold (Gavish–Donoho)"
aliases: ["umbral óptimo de Gavish-Donoho", "hard threshold SVD", "optimal truncation"]
when_to_use: "Cuando la matriz X tiene estructura de bajo rango contaminada con ruido Gaussiano blanco i.i.d., y se quiere elegir el rango de truncación óptimo."
fails_when: "El ruido no es Gaussiano blanco i.i.d. El nivel de ruido es completamente desconocido y la distribución de valores singulares no tiene una región plana (la mediana no es representativa del ruido)."
areas: [linear-algebra, data-science, numerical-analysis]
tags: [linear-algebra/matrix-decomposition, numerical-analysis/denoising]
requires: ["[[singular-values]]", "[[eckart-young-theorem]]", "[[low-rank-approximation]]"]
unlocks: []
bloom: 0
sources: ["[[brunton-kutz-ch1]]"]
seen_in_subjects: []
created: 2026-06-02
updated: 2026-06-02
---

## Cuándo usarlo

Cuando $\mathbf{X} = \mathbf{X}_\mathrm{true} + \gamma \mathbf{X}_\mathrm{noise}$, donde $\mathbf{X}_\mathrm{noise}$ tiene entradas i.i.d. Gaussianas $\mathcal{N}(0,1)$, y se desea estimar el rango óptimo de truncación [[brunton-kutz-ch1]] §1.7 p. 68.

## Umbral

**Caso 1 — $\gamma$ conocido, $\mathbf{X}$ cuadrada $n \times n$:**
$$\tau = \frac{4}{\sqrt{3}}\sqrt{n}\,\gamma.$$

**Caso 2 — $\gamma$ conocido, $\mathbf{X}$ rectangular $n \times m$ con $\beta = m/n \leq 1$:**
$$\tau = \lambda(\beta)\sqrt{n}\,\gamma, \quad \lambda(\beta) = \left(2(\beta+1) + \frac{8\beta}{(\beta+1)+(\beta^2+14\beta+1)^{1/2}}\right)^{1/2}.$$

**Caso 3 — $\gamma$ desconocido (más común en la práctica):**
$$\tau = \omega(\beta)\,\sigma_\mathrm{med}, \quad \omega(\beta) = \lambda(\beta)/\mu_\beta,$$
donde $\sigma_\mathrm{med}$ es la mediana de los valores singulares y $\mu_\beta$ se aproxima numéricamente [[brunton-kutz-ch1]] §1.7 pp. 68–70.

## Interpretación

Valores singulares $\sigma_k > \tau$ corresponden a modos de señal; $\sigma_k \leq \tau$ corresponden a ruido. El umbral es más efectivo que la heurística del 90% de la energía acumulada para matrices ruidosas de bajo rango.

## Cuándo falla

- Ruido no Gaussiano o con estructura correlacionada.
- La distribución de valores singulares no tiene una región claramente plana (la mediana no representa el nivel de ruido).

## Conexiones

- Requiere: [[singular-values]], [[eckart-young-theorem]], [[low-rank-approximation]]

## Fuentes

- [[brunton-kutz-ch1]] §1.7 pp. 68–75

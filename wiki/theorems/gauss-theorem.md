---
type: theorem
title: "Teorema de Gauss"
aliases: ["Gauss's theorem", "teorema de la divergencia", "divergence theorem", "Gauss", "teorema de Gauss-Ostrogradsky"]
areas: [math]
tags: [calculus/vector, integration, theorems]
statement_form: "if V is a solid bounded by closed surface S and X is C1 on V then triple integral of div X over V equals flux through S"
requires: ["[[surface-integral]]", "[[divergence]]", "[[stokes-theorem]]"]
unlocks: []
bloom: 0
sources: ["[[gonzalez-cvec-2023]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

## Enunciado formal

**Hipótesis:** Sea $V$ un sólido en $\mathbb{R}^3$ limitado por una superficie orientable $S$, con normal unitaria $\vec{n}$ apuntando hacia el exterior de $V$. Sea $X$ un campo vectorial de clase $C^1$ en un abierto que contiene a $V \cup S$.

**Conclusión** [[gonzalez-cvec-2023]] §2.9 p. 107:

$$\iiint_V \text{div}\, X\, \mathrm{d}V = \oiint_S X \cdot \mathrm{d}S.$$

## Intuición

Gauss relaciona la **divergencia integrada en el volumen** con el **flujo total a través de la superficie cerrada** que lo bordea. La divergencia positiva en un punto representa producción de flujo; la integral acumula todo ese flujo y lo iguala al que sale por la frontera.

Es el análogo 3D del Teorema de Green (2D) y una instancia del Teorema de Stokes generalizado.

## Aplicación: Ley de Gauss del electromagnetismo

El flujo eléctrico a través de cualquier superficie cerrada es proporcional a la carga encerrada [[gonzalez-cvec-2023]] §2.9.1 p. 111:

$$\oiint_S \vec{E} \cdot \mathrm{d}S = \frac{Q_{\text{enc}}}{\varepsilon_0}.$$

En forma diferencial: $\text{div}\, \vec{E} = \rho / \varepsilon_0$.

## Posición en la jerarquía de teoremas integrales

| Dimensión | Teorema | Relaciona |
|---|---|---|
| 1 | Barrow | derivada → diferencia de extremos |
| 2 | Green | rotor 2D → integral doble |
| 2→3 | Stokes | rotor 3D sobre superficie → borde |
| 3 | Gauss | divergencia en volumen → flujo en superficie |

## Conexiones

- Requiere: [[surface-integral]], [[divergence]], [[stokes-theorem]]
- Relacionado: [[solenoidal-field]] (si $\text{div}\, X = 0$, el flujo neto a través de toda superficie cerrada es 0)

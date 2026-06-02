---
type: concept
title: "Integral de superficie"
aliases: ["surface integral", "integral de flujo", "flux integral"]
areas: [math]
tags: [calculus/vector, integration, surfaces]
requires: ["[[parametric-surface]]", "[[line-integral]]"]
unlocks: ["[[stokes-theorem]]", "[[gauss-theorem]]"]
bloom: 0
sources: ["[[gonzalez-cvec-2023]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

### De un campo escalar

Sea $f: S \to \mathbb{R}$ continuo sobre la superficie $S$ parametrizada por $\Phi: D \to \mathbb{R}^3$ [[gonzalez-cvec-2023]] §2.6.1 p. 82:

$$\iint_S f\, \mathrm{d}S = \iint_D f(\Phi(u,v))\, \|\Phi_u \wedge \Phi_v\|\, \mathrm{d}u\, \mathrm{d}v.$$

### De un campo vectorial (flujo)

Sea $X: S \to \mathbb{R}^3$ continuo, $\mathbf{n} = \frac{\Phi_u \wedge \Phi_v}{\|\Phi_u \wedge \Phi_v\|}$ el versor normal a $S$ [[gonzalez-cvec-2023]] §2.6.2 p. 85:

$$\iint_S X \cdot \mathrm{d}S = \iint_D X(\Phi(u,v)) \cdot (\Phi_u \wedge \Phi_v)\, \mathrm{d}u\, \mathrm{d}v.$$

Interpretación: si $X$ es un campo de velocidades de un fluido, $\iint_S X \cdot \mathrm{d}S$ es el **flujo** a través de $S$ por unidad de tiempo.

## Conexiones

- Requiere: [[parametric-surface]], [[line-integral]]
- Habilita: [[stokes-theorem]], [[gauss-theorem]]
- Relacionado: [[curl]] (aparece en el enunciado de Stokes), [[divergence]] (aparece en Gauss)

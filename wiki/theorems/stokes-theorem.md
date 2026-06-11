---
type: theorem
title: "Teorema de Stokes"
aliases: ["Stokes' theorem", "teorema de Stokes", "Stokes"]
areas: [math]
tags: [calculus/vector, integration, theorems]
statement_form: "if S is a parametric surface with boundary ∂S and X is C2 then surface integral of curl equals line integral over boundary"
requires: ["[[surface-integral]]", "[[curl]]", "[[greens-theorem]]"]
unlocks: ["[[gauss-theorem]]"]
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Enunciado formal

**Hipótesis:** Sea $\Phi: V \subset \mathbb{R}^2 \to \mathbb{R}^3$ parametrización de una superficie $S$, con borde $\partial S = \Phi(C)$ donde $C$ es curva plana cerrada simple orientada en sentido antihorario. Sea $X$ un campo vectorial de clase $C^2$ en un abierto que contiene a $S \cup \partial S$.

**Conclusión** [[gonzalez-cvec-2023]] §2.6.3 p. 90:

$$\iint_S \text{rot}\, X \cdot \mathrm{d}S = \oint_{\partial S} X \cdot \mathrm{d}s.$$

## Intuición

Stokes generaliza el Teorema de Green a superficies en $\mathbb{R}^3$: relaciona el flujo del **rotor** a través de una superficie con la circulación del campo sobre su **borde**.

Si la superficie es plana (en el plano $xy$), se recupera Green.

## Posición en la jerarquía de teoremas integrales

$$\text{Green} \subset \text{Stokes} \supset \text{Gauss (en orientación dual)}$$

Los tres son instancias del teorema generalizado de Stokes: $\int_M \mathrm{d}\omega = \int_{\partial M} \omega$.

## Aplicaciones inmediatas

- Si $\text{rot}\, X = \mathbf{0}$ en una región simplemente conexa, $\oint_{\partial S} X \cdot \mathrm{d}s = 0$: confirma que $X$ es irrotacional $\Leftrightarrow$ de gradientes (en dominio simplemente conexo). Ver [[irrotational-field]].

## Conexiones

- Requiere: [[surface-integral]], [[curl]], [[greens-theorem]]
- Habilita: [[gauss-theorem]] (análogo para volúmenes)
- Relacionado: [[irrotational-field]]

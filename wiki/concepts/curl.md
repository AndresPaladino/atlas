---
type: concept
title: "Rotor"
aliases: ["curl", "rot", "rotacional", "∇×F"]
areas: [math]
tags: [calculus/vector, fields, differential-operators]
requires: ["[[jacobian]]"]
unlocks: ["[[irrotational-field]]", "[[stokes-theorem]]"]
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Definición

Para un campo vectorial $X = (P, Q, R): U \subset \mathbb{R}^3 \to \mathbb{R}^3$ de clase $C^1$, el **rotor** de $X$ es [[gonzalez-cvec-2023]] §2.6.3 p. 90:

$$\text{rot}\, X = \nabla \wedge X = \left(\frac{\partial R}{\partial y} - \frac{\partial Q}{\partial z},\; \frac{\partial P}{\partial z} - \frac{\partial R}{\partial x},\; \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right).$$

Notación: también se escribe $\text{curl}\, X$ o $\nabla \times X$.

## Intuición

El rotor mide la **tendencia de rotación local** del campo. Si $X$ es un campo de velocidades de un fluido, $\text{rot}\, X$ en un punto indica el eje y la velocidad angular de rotación local del fluido en ese punto.

Un campo con rotor nulo se llama **irrotacional**: no tiene circulación local. Ver [[irrotational-field]].

## Relación con el Teorema de Stokes

El rotor aparece naturalmente en [[stokes-theorem]]:

$$\iint_S \text{rot}\, X \cdot \mathrm{d}S = \oint_{\partial S} X \cdot \mathrm{d}s.$$

## Conexiones

- Requiere: [[jacobian]]
- Habilita: [[irrotational-field]], [[stokes-theorem]]
- Relacionado: [[divergence]] (el análogo escalar del rotor)

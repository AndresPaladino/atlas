---
type: theorem
title: "Teorema de Green"
aliases: ["Green's theorem", "teorema de Green", "Green"]
areas: [math]
tags: [calculus/vector, integration, theorems]
statement_form: "if C is a simple closed curve bounding D and X is C1 on D then line integral over C equals double integral of curl over D"
requires: ["[[line-integral]]", "[[gradient-field]]"]
unlocks: ["[[stokes-theorem]]"]
sources: ["[[gonzalez-cvec-2023]]"]
created: 2026-06-02
updated: 2026-06-02
---

## Enunciado formal

**Hipótesis:** Sea $C$ una curva plana, cerrada, simple, regular a trozos, orientada en sentido antihorario, y $D$ la componente conexa acotada de $\mathbb{R}^2 \setminus C$. Sea $X = (P, Q)$ un campo vectorial de clase $C^1$ en algún abierto que contiene a $D \cup C$.

**Conclusión** [[gonzalez-cvec-2023]] §2.4 p. 62:

$$\oint_C P\,\mathrm{d}x + Q\,\mathrm{d}y = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)\mathrm{d}x\,\mathrm{d}y.$$

## Intuición

Green relaciona una integral de línea sobre la **frontera** de una región plana con una integral doble sobre el **interior**. Es el caso 2D del Teorema de Stokes.

El término $\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}$ es la componente $z$ del rotor de $X$ en el plano: mide la rotación local del campo.

## Corolario: campos conservativos en el plano

Si $\frac{\partial Q}{\partial x} = \frac{\partial P}{\partial y}$ en $D$ (dominio simplemente conexo), entonces $\oint_C X \cdot \mathrm{d}s = 0$ para toda curva cerrada, y $X$ es de gradientes. Conecta con [[gradient-field]].

## Conexiones

- Requiere: [[line-integral]], [[gradient-field]]
- Habilita: [[stokes-theorem]] (generalización a superficies en $\mathbb{R}^3$)
- Relacionado: [[curl]] (la integrand del lado derecho es la componente $z$ del rotor)

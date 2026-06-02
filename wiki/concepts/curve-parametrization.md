---
type: concept
title: "Parametrización de curvas"
aliases: ["curve parametrization", "parametrización", "curva paramétrica"]
areas: [math]
tags: [calculus/vector, curves]
requires: []
unlocks: []
bloom: 2
sources: ["[[gonzalez-cvec-2023]]"]
unlocks: ["[[arc-length]]", "[[line-integral]]", "[[parametric-surface]]"]
seen_in_subjects: [calculo-vectorial]
created: 2026-06-02
updated: 2026-06-02
---

# Parametrización de curvas

## Definición

Una **curva paramétrica** en $\mathbb{R}^n$ es una función $\gamma: I \subseteq \mathbb{R} \to \mathbb{R}^n$, donde $I$ es un intervalo. La curva (como imagen) es $\gamma(I) \subset \mathbb{R}^n$; el parámetro $t \in I$ recorre la curva.

En $\mathbb{R}^2$: $\gamma(t) = (x(t), y(t))$.
En $\mathbb{R}^3$: $\gamma(t) = (x(t), y(t), z(t))$.

## Intuición

Pensar en $t$ como tiempo y $\gamma(t)$ como la posición de una partícula. La parametrización aporta más información que la imagen: incluye orientación (sentido del recorrido) y velocidad (cómo se recorre).

## Vector tangente

$\gamma'(t) = (x'(t), y'(t), \ldots)$ es el vector tangente en $\gamma(t)$. Su dirección da la tangente a la curva; su módulo es la "rapidez".

## Tangentes singulares

- **Tangente horizontal**: $y'(t) = 0$ y $x'(t) \neq 0$.
- **Tangente vertical**: $x'(t) = 0$ y $y'(t) \neq 0$.
- **Cúspide**: $x'(t) = 0$ **y** $y'(t) = 0$. Si la trayectoria invierte sentido en ese punto, hay cúspide visible.

Distinguir cúspide de tangente horizontal o vertical: la cúspide requiere **ambas** derivadas nulas.

## Conexiones

- Aparece en: Cálculo Vectorial, Tema 4 (Curvas paramétricas) y Tema 5 (Integrales de línea).
- Ejemplo arquetípico: [[cycloid-parametrization]].

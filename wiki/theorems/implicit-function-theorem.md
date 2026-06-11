---
type: theorem
title: "Teorema de la función implícita"
aliases: ["TFI", "implicit function theorem", "teorema función implícita"]
areas: [math]
tags: [calculus/vector, differentiation, implicit-functions]
requires: ["[[jacobian]]"]
unlocks: []
statement_form: "Si F es C^1 en un entorno de (a,b), F(a,b)=0, y la Jacobiana parcial respecto a las variables y es invertible en (a,b), entonces existe una función implícita y=φ(x) C^1 en un entorno de a tal que F(x,φ(x))=0."
sources: []
created: 2026-06-02
updated: 2026-06-02
---

# Teorema de la función implícita (TFI)

## Enunciado (caso vectorial)

Sea $F: U \subseteq \mathbb{R}^{n+m} \to \mathbb{R}^m$ de clase $C^1$. Escribimos los puntos como $(x, y)$ con $x \in \mathbb{R}^n$, $y \in \mathbb{R}^m$. Supongamos que en $(a, b) \in U$:

1. $F(a, b) = 0$,
2. la matriz Jacobiana parcial $\frac{\partial F}{\partial y}(a, b) \in \mathbb{R}^{m \times m}$ es **invertible**.

Entonces existen entornos $V$ de $a$ y $W$ de $b$, y una única función $\varphi: V \to W$ de clase $C^1$ tal que:

$$F(x, \varphi(x)) = 0 \quad \forall x \in V, \quad \varphi(a) = b.$$

Además, la derivada de $\varphi$ se calcula como:

$$D\varphi(x) = -\left[\frac{\partial F}{\partial y}(x, \varphi(x))\right]^{-1} \frac{\partial F}{\partial x}(x, \varphi(x)).$$

## Caso escalar ($m = 1$)

$F: \mathbb{R}^{n+1} \to \mathbb{R}$, condición clave: $\frac{\partial F}{\partial y}(a, b) \neq 0$.

## Intuición geométrica

La hipersuperficie $F = 0$ en $\mathbb{R}^{n+m}$ se puede expresar localmente como el grafo de una función $y = \varphi(x)$ siempre que el "espacio vertical" no sea tangente a la superficie en el punto — eso es exactamente lo que dice la condición de invertibilidad sobre $\partial F / \partial y$.

## Conexiones

- Requiere: [[jacobian]]
- Aparece en: Cálculo Vectorial, Tema 2 (Función inversa y función implícita).

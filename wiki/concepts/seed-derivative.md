---
type: concept
title: "Derivada"
aliases: ["derivative", "derivada", "tasa de cambio instantánea"]
areas: [math]
tags: [calculus/single-variable, examples/seed]
requires: []
unlocks: ["[[seed-mean-value-theorem]]"]
sources: []
created: 2026-06-23
updated: 2026-06-23
---

# Derivada

> Página semilla del template Atlas (contenido de dominio público, autocontenida).
> Sirve para probar `/query` sin ingestar nada. Borrala cuando tengas tu propio wiki.

## Definición

La **derivada** de una función $f$ en un punto $a$ es el límite del cociente incremental:

$$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

cuando ese límite existe. Si existe, se dice que $f$ es **derivable** en $a$.

## Intuición

El cociente $\frac{f(a+h)-f(a)}{h}$ es la pendiente de la recta secante que pasa por $(a, f(a))$ y $(a+h, f(a+h))$. Al hacer $h \to 0$, la secante tiende a la **recta tangente**: $f'(a)$ es su pendiente, la tasa de cambio instantánea de $f$ en $a$.

## Propiedad básica

Si $f$ es derivable en $a$, entonces es **continua** en $a$. El recíproco es falso: $f(x)=|x|$ es continua en $0$ pero no derivable ahí (las secantes por izquierda y derecha tienen pendientes distintas).

## Conexiones

- Habilita: [[seed-mean-value-theorem]] (la derivada es la hipótesis central del teorema).

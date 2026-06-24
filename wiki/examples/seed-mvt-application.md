---
type: example
title: "Aplicación del teorema del valor medio: cota de velocidad"
aliases: ["mvt application", "ejemplo TVM", "cota por valor medio"]
areas: [math]
tags: [calculus/single-variable, examples/seed]
illustrates: ["[[seed-mean-value-theorem]]"]
difficulty: 1
requires: []
sources: []
created: 2026-06-23
updated: 2026-06-23
---

# Aplicación del teorema del valor medio: cota de velocidad

> Página semilla del template Atlas (contenido de dominio público, autocontenida).
> Sirve para probar `/query` sin ingestar nada. Borrala cuando tengas tu propio wiki.

## Enunciado

Un auto recorre $180$ km en $2$ horas. Probar que en algún instante su velocímetro marcó exactamente $90$ km/h.

## Resolución

Sea $f(t)$ la posición del auto (en km) en el instante $t$ (en horas), con $t \in [0, 2]$. La posición es continua y derivable (la velocidad existe en todo momento), así que se cumplen las hipótesis del [[seed-mean-value-theorem]].

La velocidad promedio es

$$\frac{f(2) - f(0)}{2 - 0} = \frac{180}{2} = 90 \text{ km/h.}$$

Por el teorema del valor medio, existe $c \in (0, 2)$ tal que

$$f'(c) = 90.$$

Como $f'(c)$ es la velocidad instantánea en el tiempo $c$, en ese instante el velocímetro marcó exactamente $90$ km/h. $\blacksquare$

## Observación

El teorema garantiza que **existe** ese instante, pero no dice cuál: podría haber varios, y no da un método para encontrarlos. Es un resultado de existencia, no constructivo.

## Conexiones

- Ilustra: [[seed-mean-value-theorem]]

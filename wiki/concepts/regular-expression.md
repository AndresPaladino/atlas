---
type: concept
title: "Expresión regular"
aliases: ["regular expression", "ER", "regex", "expresión regular"]
areas: [computing]
tags: [formal-languages, regular-languages]
requires: []
unlocks: ["[[arden-lemma]]", "[[kleene-analysis]]"]
bloom: 3
sources: []
seen_in_subjects: [teoria-lenguajes]
created: 2026-06-02
updated: 2026-06-02
---

# Expresión regular

## Definición

Una **expresión regular** sobre un alfabeto $\Sigma$ es una expresión formal que denota un lenguaje regular. Definición inductiva:

- $\emptyset$ y $\varepsilon$ son ERs (denotan el lenguaje vacío y $\{\varepsilon\}$ respectivamente).
- Cada $a \in \Sigma$ es una ER (denota $\{a\}$).
- Si $r$ y $s$ son ERs, también lo son:
  - $r \mid s$ (alternancia) — denota $L(r) \cup L(s)$.
  - $r \cdot s$ (concatenación, usualmente escrita $rs$) — denota $L(r) \cdot L(s)$.
  - $r^*$ (estrella de Kleene) — denota $L(r)^* = \{w_1 w_2 \cdots w_k : k \geq 0, w_i \in L(r)\}$.

## Convención del curso (notación estricta)

- Concatenación: yuxtaposición o `.` ($ab$, $a \cdot b$).
- Alternancia: `|`.
- Estrella de Kleene: `*`.
- **No** usar `+` para "una o más". Escribir $r r^*$ en su lugar.
- Paréntesis para agrupar.

## Identidades útiles

- **Idempotencia**: $r \mid r = r$, $(r^*)^* = r^*$.
- **Distribución**: $r(s \mid t) = rs \mid rt$.
- **Factorización**: $rs \mid rt = r(s \mid t)$.
- **Casos especiales**: $\emptyset \mid r = r$, $\varepsilon \cdot r = r$, $\emptyset \cdot r = \emptyset$.
- Ejemplo del curso: $b \mid aa^* b = (\varepsilon \mid aa^*) b = a^* b$.

## Equivalencia con autómatas

Teorema de Kleene: los lenguajes denotados por ERs son exactamente los lenguajes reconocidos por [[finite-automaton]]s. Las dos direcciones:

- **ER → AFD**: construcción de Thompson + determinización.
- **AFD → ER**: [[kleene-analysis]] (sistema de ecuaciones + [[arden-lemma]]).

## Conexiones

- Habilita: [[arden-lemma]], [[kleene-analysis]]
- Equivalente a: [[finite-automaton]]
- Aparece en: Teoría de Lenguajes, Tema 1 (Lenguajes Regulares).

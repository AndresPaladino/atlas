---
updated: 2026-03-18
---

# Índice: Cálculo Vectorial

## Temario del curso

### Primera parte
- Tema 1: Extremos relativos y absolutos ← práctico 1 (semanas 1-2)
- Tema 2: Teoremas de la función inversa y función implícita ← práctico 2 (semanas 3-4)
- Tema 3: Extremos condicionados / Multiplicadores de Lagrange ← práctico 3 (semana 5)

### Segunda parte
- Tema 4: Curvas paramétricas ← práctico 4 (semana 6)
- Tema 5: Integrales de línea ← práctico 5 (semana 7)

**→ Primer parcial: 25 abr – 6 may**

- Tema 6: Campos de gradientes y potenciales escalares ← práctico 6 (semana 8)
- Tema 7: Teorema de Green ← práctico 7 (semana 9)

### Tercera parte
- Tema 8: Superficies paramétricas ← práctico 8 (semana 10)
- Tema 9: Integrales de superficie ← práctico 9 (semanas 11-12)
- Tema 10: Teorema de Stokes ← práctico 10 (semanas 12-13)
- Tema 11: Rotacional y divergencia ← práctico 11 (semana 14)
- Tema 12: Teorema de la divergencia de Gauss ← práctico 12 (semana 15)

**→ Segundo parcial: 27 jun – 10 jul**

## Notación del curso
- Gradiente: ∇f
- Hessiana: H_f(p)
- Derivada direccional: ∂f/∂v⃗
- Punto estacionario: ∇f(p) = 0
- Determinante Hessiana: det H_f

## Conceptos

### Entiendo
- Criterio de la hessiana: aplicación y limitaciones
- Métodos alternativos cuando la hessiana no decide (definición, restricción a curvas, Taylor orden superior)

### Tengo dudas
- Fórmula del jacobiano de φ: deducción por regla de la cadena
- Cicloide acortada y alargada (Ej 4.3 parte 2): pendiente

## Bloom actual
Extremos relativos R²: **2** (comprende herramientas y cuándo aplicar cada una)
Función implícita: **2** (comprende enunciado, hipótesis, y caso escalar vs. vectorial)

## Sesiones con Claude
| Fecha | Ejercicios / temas trabajados | Resultado |
|---|---|---|
| 2026-03-18 | Criterio hessiana indeciso: análisis por definición, restricción a curvas, Taylor orden superior | Entendido — distingue cuándo falla H y qué alternativa usar |
| 2026-03-18 | TFI: enunciado general (n+m), hipótesis, fórmula Dφ, geometría | Comprende condición ∂F/∂y≠0, casos escalar y vectorial, geometría del teorema |
| 2026-04-19 | Ej 4.3 p1: cicloide — parametrización, condición de rodadura, tangentes verticales/horizontales, cúspides | Parametrización deducida geométricamente; distingue cúspides (ambas derivadas nulas) de tangentes horizontales (solo y'=0) |

## Conceptos wiki

```dataview
TABLE bloom, areas, type
FROM "wiki/concepts" OR "wiki/theorems" OR "wiki/methods" OR "wiki/examples"
WHERE contains(seen_in_subjects, regexreplace(this.file.folder, ".*/", ""))
SORT bloom DESC, file.name ASC
```

### Fallback manual
- [[critical-point]] (bloom 2)
- [[curve-parametrization]] (bloom 2)
- [[cycloid-parametrization]] (bloom 2, example)
- [[hessian-criterion]] (bloom 2, method)
- [[implicit-function-theorem]] (bloom 2, theorem)
- [[jacobian]] (bloom 1)

> La verdad ejecutable del Bloom vive en el frontmatter de cada página wiki — la sección "Bloom actual" de arriba es referencia humana.

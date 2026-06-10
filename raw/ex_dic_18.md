<!-- atlas-local: extraído de ex_dic_18.pdf con marker v1.10.2 en cuda. No editar a mano. -->

# Universidad de la República Facultad de Ingeniería - IMERL

# Cálculo Vectorial. Segundo Semestre 2018

Examen -8 de diciembre de 2018

| Nro de Parcial | Cédula | Apellido y nombre |  |
|----------------|--------|-------------------|--|
|                |        |                   |  |
|                |        |                   |  |

- El puntaje total es 100 puntos.
- La duración del examen es 3:30 horas.

### (I) Múltiple opción. Total: 28 puntos

Puntajes: 7 puntos si la respuesta es correcta, -2,3 puntos si la respuesta es incorrecta, 0 punto por no contestar.

Indique sus respuestas en los casilleros correspondientes:

| Ejercicio 1 | Ejercicio 2 | Ejercicio 3 | Ejercicio 4 |
|-------------|-------------|-------------|-------------|
|             |             |             |             |
|             |             |             |             |

## Ejercicio 1

Se considera el campo  $F:\mathbb{R}^3-\{(0,0,0)\}\to\mathbb{R}^3$  dado por

$$F(x,y,z) = \frac{(x,y,z)}{(x^2 + y^2 + z^2)^{3/2}}$$

y la superficie cerrada  $S = \partial ([-1,1] \times [-1,1] \times [-1,1])$  orientada con normal saliente. Entonces el flujo de F a través de S corresponde a:

- A)  $4\pi$ .
- B)  $-4\pi$ .
- C)  $2\pi$ .
- D)  $-2\pi$ .

## Ejercicio 2

Consideremos las siguientes figuras en el plano

![](_page_0_Picture_20.jpeg)

y las siguientes afirmaciones

- (I) Considere la Figura (a). Sea F un campo del que se sabe que es de clase  $C^1$  y conservativo en  $\Omega$ . Entonces la circulación de F sobre la curva  $\Gamma$  es nula.
- (II) Considere la Figura (b). Sea F un campo de clase  $C^1$  en  $\Omega$ . Entonces el valor de la circulación de F sobre las curvas  $\Gamma_1$  y  $\Gamma_2$  es el mismo.
- (III) Considere la Figura (c). Sea F(x,y) = (2y,x). Entonces existe alguna curva cerrada contenida en  $\Omega$  tal que la circulación de F sobre la misma no vale cero.

Indique la opción correcta.

- A) Todas las afirmaciones son verdaderas.
- B) Sólo la afirmación (II) es verdadera.
- C) Sólo las afirmaciones (I) y (III) son verdaderas.
- D) Sólo la afirmación (I) es verdadera.

# Ejercicio 3

El mínimo de la función f(x,y)=-2x+3y sobre la curva  $\mathcal{C}=\left\{(x,y)\in\mathbb{R}^2:x^2-(y-1)^3=0\right\}$  es:

- A) 3.
- B) 4.
- C) 8.
- D) 1.

#### Ejercicio 4

Sea  $D \subset \mathbb{R}^2$  compacto tal que su área es 7. Considere la superficie

$$S = \{(x, y, z) \in \mathbb{R}^3 : (x, y) \in D, 3x - y + 2z = 10\}.$$

Entonces el área de S corresponde a:

- A) 7.

- C)  $\frac{\sqrt{14}}{2}$ . D)  $\frac{7\sqrt{14}}{2}$ .

### (II) Desarrollo. Total: 72 puntos

Todo resultado teórico que utilice en la resolución de los problemas debe estar adecuadamente justificado.

## <span id="page-1-0"></span>Problema 1 (20 puntos)

Consideremos la ecuación

$$(1) F(x,y) = 0,$$

donde  $F(x,y) = x^3 + y^3 + x^2 + xy + by$ , y b es una constante real.

(a) Determinar los valores de b para los cuales el Teorema de la función implícita aplicado a la ecuación (1) permite asegurar la existencia de funciones implícitas y = y(x) o x = x(y) de clase  $C^1$  en un entorno de (0,0).

(b) Sea y = h(x), en caso de existir, la función implícita definida por F(x, y) = 0 en un entorno de (0,0). Calcular los valores del parámetro b para que el polinomio de Taylor de segundo grado en 0 de h(x) valga 1 para x = 1.

## Problema 2 (30 puntos)

- 1. Sea  $F: U \subset \mathbb{R}^3 \to \mathbb{R}^3$  un campo continuo en U. Probar que si existe  $f: U \to \mathbb{R}$  de clase  $C^1$  tal que  $\nabla f = F \Rightarrow \int_{\mathcal{C}_1} F ds = \int_{\mathcal{C}_2} F ds$  para todo par de curvas  $\mathcal{C}_1$  y  $\mathcal{C}_2$  contenidas en U que tienen el mismo punto inicial y el mismo punto final.
- 2. En  $\mathbb{R}^2$  se considera el campo vectorial definido por:

$$F(x,y) = e^{x^2 + y^2}(ax, 20y),$$

donde  $a \in \mathbb{R}$ .

(a) Determinar el valor de a para que el campo sea conservativo.

En las siguientes partes se trabaja con el valor de a encontrado en (a).

- (b) Determinar un potencial escalar f del campo F válido en todo su dominio de definición y tal que f(0,0) = 40.
- (c) Determinar la circulación I del campo F sobre la porción de la circunferencia de centro el punto (1,0) y radio 1 situada en el primer cuadrante, limitada por las rectas x=0, y=x y recorrida en sentido horario.

## Problema 3 (22 puntos)

1. Considerar la siguiente afirmación:

Sea C una curva cerrada simple regular a trozos, positivamente orientada, en  $\mathbb{R}^2$  y sea D la unión de la región interior a C con la curva C como se ilustra en la siguiente figura.

![](_page_2_Picture_14.jpeg)

Sea  $F = (P,Q) : U \subset \mathbb{R}^2 \to \mathbb{R}^2$  un campo vectorial de clase  $C^1$  definido en un abierto que contenga a D. Entonces vale

(2) 
$$\oint_C F \cdot ds = \iint_D (Q_x - P_y) dx dy.$$

Sean ahora C<sup>1</sup> y C<sup>2</sup> dos curvas en R 2 como se muestran en la siguiente figura

![](_page_3_Picture_2.jpeg)

Consideremos R la regi´on del plano comprendida entre las curvas C<sup>1</sup> y C<sup>2</sup> y F = (P, Q) un campo de clase C <sup>1</sup> definido en un abierto W que contiene a R, probar usando la afirmaci´on anterior que:

$$\iint_{R} (Q_x - P_y) dx dy = \oint_{C_1} F ds - \oint_{C_2} F ds.$$

2. Calcular la circulaci´on del campo

$$F(x,y) = \left(\frac{x}{x^2 + y^2}, \frac{y}{x^2 + y^2}\right)$$

sobre la siguiente curva

![](_page_3_Figure_8.jpeg)
<!-- atlas-local: extraído de examenjulio2019.pdf con marker v1.10.2 en cuda. No editar a mano. -->

# Universidad de la República Facultad de Ingeniería-IMERL

### EXAMEN: CALCULO VECTORIAL

| N de parcial | Cédula | Apellido y nombre | Salón |
|--------------|--------|-------------------|-------|
|              |        |                   |       |
|              |        |                   |       |

| RESPUESTAS |   |   |   |   |   |  |  |  |
|------------|---|---|---|---|---|--|--|--|
| 1          | 2 | 3 | 4 | 5 | 6 |  |  |  |
|            |   |   |   |   |   |  |  |  |

Múltiple opción (Total: 30 puntos)

En cada pregunta hay sólo una opción correcta.

Respuesta correcta: 5 puntos, respuesta incorrecta: -1 punto, no respuesta: 0 punto.

## Ejercicio 1

Sea  $D = \{(x,y) \in \mathbb{R}^2 : x \in [0,2], y \in [0,e^x-1]\}$  región del plano. Consideramos los campos:

$$F(x,y) = \left(\frac{x-1}{(x-1)^2 + (y-1)^2}, \frac{y-1}{(x-1)^2 + (y-1)^2}\right), \quad G(x,y) = \left(\frac{x}{x+1}, \frac{y^2}{y+1}\right).$$

Entonces,  $\int_{\delta D} (F+G)$  (curva recorrida en sentido antihorario) es igual a

- (A)  $2\pi$ .
- (B)  $2\pi e$ .
- (C)  $e^2 2 + e$ .
- (D) 0.
- (E)  $e^2 1$ .

## Ejercicio 2

Se consideran las siguientes afirmaciones:

- (I) No existe ning´un campo vectorial de clase C 1 en R <sup>3</sup> que sea de rotores y que adem´as sea de gradientes.
- (II) Si X es un campo de rotores de clase C <sup>1</sup> definido en todo en R 3 , entonces su divergencia es nula.
- (III) Si X es un campo solenoidal de clase C <sup>1</sup> definido en todo R 3 , entonces es de rotores.

Entonces

- (A) S´olo la afirmaci´on (I) es verdadera.
- (B) Las tres afirmaciones son falsas.
- (C) S´olo las afirmaciones (II) y (III) son verdaderas.
- (D) Las tres tres afirmaciones son verdaderas.
- (E) S´olo la afirmaci´on (II) es verdadera.

## Ejercicio 3

Consideramos la funci´on f : R <sup>2</sup> → R definida mediante:

$$f(x,y) = y^3 + x^2y + 2x^2 + 2y^2 - 4y - 8$$

y el conjunto:

$$D = \{(x, y) \in \mathbb{R}^2 : x^2 + y^2 = 1\}.$$

Entonces

- (A) f posee m´aximo y m´ınimo absoluto en D. Adem´as el m´aximo es M = 1 y el m´ınimo es m = −1.
- (B) f posee m´aximo y m´ınimo absoluto en D. Adem´as el m´aximo es M = −4 y el m´ınimo es m = −10.
- (C) f posee m´ınimo absoluto en D, pero no m´aximo absoluto. Adem´as el m´ınimo es m = −8.
- (D) f no posee m´aximo ni m´ınimo absoluto en D.
- (E) f posee m´aximo y m´ınimo absoluto en D. Adem´as el m´aximo es M = −3 y el m´ınimo es m = −9.

## Ejercicio 4

Se consideran las curvas de ecuaciones  $y_1(x)=ax+b$   $(a,b\in R)$  e  $y_2(x)=x^{3/2}$  con  $x\in [0,1]$ . Se define  $F(a,b)=\int_0^1(y_1(x)-y_2(x))^2dx$ .

#### Entonces

- (A) F no tiene mínimo relativo en  $\mathbb{R}^2$ .
- (B) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=0 y b=0.
- (C) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=36/35 y b=-4/35.
- (D) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=-4/35 y b=2/35.
- (E) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=0 y b=1.

## Ejercicio 5

La recta tangente en (0,0) a la curva

$$\sin(x) + \cos(y) + x + y = 1$$
, con  $x, y \in \mathbb{R}$ 

es

- (A) x + y = 0.
- (B) 2x y = 0.
- (C) 2x + y = 0.
- (D) x + 2y = 0.
- (E) x 2y = 0.

#### Ejercicio 6

Dada la superficie  $S: x^2 - y^2 + z^2 = 30$  y el punto p = (3, 2, 5).

## Entonces

- (A) La superficie no posee plano tangente en dicho punto.
- (B) El plano tangente a S en el punto p corresponde a 3x + 2y + 5z = 30.
- (C) El plano tangente a S en el punto p corresponde a 3x + 2y + 5z = 38.
- (D) El plano tangente a S en el punto p corresponde a 3x 2y + 5z = 30.
- (E) El plano tangente a S en el punto p corresponde a 3x 2y + 5z = 0.

## Ejercicio de desarrollo (Total: 30 puntos)

#### Ejercicio 1

- 1. Definir campo de gradientes en una región  $D \subset \mathbb{R}^3$ .
- 2. Demostrar que si un campo X es tal que  $\int_C X = \int_{C'} X$  para todas  $C, C' \subset D$  curvas con iguales extremo y origen, entonces X es de gradientes en D.
- 3. Consideramos un campo  $X: \mathbb{R}^2 \to \mathbb{R}^2$  irrotacional, tal que  $\int_C X = 1/2$  siendo  $C = \{(x,y) \in \mathbb{R}^2: x^2 + y^2 = 1, \ y \ge 0\}$  orientada en sentido horario. Consideramos la curva C' parametrizada mediante  $\alpha(t) = (1 3t + t^2)(\cos(2\pi t), \sin(2\pi t))$  donde  $0 \le t \le 1$ . Calcular  $\int_{C'} X$ .

# Ejercicio 2

- 1. Enunciar y demostrar el teorema de Gauss.
- 2. Deducir una fórmula que permita calcular el volumen de un sólido limitado por una superficie compacta S sin borde a partir de una integral de superficie.
- 3. Calcular el volumen del sólido  $V=\{(x,y,z)\in\mathbb{R}^3:\ x^2+y^2\leq z\leq 1\}$  mediante una integral de superficie.
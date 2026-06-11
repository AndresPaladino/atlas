<!-- atlas-local: extraído de examenjulio2019_sol.pdf con marker v1.10.2 en cuda. No editar a mano. -->

# Universidad de la República Facultad de Ingeniería-IMERL

#### EXAMEN: CALCULO VECTORIAL - SOLUCIONES

| N de parcial | Cédula | Apellido y nombre | Salón |
|--------------|--------|-------------------|-------|
|              |        |                   |       |
|              |        |                   |       |

| RESPUESTAS |   |   |   |   |   |  |  |  |
|------------|---|---|---|---|---|--|--|--|
| 1          | 2 | 3 | 4 | 5 | 6 |  |  |  |
|            |   |   |   |   |   |  |  |  |

Múltiple opción (Total: 48 puntos)

En cada pregunta hay sólo una opción correcta.

Respuesta correcta: 8 puntos, respuesta incorrecta: -2 punto, no respuesta: 0 punto.

### Ejercicio 1

Sea  $D = \{(x,y) \in \mathbb{R}^2 : x \in [0,2], y \in [0,e^x-1]\}$  región del plano.

Consideramos los campos:

$$F(x,y) = \left(\frac{x-1}{(x-1)^2 + (y-1)^2}, \frac{y-1}{(x-1)^2 + (y-1)^2}\right), \quad G(x,y) = \left(\frac{x}{x+1}, \frac{y^2}{y+1}\right).$$

Sea  $\delta D$ , el borde de D, orientada en sentido antihorario. Entonces  $\int_{\delta D} (F+G)$  es igual a

- (A)  $2\pi$ .
- (B)  $2\pi e$ .
- (C)  $e^2 2 + e$ .
- (D) 0.
- (E)  $e^2 1$ .

# Ejercicio 2

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

### Ejercicio 3

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

Se consideran las curvas de ecuaciones  $y_1(x)=ax+b$   $(a,b\in\mathbb{R})$  e  $y_2(x)=x^{3/2}$  con  $x\in[0,1]$ . Se define  $F(a,b)=\int_0^1(y_1(x)-y_2(x))^2dx$ .

#### Entonces

- (A) F no tiene mínimo relativo en  $\mathbb{R}^2$ .
- (B) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=0 y b=0.
- (C) Ftiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=36/35 y b=-4/35.
- (D) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=-4/35 y b=2/35.
- (E) F tiene mínimo relativo en  $\mathbb{R}^2$  y se obtiene para a=0 y b=1.

#### Ejercicio 5

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

## Ejercicio de desarrollo (Total: 52 puntos)

## Ejercicio 1

- 1. Ver teórico.
- 2. Ver teórico.
- 3. Observamos que el origen de la curva C' es  $\alpha(0)=(1,0)$  y el extremo es  $\alpha(1)=(-1,0)$ . Observamos por otro lado que la curva -C tiene también los mismos origen y extremo que C'. Como el campo es de gradientes por ser irrotacional en  $\mathbb{R}^2$  que es simplemente conexo, deducimos que

$$\int_{C'} X = \int_{-C} X = -1/2.$$

## Ejercicio 2

- 1. Ver teórico.
- 2. Ver teórico.
- 3. Por la parte anterior sabemos que  $vol(V) = \iint_S X$  con normal exterior siendo X cualquier campo cuya divergencia sea 1, por ejemplo X = (x/3, y/3, z/3). En este caso  $S = S' \cup T$  siendo  $S' = \{(x, y, z) \in \mathbb{R}^3: z = x^2 + y^2, z \leq 1\}$  y  $T = \{(x, y, z) \in \mathbb{R}^3: z = 1, x^2 + y^2 \leq 1\}$ .

Vector normal unitario a S' lo hallamos como  $N\left(x,y,z\right)=\frac{(2x,2y,-1)}{\sqrt{1+4x^2+4y^2}}$  (observar que  $N\left(0,0,0\right)=\left(0,0,-1\right)$  por lo que N es normal exterior a S').

$$\iint_{S'} X = \iint_{S'} X.N = \iint_{S'} \frac{(x/3, y/3, z/3) \cdot (2x, 2y, -1)}{\sqrt{1 + 4x^2 + 4y^2}} = \iint_{S'} \frac{2x^2/3 + 2y^2/3 - z/3}{\sqrt{1 + 4x^2 + 4y^2}} \stackrel{z=x^2+y^2}{=} \iint_{S'} \frac{z}{3\sqrt{1 + 4z}}.$$

Parametrizamos S':  $\begin{cases} x = u \\ y = v \\ z = u^2 + v^2 \end{cases}$  con  $(u, v) \in U = \{u^2 + v^2 < 1\}$ . Entonces  $\|\varphi_u \wedge \varphi_v\| = 0$ 

 $\sqrt{1+4u^2+4v^2}$ , por lo que

$$\iint_{S'} \frac{z}{3\sqrt{1+4z}} = \iint_{U} \frac{u^2 + v^2}{3\sqrt{1+4u^2+4v^2}} \sqrt{1+4u^2+4v^2} du dv = \frac{1}{3} \iint_{U} (u^2 + v^2) du dv \stackrel{\text{polares}}{=}$$

$$\frac{1}{3} \int_0^{2\pi} \left( \int_0^1 r^3 dr \right) d\varphi = \frac{\pi}{6}.$$

Sobre T la normal unitaria exterior es N(x, y, z) = (0, 0, 1).

$$\iint_T X = \iint_T X.N = \iint_T (x/3,y/3,z/3) \,.\, (0,0,1) = \iint_T z/3 \stackrel{z=1}{=} \iint_T 1/3 = area(T)/3 = \pi/3.$$

Finalmente, obtenemos que el volumen buscado es  $\frac{\pi}{6} + \frac{\pi}{3} = \frac{\pi}{2}$ .
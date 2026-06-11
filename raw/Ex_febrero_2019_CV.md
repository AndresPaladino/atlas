<!-- atlas-local: extraído de Ex_febrero_2019_CV.pdf con marker v1.10.2 en cuda. No editar a mano. -->

# Universidad de la Rep´ublica C´alculo Vectorial. Facultad de Ingenier´ıa - IMERL Segundo Semestre 2018

Examen – 5 de febrero de 2019

| Nro de Parcial | C´edula | Apellido y nombre |  |
|----------------|---------|-------------------|--|
|                |         |                   |  |
|                |         |                   |  |

- El puntaje total es 100 puntos.
- La duraci´on del examen es 4:00 horas.

## (I) M´ultiple opci´on. Total: 28 puntos

Puntajes: 7 puntos si la respuesta es correcta, -2,3 puntos si la respuesta es incorrecta, 0 punto por no contestar.

Indique sus respuestas en los casilleros correspondientes:

| Ejercicio 1 | Ejercicio 2 | Ejercicio 3 | Ejercicio 4 |
|-------------|-------------|-------------|-------------|
|             |             |             |             |
|             |             |             |             |

### Ejercicio 1

Consideremos las 1-formas ω = xzdx + y <sup>2</sup>dy y η = dy + xdz definidas en R 3 . Entonces d ω ∧ η es:

- A) − x + y 2 dxdydz.
- B) x + y 2 dxdydz.
- C) x − y 2 dxdydz.
- D) −x + y 2 dxdydz.

#### Ejercicio 2

Sea β : I → R <sup>3</sup> una curva regular de clase C <sup>3</sup> parametrizada por longitud de arco. Consideremos las siguientes afirmaciones:

- (I) Si k(s) = 0 para todo s ∈ I, entonces Im(β) est´a contenida en una recta.
- (II) Si k(s) 6= 0 en todo punto, entonces τ (s) = hb(s), n<sup>0</sup> (s)i, para todo s ∈ I.
- (III) Si k(s) 6= 0 en todo punto, entonces t 0 (s) = k(s)n(s) para todo s ∈ I.

Donde k es la curvatura, τ es la torsi´on, t el vector tangente, n el normal y b el binormal.

- A) Todas las afirmaciones son verdaderas.
- B) S´olo la afirmaci´on (I) es verdadera.
- C) S´olo las afirmaciones (I) y (II) son verdaderas.
- D) S´olo las afirmaciones (I) y (III) son verdaderas.

#### Ejercicio 3

Sea  $S = \{(x, y, z) \in \mathbb{R}^3 : x = u - v, y = uv, z = u + v^2, \forall (u, v) \in \mathbb{R}^2\}$ . Si (0, b, 5) es un punto en el plano tangente a S en (0, 1, 2) de S, entonces b corresponde a:

- A) 1.
- B) -2.
- C) 2.
- D) 3.

## Ejercicio 4

Considere las siguientes afirmaciones:

- (I) La ecuación  $x y^3 = 0$  define una función  $y = \varphi(x)$  en un entorno de (0,0).
- (II) Si  $F: \mathbb{R}^3 \to \mathbb{R}$  es de clase  $C^1$  y existe  $P = (a, b, c) \in \mathbb{R}^3$  tal que

$$F(P) = 0 \text{ y } \frac{\partial F}{\partial x}(P) \cdot \frac{\partial F}{\partial y}(P) \cdot \frac{\partial F}{\partial z}(P) \neq 0.$$

Entonces la ecuación F(x,y,z)=0 determina implícitamente, en un entorno de P, tres funciones de clase  $C^1$  x=x(y,z), y=y(x,z) y z=z(x,y) donde  $\frac{\partial x}{\partial y}(b,c)\cdot\frac{\partial y}{\partial z}(a,c)\cdot\frac{\partial z}{\partial x}(a,b)=1$ .

(III) Si  $F: \mathbb{R}^2 \to \mathbb{R}^2$  es de clase  $C^1$  y  $det(\mathbb{J}_{(x,y)}F) \neq 0$  entonces F es globalmente invertible.

#### **Entonces:**

- A) Todas las afirmaciones son falsas.
- B) Todas las afirmaciones son correctas.
- C) Las afirmaciónes (I) y (II) son correctas, (III) es falsa.
- D) Solo la afirmación (I) es correcta.

#### (II) Desarrollo. Total: 72 puntos

Todo resultado teórico que utilice en la resolución de los problemas debe estar adecuadamente justificado.

#### Problema 1 (24 puntos)

Sea u un campo escalar de clase  $C^1$  en  $\mathbb{R}^3$  v sea F el campo vectorial definido por:

$$F(x, y, z) = (u(x, y, z), 1 + y^2, x^3z^2 + 1).$$

- (1) Determinar todos los campos escalares u(x, y, z) que hacen que F sea un campo conservativo en  $\mathbb{R}^3$ . (Justificar la respuesta)
- (2) Sea  $\mathcal{C}$  la curva definida por las ecuaciones:

$$y = x$$
,  $4xy + 9z^2 + xz(x - y) = 1$ .

- (a) Para  $u(x, y, z) = x^2 z^3$ , calcular la integral de F sobre el arco de  $\mathcal{C}$  que va desde el punto  $A = \left(\frac{1}{2}, \frac{1}{2}, 0\right)$  hasta el punto  $B = \left(0, 0, \frac{1}{3}\right)$ .
- (b) Se considera la superficie S formada por todos los segmentos que unen los puntos de  $\mathcal{C}$  y el punto (1,0,0) orientada de forma que su normal en el punto A tiene la primera

componente positiva. Calcular el flujo a trav´es de S del rotacional del campo vectorial H definido por:

$$H(x, y, z) = (x^2 z^3 \cos(y - x), 1 + 2xy - y^2, (y^3 z^2 + 1)e^{x - y}).$$

## Problema 2 (24 puntos)

- (1) Enunciar el teorema de la divergencia.
- (2) Sea f : R <sup>+</sup> → R una funci´on de clase C<sup>∞</sup> estrictamente mon´otona y r : Ω ⊂ R <sup>3</sup> → R definida mediante:

$$r(x, y, z) = \sqrt{x^2 + y^2}$$

Dada la funci´on f definida anteriormente, se define el campo vectorial F : Ω ⊂ R <sup>3</sup> → R 3 mediante:

$$F(x, y, z) = \nabla(f \circ r)(x, y, z)$$

Es decir F es el gradiente de la funci´on f ◦ r.

- (a) Determinar el dominio m´as amplio Ω para que F sea de clase C∞.
- (b) Determinar todas las funciones f <sup>0</sup> que hacen que div(F) = 0.
- (c) Sea S = {(x, y, z) ∈ R 3 : x <sup>2</sup> + y <sup>2</sup> = R<sup>2</sup> , 0 ≤ z ≤ 1} orientada con normal que apunta hacia su eje de simetr´ıa.

Si adem´as RR S F dS = 1. Determinar expl´ıcitamente el campo F.

## Problema 3 (24 puntos)

- (1) Sean X : U ⊂ R <sup>3</sup> → R <sup>3</sup> un campo vectorial de clase C <sup>1</sup> y f : U ⊂ R <sup>3</sup> → R un campo escalar de clase C 2 . Probar de forma directa las siguientes afirmaciones:
  - (a) rot fX = f rot X + ∇f ∧ X.
  - (b) rot ∇f = 0.
- (2) Probar que si X : U ⊂ R <sup>3</sup> → R <sup>3</sup> un campo vectorial de clase C 1 es un campo de gradientes y U es un abierto de R 3 , entonces X es irrotacional. Justificar todo resultado te´orico usado.
- (3) Vale el rec´ıproco del resultado enunciado en la parte 2? En caso afirmativo probarlo y en caso negativo construir un contraejemplo.
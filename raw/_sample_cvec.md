<!-- atlas-local: extraído de _sample_cvec.pdf con marker v1.10.2 en mps. No editar a mano. -->

*1.* Si todos los valores propios *λ*1*, . . . , λ<sup>n</sup>* de *H*(*a*) son positivos, entonces *m* = m´ın{*λ*1*, . . . , λn*} *>* 0 y podemos tomar *u* tal que 0 *< u < m*. Se sigue que los números *λ*<sup>1</sup> − *u, . . . , λ<sup>n</sup>* − *u* también son positivos. De acuerdo al lema anterior *λ*<sup>1</sup> − *u, . . . , λ<sup>n</sup>* − *u* son los valores propios de la matriz *H*(*a*) − *u* Id, y por ser todos positivos el Teorema 1.3.8 asegura que *Q*(*v*) = *v*(*H*(*a*) − *u* Id)*v <sup>t</sup> >* 0 para todo *v* 6= 0 . Observar ahora que *Q*(*v*) = *v*(*H*(*a*) − *u* Id)*v <sup>t</sup>* = *vH*(*a*)*v <sup>t</sup>* − *u*||*v* 2 || y por lo tanto tenemos *vH*(*a*)*v <sup>t</sup> > u*||*v* 2 ||. Utilizando la la fórmula de Taylor:

$$f(a+v) - f(a) > \frac{1}{2}u\|v\|^2 + r(a,v) = \|v\|^2(\frac{1}{2}u + \frac{r(a,v)}{\|v\|^2}), \quad \text{con } \lim_{v \to 0} \frac{r(a,v)}{\|v\|^2} = 0.$$

Como l´ım*v*→<sup>0</sup> *r*(*a,v*) k*v*k <sup>2</sup> = 0 existe *δ >* 0 tal que si k*v*k *< δ*, entonces | *r*(*a,v*) k*v*k <sup>2</sup> | *<* 1 2 *u* y por lo tanto si k*v*k *< δ*, entonces <sup>1</sup> 2 *u* + *r*(*a,v*) k*v*k <sup>2</sup> *>* 0. Esto prueba que si k*v*k *< δ*, entonces *f*(*a* + *v*) − *f*(*a*) *>* 0, o lo que es lo mismo que *f* tiene un mínimo relativo en *a*.

- *2.* La prueba de *2.* es totalmente análoga a la de *1.* y queda como ejercicio para el lector. **Es imprescindible hacerla para chequear que se entendió.**
- *3.* Primero observamos que si *λ* es valor propio de *H*(*a*), entonces:

$$f(a+v) - f(a) = \frac{1}{2}\lambda ||v||^2 + r(a,v) = ||v||^2 (\frac{1}{2}\lambda + \frac{r(a,v)}{||v||^2})$$
 para todo  $v \in S_\lambda$ .

En particular, existe *δ >* 0 tal que si ||*v*|| *< δ*, entonces | *r*(*a,v*) k*v*k <sup>2</sup> | *<* 1 2 *λ* y por lo tanto si ||*v*|| *< δ*, entonces el signo de *f*(*a* + *v*) − *f*(*a*) es el signo de *λ* para todo *v* ∈ *Sλ*. Se deduce que si *λ*<sup>1</sup> y *λ*<sup>2</sup> son valores propios de *H*(*a*) tales que *λ*<sup>1</sup> *>* 0 y *λ*<sup>2</sup> *<* 0, *f*(*a* + *v*) − *f*(*a*) toma valores tanto positivos como negativos en cualquier entorno de 0, es decir, que *a* es un punto silla.

## **1.3.4. Test de la derivada segunda para funciones de dos variables**

Aplicando el Teorema anteior al caso *n* = 2 se obtiene lo que se llama el "test de la derivada segunda", que consiste en mirar el signo de la derivada segunda *fxx*(*a*) y el determinante de *H*(*a*) para clasificar el punto crítico:

**Proposición 1.3.11.** *Sea f* : *D* ⊂ R <sup>2</sup> → R *con derivadas parciales de segundo orden continuas en un entorno del punto a* ∈ *D, y sea* ∆ = det(*H*(*a*))*.*

*Entonces :*

*1. Si* ∆ *<* 0*, entonces f tiene un punto silla en a.*

- *2. Si* ∆ *>* 0*, miro el signo de fxx*(*a*)*:*
  - a*) si fxx*(*a*) *>* 0*, entonces f tiene un mínimo relativo en a.*
  - b*) si fxx*(*a*) *<* 0*, entonces f tiene un máximo relativo en a.*
- *3. Si* ∆ = 0*, entonces el test no permite concluir.*

*Demostración.* Sean *λ*1*, λ*<sup>2</sup> los valores propios de *H*(*a*).

- *1.* Observemos que ∆ = *λ*1*λ*2, por lo cual si ∆ *<* 0 significa que *H*(*a*) tiene un valor propio positivo y otro negativo. Se deduce entonces que *f* tiene un punto silla en *a* directamente del teorema anterior.
- *2.* Como ∆ *>* 0, sabemos que ambos valores propios son positivos o ambos valores propios son negativos. Sabemos también que *fxx*(*a*)*fyy*(*a*) *>* (*fxy*(*a*))<sup>2</sup> ≥ 0, por lo cual *fxx*(*a*) y *fyy*(*a*) son ambos mayores o iguales a cero, o ambos menores o iguales a cero. Si *fxx*(*a*) *>* 0, entonces la traza de *H*(*a*), que vale *λ*1+*λ*<sup>2</sup> = *fxx*(*a*)+*fyy*(*a*) *>* 0 y por lo tanto los dos valores propios *λ*<sup>1</sup> y *λ*<sup>2</sup> son positivos. Se deduce del teorema anterior que *f* tiene un mínimo relativo en *a*. De igual forma, Si *fxx*(*a*) *<* 0, entonces *λ*1+*λ*<sup>2</sup> = *fxx*(*a*)+*fyy*(*a*) *<* 0 y por lo tanto los dos valores propios *λ*<sup>1</sup> y *λ*<sup>2</sup> son negativos. Se deduce del teorema anterior que *f* tiene un máximo relativo en *a*.
- *3.* Considerando las funciones *f*(*x, y*) = *x* <sup>3</sup> − 3*xy*<sup>2</sup> y *g*(*x, y*) = *x* 2*y* 2 , observamos que el determinante de las matrices Hessianas en ambos casos es cero en el origen, pero sin embargo *f* tiene un punto silla en el origen, y *g* un mínimo en el origen.
- **Ejemplos 1.3.1.** 1. Estudiar los puntos críticos de *f*(*x, y*) = *x* <sup>3</sup> + *y* <sup>3</sup> − 9*xy*. Primero veamos como queda el gradiente de *f*: *f<sup>x</sup>* = 3*x* <sup>2</sup> − 9*y*, *f<sup>y</sup>* = 3*y* <sup>2</sup> − 9*x*. Resolviendo ∇*f* = 0 se obtienen los puntos críticos (0*,* 0), (3*,* 3). Para clasificarlos hallemos la matriz *H* en cada caso.

$$H = \begin{pmatrix} f_{xx}(a) & f_{xy}(a) \\ f_{xy}(a) & f_{yy}(a) \end{pmatrix} = \begin{pmatrix} 6x & -9 \\ -9 & 6y \end{pmatrix}.$$

En el punto (0*,* 0), *H* = 0 −9 <sup>−</sup>9 0 ! ⇒ det *H <* 0 ⇒ (0*,* 0) es punto silla. En el punto (3*,* 3), *H* = 18 −9 <sup>−</sup>9 18 ! ⇒ det *H >* 0, como *fxx* = 18 *>* 0 entonces (3*,* 3) es un mínimo relativo.

2. Estudiar los puntos críticos de *f*(*x, y*) = *x* <sup>3</sup> −3*xy*<sup>2</sup> . Veamos como queda el gradiente de *f*, *f<sup>x</sup>* = 3*x* <sup>2</sup> − 3*y* 2 , *f<sup>y</sup>* = −6*xy*. Entonces (0*,* 0) es el único punto crítico. En (0*,* 0),

$$H = \left(\begin{array}{cc} 0 & 0 \\ 0 & 0 \end{array}\right) .$$

En este caso el criterio no identifica el tipo de punto. Sin embargo, un argumento directo nos muestra que no es un extremo: *f*(*x,* 0) = *x* 3 , por lo tanto *f* toma valores positivos negativos en todo entorno de (0*,* 0) y *f*(0*,* 0) = 0.

3. Consideremos *f*(*x, y*) = *x* <sup>2</sup> + *y* 2 (*x* + 1)<sup>3</sup> , su gradiente es ∇*f*(*x, y*) = *fx, f<sup>y</sup>* = 2*x* + *y* <sup>2</sup>3(*x* + 1)<sup>2</sup> *,* 2*y*(*x* + 1)<sup>3</sup> , que si es nulo entonces 2*y*(*x* + 1)<sup>3</sup> = 0 ⇒ *y* = 0 o *x* = −1. Si *y* = 0 ⇒ 2*x* = 0 ⇒ *x* = 0*.* Si *x* = −1 ⇒ *fx*(−1*, y*) = −2 6= 0, por lo tanto el único punto crítico es (0*,* 0). Clasifiquémoslo:

$$H(x,y) = \begin{pmatrix} 2 + y^2 6(x+1) & 6y(x+1)^2 \\ 6y(x+1)^2 & 2(x+1)^3 \end{pmatrix} \Rightarrow H(0,0) = \begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}$$

Por lo tanto (0*,* 0) es un mínimo relativo, sin embargo no es absoluto ya que *f* −2*,* √ 5 *< f*(0*,* 0).

## **1.3.5. Extremos Absolutos**

Ya se dio la definición anteriormente (Definición 1.2.1). Un caso particular en que se puede asegurar la existencia de extremos (máximo y mínimo) absolutos es cuando el dominio *D* es compacto y la función es continua (teorema de Weierstrass). Supondremos, en lo que sigue, *f* diferenciable. Como ya se dijo, un extremo absoluto que se da en un punto interior es también relativo, y por lo tanto un punto crítico. Si se quiere entonces encontrar los extremos absolutos de una función diferenciable en un dominio *D* compacto, basta entonces estudiar:

- 1. Los puntos críticos (que estarán en el interior de *D*).
- 2. La frontera de *D*.

**Ejemplo 1.3.7.** Consideremos la función *f* : *D* ⊂ R <sup>2</sup> → R dada por

$$f(x,y) = x^2 + y^2 - xy - x - y,$$

donde *D* = (*x, y*) : *x* ≥ 0*, y* ≥ 0*, x* + *y* ≤ 3 .

El dominio es el triángulo de vértices *O* = (0*,* 0), *A* = (3*,* 0) y *B* = (0*,* 3).

**Puntos críticos**: *f<sup>x</sup>* = 2*x* − *y* − 1 = 0 y *f<sup>y</sup>* = 2*y* − *x* − 1 entonces punto crítico interior a *D*: (1*,* 1), además *f*(1*,* 1) = −1.

**Frontera**: Hay que estudiar que pasa en cada lado del triángulo.

- Lado *OA*, 0 ≤ *x* ≤ 3, *y* = 0, *f*(*x,* 0) = *x* <sup>2</sup> − *x*, *f*(*x,* 0)<sup>0</sup> = 2*x* − 1, *f*(0*,* 0) = 0, *f* 1 2 *,* 0 = − 1 4 y *f*(3*,* 0) = 6. Entonces
  - El máximo de *f* en *OA* se da en *A* y vale 6.

- El mínimo de f en OA se da en  $(\frac{1}{2})$  y vale  $-\frac{1}{4}$ .
- $\blacksquare$  Lado OB, es igual al caso anterior sustituyendo x por y. Entonces
  - El máximo de f en OB se da en B y vale 6.
  - El mínimo de f en OB se da en  $(0, \frac{1}{2})$  y vale  $-\frac{1}{4}$ .
- Lado AB,  $0 \le x \le 3$ , y = 3 x,  $f(x, 3 x) = 3(x^2 3x + 2)$ . Su deivada es 6x 9, se anula en  $x = \frac{3}{2}$ , f(0,3) = 6, f(3,0) = 6 y  $f(\frac{3}{2}, \frac{3}{2}) = -\frac{3}{4}$ .
  - El máximo de f en AB se da en A y B y vale 6.
  - El mínimo de f en AB se da en  $(\frac{3}{2}, \frac{3}{2})$  y vale  $-\frac{3}{4}$ .

Se sabe que f tiene máximo y mínimo absoluto en D. Luego debe ser alguno de los puntos encontrados. Comparando, se obtiene que

- Máximo absoluto de f en D: 6 en los puntos A y B.
- Mínimo absoluto de f en D: -1 en el punto (1,1).

## 1.4. Función inversa

Recordemos que dado un conjunto A, la función  $id_A:A\to A$  es la identidad en A definida por  $id_A(x)=x$  para todo  $x\in A$ .

**Definición 1.4.1.** Se dice que un campo  $F: D(\subset \mathbb{R}^n) \to \mathbb{R}^n$  es **localmente invertible** en a interior a D, si existen entornos U y V de a y F(a) respectivamente, tales que  $F|_U: U \to V$  es biyectiva, o sea que existe  $F^{-1}: V \to U$ , con  $F \circ F^{-1} = id_V$  y  $F^{-1} \circ F = id_U$ . Nótese que V = F(U).

Por ejemplo,  $F(x,y) = (\sin x, \sin y)$  es localmente invertible en (0,0), pero  $G(x,y) = (x^2,y)$  no lo es, ya que  $G(-\varepsilon,y) = G(\varepsilon,y)$  por más chico que sea  $\varepsilon$ , por lo tanto g no puede ser inyectiva en ningún entorno de (0,0).

Si tenemos una función f(x) de una variable, de clase  $C^1$  con  $f'(x_0) \neq 0$ , sabemos que existe una función inversa  $x = f^{-1}(y)$  definida en un entorno de  $y_0 = f(x_0)$ . Además,  $f^{-1}$  es derivable en  $y_0$  y  $(f^{-1})'(y_0) = \frac{1}{f'(x_0)}$ .

La condición  $f'(x_0) \neq 0$  anterior equivale a pedir que  $f'(x_0)$  tenga inverso o que  $df_{x_0}$  sea una transformación lineal invertible.

Si pensamos ahora en el campo  $F: \mathbb{R}^n \to \mathbb{R}^n$  parece natural exigir que  $J_F(a)$  sea una matriz  $n \times n$  invertible, lo que equivale a decir que  $dF_a$  es invertible.

En este sentido tenemos el siguiente teorema.

**Teorema 1.4.2** (de la función inversa). Sea  $F: D(\subset \mathbb{R}^n) \to \mathbb{R}^n$  de clase  $C^k$ , a interior a D,  $J_F(a)$  invertible. Entonces F es localmente invertible y su inversa  $F^{-1}$  es de clase  $C^k$ . Además

$$J_{F^{-1}}(F(a)) = (J_F(a))^{-1}.$$

**Ejemplo 1.4.1** (Una inversa global). Consideremos la función  $F: \mathbb{R}^2 \to \mathbb{R}^2$  dada por

$$F(x,y) = (x, x^2 + y).$$

En este caso podemos hallar la función inversa, ya que

$$\begin{cases} u = x \\ v = x^2 + y \end{cases}$$

Entonces es fácil despejar x e y para obtener:

$$\begin{cases} x = u \\ y = v - u^2 \end{cases}$$

Lo cual define a la función inversa  $F^{-1}$ . En este contexto podemos decir que F posee una inversa global en todo el plano. Observemos que el Jacobiano de F es

$$\det \left( \begin{array}{cc} \frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} \end{array} \right) = \det \left( \begin{array}{cc} 1 & 0 \\ 2x & 1 \end{array} \right) = 1.$$

Lo cual es coherente con la existencia de una inversa diferenciable en todo punto. También podemos verificar la relación de las matrices Jacobianas.

$$J_F(x,y) = \left(\begin{array}{cc} 1 & 0\\ 2x & 1 \end{array}\right)$$

У

$$J_{F^{-1}}(F(x,y)) = \begin{pmatrix} 1 & 0 \\ -2x & 1 \end{pmatrix}.$$

Es inmediato verificar que  $J_F(x,y)J_{F^{-1}}(F(x,y))=I$ .

**Ejemplo 1.4.2.** Consideremos la función  $F: \mathbb{R}^2 \to \mathbb{R}^2$  dada por  $F(x,y) = (e^x \cos y, e^x \sin y)$ . La matriz Jacobiana de F es

$$J_F(x,y) = \begin{pmatrix} e^x \cos y & -e^x \sin y \\ e^x \sin y & e^x \cos y \end{pmatrix}.$$

La misma es invertible  $\forall (x,y) \in \mathbb{R}^2$  ya que det  $J_F(x,y) = e^{2x} \neq 0$ . Por lo tanto existe una inversa local en un entorno de cualquier punto. Sin embargo, es evidente que no puede existir una inversa global, porque el punto  $(x_0, y_0)$  y el punto  $(x_0, y_0 + 2\pi)$  tienen la misma
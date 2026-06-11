<!-- atlas-local: extraído de examenfebrero2024-solucion.pdf con marker v1.10.2 en cuda. No editar a mano. -->

## Universidad de la República Facultad de Ingeniería - IMERL

Cálculo Vectorial Febrero 2024

EXAMEN – SÁBADO 6 DE FEBRERO DE 2024

Ejercicio 1.(20 pts.)

Se considera el campo  $f(x,y) = (\sin(y) - y\sin(x) + x,\cos(x) + x\cos(y) + y)$ .

- (1) Determinar si f es un campo de gradientes en  $\mathbb{R}^2$ .
- (2) Si f es un gradiente, encontrar la correspondiente función potencial. Si f no es un gradiente, demuéstrelo.

**Solución:** Como el dominio considerado es  $\mathbb{R}^2$  que es simplemente conexo, es equivalente verificar si el campo es irrotacional. Llamemos f(x,y) = (P(x,y),Q(x,y))

$$Q_x = -\sin(x) + \cos(y)P_y = \cos(y) - \sin(x)$$

Como f es irrotacional, concluimos que es de gradientes en  $\mathbb{R}^2$ .

Para hallar un potencial escalar buscamos una  $g: \mathbb{R}^2 \to \mathbb{R}$  tal que  $\nabla g(x,y) = (g_x,g_y) = (P,Q)$ 

Igualando la primer coordenada e integrando respecto de x obtenemos:

$$g(x,y) = x\sin(y) + y\cos(x) + \frac{x^2}{2} + C(y)$$

donde  $C: \mathbb{R} \to \mathbb{R}$  cumple que derivando toda la expresión respecto de y e igualando a Q:

$$x\cos(y) + \cos(x) + C'(y) = \cos(x) + x\cos(y) + y$$

Despejando obtenemos

$$C'(y) = y$$

Por lo que basta tomar

$$C(y) = \frac{y^2}{2}$$

Por último sustituyendo obtenemos el potencial escalar buscado:

$$g(x,y) = x\sin(y) + y\cos(x) + \frac{x^2 + y^2}{2}$$

**Ejercicio 2.**(30 pts.) Se considera  $f:D\subset\mathbb{R}^n\to\mathbb{R}$  diferenciable en el punto a interior a D conderivadas parciales de segundo orden continuas en un entorno de a.

- (1) Escribir la fórmula de Taylor de segundo orden para f en el punto a.
- (2) Sea  $f(x,y) = x^3 6x^2 3y^2$ . Clasifique los puntos críticos de f.
- (3) Encontrar los puntos de la superficie  $x^2 yz = 1$  más cercanos al origen.

## Soluci´on:

(a) <sup>f</sup>(<sup>a</sup> <sup>+</sup> <sup>v</sup>) <sup>−</sup> <sup>f</sup>(a) = dfa(v) + <sup>1</sup> 2 d 2 fa(v) + ra(v),

donde lim v→0 ra(v) k v k 2 = 0 para todo v con norma suficientemente peque˜na.

(b) Puntos cr´ıticos: ∇f(x, y) = 0 ⇔ 3x <sup>2</sup> − 12x, −6y = (0, 0) ⇔ 3x(x − 4) = 0, y = 0. Entonces los puntos cr´ıticos son: (0, 0),(4, 0). Clasificaci´on de los puntos cr´ıticos:

$$H_f(x,y) = \begin{pmatrix} 6x - 12 & 0\\ 0 & -6 \end{pmatrix}$$

- <sup>H</sup><sup>f</sup> (0, 0) = −12 0 0 −6 ! ⇒ f tiene en (0, 0) un m´aximo relativo.
- <sup>H</sup><sup>f</sup> (4, 0) = 12 0 0 −6 ! ⇒ f tiene en (4, 0) un punto silla.
- (c) La funci´on que queremos minimizar es la distancia al origen condicionada a la superficie

$$S = \{(x, y, z) \in \mathbb{R}^3 : x^2 - yz = 1\}.$$

Recordemos que, como la funci´on ra´ız cuadrada es creciente, podemos tomar la distancia al cuadrado para encontrar los puntos m´as cercanos al origen. Sea f(x, y, z) = x <sup>2</sup> + y <sup>2</sup> + z 2 .

La funci´on g(x, y, z) = x <sup>2</sup> − yz − 1 es la que define la superficie S. Observemos que tanto f como g son funciones C∞. Para estar en las hip´otesis del teorema de multiplicadores de Lagrange tenemos que estudiar que pasa con ∇g.

∇g(x, y, z) = 2x, −z, −y = (0, 0, 0) ⇔ (x, y, z) = (0, 0, 0), pero este punto no est´a en S. Por lo tanto podemos usar el teorema para encontrar los candidatos.

$$\nabla f(x,y,z) = \lambda \nabla g(x,y,z) \Leftrightarrow 2(x,y,z) = \lambda (2x,-z,-y) \Leftrightarrow \begin{cases} 2(\lambda-1)x & = & 0 \\ 2y & = & -\lambda z \\ 2z & = & -\lambda y \end{cases}$$

$$(\lambda - 1)x = 0 \Leftrightarrow x = 0 \text{ o } \lambda = 1.$$

- Si λ = 1 : 2y = −z y 2z = −y ⇒ y = z = 0. (x, 0, 0) ∈ S ⇒ x <sup>2</sup> = 1 ⇒ x = ±1 ⇒ (1, 0, 0),(−1, 0, 0).
- Si x = 0: observar que (0, y, z) ∈ S ⇔ yz = −1 ⇒ y 6= 0, z 6= 0. Por lo tanto

$$\lambda = -2\frac{y}{z} = -2\frac{z}{y} \Rightarrow y^2 = z^2 \Rightarrow \begin{cases} z = y \\ z = -y \end{cases}$$

Si y = z ⇒ −1 = yz = y <sup>2</sup> no existe soluci´on.

Si 
$$y = -z \Rightarrow -1 = yz = -y^2 \Rightarrow y = \pm 1 \Rightarrow (0, 1, -1), (0, -1, 1).$$

Evaluemos la funci´on f en los cuatro puntos:

$$f(1,0,0) = f(-1,0,0) = 1, f(0,1,-1) = f(0,-1,1) = 2.$$

Veamos que se da un mínimo en los puntos (1,0,0) y (-1,0,0): Sea  $(x,y,z) \in S$  entonces  $x^2 - yz = 1 \Rightarrow x^2 = 1 + yz$ .

$$f(x,y,z) = x^2 + y^2 + z^2 = (1+yz)^2 + y^2 + z^2 = 1 + 2yz + y^2z^2 + y^2 + z^2 = 1 + (y+z)^2 + y^2z^2 \ge 1.$$

Entonces  $f(x, y, z) \ge 1$  para todo  $(x, y, z) \in S$ . Por lo tanto se da el mínimo en los puntos (1, 0, 0) y (-1, 0, 0).

**Ejercicio 3.** (20 pts.) Sea R el rectángulo en el plano xy de vértices (0,0), (0,2), (3,2) y (3,0). Sea  $f(x,y)=\frac{2}{3}x^{\frac{3}{2}}$ . Hallar el área del gráfico de  $f|_R$ .

## Solución:

 $R = [0;3] \times [0;2] \subset \mathbb{R}^2$  y sea  $S = \{(x,y,f(x,y)) \in \mathbb{R}^3 \mid (x,y) \in R\}$  el gráfico de  $f(x,y) = \frac{2}{3}x^{3/2}$ . Entonces  $\Phi: R \to S$  dada por  $\Phi(x,y) = (x,y,\frac{2}{3}x^{3/2})$  es una parametrización de S.

$$\text{Área}(S) = \int_{S} dA = \int \int_{R} \|\partial_{x} \Phi \times \partial_{y} \Phi\| \, dx dy 
 = \int_{0}^{2} \int_{0}^{3} \| \left( 1, 0, x^{1/2} \right) \times (0, 1, 0) \| \, dx dy 
 = \int_{0}^{2} \int_{0}^{3} \| \left( -x^{1/2}, 0, 1 \right) \| \, dx dy 
 = \int_{0}^{2} \int_{0}^{3} (x+1)^{1/2} \, dx dy 
 = 2\frac{2}{3} (x+1)^{3/2} |_{0}^{3} 
 = \frac{4}{2} (2^{3} - 1) = \frac{28}{2}$$

**Ejercicio 4.** (20 pts.) Sea S la esfera  $x^2 + y^2 + z^2 = 4$ , y sea F(x, y, z) = (3x, 4y, 5z). Calcular  $\iint_S F \cdot n$ , donde n es la normal saliente.

Solución: Primero observamos que estamos en las hipótesis del Teorema de Gauss pues el campo es  $C^1$  en  $\mathbb{R}^3$ , por lo tanto si consideramos V la región acotada por la esfera S tenemos:

$$\iint_{S} F \cdot n = \iiint_{V} div(F) = 12vol(V) = 12\frac{4}{3}\pi 2^{3} = 128\pi$$

**Ejercicio 5.** (10 pts.) Se considera el paraboloide de ecuación  $z = x^2 + y^2$  orientado con la normal apuntando hacia abajo (coordenada z negativa). Sea C la curva resultante de la intersección del paraboloide con el plano de ecuación z = 2x, orientada como borde de la porción de paraboloide debajo del plano z = 2x. Sea F(x, y, z) = (z, x, y). Calcular  $\int_C F$ .

**Solución:** Observamos primero que estamos en las hipótesis del Teorema de Stokes pues el campo es  $C^1$  en  $\mathbb{R}^3$ . Por lo tanto podemos aplicar el teorema mirando la curva C como borde de la porción de plano que acota S y obtener:  $\int_C F = \int_S rot(F) \cdot n$ , y teniendo en cuenta la orientación dada, debemos considerar  $n = \frac{(2,0,-1)}{\sqrt{5}}$ , por lo tanto:

$$\int_{C} F = \int_{S} rot(F) \cdot n = \int_{S} (1, 1, 1) \cdot \frac{(2, 0, -1)}{\sqrt{5}} = \frac{area(S)}{\sqrt{5}}$$

Ahora basta observar que S es la imagen del disco D de centro (1,0) y radio 1 en el plano xy por la parametrización  $\varphi(x,y)=(x,y,2x)$ . Calculamos entonces el área de S utilizando la fórmula: área $(S)=\int_D ||\varphi_x\wedge\varphi_y||dudv=\int_D \sqrt{5}dudv=\sqrt{5}area(D)=\sqrt{5}\pi$ . Concluimos entonces que

$$\int_C F = \pi$$
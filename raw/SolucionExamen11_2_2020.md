<!-- atlas-local: extraído de SolucionExamen11_2_2020.pdf con marker v1.10.2 en cuda. No editar a mano. -->

(I) 1. Calculemos el rotor de Q, para esto, si  $T: \mathbb{R}^2 \to \mathbb{R}^2$  es  $T(x,y) = (x-x_0,y-y_0) = (t_1(x,y),t_2(x,y))$  entonces  $Q=F\circ T$ . Denotemos F(x,y)=(M(x,y),N(x,y)), entonces  $Q=(M\circ T,N\circ T)$  por lo cual de la regla de la cadena se tiene:

$$\frac{\partial N \circ T}{\partial x}(x,y) = \frac{\partial N}{\partial x}(x-x_0,y-y_0)\frac{\partial t_1}{\partial x}(x,y) + \frac{\partial N}{\partial y}(x-x_0,y-y_0)\frac{\partial t_2}{\partial x}(x,y) = \frac{\partial N}{\partial x}(x-x_0,y-y_0)$$

análogamente se tiene  $\frac{\partial M \circ T}{\partial y}(x,y) = \frac{\partial M}{\partial y}(x-x_0,y-y_0)$ . Se concluye que

rot 
$$Q(x, y) = \text{rot } F(x - x_0, y - y_0) = 0$$

- 2. El mapa T es una traslación, por lo cual el campo Q en un punto (x,y) es el valor del campo F en el punto trasladado. El campo de vectores Q se verá igual que el campo F pero trasladado un vector  $(x_0, y_0)$ .
- 3. El campo G es de gradientes, esto se puede ver de al menos dos formas. La primera es calcular un potencial escalar, es decir, hallar una función  $f: \mathbb{R}^2 \{0\} \to \mathbb{R}$  de clase  $C^1$  tal que  $\nabla f = G$ . Para esto debe cumplirse

$$\begin{cases} \frac{\partial f}{\partial x} = -\frac{x}{x^2 + y^2} \\ \frac{\partial f}{\partial y} = -\frac{y}{x^2 + y^2} \end{cases}$$

de la primera ecuación se sigue que  $f(x,y) = -\frac{1}{2}\ln(x^2 + y^2) + g(y)$ , ahora derivando esto respecto a y se tiene  $\frac{\partial f}{\partial y} = \frac{-y}{x^2 + y^2} + g'(y)$ , entonces usando la segunda ecuación en los corchetes se sigue que g'(y) = 0 soluciona, en resumen se tiene que  $f(x,y) = -\frac{1}{2}\ln(x^2 + y^2)$  cumple con la ecuación del gradiente, además es de clase  $C^1$  en  $\mathbb{R}^2 - \{0\}$  mostrando que es un potencial escalar de G. De ser de gradientes se sigue que el campo es irrotacional.

Alternativamente, uno podía chequear primero que el campo es irrotacional, esto es una cuenta. Luego como el campo es irrotacional una aplicación de Stokes era ver que

$$\int_{\mathcal{C}} X \ dl = nI_0$$

siendo n la cantidad de vueltas de  $\mathcal{C}$  al 0 y  $I_0 = \int_S X \ dl$  con S la circunferencia de centro 0 y radio 1. Se puede ver que  $I_0 = 0$  tanto geométricamente como analíticamente, por lo cual se concluye que  $\int_{\mathcal{C}} X \ dl = 0$  para toda curva  $\mathcal{C}$ , por lo cual el campo es de gradientes. Lo importante de este argumento es ver que la circulación es 0 para toda curva!, no alcanza verficarlo solo con algunas curvas nomas.

¿Es condición necesaria que el dominio de un campo irrotacional sea simplemente conexo para que sea de gradientes?

El G anterior es un ejemplo de un campo irrotacional en un dominio que no es simplemente conexo y que termina siendo de gradientes, por lo cual no es condición necesaria que el dominio sea simplemente conexo. Lo que es cierto es que es una condición suficiente.

- 4. Ver teórico.
- 5. La mejor forma de entender el campo es observar que X(x,y) = G(x-10,y) + G(x+10,y), pero aún sin ver esto: Si uno comienza calculando X(0,y) observa que a lo largo del eje y el campo tiene dirección vertical y siempre apuntando hacia el origen. Respecto al módulo, el mismo vale 0 en el origen, y hacia el infinito tiende a 0. Si uno se ponía fino aquí puede

verse que para y ≥ 0 el módulo parte de 0 y va creciendo hasta un cierto máximo y luego decrece a 0 al irse a innito. Observando X(0, x) uno ve que los vectores a lo largo del eje x son horizontales y siempre apuntan al punto que tienen más cerca entre (−10, 0) y (10, 0), como si se tratase de la lucha entre dos fuerzas. Respecto al módulo, hacia el innito decrece, para |x| < 10 el mismo va decreciendo al ir acercándose al origen. Con las observaciones vistas el bosquejo hasta el momento va:

![](_page_1_Picture_1.jpeg)

> **Figura:** La figura muestra un diagrama de flujo bidimensional con ejes x e y marcados a ambos lados del centro. Las flechas horizontales representan el flujo en la dirección x, mientras que las flechas verticales indican el flujo en la dirección y. Los valores -40 y 40 probablemente representen los límites de los ejes respectivos, lo cual sugiere un rango de variación para cada dirección del flujo.

Figura 1: Construyendo el bosquejo de X. Este bosquejo fue extraído de un examen.

La clave para terminar de entender el campo es ver que X(x, y) = G(x−10, y)+G(x+10, y), entonces para entender el campo X vale la pena entender el campo G, el campo G es bastante más simple, el mismo es radial, hacia adentro con centro en el origen, su módulo va creciendo a medida que el radio se acerca a 0, el mismo luce como se ve en la gura:

![](_page_1_Picture_4.jpeg)

> **Figura:** Esta figura muestra un diagrama de flujo vectorial con dos curvas representadas: \(y = x\) y \(y = -x\), ambas pasando por el origen \((0, 0)\). Las flechas indican la dirección del flujo en cada punto, sugiriendo una relación lineal entre las variables \(x\) e \(y\), con valores clave que se pueden interpretar como pendientes positiva y negativa respectivamente.

Figura 2: Bosquejo del campo Q. Este bosquejo fue extraído de un examen.

Ahora por la parte 2. el campo X es la superposición del campo G trasladado en (−10, 0) y (10, 0). Como el módulo de G tiende a innito a medida que (x, y) se acerca al origen podemos decir que en un entorno sucientemente chico de (−10, 0) el campo X luce prácticamente igual que G(x + 10, y). Análogamente en el entorno de (10, 0). Entonces juntado lo hecho

![](_page_1_Figure_7.jpeg)

> **Figura:** Esta figura muestra un diagrama de flujo de vectores en el plano cartesiano, con ejes x e y marcados. Las líneas punteadas representan las rectas \(y = -x + 10\), \(y = x + 10\), \(y = -x - 10\) y \(y = x - 10\). Los vectores indican la dirección del flujo en cada punto, sugiriendo una distribución simétrica alrededor de los ejes.

Figura 3: Bosquejando X

Finalmente evaluando el campo en algunos puntos más o estudiando más detenidamente como cambia el campo en los distintos cuadrantes, se llega a un bosquejo del estilo:

![](_page_2_Picture_1.jpeg)

> **Figura:** Esta figura muestra un diagrama de flujo de líneas de corriente o vectores de velocidad en un sistema bidimensional. Las flechas representan la dirección y magnitud del flujo, con curvas que indican cambios en el flujo a lo largo de las líneas horizontales. Los valores clave se encuentran en los extremos de las líneas horizontales, posiblemente representando condiciones o parámetros específicos del sistema.

Figura 4: Bosquejo del campo X. Este bosquejo fue extraído de un examen.

- 6. De forma análoga a como se probo 1., se tiene que G(x − x0, y − y0) es de gradientes si G lo es. Entonces X es de gradientes. Siendo de gradientes se puede cambiar la curva de la letra por cualquier curva que comience en (0, −10) a (0, 10). Una curva fácil es el segmento vertical de (0, −10) a (0, 10), a lo largo de esta curva se observa que el campo y la velocidad apuntan en el mismo sentido en (0, y) con y < 0, y con iguales módulos pero en sentido contrario para (0, −y), por lo cual el aporte del campo a la circulación se cancela, dando una circulación de 0.
- (II) 1. (a) Ver Teórico
  - (b) Sea n la normal del plano π, entonces tomando la denición intrínseca del rotor con las curvas γ<sup>n</sup> se tiene que

$$\langle \operatorname{rot} X(p), n \rangle = \lim_{n \to \infty} \frac{1}{A_n} \int_{\gamma_n} X \cdot dl$$

pero por letra R γn X · dl = 0 ∀n entonces la sucesión en el límite anterior vale 0 para todo n, en particular el límite vale 0 probando que la componente del rotor que es normal al plano es nula.

- 2. (a) Sí es posible, por ejemplo con el campo F de la sugerencia tomando p = 0, y C<sup>r</sup> la circunferencia de centro 0 y radio r, entonces es fácil ver que la circulación es no nula para todo r. Esto se podía vericar tanto analíticamente como geometricamente. Entonces en resumen hemos encontrado curvas arbitrariamente pequeñas (al tomar r sucientemente chico) donde la circulación no es 0.
  - (b) Sí se modica. Llamemosle D<sup>r</sup> al disco de la letra, entonces si tomo curvas (αn) sucientemente pequeñas tal que Im α<sup>n</sup> ⊂ D ∀n entonces por Stokes se sigue que

$$\int_{\alpha_n} X \cdot dl = \iint_{\text{int } \gamma_n} \text{rot } X \, dx dy = 0$$

pues rot X ≡ 0 en int γ<sup>n</sup> ⊂ D.

(c) En esta parte había al menos dos argumentos posibles. El primero es utilizando la interpretación intrínseca del rotor: Sea γ una curva cualquiera entorno a p, haciendo homotecias de valor 1/n y centro en p se consigue una sucesión γ<sup>n</sup> de curvas que tienden a p en el sentido que todas tienen a p en su interior y diam  $\gamma_n \to 0$ . Por la interpretación intrínseca se sigue que lím  $\frac{1}{A_n} \int_{\gamma_n} X \cdot dl = \operatorname{rot} X(p) \neq 0$ , y por lo tanto existe m tal que

$$\frac{1}{A_m} \int_{\gamma_m} X \cdot dl \neq 0 \Rightarrow \int_{\gamma_m} X \cdot dl \neq 0$$

lo cual dice que si se achica  $\gamma$  lo suficiente entonces habra circulación.

Otro argumento es utilizar Stokes y continuidad: sin perdida de generalidad supongamos que rot X(p) > 0, entonces por continuidad existe  $B(p, \delta)$  tal que Rot X(q) >Rot  $X(p)/2 \ \forall q \in B(p, \delta)$ . Ahora si  $\gamma$  es una curva cerrada simple cualquiera con p en su interior, recorrida en sentido antihorario y tal que diam $(\gamma) < \delta/2$  entonces es claro que Im  $\gamma \subset B(p, \delta)$  y entonces

$$\int\limits_{\gamma} X \cdot dl = \iint\limits_{\text{int } \gamma} \text{rot} X(x,y) \ dxdy > A(\text{int } \gamma) \text{rot} X(p)/2 > 0 \Rightarrow \int\limits_{\gamma} X \cdot dl \neq 0$$

donde  $A(\text{int }\gamma)$  es el área en el interior de la curva  $\gamma$ . Para curvas recorridas con sentido horario el razonamiento es igual, también es igual para el caso en que rot X(p) < 0.
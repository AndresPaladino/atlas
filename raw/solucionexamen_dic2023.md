<!-- atlas-local: extraído de solucionexamen_dic2023.pdf con marker v1.10.2 en cuda. No editar a mano. -->

EXAMEN – SÁBADO 16 DE DICIEMBRE DE 2023

## SOLUCIÓN

#### Ejercicio 1.(40 pts.)

Se considera la función tan :  $(-\pi/2,\pi/2) \to \mathbb{R}, \ \tan(x) = \frac{sen(x)}{cos(x)}$ 

- (1) Demostrar que la función tan es invertible.
- (2) Se considera arctan :  $\mathbb{R} \to (-\pi/2, \pi/2)$  la función inversa de tan. Demostrar que arctan' $(x) = \frac{1}{1+x^2}$  para todo  $x \in \mathbb{R}$ .
- (3) Se considera la función  $f(x,y) = \arctan(y/x)$ . Hallar  $\nabla f(x,y)$  para todo (x,y) en el dominio de f.
- (4) Se consideran los abiertos de  $\mathbb{R}^2$ :

$$U = \{(x, y) \in \mathbb{R}^2 : (x, y) \neq (0, 0)\},\$$

$$V = \{(x, y) \in \mathbb{R}^2 : x > 0\},\$$

y el campo  $F(x,y)=(\frac{-y}{x^2+y^2},\frac{x}{x^2+y^2}).$ 

- (a) Es F de gradientes en U? Justifique su respuesta.
- (b) Es F de gradientes en V? Justifique su respuesta.

## Solución:

- (1) Hay que probar que es inyectiva y sobreyectiva. Para ver que es inyectiva, calculamos su derivada:  $\frac{\cos^2(x)+\sin^2(x)}{\cos^2(x)}=\frac{1}{\cos^2(x)}$ . Como  $\cos^2(x)>0$  en  $(-\pi/2,\pi/2)$ , tan es monótona estrictamente creciente, y por lo tanto es inyectiva. Para probar que es sobreyectiva, hay que probar que toma todos los valores reales. Esto se hace calculando los límites  $\lim_{x\to\pi/2^-}\tan(x)=+\infty, \lim_{x\to-\pi/2^+}\tan(x)=-\infty$  y aplicando el teorema del valor medio para funciones continuas. Si queremos probar que la función tan toma el valor  $y\in\mathbb{R}$ , sabemos por el cálculo de límites que hicimos que existen  $x_1,x_2\in(-\pi/2,\pi/2)$  tales que  $\tan(x_1)< y$  y  $\tan(x_2)> y$ . Ahora observamos que la función tan es continua en  $[x_1,x_2]$  y por lo tanto toma todos los valores comprendidos entre  $\tan(x_1)$  y  $\tan(x_2)$ . En particular, existe  $x\in(-\pi/2,\pi/2)$  tal que f(x)=y, y la función es sobreyectiva.
- (2) Por definición de función inversa, tenemos que  $\tan(\arctan(x)) = x$  para todo  $x \in \mathbb{R}$ . Utilizando la regla de la cadena,  $\tan'(\arctan(x))\arctan'(x) = 1$  para todo  $x \in \mathbb{R}$ . Por lo tanto,  $\arctan'(x) = \frac{1}{\tan'(\arctan(x))} = \cos^2(\arctan(x))$ . Para saber cuánto da  $\cos^2(\arctan(x))$  tenemos que hacer aparecer la función tan por lo cual escribimos  $\cos^2(\arctan(x)) = 1 \sin^2(\arctan(x))$  y a su vez  $\sin^2(\arctan(x)) = \frac{\sin^2(\arctan(x))}{\cos^2(\arctan(x))} \cos^2(\arctan(x)) = \tan^2(\arctan(x)) \cos^2(\arctan(x)) = \cot^2(\arctan(x))$

x 2 cos<sup>2</sup> (arctan(x)). Concluimos que cos<sup>2</sup> (arctan(x)) = 1 − x 2 cos<sup>2</sup> (arctan(x)), o equivalentemente, cos<sup>2</sup> (arctan(x)) = arctan<sup>0</sup> (x) = <sup>1</sup> 1+x<sup>2</sup> .

- (3) Utilizando la parte anterior y la regla de la cadena, se obtiene ∇f(x, y) = ( <sup>−</sup><sup>y</sup> x2+y 2 , x x2+y <sup>2</sup> ) para todo (x, y) en el dominio de f.
- (4) (a) Sabemos que F no es de gradientes en U pues existe una curva cerrada C contenida en U tal que R C F 6= 0. De hecho, cualquier curva cerrada simple en U que contenga al 0 en la componente acotada de su complemento tiene esta propiedad. Por lo tanto, F no puede ser de gradientes.
  - (b) F es de gradientes en V puesto que V est´a contenido en el dominio de la funci´on f(x, y) = arctan(y/x), por lo tanto, por el c´alculo de la parte anterior, la funci´on f es un potencial escalar para F en V , es decir, F(x, y) = ∇f(x, y) para todo (x, y) ∈ V.

Ejercicio 2.(20 pts.) Se considera f : D ⊂ R <sup>n</sup> → R diferenciable en el punto a interior a D con derivadas parciales de segundo orden continuas en un entorno de a.

- (1) Escribir la f´ormula de Taylor de segundo orden para f en el punto a.
- (2) Sea f(x, y) = x <sup>2</sup> − 2xy + 1 3 y <sup>3</sup> − 3y. Encuentre y clasifique los puntos cr´ıticos de f en D = R 2 .

# Soluci´on:

(1) <sup>f</sup>(<sup>a</sup> <sup>+</sup> <sup>v</sup>) <sup>−</sup> <sup>f</sup>(a) = <sup>d</sup>af(v) + <sup>1</sup> 2 d 2 fa(v) + r(a, v), donde limv→<sup>0</sup> r(a,v) kvk <sup>2</sup> = 0 y ||v|| es suficientemente peque˜na.

(2) fx(x, y) = 2x−2y, fy(x, y) = −2x+y <sup>2</sup> −3. Por lo tanto f<sup>x</sup> = 0 sii x = y. Sustituyendo en f<sup>y</sup> obtenemos la ecuaci´on x <sup>2</sup> − 2x + 3 = 0 para los puntos cr´ıticos de f. Por lo tanto, los puntos cr´ıticos de f son (3, 3) y (−1, −1). Para clasificarlos hallamos las derivadas segundas de f: fxx(x, y) = 2, fyy(x, y) = 2y, fxy(x, y) = −2. Aplicamos el criterio del Hessiano y obtenemos que f tiene un m´ınimo relativo en (3, 3), porque |H(3, 3)| = 8 > 0 y fxx(3, 3) = 2 > 0. Por el mismo criterio, f tiene un punto silla en (−1, −1), porque |H(−1, −1)| = −8 < 0.

Ejercicio 3.(20 pts.) Sea F(x, y) = (y sin(x), − cos(x)) y C la curva compuesta por el semic´ırculo x <sup>2</sup> + y <sup>2</sup> = 9, y ≥ 0 y el segmento y = 0, −3 ≤ x ≤ 3, orientada en sentido antihorario. Calcular R C F.

Soluci´on: Las funciones sin y cos son infinitamente derivables en toda la recta real, por lo que F es C 1 en R 2 , y C es una curva cerrada simple orientada en sentido antihorario, por lo que estamos en las hip´otesis del Teorema de Green. Aplicando el teorema tenemos

$$\int_{C} F = \oint_{\partial \Omega} F = \int \int_{\Omega} (\sin x - \sin x) = 0$$

siendo Ω la regi´on interior a la curva C.

## Otra forma:

Basta con observar que C es una curva cerrada y la funci´on φ (x, y) = −y cos x tiene gradiente ∇φ = F en todo R 2 . Luego,

$$\int_C F = \oint_C \nabla \phi = 0$$

Ejercicio 4.(20 pts.) Calcular RR S rotF · n, donde F(x, y, z) = (z <sup>2</sup>y, −x, z sin(x 2y 2 z)), S es la parte del cilindro x <sup>2</sup> + y <sup>2</sup> = 15 entre los planos z = −1 y z = 2, y n normal unitario se dirige alej´andose del eje z.

Soluci´on: Primero observamos que el campo es de clase C<sup>∞</sup> en todo R 3 , por lo que estamos en las hip´otesis del Teorema de Stokes para aplicarlo al cilindro orientado con la normal apuntando alej´andose del eje z y sus dos componentes de borde orientadas con la orientaci´on inducida. Consideremos las componentes de borde de S, Cz, z ∈ {−1, 2} parametrizadas por

$$\alpha_z : [0, 2\pi] \to \mathbb{R}^3 / \alpha_z(t) = \sqrt{15}(\cos t, \sin t, z)$$

Observar que C−<sup>1</sup> est´a orientada coherentemente con S y C<sup>2</sup> tiene la orientaci´on opuesta.

Como el campo es de clase C 1 en R <sup>3</sup> podemos aplicar el teorema de Stokes para obtener:

$$\int_{S} rot(F) \cdot n = \int_{C_{-1}} F - \int_{C_{2}} F$$

Observar ahora que R C−<sup>1</sup> F = R ∂D−<sup>1</sup> <sup>F</sup>, donde <sup>D</sup>−<sup>1</sup> es el disco de centro 0 y radio <sup>√</sup> 15 en el plano z = −1 orientado con la normal (0, 0, 1). Por lo tanto, aplicando el teorema de Stokes nuevamente R C−<sup>1</sup> F = R ∂D−<sup>1</sup> F = RR D−<sup>1</sup> rotF · (0, 0, 1) , por lo cual solo nos interesa la tercer componente de rotF que vale (−1 − z 2 ). Obtenemos entonces: R C−<sup>1</sup> F = RR D−<sup>1</sup> −2 = −2area(D−1) = −30π.

An´alogamente para la otra componente de borde obtenemos: R C<sup>2</sup> F = R ∂D<sup>2</sup> F, donde D<sup>2</sup> es el disco de centro 0 y radio <sup>√</sup> 15 en el plano z = 2 orientado con la normal (0, 0, −1). Por lo tanto, aplicando el teorema de Stokes nuevamente R C<sup>2</sup> F = R ∂D<sup>2</sup> F = RR D<sup>2</sup> rotF · (0, 0, 1) = RR D<sup>2</sup> −5 = −5area(D2) = −75π , por lo cual obtenemos:

$$\int_{S} rot(F) \cdot n = \int_{C_{-1}} F - \int_{C_{2}} F = -30\pi - (-75\pi) = 45\pi$$

Otra forma: Tambi´en se pueden calcular las integrales directamente:

$$\int_{C_z} F = \int_0^{2\pi} F(\alpha_z(t)) \cdot \alpha_z'(t) dt = \int_0^{2\pi} (\sqrt{15}z^2 \sin(t), -\sqrt{15}\cos(t), *) \cdot \sqrt{15}(-\sin(t), \cos(t), 0) dt$$

$$= -15 \int_0^{2\pi} z^2 \sin^2(t) + \cos^2(t) dt = -15 \left( z^2 \int_0^{2\pi} \sin^2(t) + \int_0^{2\pi} \cos^2(t) \right) = -15\pi \left( z^2 + 1 \right)$$

 $Sustituy endo\ obtenemos:$ 

$$\int_{S} rot(F) \cdot n = -30\pi - (-75\pi) = 45\pi$$
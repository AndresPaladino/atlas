<!-- atlas-local: extraído de examen_feb2022.pdf con marker v1.10.2 en cuda. No editar a mano. -->

## Examen de Cálculo Vectorial

|               |                   | Martes 8 de febrero de 2022. |
|---------------|-------------------|------------------------------|
|               |                   |                              |
|               | Nombre y Apellido | Cédula de Identidad          |
| No. de Examen |                   |                              |

## Antes de iniciar el examen, tenga en cuenta los siguientes puntos:

- Asegúrese que esta hoja esté impresa por ambas carillas (son dos preguntas por carilla).
- Identifique tanto esta hoja como las hojas donde entrega sus respuestas.
- Puede usar lápiz o lapicera, pero asegúrese que su escrito sea legible.
- No está permitido el uso de calculadoras ni de ningún otro dispositivo de cómputo.
- Justifique detalladamente todas sus respuestas.
- Puede usar cualquier resultado (proposición, teorema, propiedad, etc) visto en clases o que esté en las notas de teórico. No es necesario que lo demuestre, pero sí verificar que se cumplan las hipótesis del resultado dentro de la situación en la que lo vaya a emplear.

Pregunta 1. Un servicio de entrega de paquetes requiere que las dimensiones de una caja rectangular sea tal que la longitud (x) más el doble del ancho (y) más el doble de la altura (z) no rebase los 300 centímetros. Se desea determinar el volumen de la caja más grande que puede enviar la compañía.

- (a) Sin hacer ningún cálculo, justifique por qué se puede hallar tal caja con volumen máximo. [5 pts.]
- (b) Sea (x, y, z) el vector de dimensiones de una caja cuyo volumen es máximo. Justifique por qué deben cumplirse las condiciones x, y, z > 0 y x + 2y + 2z = 300. [10 pts.]
- (c) Calcule el volumen de la caja más grande que puede enviar la compañía. [10 pts.]

Pregunta 2. Sea α: I(⊆ R) → R <sup>3</sup> una curva paramétrica regular definida sobre un intervalo I, de clase C <sup>2</sup> y parametrizada por longitud de arco.

(a) Demuestre que α 0 (s) y α <sup>00</sup>(s) son ortogonales para todo s ∈ I. [5 pts.]

Ahora, sea P ∈ R <sup>3</sup> un punto fijo fuera de la traza de esta curva (es decir, P 6∈ α(I)), y tal que la recta tangente a α en el punto α(s) pasa por P, para todo s ∈ I.

(b) Demuestre que existe una función λ: I → R de clase C 2 tal que

$$P = \alpha(s) + \lambda(s)\alpha'(s),$$

para todo s ∈ I. [10 pts.]

(c) Demuestre que la traza de α está contenida en una recta. [10 pts.]

## Pregunta 3. Demuestre las siguientes afirmaciones:

- (a) No es posible hallar un campo vectorial cuyo rotacional es el campo F(x, y, z) = (x, y, z). [5 pts.]
- (b) Si F = (P, Q, R): R <sup>3</sup> → R 3 es un campo vectorial de clase C 2 , entonces se cumple la igualdad

$$\operatorname{rot}(\operatorname{rot}(\boldsymbol{F})) = \nabla(\operatorname{div}(\boldsymbol{F})) - \nabla^2(\boldsymbol{F}).$$

Aquí, ∇<sup>2</sup> es el operador definido como

$$\nabla^2({\pmb F}) = (\nabla^2(P), \nabla^2(Q), \nabla^2(R)) = (P_{xx} + P_{yy} + P_{zz}, Q_{xx} + Q_{yy} + Q_{zz}, R_{xx} + R_{yy} + R_{zz}).$$
 [20 pts.]

Pregunta 4. Calcule las integrales de línea R C F para los campos F y curvas C indicados.

(a) El campo F : R <sup>3</sup> → R <sup>3</sup> viene dado por

$$\boldsymbol{F}(x,y,z) = (z,x,y)$$

y C es la curva de intersección entre el paraboloide z = x <sup>2</sup> + y <sup>2</sup> y el plano z = 2x. Si S es la sección acotada del paraboloide cuyo borde es C, se considera a S con orientación dada por el campo normal con altura z < 0, y a C con la orientación compatible con S. [12 pts.]

(b) El campo F : R <sup>2</sup> → R <sup>2</sup> viene dado por

$$\mathbf{F}(x,y) = (e^{x^2} - y^3, e^{y^2} + x^3)$$

y C = ∂D, donde D es la región delimitada por las circunferencias de centro (0, 1) y radio 1, y de centro (0, 2) y radio 2. Es decir,

$$D = \{(x, y) \in \mathbb{R}^2 : x^2 + (y - 1)^2 \ge 1 \text{ y } x^2 + (y - 2)^2 \le 4\}.$$

Se orienta a C positivamente según Green. [13 pts.]

Sugerencia: Puede ser de utilidad representar los puntos (x, y) ∈ D mediante coordenadas polares x = r cos(θ) e y = r sin(θ).

## Algunas identidades de utilidad:

- sin<sup>2</sup> (θ) + cos<sup>2</sup> (θ) = 1
- sin(2θ) = 2 sin(θ) cos(θ)
- cos(2θ) = cos<sup>2</sup> (θ) − sin<sup>2</sup> (θ)

• 
$$\int \sin^n(\theta) \ d\theta = -\frac{\sin^{n-1}(\theta)\cos(\theta)}{n} + \frac{n-1}{n} \int \sin^{n-2}(\theta) \ d\theta \ \text{con } n \in \mathbb{Z}_{>0}$$
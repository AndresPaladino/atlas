<!-- atlas-local: extraído de Examen11_2_20.pdf con marker v1.10.2 en cuda. No editar a mano. -->

## Examen Cálculo Vectorial y Cálculo 3, 11 de febrero de 2020

## Nombre:

## C.I.:

## Número de examen:

- (I) 1. Sea  $F: \mathbb{R}^2 \to \mathbb{R}^2$  un campo vectorial de clase  $C^1$ . Prueba que si F es irrotacional entonces el campo  $Q: \mathbb{R}^2 \to \mathbb{R}^2$  dado por  $Q(x,y) = F(x-x_0,y-y_0)$  también es irrotacional para todo  $(x_0,y_0) \in \mathbb{R}^2$ .
  - 2. Explica qué relación tiene el campo Q con el F en cuanto a lo geométrico (sus bosquejos).
  - 3. Sea  $G: \mathbb{R}^2 \{(0,0)\} \to \mathbb{R}^2$  dado por  $G(x,y) = \left(-\frac{x}{x^2+y^2}, -\frac{y}{x^2+y^2}\right)$ . Prueba que G es irrotacional. ¿Es un campo de gradientes? ¿Es condición necesaria que el dominio de un campo irrotacional sea simplemente conexo para que sea de gradiente?
  - 4. Explica alguna propiedad de los campos de gradiente y demuéstrala.
  - 5. Sea el campo  $X: \mathbb{R}^2 \{(-10,0), (10,0)\} \to \mathbb{R}^2$  definido por

$$X(x,y) = \left(-\frac{x+10}{(x+10)^2 + y^2} - \frac{x-10}{(x-10)^2 + y^2}, -\frac{y}{(x+10)^2 + y^2} - \frac{y}{(x-10)^2 + y^2}\right)$$

Bosqueja el campo vectorial. Sug: dibuja las flechas del campo en los puntos de la forma (0, y).

6. Considera  $\mathcal{C}$  la curva de la figura.

![](_page_0_Figure_12.jpeg)

Calcula la circulación de X a través de  $\mathcal{C}$  con argumentos puramente geométricos. No vale ninguna cuenta. Puede ser útil la sugerencia de la parte anterior.

- (II) 1. a) Enuncia y demuestra la expresión intrínseca del rotor.
  - b) Considera que  $F: \mathbb{R}^3 \to \mathbb{R}^3$  es un campo de clase  $C^{\infty}$ . Sea  $p \in \mathbb{R}^3$ , y  $\pi$  un plano tal que  $p \in \pi$ . Sea  $\gamma_n$  una sucesión de curvas simples cerradas contenidas en  $\pi$ , p pertenece a la componente acotada plana de  $\pi \gamma_n$  y diam $(\gamma_n)$  tiende a cero cuando n tiende a infinito. Además la circulación del campo en las curvas  $\gamma_n$  es nula para todo n. Prueba que la componente del rotor en p según la normal a  $\pi$  es nula.
  - 2. a) Sea  $G: \mathbb{R}^2 \to \mathbb{R}^2$  un campo de clase  $C^{\infty}$  y  $p \in \mathbb{R}^2$  tal que el rotor en p es nulo. ¿Es posible que existan curvas cerradas simples con p en su interior y de diámetro arbitrariamente pequeño donde la circulación de G sea no nula? Sug: Considerar  $G: \mathbb{R}^2 \to \mathbb{R}^2$  tal que  $G(x, y) = (-y^3, x^3)$ .
    - b) Y si en las mismas condiciones de la parte anterior se agrega la información que el rotor se anula en todos los puntos de un disco centrado en p, ¿se modifica la respuesta?
    - c) Ahora suponga que  $G: \mathbb{R}^2 \to \mathbb{R}^2$  un campo de clase  $C^{\infty}$  y  $p \in \mathbb{R}^2$  tal que el rotor en p es no nulo. Prueba que para toda curva cerrada simple con p en su interior y de diámetro suficientemente pequeño se verifica que la circulación de G es no nula.
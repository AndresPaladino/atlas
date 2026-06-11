<!-- atlas-local: extraído de sol_ex_feb_19_CV.pdf con marker v1.10.2 en cuda. No editar a mano. -->

Solucion examen – 05 de febrero de 2019 ´

# (I) M´ultiple opci´on. Total: 28 puntos

Puntajes: 7 puntos si la respuesta es correcta, -2,3 puntos si la respuesta es incorrecta, 0 punto por no contestar.

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| B | A | D | D |

### (II) Desarrollo. Total: 72 puntos

Todo resultado te´orico que utilice en la resoluci´on de los problemas debe estar adecuadamente justificado.

### Problema 1

1. Dado que el dominio del campo es todo el espacio R 3 , para garantizar que es conservativo alcanza con que el rotor sea nulo. Calculando el rotor se tiene:

$$\operatorname{Rot}(F) = \left(0, -3x^2z^2 + \frac{\partial u}{\partial z}, \frac{\partial u}{\partial y}\right)$$

Igualando dicho rotor a (0, 0, 0) obtenemos:

$$u(x, y, z) = x^2 z^3 + k(x)$$

- 2. a) Una forma de resolver es construir un potencial, por ejemplo podr´ıamos tomar f(x, y, z) = x 3 z <sup>3</sup>/3 + y <sup>3</sup>/3 + y + z. De esta manera evaluando dicho potencial en B y A obtenemos que la integral sobre la curva es: -5/24.
  - b) Usando Stokes basta calcular la integral sobre la curva del campo H, si observamos que H es igual a F sobre la curva C y usamos que F es conservativo concluimos que el flujo del rotor de H sobre S es cero.

## Problema 2

- 1. Ver te´orico.
- 2. (a) El dominio m´as amplio para que F sea C<sup>∞</sup> corresponde a:

$$\Omega = \{(x, y, z) \in \mathbb{R}^3 : x^2 + y^2 \neq 0\}$$

Es decir todo el espacio menos el eje Oz.

(b) Usando la regla de la cadena se tiene que:

$$F(x,y,z) = \frac{f'(r)}{r}(x,y,0)$$

Luego la divergencia de F es:

$$\operatorname{div}(F) = \frac{f''(r)r + f'(r)}{r}$$

Por lo tanto para hallar todas las funciones f' que hacen que la divergencia sea 0 debemos resolver la ecuación diferencial:

$$f''(r)r + f'(r) = 0$$

La cual se resuelve mediante variables separables y se obtiene que:

$$f'(r) = \frac{K}{r}, \ K \in \mathbb{R} - \{0\}$$

(c) Por el item anterior, el campo F es de la forma:

$$F(x, y, z) = \frac{K}{r^2}(x, y, 0)$$

donde K es una constante no nula.

Aquí la superficie está orientada con normal apuntando hacia su eje de simetría, es decir el campo de versores normales corresponde a:

$$n(x, y, z) = -\frac{(x, y, 0)}{r}$$

Entonces:

$$\iint_S F\,dS = \iint_S \langle \frac{K}{r^2}(x,y,0), -\frac{(x,y,0)}{r} \rangle\,dS = -\frac{K}{R}A(S) = -2\pi K$$

luego:

$$K = -\frac{1}{2\pi}$$

Y por lo tanto:

$$F(x,y,z) = -\frac{1}{2\pi} \left( \frac{x}{x^2 + y^2}, \frac{y}{x^2 + y^2}, 0 \right)$$

#### Problema 3

- 1. Ver teórico.
- 2. Ver teórico.
- 3. Claramente es falso, un contra-ejemplo es  $X(x,y,z) = \left(\frac{-y}{x^2+y^2}, \frac{x}{x^2+y^2}, 0\right)$ .
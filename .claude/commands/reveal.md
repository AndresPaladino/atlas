---
description: Válvula de escape del firewall — ver el resultado bloqueado sin salir de /practice
---

El usuario está en `/practice` y quiere ver un resultado bloqueado por el firewall
(típicamente un cálculo o procedimiento puntual), sin abandonar la sesión Socrática.

1. Corré `atlas session reveal` — habilita la próxima lectura bloqueada.
2. Leé la página que necesitabas y respondé el punto puntual que pidió el usuario.
3. Avisá que el firewall queda **abierto** hasta volver a `/practice`, y que el
   reveal queda registrado (estado de sesión + visible en git).
4. Cuando el usuario quiera seguir practicando, re-armá el firewall corriendo de
   nuevo `atlas session set "<T>"` con el mismo tema.

Esto es deliberado y auditable: el firewall sigue siendo garantía (default deny);
el override es consciente, no un filtrado por descuido.

# Prueba-de-programacion-AtomicLabs
## Analisis y comprensión del problema
Primero se analizo lo solicitado y se escribieron los requerimientos funcionales del juego:
 - El juego debe ser en un tablero
 - El juego requiere de una matriz para registrar los elementos del tablero
 - El juego debe tener 8 espacios para ventanas
 - El juego debe tener 2 zombies
 - El juego debe tener a los sobrevivientes en las coordenadas solicitadas
 - El juego debe permitir el movimiento de los supervivientes con instrucciones del jugador
 - El juego debe permitir a los supervivientes moverse 2 casillas
 - El juego debe permitir a los zombies moverse 4 casillas
 - El juego debe mover a los zombies de forma aleatoria sin regresar a la casilla en la que estaban anteriormente
 - El juego debe evitar que un zombie o sobreviviente traspase una pared
 - El juego debe evitar que sobrevivientes o zombies esten en la misma ubicación
 - El juego debe permitir que un zombie convierta a un superviviente en zombie si esta en sus casillas adyacentes
 - El juego debe convertir a un superviviente en zombie despues de dos turnos de estar cerca de un zombie
 - El juego debe sacar del tablero a los jugadores que se salven estando en las casillas de salida
 - El juego debe contar a los jugadores salvados
 - El juego debe terminar cuando solo queden zombies en el tablero

Luego se analizaron requerimientos no funcionales del juego:
 - El juego debe guardar en un archivo la iteración, numero de zombies, numero de supervivientes y numero de supervivientes salvados
 - El juego debe mostrar en consola la casilla de las ventanas por donde aparece un zombie
 - El juego debe mostrar en consola las coordenadas de un humano que haya sido infectado
 - El juego debe mostrar en consola las coordenadas de un humano que haya sido salvado
 - El juego debe mostrarse de forma grafica

## Lenguje de programación
Se tenian 3 opciones de lenguaje de programación para el desarrollo del videojuego: Allegro (lenguaje c), Pygame (Python), Unity (C#).
Ya que se tiene experiencia en estos. Primero se opto por Unity por ser un framework dedicado completamente al desarrollo de videojuegos.
Como en Unity es facil en el apartado visual, se buscaron y tambien se crearon imagenes para el proyecto (personajes, celdas del tablero, paredes, etcetera).
Teniendo las imagenes que se ocuparían para darle forma al juego, se modelo el tablero y la posición de los supervivientes. Aqui había un problema con Unity, ya que el modelado grafico era muy sencillo, pero la programación de las coordenadas y uso de matrices se iba a complicar por el sistema de ubicación que utiliza Unity.
Por lo que se opto por otra de las 3 opciónes. Allegro (lenguaje C) al ser una libreria en un lenguaje estructural, el uso de matrices sería muy sencillo, pero el uso de graficos y de la libreria es de un nivel muy complejo. Por lo que se escogio Pygame(Python) para el desarrollo del videojuego, esto por ser la ultima opción que se tenia, pero tambien beneficia el hecho de ser un lenguaje orientado a objetos y el manejo de graficos no es tan complejo.

## Desarrollo
En le desarrollo ya trabajando con Pygame, se establecio un tamaño comodo y visible para la pantalla que contendria el videojuego. Despues se coloco el tablero modelado en Unity. Se definieron variables e imagenes para su uso. Se planteo el punto de inicio de para la impresión de un personaje en la coordenada (0, 0) del tablero. Se obtuvo las coordenadas en pixeles de este punto de inicio y tambien sus intervalos (x, y) en pixeles para el personaje se pueda mover de manera uniforme en las celdas.
Se planteo el uso de clases para contener los atributos del objeto Humano y del objeto Zombie. Se establecieron las coordenadas del tablero para poder realizar una matriz que contenga los elementos del tablero.


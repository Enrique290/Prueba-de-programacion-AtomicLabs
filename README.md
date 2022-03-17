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
Ya que se tiene experiencia en estos.

Primero se opto por Unity por ser un framework dedicado completamente al desarrollo de videojuegos.
Como en Unity es facil en el apartado visual, se buscaron y tambien se crearon imagenes para el proyecto (personajes, celdas del tablero, paredes, etcetera).
Teniendo las imagenes que se ocuparían para darle forma al juego, se modelo el tablero y la posición de los supervivientes. Aqui había un problema con Unity, ya que el modelado grafico era muy sencillo, pero la programación de las coordenadas y uso de matrices se iba a complicar por el sistema de ubicación que utiliza Unity.

Por lo que se opto por otra de las 3 opciónes. Allegro (lenguaje C) al ser una libreria en un lenguaje estructural, el uso de matrices sería muy sencillo, pero el uso de graficos y de la libreria es de un nivel muy complejo. Por lo que se escogio Pygame(Python) para el desarrollo del videojuego, esto por ser la ultima opción que se tenia, pero tambien beneficia el hecho de ser un lenguaje orientado a objetos y el manejo de graficos no es tan complejo.

![1](url)

## Desarrollo
En le desarrollo ya trabajando con Pygame, se establecio un tamaño comodo y visible para la pantalla que contendria el videojuego. Despues se coloco el tablero modelado en Unity.

![1](url)

Se definieron variables e imagenes para su uso. Se planteo el punto de inicio de para la impresión de un personaje en la coordenada (0, 0) del tablero. Se obtuvo las coordenadas en pixeles de este punto de inicio y tambien sus intervalos (x, y) en pixeles para el personaje se pueda mover de manera uniforme en las celdas.
Se planteo el uso de clases para contener los atributos del objeto Humano y del objeto Zombie. Se establecieron las coordenadas del tablero para poder realizar una matriz que contenga los elementos del tablero.

![2](url)

Teniendo la matriz, se lleno con ayuda de un documento json. Esta decisión se tomo por ser una forma comoda de llenar muchos datos y que este documento puede ser dinamico para la incersión de cuantos supervivientes se deséen. Una vez teniendo el juego con los personajes colocados en sus coordenas por un sistema en el que al colocar las coordenadas (matriz) del personajes, este se imprime el personaje en su ubicación en la pantalla del juego, sin necesidad de hacer calculos propios y colocarlos.

![2](url)

Lo siguiente fue el movimiento de los humanos, fue lo mas laborioso del juego. Ya que no sabia como reconocer un click en una imagen. Por loque toco investigar como reconocer la ubicación de una imagen, cosa que no se logro, pero se encontro un sistema en el que se tiene la medida del tablero (pixeles) y se divide en el numero de columnas y renglones que se tienen, obteniendo asi el tamaño area por celda del tablero. Despues con la posición del cursor, esta posición se debe dividir entre el tamaño de las celdas obtenido anteriormente y el resultado es la cordenada en el tablero (matriz). Por lo que al hacer click en el juego, se obtenia la ubicación matricial del tablero y el manejo de personajes y posicones se facilito mucho mas de lo que se buscaba.

Despues se trbajo en como mover a los humanos, por lo que tome la idea de un juego de damas inglesas, colocando puntos en el tablero donde el personaje se pueda mover, analizando la posicion del click, si este le daba a un superviviente y mostrando al rededor del superviviente seleccionado los puntos (depues de un analisis con la posición del personaje y los elementos a su alrededor).

![2](url)

Se trabajo en que solo este movimiento se pueda realizar dos veces, por lo que se rresolvio con banderas y variables auxiliares que guardaran datos de variables que tenian que guardar sus datos todo el tiempo.

Teniendo completado el movimiento del superviviente, solo quedaba la validación de cuando este llegara a la meta. Por lo que no fue algo complicado al trabajar todo con coordenadas. Solo que cuando el superviviente llega a la meta, a este se le elimina del juego y se incrementa el contador de supervivientes salvados.

En todo momento se busco hacer uso de funciones, para que la función principal donde se desarrolla el juego quede limpia y conciza.

El cambio de turno de humanos y zombies se logro con las banderas utilizadas para los turnos del jugador. La progamación del los zombies fua mas sencilla, ya que no habia nadie quien los tuviera que controlar, y estos se mueven de forma aleatoria. Por lo que se creo una sistema parecido al del humano (para no moverse a lugares donde no puede) y depues mover al personaje de forma aleatoria (sin regresar al punto anterior de donde se movio). Para comverir a los humanos en zombies, esta validación se hace cuando se terminan de mover todos los zombies y estos ya tienen una ubicación final para despues infectar a los humanos en las ubicacones adyacentes al zombie. Cuando un humano es infectado, se le prende una bandera y se le cambia el asset para identificar cuales estan infectados. Al finalizar el turno de los zombies, se recorre la lista de supervivientes y se busca quienes estan infectado y se les incrementa su contador para converitse en zombies.



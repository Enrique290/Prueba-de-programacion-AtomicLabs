# Prueba-de-programación-AtomicLabs
## Importante
El proyecto fue creado con python y la librería pygame. Pygame es una librería de python que sirve para poder hacer uso de métodos gráficos en 2d con el lenguaje de programación, y su mayor uso es para videojuego.

### Instalar Pygame

![pygame](https://github.com/Enrique290/Prueba-de-programacion-AtomicLabs/blob/master/github_img/pygame_logo.png)

Para instalar Pygame es necesario tener instalado python en la computadora. Después en la terminal del sistema operativo se debe escribir lo siguiente:

***pip install pygame***

Dar enter y esperar a que finalice la instalación. Listo, se puede hacer uso de la librería y jugar el videojuego del repositorio. Que lo disfrutes.

Para más información puedes consultar: https://pypi.org/project/pygame/

## Introducción
En el presente repositorio se presenta el desarrollo de un videojuego de estrategia por turnos 2d. En donde el objetivo del jugador es sacar a todas las personas de una oficina, para que estas no se transformen en zombies. Por turno, se podrá mover un solo personaje 2 casillas y en el siguiente turno los zombies se moverán de forma aleatoria 4 casillas, sin regresar a la anterior de la que se movieron. El juego termina al solo quedar zombies en la oficina.

## Análisis y comprensión del problema
Primero se analizó lo solicitado y se escribieron los requerimientos funcionales del juego:
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
 - El juego debe evitar que sobrevivientes o zombies estén en la misma ubicación
 - El juego debe permitir que un zombie convierta a un superviviente en zombie si está en sus casillas adyacentes
 - El juego debe convertir a un superviviente en zombie después de dos turnos de estar cerca de un zombie
 - El juego debe sacar del tablero a los jugadores que se salven estando en las casillas de salida
 - El juego debe contar a los jugadores salvados
 - El juego debe terminar cuando solo queden zombies en el tablero

Luego se analizaron requerimientos no funcionales del juego:
 - El juego debe guardar en un archivo la iteración, numero de zombies, numero de supervivientes y numero de supervivientes salvados
 - El juego debe mostrar en consola la casilla de las ventanas por donde aparece un zombie
 - El juego debe mostrar en consola las coordenadas de un humano que haya sido infectado
 - El juego debe mostrar en consola las coordenadas de un humano que haya sido salvado
 - El juego debe mostrarse de forma grafica

## Lenguaje de programación
Se tenían 3 opciones de lenguaje de programación para el desarrollo del videojuego: Allegro (lenguaje c), Pygame (Python), Unity (C#).
Ya que se tiene experiencia en estos.

Primero se optó por Unity por ser un framework dedicado completamente al desarrollo de videojuegos.
Como en Unity es fácil en el apartado visual, se buscaron y también se crearon imágenes para el proyecto (personajes, celdas del tablero, paredes, etcétera).
Teniendo las imágenes que se ocuparían para darle forma al juego, se modelo el tablero y la posición de los supervivientes. Aquí había un problema con Unity, ya que el modelado grafico era muy sencillo, pero la programación de las coordenadas y uso de matrices se iba a complicar por el sistema de ubicación que utiliza Unity.

Por lo que se optó por otra de las 3 opciones. Allegro (lenguaje C) al ser una librería en un lenguaje estructural, el uso de matrices sería muy sencillo, pero el uso de gráficos y de la librería es de un nivel muy complejo. Por lo que se escogió Pygame (Python) para el desarrollo del videojuego, esto por ser la última opción que se tenía, pero también beneficia el hecho de ser un lenguaje orientado a objetos y el manejo de gráficos no es tan complejo.

## Desarrollo
En el desarrollo ya trabajando con Pygame, se estableció un tamaño cómodo y visible para la pantalla que contendría el videojuego. Después se colocó el tablero modelado en Unity.

![Board](https://github.com/Enrique290/Prueba-de-programacion-AtomicLabs/blob/master/github_img/Board.png)

Se definieron variables e imágenes para su uso. Se planteo el punto de inicio de para la impresión de un personaje en la coordenada (0, 0) del tablero. Se obtuvo las coordenadas en pixeles de este punto de inicio y también sus intervalos (x, y) en pixeles para el personaje se pueda mover de manera uniforme en las celdas.
Se planteo el uso de clases para contener los atributos del objeto Humano y del objeto Zombie. Se establecieron las coordenadas del tablero para poder realizar una matriz que contenga los elementos del tablero.

![Matriz](https://github.com/Enrique290/Prueba-de-programacion-AtomicLabs/blob/master/github_img/matrix.png)

Teniendo la matriz, se llenó con ayuda de un documento json. Esta decisión se tomó por ser una forma cómoda de llenar muchos datos y que este documento puede ser dinámico para la inserción de cuantos supervivientes se deseen. Una vez teniendo el juego con los personajes colocados en sus coordenadas por un sistema en el que al colocar las coordenadas (matriz) del personaje, este se imprime el personaje en su ubicación en la pantalla del juego, sin necesidad de hacer cálculos propios y colocarlos.

![MatrizLlena](https://github.com/Enrique290/Prueba-de-programacion-AtomicLabs/blob/master/github_img/Board-fill.png)

Lo siguiente fue el movimiento de los humanos, fue lo más laborioso del juego. Ya que no sabía cómo reconocer un click en una imagen. Por loque toco investigar como reconocer la ubicación de una imagen, cosa que no se logró, pero se encontró un sistema en el que se tiene la medida del tablero (pixeles) y se divide en el número de columnas y renglones que se tienen, obteniendo así el tamaño área por celda del tablero. Después con la posición del cursor, esta posición se debe dividir entre el tamaño de las celdas obtenido anteriormente y el resultado es la coordenada en el tablero (matriz). Por lo que al hacer click en el juego, se obtenía la ubicación matricial del tablero y el manejo de personajes y posiciones se facilitó mucho más de lo que se buscaba.

Después se trabajó en como mover a los humanos, por lo que tome la idea de un juego de damas inglesas, colocando puntos en el tablero donde el personaje se pueda mover, analizando la posición del click, si este le daba a un superviviente y mostrando al rededor del superviviente seleccionado los puntos (después de un análisis con la posición del personaje y los elementos a su alrededor).

![Puntos](https://github.com/Enrique290/Prueba-de-programacion-AtomicLabs/blob/master/github_img/Board-points.png)

Se trabajo en que solo este movimiento se pueda realizar dos veces, por lo que se resolvió con banderas y variables auxiliares que guardaran datos de variables que tenían que guardar sus datos todo el tiempo.

Teniendo completado el movimiento del superviviente, solo quedaba la validación de cuando este llegara a la meta. Por lo que no fue algo complicado al trabajar todo con coordenadas. Solo que cuando el superviviente llega a la meta, a este se le elimina del juego y se incrementa el contador de supervivientes salvados.

En todo momento se buscó hacer uso de funciones, para que la función principal donde se desarrolla el juego quede limpia y concisa.

El cambio de turno de humanos y zombies se logró con las banderas utilizadas para los turnos del jugador. La programación de los zombies fua más sencilla, ya que no había nadie quien los tuviera que controlar, y estos se mueven de forma aleatoria. Por lo que se creó un sistema parecido al del humano (para no moverse a lugares donde no puede) y después mover al personaje de forma aleatoria (sin regresar al punto anterior de donde se movió). Para convertir a los humanos en zombies, esta validación se hace cuando se terminan de mover todos los zombies y estos ya tienen una ubicación final para después infectar a los humanos en las ubicaciones adyacentes al zombie. Cuando un humano es infectado, se le prende una bandera y se le cambia el asset para identificar cuales están infectados. Al finalizar el turno de los zombies, se recorre la lista de supervivientes y se busca quienes están infectado y se les incrementa su contador para convertirse en zombies. Al pasar dos iteraciones este contador, se le elimina al humano de la lista de humanos y se le agrega a la lista de zombies con las coordenadas en donde estaba cuando era humano.

Después se hizo una pulida en funciones, manejo de datos y detalles en lo desarrollado. Los mensajes por consola solo se agregaron a líneas de código donde pasaban dichos eventos y la escritura y actualización del archivo para conocer las iteraciones, numero de zombies, numero de supervivientes y numero de supervivientes salvados, se creó de forma sencilla agregando esta escritura al inicio del juego y en los términos de las iteraciones.

Finalmente se validó la finalización del juego si la lista de humanos queda vacía. Y se agregaron detalles como cambio en colores, imágenes nuevas, el mostrador de turnos de humanos o zombies y sonidos para no dejar solo en lo visual al juego.

![InGame](https://github.com/Enrique290/Prueba-de-programacion-AtomicLabs/blob/master/github_img/Board-inGame.png)

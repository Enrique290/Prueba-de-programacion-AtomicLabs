"""
Un videojuego en el que tu objetivos es rescatar a las personas de una oficina de los hambrinetos zombies

Un videojuego de estrategia por turnos 2d. El objetivo del jugador es sacar a todas las personas de una oficina,
para que estas no se transformen en zombies. Por turno, se podra mover un solo personaje 2 casillas y en el 
siguiente turno los zombies se moveran de forma aleatoria 4 casillas, sin regresar a la anterior de la que se 
movieron.El juego termina al solo quedar zombies en la oficina.

Autor: Enrique Castillo Corona
Fecha de creación: 14/03/2022
"""

# Importaciones.
from types import NoneType
import pygame, sys, random
from pygame.locals import *
import json

# Iniciazión de pygame y tamaño de la ventana del programa.
pygame.init()
size = (780,780)

# Crear ventana.
screen = pygame.display.set_mode(size)
pygame.display.set_caption('¡Ataque Zombie en AtomicLabs!')

# Controlador de FPS.
clock = pygame.time.Clock()

# Definicion de colores.
BLACK = (0, 0, 0)

# Definicion de imagenes.
background = pygame.image.load("./assets/board.png")
human_img = pygame.image.load("./assets/human.png")
human_selected_img = pygame.image.load("./assets/human-select.png")
human_infected_img = pygame.image.load("./assets/human-infected.png")
zombie_img = pygame.image.load("./assets/zombie.png")
point_img = pygame.image.load("./assets/point.png")
point_H_img = pygame.image.load("./assets/point-H.png")
point_Z_img = pygame.image.load("./assets/point-Z.png")
gameOver_img = pygame.image.load("./assets/GameOver.png")
pygame.display.set_icon(zombie_img)

# Renderizado de imagenes.
background_rend = pygame.transform.scale(background, (780,780))
human_rend = pygame.transform.scale(human_img, (32,36))
human_selected_rend = pygame.transform.scale(human_selected_img, (34,38))
human_infected_rend = pygame.transform.scale(human_infected_img, (32,36))
zombie_rend = pygame.transform.scale(zombie_img, (32,36))
point_rend = pygame.transform.scale(point_img, (32,32))
point_H_rend = pygame.transform.scale(point_H_img, (40,40))
point_Z_rend = pygame.transform.scale(point_Z_img, (40,40))
gameOver_rend = pygame.transform.scale(gameOver_img, (600,300))

# Definición de sonidos
zombie_mp3 = pygame.mixer.Sound("./audio/zombie.mp3")
infected_mp3 = pygame.mixer.Sound("./audio/damage.mp3")
escape_mp3 = pygame.mixer.Sound("./audio/orb.mp3")
gameOver_mp3 = pygame.mixer.Sound("./audio/game_over.mp3")

# Calculo el tamaño por celda.
width, cols = 702, 18
cell_size = width//cols

# Clase Humano.
class Human:
    def __init__(self, img, x_coord, y_coord, i):
        self.number = i
        self.img = img
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_game = 44+(39*(y_coord))
        self.y_game = 40+(39*(x_coord))
        self.infected_status = False
        self.virus_growing = 0
    
    def mov(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_game = 44+(39*(y_coord))
        self.y_game = 40+(39*(x_coord))

    def infected(self):
        self.img = human_infected_rend
        self.infected_status = True

    def transform(self):
        self.virus_growing += 1

# Clase Zombie.
class Zombie:
    def __init__(self, img, cell):
        self.img = img
        self.x_coord = cell+1
        self.x_game = (44+(39*(cell+2))) if cell < 4 else (44+(39*(cell+8)))
        self.y_game = 1

    def mov(self, x_coord, y_coord, x_previous, y_previous):
        self.x_previous = x_previous
        self.y_previous = y_previous
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_game = 44+(39*(y_coord))
        self.y_game = 40+(39*(x_coord))

# Función para cargar un archivo json.
# Regresa: un arreglo con la información obtenida del json.
def load_json(file):
    with open(file) as data:
        print(f"\n Documento '{file}' cargado correctamente!\n")
        return json.load(data)

# Función para verificación de datos del json que no son permitidos.
# Regresa: un booleano para permitir o denegar el inicio del juego.
def data_check(start_game, no_zombies, humans_coords):
    if(no_zombies < 1 or no_zombies > 8):
        print("\n [ERROR] Cantidad de zombies no permitido dentro del documento config.json \n")
        start_game = False

    if(len(humans_coords) > 273 or len(humans_coords) < 1):
        print("\n [ERROR] Cantidad de humanos no permitido dentro del documento config.json \n")
        start_game = False

    for coords in humans_coords:
        if(coords["x"] < 0 or coords["x"] > 17 or coords["y"] < 0 or coords["y"] > 17):
            print("\n [ERROR] Coordenadas invalidas dentro del documento config.json \n")
            start_game = False
            
        count = 0
        for aux in humans_coords:
            if ((coords["x"],coords["y"]) == (aux["x"],aux["y"])):
                count+=1
                if(count>1):
                    print("\n [ERROR] Coordenadas repetidas dentro del documento config.json \n")
                    start_game = False

        if(start_game==False):
            break

    return start_game

# Función que contine funciones basicas de pygame.
def pygame_config(clock_refresh=10):
    #Refrescar pantalla
    pygame.display.flip()
    #Definir FPS
    clock.tick(clock_refresh)
    #Background color
    screen.fill(BLACK)
    #Background
    screen.blit(background_rend, (0,0))
    #Turno
    if(clock_refresh==10):
        screen.blit(point_H_rend, (371,0))
        screen.blit(pygame.transform.scale(human_img, (24,30)), (380,7))
    else:
        screen.blit(point_Z_rend, (371,0))
        screen.blit(pygame.transform.scale(zombie_img, (24,30)), (380,7))

# Función que llena un arreglo de la clase Humano con la información obtenida del json.
# Regresa: un arreglo de la clase Humano.
def fill_humans(humans, humans_coords):
    i=0
    for coords in humans_coords:
        i+=1
        humans.append(Human(human_rend, coords["x"], coords["y"], i))
    return humans

# Función que llena un arreglo de la clase Zombie con la información obtenida del json.
# Regresa: un arreglo de la clase Zombie.
def fill_zombies(no_zombies, zombies):
    for aux in range(no_zombies):
        no_random=0
        if(aux == 0):
            no_random = random.randrange(8)
            zombies.append(Zombie(zombie_rend, no_random))
        else:
            i=True
            while i:
                no_random = random.randrange(8)
                for zombie in zombies:
                    if(zombie.x_coord-1 != no_random):
                        i=False
                    else:
                        i=True
                        break
            zombies.append(Zombie(zombie_rend, no_random))
        print(f"Un zombie llego por la ventana {no_random+1}")
    return zombies

# Función que llena la matriz que sirve para saber la ubicación de los componentes del 
# tablero y muestra los humanos y los zombies en el tablero.
# Importante: 1 = Humano, 2 = Zombie, 3 = Pared, 4 = Salida.
# Regresa: una matriz numerica (tablero).
def fill_board(board, humans, zombies):
    i=0
    for row in board:
        for col in range(len(row)):
            board[i][col]=0
            if(col==18):
                board[i][col]=3
            if(col==18 and i>13):
                board[i][col]=4
        i+=1
    for human in humans:
        board[human.x_coord][human.y_coord]=1
    for zombie in zombies:
        if(zombie.y_game != 1):
            board[zombie.x_coord][zombie.y_coord]=2
    rows=[3,11,9,15]
    for row in rows:
        for i in range(1,7):
            board[row][i]=3
    board[9][0]=3
    board[9][7]=3
    for i in range(9,16):
        board[3][i]=3
    for i in range(11,18):
        board[9][i]=3
    for i in range(4,7):
        board[i][12]=3
    cols=[11,15]
    for col in cols:
        for i in range(11,15):
            board[i][col]=3
    return board

# Función que muestra los assets de humanos y zombies
def print_characters(humans, zombies):
    for human in humans:
        screen.blit(human.img, (human.x_game, human.y_game))
    for zombie in zombies:
        screen.blit(zombie.img, (zombie.x_game, zombie.y_game))

# Función relacionada con la función "point_to_move_2".
# Función que elige en analizar un arreglo de humanos o un unico humano.
# Regresa: ubicación de puntos al presionar en un humano, un booleano que identifica
#          si se hizo click en un humano y el humano seleccionado.
def points_to_move(board, humans, points, row_click, col_click, select, select_human, humans_moves):
    if(humans_moves == 0):
        for human in humans:
            points, select, select_human = points_to_move_2(board, human, points, row_click, col_click, select, select_human)
    else:
        points, select, select_human = points_to_move_2(board, humans, points, row_click, col_click, select, select_human)
    return points, select, select_human

# Función que analiza el click realizado y si se hizo click en un humano.
# Regresa: ubicación de puntos donde se puede mover el humano seleccionado humano,
#          un booleano que identifica si se hizo click en un humano y el humano
#          seleccionado.
def points_to_move_2(board, human, points, row_click, col_click, select, select_human):
    if(human.x_coord == row_click and human.y_coord == col_click):
        screen.blit(human_selected_rend, (human.x_game-1, human.y_game-1))
        select=True
        select_human=human
        for x in range(human.x_coord-1,human.x_coord+2):
            for y in range(human.y_coord-1,human.y_coord+2):
                if(x>=0 and y>=0 and x<18 and y<19):
                    if(board[x][y] != 3 and board[x][y] != 1 and board[x][y] != 2):
                        screen.blit(point_rend, (44+(39*(y)),40+(39*(x))))
                        points.append((x,y))
    return points, select, select_human

# Función que elimina a un Humano del arreglo de humanos por sus coordenadas.
# Regresa: el arreglo de humanos.
def delete_human(humans, x_coord, y_coord):
    count = 0
    found = False
    delete = 0
    for human in humans:
        if((human.x_coord, human.y_coord)==(x_coord, y_coord)):
            delete = count
            found = True
        count+=1
    if(found):
        del humans[delete]
    return humans

# Función que mueve a un humano de ubicación y si este cruza la salida, lo elimina,
# aumenta el contador de humanos salvados y termina el turno. Tambien se analiza si
# ya termino el turno y lo termina.
# Regresa: los movimientos que a realizado el personaje, el arreglo de humanos, el
#          el contador de humanos salvados y un booleano que determina si ya se
#          acabo el turno de los humanos.
def human_mov(selected_points, row_click, col_click, selected_human, humans_moves, humans, saved_humans, humans_turn):
    for move_to in selected_points:
        if(move_to == (row_click, col_click)):
            selected_human.mov(row_click, col_click)
            humans_moves+=1
            for i in range(14, 18):
                if((selected_human.x_coord, selected_human.y_coord)==(i,18)):
                    print(f"Humano {selected_human.number} salvado en la casilla ({selected_human.x_coord},{selected_human.y_coord})")
                    escape_mp3.play()
                    humans = delete_human(humans, selected_human.x_coord, selected_human.y_coord)
                    saved_humans += 1
                    humans_moves=2
                    break
            if(humans_moves>=2):
                humans_moves = 0
                humans_turn = False
    return humans_moves, humans, saved_humans, humans_turn

# Función que mueve a los zombies de manera aleatoria, sin regresar a la casilla de
# donde se movieron.
# Regresa: el arreglo de zombies.
def zombies_mov(zombies, board, humans):
    for zombie in zombies:
        for i in range(4):
            if(zombie.y_game == 1):
                y_zombie = (zombie.x_game-44) // 39
                y_zombie = (y_zombie-1) + random.randrange(3)
                if (board[0][y_zombie]==0):
                    zombie.mov(0, y_zombie, -1, -1)
            else:
                generated=True
                while generated:
                    x_zombie=random.randrange(zombie.x_coord-1,zombie.x_coord+2)
                    y_zombie=random.randrange(zombie.y_coord-1,zombie.y_coord+2)
                    if(x_zombie >= 0 and y_zombie >= 0 and x_zombie < 18 and y_zombie < 18):
                        if((zombie.x_previous, zombie.y_previous) != (x_zombie, y_zombie)):
                            if(board[x_zombie][y_zombie] == 0):
                                zombie.mov(x_zombie, y_zombie, zombie.x_coord, zombie.y_coord)
                                generated=False
                            else:
                                generated=True
                        else:
                            generated=True
                    else:
                        generated=True
            pygame_config(1)
            print_characters(humans, zombies)
            board = fill_board(board, humans, zombies)
    return zombies, board

# Función que analiza las casillas adyacentes del zombie, para infetar a un Humano
# si es que hay uno en dichas casillas.
# Regresa: el arreglo de humanos.
def humans_infected(zombies, board, humans):
    for zombie in zombies:
        for x_coord in range(zombie.x_coord-1, zombie.x_coord+2):
            for y_coord in range(zombie.y_coord-1, zombie.y_coord+2):
                if(board[x_coord][y_coord] == 1):
                    for human in humans:
                        if(human.x_coord == x_coord and human.y_coord == y_coord and human.infected_status == False):
                            human.infected()
                            print(f"Humano {human.number} infectado en la casilla ({human.x_coord},{human.y_coord})")
                            infected_mp3.play()
    return humans

# Función que analiza a los humanos infectados, les aumenta su status y si llega a ser 3,
# elimina al Humano del arreglo de humanos y lo integra con sus coordenadas a la de zombies.
# Regresa: el arreglo de humanos y el arrgelo de zombies.
def humans_to_zombies(humans, zombies):
    for human in humans:
        if(human.infected_status):
            human.transform()
            if(human.virus_growing==3):
                zombies.append(Zombie(zombie_rend, 0))
                zombies[len(zombies)-1].mov(human.x_coord, human.y_coord, -1, -1)
                delete_human(humans, human.x_coord, human.y_coord)
    return humans, zombies

# Función que abre, sobrescribe y actualiza el archivo "iteraciones.txt".
# Registra: numero de iteración, numero de zombies, numero de humanos y 
#           humanos salvados.
def save_archive(iteration, no_humans, no_zombies, saved_humans, mode=2):
    if(mode == 1):
        f = open("iteraciones.txt","w+")
    if(mode == 2):
        f = open("iteraciones.txt","a+")
    
    f.write(f"{iteration} | {no_zombies} | {no_humans} | {saved_humans} \n")
    f.close()

# Función que analiza si terminar o no el juego
# Importante: True = termina el juego, False = continua el juego
# Regresa: un booleano
def change_gameOver(no_humans):
    if(no_humans==0):
        return True
    else:
        return False
        
# Función principal donde se lleva acabo el juego y se llaman la mayoria de funciones
# y clases.
def game_function(humans_coords, no_zombies):
    humans = []
    zombies = []
    board = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for row in board:
        for i in range(19):
            row.append(0)
    mouse_pos = (-1,-1)
    points = []
    selected_points = []
    select = False
    select_human = Human(NoneType,0,0,0)
    selected_human = Human(NoneType,0,0,0)
    saved_humans = 0
    humans_turn = True
    humans_moves = 0
    iteration = 0
    gameOver = False

    humans = fill_humans(humans, humans_coords)
    zombies = fill_zombies(no_zombies, zombies)

    save_archive(iteration, len(humans), len(zombies), saved_humans, 1)

    while True:
        pygame_config()
        board = fill_board(board, humans, zombies)
        print_characters(humans, zombies)
        select = False

        #Scaneo de eventos dentro del juego
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        if(gameOver == False):
            if(humans_turn):
                x_click, y_click = mouse_pos
                row_click = (y_click // cell_size) - 1
                col_click = (x_click // cell_size) - 1

                if(humans_moves==0):
                    points, select, select_human = points_to_move(board, humans, points, row_click, col_click, select, select_human, humans_moves)
                else:
                    points, select, select_human = points_to_move(board, selected_human, points, select_human.x_coord, select_human.y_coord, select, select_human, humans_moves)

                if(select):
                    selected_human = select_human
                    selected_points = points

                humans_moves, humans, saved_humans, humans_turn = human_mov(selected_points, row_click, col_click, selected_human, humans_moves, humans, saved_humans, humans_turn)

                if(humans_turn==False):
                    selected_points = []
                    select_human = Human(NoneType,0,0,0)
                    selected_human = Human(NoneType,0,0,0)
                    mouse_pos = (-1,-1)
                    gameOver = change_gameOver(len(humans))
                    select = False
                
                if(gameOver):
                    gameOver_mp3.play()
                    iteration += 1
                    save_archive(iteration, len(humans), len(zombies), saved_humans)

                points = []
            else:
                zombie_mp3.play()
                zombies, board = zombies_mov(zombies, board, humans)
                humans = humans_infected(zombies, board, humans)
                humans, zombies = humans_to_zombies(humans, zombies)
                
                iteration += 1
                save_archive(iteration, len(humans), len(zombies), saved_humans)
                humans_turn = True

                gameOver = change_gameOver(len(humans))
                if(gameOver):
                    gameOver_mp3.play()
        else:
            screen.blit(gameOver_rend, (90,240))

# Main del programa, verifica que el juego se pueda iniciar adecuadamente            
def main():
    start_game = True
    data = load_json("config.json")
    no_zombies = data[0]["Zombies_number"]
    humans_coords = data[1]["Coordinates"]

    start_game = data_check(start_game, no_zombies, humans_coords)
    
    if start_game:
        game_function(humans_coords, no_zombies)
        
# Se llama a la función Main
if __name__ == "__main__":
    main()
from select import select
from types import NoneType
import pygame, sys, random
from pygame.locals import *
import json

#Iniciazion
pygame.init()
size = (780,780)

#Crear ventana
screen = pygame.display.set_mode(size)

#Controlador de FPS
clock = pygame.time.Clock()

#Definicion de colores
BLACK = (0, 0, 0)

#Definicion de imagenes
background = pygame.image.load("./assets/board.png")
human_img = pygame.image.load("./assets/human.png")
human_selected_img = pygame.image.load("./assets/human-select.png")
human_infected_img = pygame.image.load("./assets/human-infected.png")
zombie_img = pygame.image.load("./assets/zombie.png")
point_img = pygame.image.load("./assets/point.png")

#Renderizado de imagenes
background_rend = pygame.transform.scale(background, (780,780))
human_rend = pygame.transform.scale(human_img, (32,36))
human_selected_rend = pygame.transform.scale(human_selected_img, (34,38))
human_infected_rend = pygame.transform.scale(human_infected_img, (32,36))
zombie_rend = pygame.transform.scale(zombie_img, (32,36))
point_rend = pygame.transform.scale(point_img, (32,32))

#Calcular el tamaño de cada celda
width, cols = 702, 18
cell_size = width//cols

class Human:
    def __init__(self, img, x_coord, y_coord):
        self.img = img
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_game = 44+(39*(y_coord))
        self.y_game = 40+(39*(x_coord))
        self.infected = False
        self.status = 0
    
    def mov(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_game = 44+(39*(y_coord))
        self.y_game = 40+(39*(x_coord))

class Zombie:
    def __init__(self, img, cell):
        self.img = img
        self.x_coord = cell+1
        self.x_game = (44+(39*(cell+2))) if cell < 4 else (44+(39*(cell+8)))
        self.y_game = 1

    def mov(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_game = 44+(39*(y_coord))
        self.y_game = 40+(39*(x_coord))

#Carga de json
def load_json(file):
    with open(file) as data:
        print(f"\n Documento '{file}' cargado correctamente!")
        return json.load(data)

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

def pygame_config():
    #Refrescar pantalla
    pygame.display.flip()
    #Definir FPS
    clock.tick(10)
    #Background color
    screen.fill(BLACK)
    #Background
    screen.blit(background_rend, (0,0))

def zombies_coords(no_zombies, zombies):
    for aux in range(no_zombies):
        if(aux == 0):
            zombies.append(Zombie(zombie_rend, random.randrange(8)))
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
    return zombies

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
    
    for human in humans:
        screen.blit(human.img, (human.x_game, human.y_game))

    for zombie in zombies:
        screen.blit(zombie.img, (zombie.x_game, zombie.y_game))

    return board

def points_to_move(board, humans, points, row_click, col_click, select, select_human, humans_moves):
    if(humans_moves == 0):
        for human in humans:
            points, select, select_human = points_to_move_2(board, human, points, row_click, col_click, select, select_human)
    else:
        points, select, select_human = points_to_move_2(board, humans, points, row_click, col_click, select, select_human)
    return points, select, select_human

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
    select_human = Human(NoneType,0,0)
    selected_human = Human(NoneType,0,0)
    saved_humans = 0
    humans_turn = True
    humans_moves = 0
    iteration = 0

    for coords in humans_coords:
        humans.append(Human(human_rend, coords["x"], coords["y"]))
    
    zombies = zombies_coords(no_zombies, zombies)

    while True:
        pygame_config()
        board = fill_board(board, humans, zombies)
        select = False

        #Scaneo de eventos dentro del juego
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        
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
            
            for move_to in selected_points:
                if(move_to == (row_click, col_click)):
                    selected_human.mov(row_click, col_click)
                    humans_moves+=1
                    for i in range(14, 18):
                        if((selected_human.x_coord, selected_human.y_coord)==(i,18)):
                            humans = delete_human(humans, selected_human.x_coord, selected_human.y_coord)
                            saved_humans+=1
                            mouse_pos = (-1,-1)
                            humans_moves=2
                            break
                    if(humans_moves>=2):
                        humans_turn = False

            print(saved_humans)
            points = []
        else:
            print("Zombies turn")
                      

def main():
    start_game = True
    data = load_json("config.json")
    no_zombies = data[0]["Zombies_number"]
    humans_coords = data[1]["Coordinates"]

    start_game = data_check(start_game, no_zombies, humans_coords)
    
    if start_game:
        game_function(humans_coords, no_zombies)
        

if __name__ == "__main__":
    main()
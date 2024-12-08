import pygame

##################################### CONSTANTE GENERALES #####################################
GRID_SIZE = 8
CELL_SIZE = 80

MENU_UNIT_CELL_SIZE = CELL_SIZE * 2
UNIT_CELL_SIZE = CELL_SIZE * (4/5)

WIDTH = GRID_SIZE * CELL_SIZE + CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 100
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MARGIN = 10

NUM_PLAYERS_0 = 3
NUM_PLAYERS_1 = 3


###################################### POLICES #####################################
pygame.font.init()
menu_font = pygame.font.SysFont('Arial Black', 25)
grid_font = pygame.font.SysFont('Arial Black', 18)


###################################### CLASSE COORDONNEES #####################################
class Coordinates:
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


##################################### IMAGES #####################################
IMAGES = {
    "attack": pygame.transform.scale(
        pygame.image.load("images/attaque_selectionnee.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
    "enemy": pygame.transform.scale(
        pygame.image.load("images/enemy.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
    "ally": pygame.transform.scale(
        pygame.image.load("images/ally.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
}

TERRAIN_TYPES = {
    "plain": pygame.transform.scale(
        pygame.image.load("images/terrain.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
    "water": pygame.transform.scale(
        pygame.image.load("images/water.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
    "fire": pygame.transform.scale(
        pygame.image.load("images/lava.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
    "wall": pygame.transform.scale(
        pygame.image.load("images/mur.png"),
        (CELL_SIZE, CELL_SIZE)
    ),
}

MENU_UNIT_IMAGES = {
    "MAGE": pygame.transform.scale(
        pygame.image.load("images/mage.png"),
        (MENU_UNIT_CELL_SIZE, MENU_UNIT_CELL_SIZE)
    ),
    "CHEVALIER": pygame.transform.scale(
        pygame.image.load("images/knight.png"),
        (MENU_UNIT_CELL_SIZE, MENU_UNIT_CELL_SIZE)
    ),
    "ARCHER": pygame.transform.scale(
        pygame.image.load("images/archer.png"),
        (MENU_UNIT_CELL_SIZE, MENU_UNIT_CELL_SIZE)
    ),
}

UNIT_IMAGES = {
    "MAGE": pygame.transform.scale(
        pygame.image.load("images/mage.png"),
        (UNIT_CELL_SIZE, UNIT_CELL_SIZE)
    ),
    "CHEVALIER": pygame.transform.scale(
        pygame.image.load("images/knight.png"),
        (UNIT_CELL_SIZE, UNIT_CELL_SIZE)
    ),
    "ARCHER": pygame.transform.scale(
        pygame.image.load("images/archer.png"),
        (UNIT_CELL_SIZE, UNIT_CELL_SIZE)
    ),
}


##################################### CONSTANTES DU MENU START EXIT #####################################
MENU_ITEM_WIDTH = 150
MENU_ITEM_HEIGHT = 50

HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2

START_COORDINATES = Coordinates(
    x = HALF_WIDTH - MARGIN - MENU_ITEM_WIDTH,
    y = HALF_HEIGHT - MENU_ITEM_HEIGHT / 2,
    width = MENU_ITEM_WIDTH,
    height = MENU_ITEM_HEIGHT
)

EXIT_COORDINATES = Coordinates(
    x = HALF_WIDTH + MARGIN,
    y = HALF_HEIGHT - MENU_ITEM_HEIGHT / 2,
    width = MENU_ITEM_WIDTH,
    height = MENU_ITEM_HEIGHT
)


############################# CONSTANTES DU MENU SELECTION DE JOUEURS #############################

THIRD_OF_WIDTH = int(WIDTH / 3)
SIXTH_OF_WIDTH = int(WIDTH / 6)
THIRD_OF_HEIGHT = int(HEIGHT / 3)

PLAYER_0_MENU_COORDINATES = [Coordinates(
    x = THIRD_OF_WIDTH * i + SIXTH_OF_WIDTH - MENU_UNIT_CELL_SIZE / 2,
    y = THIRD_OF_HEIGHT - MENU_UNIT_CELL_SIZE / 2,
    width = MENU_UNIT_CELL_SIZE,
    height = MENU_UNIT_CELL_SIZE
) for i in range(NUM_PLAYERS_0)]

# La seule chose différente par rapport à au-dessus est le y -> 2/3 de la hauteur au lieu de 1/3
PLAYER_1_MENU_COORDINATES = [Coordinates(
    x = THIRD_OF_WIDTH * i + SIXTH_OF_WIDTH - MENU_UNIT_CELL_SIZE / 2,
    y = THIRD_OF_HEIGHT * 2 - MENU_UNIT_CELL_SIZE / 2,
    width = MENU_UNIT_CELL_SIZE,
    height = MENU_UNIT_CELL_SIZE
) for i in range(NUM_PLAYERS_1)]


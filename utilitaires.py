import pygame

### Constantes
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

# Polices
pygame.font.init()
menu_font = pygame.font.SysFont('Arial Black', 25)
grid_font = pygame.font.SysFont('Arial Black', 18)

# Classe coordonnées
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

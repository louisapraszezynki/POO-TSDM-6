import pygame

### Constantes
GRID_SIZE = 8
CELL_SIZE = 120

MENU_UNIT_CELL_SIZE = 240
UNIT_CELL_SIZE = 80

WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MARGIN = 10

NUM_PLAYERS_0 = 3
NUM_PLAYERS_1 = 3

# Police
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

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


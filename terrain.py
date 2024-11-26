import pygame

CELL_SIZE = 120

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
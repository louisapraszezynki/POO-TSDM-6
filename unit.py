import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
            unit_type : str : Type de l'unité ('mage', 'chevalier', ou 'archer')
        """
        self.x = x
        self.y = y
        self.health = health
        self.resistance = resistance
        self.speed = speed
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.unit_type = unit_type # 'MAGE' ou 'CHEVALIER' ou 'ARCHER'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        # Couleurs par défaut
        if self.team == 'player':
            if self.unit_type == 'mage':
                color = (0, 0, 255)  # Bleu
            elif self.unit_type == 'chevalier':
                color = (0, 255, 0)  # Vert
            elif self.unit_type == 'archer':
                color = (255, 255, 0)  # Jaune
        else:
            if self.unit_type == 'mage':
                color = (128, 0, 128)  # Violet
            elif self.unit_type == 'chevalier':
                color = (255, 0, 0)  # Rouge
            elif self.unit_type == 'archer':
                color = (255, 165, 0)  # Orange

        # Dessin de l'unité
        if self.is_selected:
            pygame.draw.rect(screen, (0, 255, 255), (self.x * CELL_SIZE,
                                                     self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# Définition des sous-classes des différentes unités
class Mage(Unit):

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        super().__init__(x, y, health, attack_power, resistance, speed, team , unit_type)
        self.health == 100
        self.attack_power == 10
        self.resistance == 8
        self.speed == 4
        self.unit-type == 'MAGE'

class Chevalier(Unit):

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        super().__init__(x, y, health, attack_power, resistance, speed, team , unit_type)
        self.health == 120
        self.attack_power == 12
        self.resistance == 9
        self.speed == 5
        self.unit-type == 'CHEVALIER'

class Archer(Unit):

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        super().__init__(x, y, health, attack_power, resistance, speed, team , unit_type)
        self.health == 100
        self.attack_power == 11
        self.resistance == 10
        self.speed == 3
        self.unit-type == 'ARCHER'




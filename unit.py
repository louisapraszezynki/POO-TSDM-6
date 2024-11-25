import pygame
import random

################### Constantes ###################
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
##################################################

TERRAIN_TYPES = {
    "plain": (200, 200, 200),  # Gris clair
    "water": (0, 0, 255),      # Bleu
    "fire": (255, 0, 0),       # Rouge
    "wall": (50, 50, 50)       # Gris foncé
}

#### SuperClasse d'attaques ####
class Skills:
    def __init__(self, attack_type, range, power, area_of_effect):
        self.attack_type = attack_type
        self.range = range
        self.power = power
        self.area_of_effect = area_of_effect
    

# Sous-classes d'attaques
class Spell(Skills):
    def __init__(self, attack_type, range, power, area_of_effect):
        super().__init__(attack_type, range, power, area_of_effect)
        self.attack_type == 'spell'

class Weapon(Skills):
    def __init__(self, attack_type, range, power, area_of_effect):
        super().__init__(attack_type, range, power, area_of_effect)
        self.attack_type == 'weapon'

class Regen(Skills):
    def __init__(self, attack_type, range, power, area_of_effect):
        super().__init__(attack_type, range, power, area_of_effect)
        self.attack_type == 'regen'


#### SuperClasse des Unités ###
class Unit:

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        self.x = x
        self.y = y
        self.health = health
        self.resistance = resistance
        self.speed = speed
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.unit_type = unit_type # 'MAGE' ou 'CHEVALIER' ou 'ARCHER'
        self.is_selected = False

    def move(self, dx, dy, terrain_grid):
        """Déplace l'unité en tenant compte des restrictions du terrain."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifiez que la position cible est dans la grille
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            terrain_type = terrain_grid[new_y][new_x]

            # Bloquez le déplacement sur un mur
            if terrain_type == "wall":
                return  # Pas de déplacement si c'est un mur

            # Appliquez des effets selon le type de terrain
            if terrain_type == "fire":
                self.health -= 5  # Le feu inflige des dégâts

            # Déplacez l'unité si le terrain est accessible
            self.x = new_x
            self.y = new_y

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""

        # Couleurs des unités
        if self.team == 'player':
            if self.unit_type == 'mage':
                color = (0, 0, 255)  # Bleu
            elif self.unit_type == 'chevalier':
                color = (0, 255, 0)  # Vert
            elif self.unit_type == 'archer':
                color = (255, 255, 0)  # Jaune
        else:
            if self.unit_type == 'mage':
                color = (0, 0, 255)  # Bleu
            elif self.unit_type == 'chevalier':
                color = (0, 255, 0)  # Vert
            elif self.unit_type == 'archer':
                color = (255, 255, 0)  # Jaune

        # Dessin de l'unité
        if self.is_selected:
            pygame.draw.rect(screen, (0, 255, 255), (self.x * CELL_SIZE,
                                                     self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2,
                                           self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


# Sous-classes des unités
class Mage(Unit):

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        super().__init__(x, y, health, attack_power, resistance, speed, team , unit_type)
        self.health == 100
        self.attack_power == 10
        self.resistance == 10
        self.speed == 4
        self.unit_type == 'MAGE'

    skills = [Spell('spell', 4, 3, 3), Regen('regen', 3, 7, 3)]


class Chevalier(Unit):

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        super().__init__(x, y, health, attack_power, resistance, speed, team , unit_type)
        self.health == 120
        self.attack_power == 12
        self.resistance == 7
        self.speed == 5
        self.unit_type == 'CHEVALIER'
    
    skills = [Weapon('weapon', 1, 1, 1), Regen('regen', 1, 3, 1)]


class Archer(Unit):

    def __init__(self, x, y, health, attack_power, resistance, speed, team , unit_type):
        super().__init__(x, y, health, attack_power, resistance, speed, team , unit_type)
        self.health == 100
        self.attack_power == 11
        self.resistance == 12
        self.speed == 3
        self.unit_type == 'ARCHER'
    
    skills = [Weapon('weapon', 6, 1, 2), Regen('regen', 1, 2, 1)]
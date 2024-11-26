import pygame
from utilitaires import *




def display_character(
    screen,
    coordinates,
    class_type,
    selected: bool,
    in_menu: bool = False
):
    # Si le personnage actuellement en train d'être selectionné est celui-ci, alors on fait un cercle blanc
    # un peu plus large derrière pour le distinguer
    if selected:
        pygame.draw.rect(screen, RED,
                         (coordinates.x - 2, coordinates.y - 2, coordinates.width + 4, coordinates.height + 4), width=3)

        unit_class = UNIT_CLASSES[class_type]
        health = unit_class.health
        attack_power = unit_class.attack_power
        full_string = f"Health: {health}, Attack power: {attack_power}"

        start_text_surface = font.render(full_string, False, WHITE)
        screen.blit(start_text_surface, (MARGIN, HEIGHT - 50))

    if in_menu:
        screen.blit(MENU_UNIT_IMAGES[class_type], (coordinates.x, coordinates.y))
    else:
        screen.blit(UNIT_IMAGES[class_type], (coordinates.x, coordinates.y))


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
        self.attack_type = 'spell'

class Weapon(Skills):
    def __init__(self, attack_type, range, power, area_of_effect):
        super().__init__(attack_type, range, power, area_of_effect)
        self.attack_type = 'weapon'

class Regen(Skills):
    def __init__(self, attack_type, range, power, area_of_effect):
        super().__init__(attack_type, range, power, area_of_effect)
        self.attack_type = 'regen'


#### SuperClasse des Unités ###
class Unit:
    health = None
    resistance = None
    attack_power = None
    unit_type = None # 'MAGE' ou 'CHEVALIER' ou 'ARCHER'


    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def draw_health_bar(self, screen):
        """Dessine la barre de vie de l'unité."""
        # Position de la barre (au-dessus de l'unité)
        bar_width = CELL_SIZE - 10
        bar_height = 5
        bar_x = self.x * CELL_SIZE + 5
        bar_y = self.y * CELL_SIZE - bar_height - 2

        # Calcul de la largeur de la barre en fonction des PV restants
        health_percentage = max(0, self.health / 100)  # Supposons que 100 est le max des PV
        current_bar_width = int(bar_width * health_percentage)

        # Barre de fond (rouge)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Barre de vie (vert)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))

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
        gauche_de_case = self.x * CELL_SIZE + (CELL_SIZE - UNIT_CELL_SIZE) / 2
        haut_de_case = self.y * CELL_SIZE + (CELL_SIZE - UNIT_CELL_SIZE) / 2

        coordinates = Coordinates(gauche_de_case, haut_de_case, UNIT_CELL_SIZE, UNIT_CELL_SIZE)
        display_character(screen, coordinates, self.unit_type, self.is_selected)

        self.draw_health_bar(screen)


class Mage(Unit):
    health = 100
    attack_power = 10
    resistance = 4
    speed = 4
    unit_type = 'MAGE'
    skills = [
        Spell('spell', 4, 3, 3),
        Regen('regen', 3, 7, 3)
    ]


class Chevalier(Unit):
    health = 120
    attack_power = 12
    resistance = 7
    speed = 5
    unit_type = 'CHEVALIER'
    skills = [
        Weapon('weapon', 1, 1, 1),
        Regen('regen', 1, 3, 1)
    ]


class Archer(Unit):
    health = 100
    attack_power = 11
    resistance = 12
    speed = 3
    unit_type = 'ARCHER'
    skills = [
        Weapon('weapon', 6, 1, 2),
        Regen('regen', 1, 2, 1)
    ]

UNIT_TYPES = ["MAGE", "ARCHER", "CHEVALIER"]
UNIT_CLASSES = {
    'MAGE': Mage,
    'CHEVALIER': Chevalier,
    'ARCHER': Archer,
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

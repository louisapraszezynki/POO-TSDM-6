import pygame
from utilitaires import *



# Affichage des types d'unités dans le menu de sélection des personnages
def display_character_in_menu(
    screen,
    coordinates,
    class_type,
    selected,
    team
):
    # Si le personnage actuellement en train d'être selectionné est celui-ci, alors on fait un carré blanc
    # un peu plus large derrière pour le distinguer
    if selected:
        pygame.draw.rect(screen, RED if team == 'enemy' else BLUE,
                         (coordinates.x - 2, coordinates.y - 2, coordinates.width + 4, coordinates.height + 4), width=3)

        unit_class = UNIT_CLASSES[class_type]
        health = unit_class.health
        attack_power = unit_class.attack_power
        speed = unit_class.speed
        full_string = f"Health: {health}, Attack power: {attack_power}, Speed: {speed}"

        start_text_surface = menu_font.render(full_string, False, WHITE)
        screen.blit(start_text_surface, (MARGIN, HEIGHT - 50))

    screen.blit(MENU_UNIT_IMAGES[class_type], (coordinates.x, coordinates.y))


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
        # La Regen utilise un power négatif
        # Un type avec des grosses résis se fera plus heal
        super().__init__(attack_type, range, power, area_of_effect)
        self.attack_type = 'regen'


#### SuperClasse des Unités ###
class Unit:
    health = None
    max_health = None
    resistance = None
    attack_power = None
    unit_type = None # 'MAGE' ou 'CHEVALIER' ou 'ARCHER'

    def __init__(self, x, y, team, position):
        self.x = x
        self.y = y
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.action_1_selected = False
        self.action_2_selected = False
        self.already_attacked = False
        self.movement_this_turn = 0
        self.position = position

# Dessins permanents
    def draw_health_bar(self, screen):
        # Position de la barre (au-dessus de l'unité)
        bar_width = CELL_SIZE - 10
        bar_height = 5
        bar_x = self.x * CELL_SIZE + 5
        bar_y = self.y * CELL_SIZE + bar_height - 2

        # Calcul de la largeur de la barre en fonction des PV restants
        health_percentage = (self.health*100) / self.max_health
        current_bar_width = int((health_percentage*bar_width)/100)

        # Barre d'équipe
        pygame.draw.rect(screen, BLUE if self.team == 'player' else RED, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))

        # Barre de fond (rouge)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))

        # Barre de vie (vert)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_bar_width, bar_height))

    def display_teams(self,
        screen,
        position,
        selected: bool
    ):
        
        largeur = WIDTH - (CELL_SIZE - 5)
        hauteur = (CELL_SIZE * position) + 10

        screen.blit(UNIT_IMAGES[self.unit_type], (largeur , hauteur))
        if selected:
            pygame.draw.rect(
                screen, 
                BLUE, 
                (largeur - 2, hauteur - 2, UNIT_CELL_SIZE + 4, UNIT_CELL_SIZE + 4), 
                width=3
            )

    def display_ennemies(self,
        screen,
        position,
        selected: bool
    ):
        
        largeur = WIDTH - (CELL_SIZE - 5)
        hauteur = HEIGHT - (CELL_SIZE * position) - 10

        screen.blit(UNIT_IMAGES[self.unit_type], (largeur , hauteur))
        if selected:
            pygame.draw.rect(
                screen, 
                BLUE, 
                (largeur - 2, hauteur - 2, UNIT_CELL_SIZE + 4, UNIT_CELL_SIZE + 4), 
                width=3
            )

    def draw(self, screen):
        self.display_character_on_map(screen, self.is_selected)
        self.draw_health_bar(screen)

    def draw_teams(self, screen):
        self.display_teams(screen, self.position, self.is_selected)
    
    def draw_ennemies(self, screen):
        self.display_ennemies(screen, self.position, self.is_selected)

    def display_character_on_map(
        self,
        screen,
        selected: bool,
    ):
       
        gauche_de_case = self.x * CELL_SIZE + (CELL_SIZE - UNIT_CELL_SIZE) / 2
        haut_de_case = self.y * CELL_SIZE + (CELL_SIZE - UNIT_CELL_SIZE) / 2
        
        # Si le personnage actuellement en train d'être selectionné est celui-ci, alors on fait un carré bleu
        # un peu plus large derrière pour le distinguer
        if selected:
            pygame.draw.rect(
                screen, 
                BLUE, 
                (gauche_de_case - 2, haut_de_case - 2, UNIT_CELL_SIZE + 4, UNIT_CELL_SIZE + 4), 
                width=3
            )

            movement_left = max(0, self.speed - self.movement_this_turn)
            full_string = f"Health: {self.health}    Attack power: {self.attack_power}    Movement left: {movement_left}"

            start_text_surface = grid_font.render(full_string, False, WHITE)
            screen.blit(start_text_surface, (MARGIN, HEIGHT - 40))

        screen.blit(UNIT_IMAGES[self.unit_type], (gauche_de_case, haut_de_case))

# Dessins joueur par joueur
    def draw_stats(self, screen):
        action_string = f"Action 1 (A): {self.actions[0]}      Action 2 (Z): {self.actions[1]}"
        start_text_surface = grid_font.render(action_string, False, WHITE)
        screen.blit(start_text_surface, (MARGIN, HEIGHT - 90))
    
    def draw_selected_stat(self, screen):
        if self.action_1_selected is True :
            action_string = f"Selected action : {self.actions[0]}"
            start_text_surface = grid_font.render(action_string, False, BLUE)
            screen.blit(start_text_surface, (MARGIN, HEIGHT - 65))
        
        if self.action_2_selected is True:
            action_string = f"Selected action : {self.actions[1]}"
            start_text_surface = grid_font.render(action_string, False, BLUE)
            screen.blit(start_text_surface, (MARGIN, HEIGHT - 65))


# Actions
    def move(self, dx, dy, terrain_grid, unit_positions):

        # Si l'unité ne se déplace pas, on return tout de suite pour ne pas subi de malus additionnels
        if dx == 0 and dy == 0:
            return False

        # Déplace l'unité en tenant compte des restrictions du terrain
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifiez que la position cible est dans la grille
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            terrain_type = terrain_grid[new_y][new_x]

            # Bloquez le déplacement sur un mur
            if terrain_type == "wall" or (new_x, new_y) in unit_positions:
                return False

            # Le feu inflige des dégâts
            if terrain_type == "fire":
                self.health -= 5

            # L'eau ralentit
            if terrain_type == "water":
                if self.speed > 0:
                    self.speed -= 1


            # Déplacez l'unité si le terrain est accessible
            self.x = new_x
            self.y = new_y

        return True

    def attack(self, skill, target):

        if self.already_attacked:
            return

        # Correspond aux stats dans Dofousse
        attack_power = self.attack_power

        # Correspond a la plage de degats de base du sort
        skill_power = skill.power 

        attack = skill_power + skill_power * (attack_power / 100)

        # Degats qu'on enleve des degats finaux = on se protege
        resistances = target.resistance

        total_attack = attack - resistances

        target.health -= total_attack

        # Pour pas que les unit aient plus de 100% de leur vie
        if target.health > target.max_health:
            target.health = target.max_health

        self.already_attacked = True

    def get_action_range(self, action_range):
        # Retourne les coordonnées accessibles en fonction de la portée
        accessible_cells = []
        for dx in range(-action_range, action_range + 1):
            for dy in range(-action_range, action_range + 1):
                if abs(dx) + abs(dy) <= action_range:  # Portée en Manhattan
                    x, y = self.x + dx, self.y + dy
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Vérifie les limites de la grille
                        accessible_cells.append((x, y))
        return accessible_cells


# Sous classes des Unités
class Mage(Unit):
    health = 100
    max_health = 100
    attack_power = 100
    resistance = 4
    speed = 4
    unit_type = 'MAGE'
    actions = ['Spell', 'Regen']
    skills = [
        Spell('spell', 4, 10, 3), # attack_type, range, power, area_of_effect
        Regen('regen', 3, -7, 3) # attack_type, range, power, area_of_effect
    ]


class Chevalier(Unit):
    health = 120
    max_health = 120
    attack_power = 120
    resistance = 7
    speed = 5
    unit_type = 'CHEVALIER'
    actions = ['Weapon', 'Regen']
    skills = [
        Weapon('weapon', 1, 15, 1), # attack_type, range, power, area_of_effect
        Regen('regen', 1, 3, 1) # attack_type, range, power, area_of_effect
    ]


class Archer(Unit):
    health = 100
    max_health = 100
    attack_power = 80
    resistance = 12
    speed = 3
    unit_type = 'ARCHER'
    actions = ['Weapon', 'Regen']
    skills = [
        Weapon('weapon', 6, 6, 2), # attack_type, range, power, area_of_effect
        Regen('regen', 1, 2, 1) # attack_type, range, power, area_of_effect
    ]


UNIT_TYPES = ["MAGE", "ARCHER", "CHEVALIER"]
UNIT_CLASSES = {
    'MAGE': Mage,
    'CHEVALIER': Chevalier,
    'ARCHER': Archer,
}
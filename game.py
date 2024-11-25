import pygame
import random

from unit import *

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


MARGIN = 10

##################################### CONSTANTES POUR LE MENU #####################################
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
###################################################################################################

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)




############################# CONSTANTES POUR LA SELECTION DE JOUEURS #############################
NUM_PLAYERS_0 = 3
NUM_PLAYERS_1 = 3
CIRCLE_RADIUS = 30

THIRD_OF_WIDTH = int(WIDTH / 3)
SIXTH_OF_WIDTH = int(WIDTH / 6)
THIRD_OF_HEIGHT = int(HEIGHT / 3)

PLAYER_0_MENU_COORDINATES = [Coordinates(
    x = THIRD_OF_WIDTH * i + SIXTH_OF_WIDTH,
    y = THIRD_OF_HEIGHT,
    width = CIRCLE_RADIUS,
    height = CIRCLE_RADIUS
) for i in range(NUM_PLAYERS_0)]

# La seule chose différente par rapport à au-dessus est le y -> 2/3 de la hauteur au lieu de 1/3
PLAYER_1_MENU_COORDINATES = [Coordinates(
    x = THIRD_OF_WIDTH * i + SIXTH_OF_WIDTH,
    y = THIRD_OF_HEIGHT * 2,
    width = CIRCLE_RADIUS,
    height = CIRCLE_RADIUS
) for i in range(NUM_PLAYERS_1)]
###################################################################################################

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [
            Unit(0, 0, 50, 40, 10, 4, 'player', 'mage'),
            Unit(1, 0, 100, 20, 30, 2, 'player', 'archer'),
            Unit(2, 0, 70, 25, 5, 3, 'player', 'chevalier')
        ]

        self.enemy_units = [
            Unit(6, 6, 50, 40, 10, 4, 'enemy', 'mage'),
            Unit(7, 6, 100, 20, 30, 2, 'enemy', 'archer'),
            Unit(5, 6, 70, 25, 5, 3, 'enemy', 'chevalier')
        ]

        # On déclare que l'état initial du menu sera d'être sur "START".
        self.selected_menu_item = 'START'

        # On déclare que l'état initial de sélection des joueurs sera sur le premier joueur
        self.selected_character_in_menu = 0
        # terrain types: plain, water, fire, wall
        self.terrain_grid = [
            ["plain", "plain", "water", "plain", "plain", "fire", "plain", "wall"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"],
            ["plain", "plain", "plain", "plain", "plain", "plain", "plain", "plain"]
        ]

    #### MENU DEMARRER - QUITTER ####
    def show_menu(self):
        
        self.screen.fill(BLACK) # Remplit l'écran en noir

        # On boucle à travers les événements PyGame
        for event in pygame.event.get():

            # Si on appuie sur la croix, alors le jeu doit se fermer
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Gestion des touches du clavier
            if event.type == pygame.KEYDOWN:
                # Si on appuie sur gauche et que "EXIT" est actuellement sélectionné, alors on va sur "START"
                if event.key == pygame.K_LEFT and self.selected_menu_item == 'EXIT':
                    self.selected_menu_item = 'START'

                # Si on appuie sur droite et que "START" est actuellement sélectionné, alors on va sur "EXIT"
                elif event.key == pygame.K_RIGHT and self.selected_menu_item == 'START':
                    self.selected_menu_item = 'EXIT'

                # Si on appuie sur la touche espace, alors on valide ce qui se passe sur le menu. START -> on démarre
                # EXIT -> on quitte le jeu (on a juste cp/cv ce qu'on fait lorsqu'on appuie sur la croix).
                elif event.key == pygame.K_SPACE:
                    if self.selected_menu_item == 'START':
                        return True
                    elif self.selected_menu_item == 'EXIT':
                        pygame.quit()
                        exit()

            # On dessine le bouton start avec pour but qu'il soit au milieu, à gauche de l'écran
            start_button = pygame.Rect(START_COORDINATES.x, START_COORDINATES.y, START_COORDINATES.width, START_COORDINATES.height)
            start_text_surface = my_font.render('START', False, WHITE)
            self.screen.blit(start_text_surface, (START_COORDINATES.x + MARGIN, START_COORDINATES.y))

            # On dessine le bouton exit avec pour but qu'il soit au milieu, à droite de l'écran
            exit_button = pygame.Rect(EXIT_COORDINATES.x, EXIT_COORDINATES.y, EXIT_COORDINATES.width, EXIT_COORDINATES.height)
            exit_text_surface = my_font.render('EXIT', False, WHITE)
            self.screen.blit(exit_text_surface, (EXIT_COORDINATES.x + MARGIN, EXIT_COORDINATES.y))

            # On donne une épaisseur de 5 au bouton s'il est sélectionné, 1 sinon
            pygame.draw.rect(self.screen, WHITE, start_button, 5 if self.selected_menu_item == 'START' else 1)
            pygame.draw.rect(self.screen, WHITE, exit_button, 5 if self.selected_menu_item == 'EXIT' else 1)

            pygame.display.flip()

        return False

    #### SELECTION DES PERSONNAGES ####
    def select_characters(self):

        # On commence par remplir l'écran de noir
        self.screen.fill(BLACK)

        # On boucle à travers les événements PyGame
        for event in pygame.event.get():

            # Si on appuie sur la croix, alors le jeu doit se fermer
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Gestion des touches du clavier
            if event.type == pygame.KEYDOWN:
                # Si on appuie sur la barre espace, on passe au personnage suivant qu'il faudra sélectionner
                if event.key == pygame.K_SPACE:
                    self.selected_character_in_menu += 1

                    if self.selected_character_in_menu >= NUM_PLAYERS_1 + NUM_PLAYERS_0:
                        return True

                # Si on appuie sur backspace, on revient au personnage précédent (sans pouvoir aller avant 0)
                if event.key == pygame.K_BACKSPACE:
                    self.selected_character_in_menu -= 1

                    if self.selected_character_in_menu < 0:
                        self.selected_character_in_menu = 0

            # On garde un index de personnage pour savoir si on est bien sur celui que nous sommes en train de changer
            character_index = 0

            def display_character(coordinates, color, index):
                # Si le personnage actuellement en train d'être selectionné est celui-ci, alors on fait un cercle blanc
                # un peu plus large derrière pour le distinguer
                if self.selected_character_in_menu == index:
                    pygame.draw.circle(self.screen, WHITE, (coordinates.x, coordinates.y), coordinates.width + 3)

                pygame.draw.circle(self.screen, color, (coordinates.x, coordinates.y), coordinates.width)

            for coordinates in PLAYER_0_MENU_COORDINATES:
                display_character(coordinates, RED, character_index)
                # On passe au personnage suivant, alors on augmente le character index
                character_index += 1

            for coordinates in PLAYER_1_MENU_COORDINATES:
                display_character(coordinates, BLUE, character_index)
                # On passe au personnage suivant, alors on augmente le character index
                character_index += 1

            pygame.display.flip()

        return False

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            movement = 0  # Compteur de mouvement
            player_movement_limit = selected_unit.speed  # Limite en fonction de la vitesse de l'unité

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0

                        # Déplacement (limité par la vitesse)
                        if movement < player_movement_limit:  # Vérification de la limite
                            if event.key == pygame.K_LEFT:
                                dx = -1
                                movement += 1
                            elif event.key == pygame.K_RIGHT:
                                dx = 1
                                movement += 1
                            elif event.key == pygame.K_UP:
                                dy = -1
                                movement += 1
                            elif event.key == pygame.K_DOWN:
                                dy = 1
                                movement += 1

                            selected_unit.move(dx, dy , self.terrain_grid)
                            self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy , self.terrain_grid)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu."""
        # Efface l'écran en noir
        self.screen.fill(BLACK)

        # Parcours de la grille et affichage des types de terrain
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # Définir le rectangle de chaque cellule
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                # Récupérer le type de terrain
                terrain_type = self.terrain_grid[y][x]

                # Remplir la cellule avec la couleur correspondante
                pygame.draw.rect(self.screen, TERRAIN_TYPES[terrain_type], rect)

                # Dessiner une bordure (blanche) autour de chaque cellule
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités sur la grille
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Rafraîchit l'affichage
        pygame.display.flip()

    ()


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Avant de passer à la boucle principale du jeu, on passe par le menu.
    game_ready_to_start = False
    while not game_ready_to_start:
        game_ready_to_start = game.show_menu()

    # Avant de passer à la boucle principale du jeu, on passe par le menu.
    characters_chosen = False
    while not characters_chosen:
        characters_chosen = game.select_characters()

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()

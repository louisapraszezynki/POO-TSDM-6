import pygame
import random

from unit import *
from terrain import TERRAIN_TYPES
from utilitaires import *


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


############################# CONSTANTES POUR LA SELECTION DE JOUEURS #############################

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
###################################################################################################


class Game:

    def __init__(self, screen):
 
        self.player_units = []
        self.enemy_units = []

        self.screen = screen

        # On déclare que l'état initial du menu sera d'être sur "START".
        self.selected_menu_item = 'START'

        # On déclare que l'état initial de sélection des joueurs sera sur le premier joueur
        # La valeur de cette variable se mettra à jour lorsque l'on appuie sur Espace/Return
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


        # Initialisation des unit types affichés dans le menu personnages
        # On veut mettre à jour cette liste pour que ça se change de manière dynamique
        # en appuyant sur la fleche droite
        self.unit_types = [0, 0, 0, 0, 0, 0]

    def init_units(self):
        # self.unit_types
        # [0, 0, 0, 0, 0, 0]

        # UNIT_TYPES = ["MAGE", "ARCHER", "CHEVALIER"]

        # UNIT_CLASSES = {
        #     'MAGE': Mage,
        #     'CHEVALIER': Chevalier,
        #     'ARCHER': Archer,
        # }

        self.player_units = [
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[0]]](0, 0, 'player'),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[1]]](1, 0, 'player'),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[2]]](2, 0, 'player'),
        ]

        self.enemy_units = [
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[3]]](6, 6, 'player'),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[4]]](7, 6, 'player'),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[5]]](5, 6, 'player'),
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
            start_text_surface = font.render('START', False, WHITE)
            self.screen.blit(start_text_surface, (START_COORDINATES.x + MARGIN, START_COORDINATES.y))

            # On dessine le bouton exit avec pour but qu'il soit au milieu, à droite de l'écran
            exit_button = pygame.Rect(EXIT_COORDINATES.x, EXIT_COORDINATES.y, EXIT_COORDINATES.width, EXIT_COORDINATES.height)
            exit_text_surface = font.render('EXIT', False, WHITE)
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


                if event.key == pygame.K_RIGHT:
                    current_value = self.unit_types[self.selected_character_in_menu]

                    # On va chercher la classe suivante dans UNIT_TYPES
                    current_value = current_value + 1

                    # On a que trois classes, donc on prend le modulo
                    current_value = current_value % 3

                    self.unit_types[self.selected_character_in_menu] = current_value

            # On garde un index de personnage pour savoir si on est bien sur celui que nous sommes en train de changer
            character_index = 0

            for coordinates in PLAYER_0_MENU_COORDINATES:
                # Le type de l'unit qu'on est actuellement en train de dessiner (0, 1, 2)
                current_unit_type = self.unit_types[character_index]
                # On récupère le type sous forme de chaîne de caractère
                current_unit_type = UNIT_TYPES[current_unit_type]

                display_character(self.screen, coordinates, current_unit_type, character_index == self.selected_character_in_menu, in_menu=True)
                # On passe au personnage suivant, alors on augmente le character index
                character_index += 1

            for coordinates in PLAYER_1_MENU_COORDINATES:
                # Le type de l'unit qu'on est actuellement en train de dessiner (0, 1, 2)
                current_unit_type = self.unit_types[character_index]
                # On récupère le type sous forme de chaîne de caractère
                current_unit_type = UNIT_TYPES[current_unit_type]

                display_character(self.screen, coordinates, current_unit_type, character_index == self.selected_character_in_menu, in_menu=True)
                # On passe au personnage suivant, alors on augmente le character index
                character_index += 1

            pygame.display.flip()

        return False

    #### TOURS DE JEU ####
    def handle_player_turn(self):

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
                        sx, sy = 0, 0

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
                        
                            selected_unit.move(dx, dy, self.terrain_grid)
                            self.flip_display()

                        # Choix de l'action 
                        if event.key == pygame.K_a:
                            selected_unit.action_1_selected = True
                            selected_unit.action_2_selected = False

                            # while action_1_selected:
                                # Touches directionnelles = déplacement du carré rouge dans la zone en surbrillance
                                # if event.key == pygame.K_LEFT:
                                #     sx = -1
                                # elif event.key == pygame.K_RIGHT:
                                #     sx = 1
                                # elif event.key == pygame.K_UP:
                                #     sy = -1
                                # elif event.key == pygame.K_DOWN:
                                #     sy = 1

                                # elif event.key == pygame.K_SPACE:
                                    # get coordonnées de la cellule sélectionnée
                                    # if (abs(dx) + abs(dy)) de la cellule sélectionnée < range: 
                                    # unit de coordonnées de la cellule sélectionnée = target
                                    # do selected_action sur target
                                        # Attaque (touche espace)
                                        # if event.key == pygame.K_SPACE:
                                            # for enemy in self.enemy_units:
                                                # if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                                    # selected_unit.attack(enemy)
                                                        # if enemy.health <= 0:
                                                            # self.enemy_units.remove(enemy)
                                    # action_1_selected = False
                                    

                        elif event.key == pygame.K_z:
                            selected_unit.action_2_selected = True
                            selected_unit.action_1_selected = False


                        # Mettre fin au tour 
                        elif event.key == pygame.K_RETURN:
                            has_acted = True
                            selected_unit.is_selected = False

                        self.flip_display()


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

    #### DESSIN DE L'ECRAN ####
    def flip_display(self):
    
        # Remplit l'écran en noir
        self.screen.fill(BLACK)

        # Affiche les terrains
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                a = x * CELL_SIZE
                b = y * CELL_SIZE
                self.screen.blit(TERRAIN_TYPES[self.terrain_grid[y][x]], (a, b))

        # Affiche les unités sur la grille
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

            if unit.is_selected:
                unit.draw_stats(self.screen)
                print(unit.is_selected, unit.action_1_selected, unit.action_2_selected)
            
                if unit.action_1_selected:
                    unit.draw_selected_stat(self.screen)
                    # draw_range() # Mise en surbrillance pour la range de l'action 1
                    # draw_selection_range() # Carré rouge de déplacement de l'action 1

                if unit.action_2_selected:
                    unit.draw_selected_stat(self.screen)
                    # draw_range() # Mise en surbrillance pour la range de l'action 2
                    # draw_selection_range() # Carré rouge de déplacement de l'action 2
        
        # Rafraîchit l'affichage
        pygame.display.flip()


#### Main ####
def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Avant de passer à la boucle principale du jeu, on passe par le menu démarrer
    game_ready_to_start = False
    while not game_ready_to_start:
        game_ready_to_start = game.show_menu()

    # Avant de passer à la boucle principale du jeu, on passe par le menu de choix de personnages
    characters_chosen = False
    while not characters_chosen:
        characters_chosen = game.select_characters()

    game.init_units()

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()

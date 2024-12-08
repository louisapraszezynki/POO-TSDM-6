import pygame
import random

from unit import *
from utilitaires import *
from objects import *


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
            ["water", "water", "water", "plain", "plain", "plain", "wall", "wall"],
            ["water", "water", "plain", "plain", "fire", "fire", "fire", "wall"],
            ["water", "plain", "plain", "plain", "fire", "fire", "wall", "plain"],
            ["water", "plain", "plain", "plain", "plain", "fire", "plain", "plain"],
            ["plain", "water", "water", "water", "plain", "plain", "plain", "plain"],
            ["plain", "wall", "wall", "water", "plain", "plain", "plain", "wall"],
            ["wall", "wall", "plain", "plain", "plain", "plain", "plain", "wall"],
            ["wall", "wall", "plain", "plain", "plain", "plain", "wall", "wall"]
        ]

        # Initialisation des unit types affichés dans le menu personnages
        # On veut mettre à jour cette liste pour que ça se change de manière dynamique
        # en appuyant sur la fleche droite
        self.unit_types = [0, 0, 0, 0, 0, 0]

        self.selected_attack_position = [1, 1]

        self.objects = [Apple(6, 3), Apple(3, 3), Chicken(7, 2), Chicken(3, 6), Apple(5, 0)]

    #### INITIALISATION EQUIPES ####
    def init_units(self):

        self.player_units = [
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[0]]](3, 0, 'player', 0),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[1]]](2, 1, 'player', 1),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[2]]](1, 2, 'player', 2),
        ]

        self.enemy_units = [
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[3]]](6, 5, 'enemy', 3),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[4]]](6, 6, 'enemy', 4),
            UNIT_CLASSES[UNIT_TYPES[self.unit_types[5]]](5, 7, 'enemy', 5),
        ]

    #### MENU STRAT EXIT ####
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
            start_text_surface = menu_font.render('START', False, WHITE)
            self.screen.blit(start_text_surface, (START_COORDINATES.x + MARGIN, START_COORDINATES.y))

            # On dessine le bouton exit avec pour but qu'il soit au milieu, à droite de l'écran
            exit_button = pygame.Rect(EXIT_COORDINATES.x, EXIT_COORDINATES.y, EXIT_COORDINATES.width, EXIT_COORDINATES.height)
            exit_text_surface = menu_font.render('EXIT', False, WHITE)
            self.screen.blit(exit_text_surface, (EXIT_COORDINATES.x + MARGIN, EXIT_COORDINATES.y))

            # On donne une épaisseur de 5 au bouton s'il est sélectionné, 1 sinon
            pygame.draw.rect(self.screen, WHITE, start_button, 5 if self.selected_menu_item == 'START' else 1)
            pygame.draw.rect(self.screen, WHITE, exit_button, 5 if self.selected_menu_item == 'EXIT' else 1)

            pygame.display.flip()

        return False

    #### MENU SELECTION DES PERSONNAGES ####
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

                display_character_in_menu(self.screen, coordinates, current_unit_type, character_index == self.selected_character_in_menu, team='player')
                # On passe au personnage suivant, alors on augmente le character index
                character_index += 1

            for coordinates in PLAYER_1_MENU_COORDINATES:
                # Le type de l'unit qu'on est actuellement en train de dessiner (0, 1, 2)
                current_unit_type = self.unit_types[character_index]
                # On récupère le type sous forme de chaîne de caractère
                current_unit_type = UNIT_TYPES[current_unit_type]

                display_character_in_menu(self.screen, coordinates, current_unit_type, character_index == self.selected_character_in_menu, team='enemy')
                # On passe au personnage suivant, alors on augmente le character index
                character_index += 1

            pygame.display.flip()

        return False

    #### TOURS DE JEU ####
    def handle_player_turn(self):
        for selected_unit in self.player_units:

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
                        if selected_unit.action_1_selected is False and selected_unit.action_2_selected is False:
                            if selected_unit.movement_this_turn < selected_unit.speed:  # Vérification de la limite
                                if event.key == pygame.K_LEFT:
                                    dx = -1
                                elif event.key == pygame.K_RIGHT:
                                    dx = 1
                                elif event.key == pygame.K_UP:
                                    dy = -1
                                elif event.key == pygame.K_DOWN:
                                    dy = 1

                                unit_has_moved = selected_unit.move(dx, dy, self.terrain_grid, self.get_unit_positions())

                                if unit_has_moved:
                                    selected_unit.movement_this_turn += 1
                                    for object in self.objects:
                                        if (selected_unit.x, selected_unit.y) == (object.x, object.y):
                                            selected_unit.health += object.health
                                            object.is_used = True

                            self.dead_or_alive()

                            if not self.player_units or not self.enemy_units:
                                return

                        else:
                            if selected_unit.action_1_selected:
                                range = selected_unit.skills[0].range
                            elif selected_unit.action_2_selected:
                                range = selected_unit.skills[1].range

                            accessible_cells = selected_unit.get_action_range(range)

                            current_x = selected_unit.x + self.selected_attack_position[0]
                            current_y = selected_unit.y + self.selected_attack_position[1]

                            if event.key == pygame.K_LEFT:
                                if (current_x - 1, current_y) in accessible_cells:
                                    self.selected_attack_position[0] -= 1
                            elif event.key == pygame.K_RIGHT:
                                if (current_x + 1, current_y) in accessible_cells:
                                    self.selected_attack_position[0] += 1
                            elif event.key == pygame.K_UP:
                                if (current_x, current_y - 1) in accessible_cells:
                                    self.selected_attack_position[1] -= 1
                            elif event.key == pygame.K_DOWN:
                                if (current_x, current_y + 1) in accessible_cells:
                                    self.selected_attack_position[1] += 1

                        # Choix de l'action
                        if event.key == pygame.K_a:
                            if selected_unit.action_1_selected is True:
                                selected_unit.action_1_selected = False
                            else:
                                selected_unit.action_1_selected = True
                                selected_unit.action_2_selected = False
                            self.selected_attack_position = [0, 0]

                        elif event.key == pygame.K_z:
                            if selected_unit.action_2_selected is True:
                                selected_unit.action_2_selected = False
                            else:
                                selected_unit.action_2_selected = True
                                selected_unit.action_1_selected = False
                            self.selected_attack_position = [0, 0]

                        elif event.key == pygame.K_SPACE:
                            current_x = selected_unit.x + self.selected_attack_position[0]
                            current_y = selected_unit.y + self.selected_attack_position[1]

                            target = self.target_unit(current_x, current_y)

                            if target is not None:
                                if selected_unit.action_1_selected:
                                    selected_unit.attack(selected_unit.skills[0], target)
                                elif selected_unit.action_2_selected:
                                    selected_unit.attack(selected_unit.skills[1], target)
                                
                                self.dead_or_alive()

                                if not self.player_units or not self.enemy_units:
                                    return
                            
                        # Mettre fin au tour
                        elif event.key == pygame.K_RETURN:
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.already_attacked = False
                            selected_unit.movement_this_turn = 0  # Compteur de mouvement

                        self.flip_display()

    def handle_enemy_turn(self):
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy , self.terrain_grid, self.get_unit_positions())

            for object in self.objects:
                if (enemy.x, enemy.y) == (object.x, object.y):
                    enemy.health += object.health
                    object.is_used = True

            viable_attacks = [skill for skill in enemy.skills if skill.attack_type != 'regen']

            # Attaque si possible
            enemy_attack = random.choice(viable_attacks)
            range = enemy_attack.range

            if abs((enemy.x - target.x) + (enemy.y - target.y)) <= range:
                enemy.attack(enemy_attack, target)

                if target.health <= 0:
                    self.player_units.remove(target)

                if not self.player_units or not self.enemy_units:
                    return
            
            enemy.already_attacked = False

    #### FIN DE LA PARTIE ####
    def show_results(self, result):
        self.screen.fill(BLACK) # Remplit l'écran en noir

        exit_text_surface = menu_font.render(result, False, WHITE)
        self.screen.blit(exit_text_surface, (WIDTH / 2 - 100 + 5, HEIGHT / 2 - 120))
        pygame.draw.rect(self.screen, WHITE, (WIDTH / 2 - 130, HEIGHT / 2 - 120, 260, 50), 1)

        # On boucle à travers les événements PyGame
        for event in pygame.event.get():

            # Si on appuie sur la croix, alors le jeu doit se fermer
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            pygame.display.flip()

    #### HELPERS METHODS ####
    def dead_or_alive(self):
        # Regarde si des joueurs sont morts et les supprime de leur équipe respective
        for player in self.player_units:
            if player.health <= 0:
                self.player_units.remove(player)

        for enemy in self.enemy_units:
            if enemy.health <= 0:
                self.enemy_units.remove(enemy)

    def get_unit_positions(self):
        # Renvoie une liste de toutes les positions actuellement occupées par une entité
        unit_positions = []
        for player in self.player_units:
            unit_positions.append((player.x, player.y))
        for enemy in self.enemy_units:
            unit_positions.append((enemy.x, enemy.y))
        return unit_positions

    def target_unit(self, x, y):
        for player in self.player_units:
            if player.x == x and player.y == y:
                return player
            
        for enemy in self.enemy_units:
            if enemy.x == x and enemy.y == y:
                return enemy

    def draw_range(self, unit, action_range):
        """Dessine les cases accessibles pour une unité donnée."""
        accessible_cells = unit.get_action_range(action_range)
        for x, y in accessible_cells:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, BLUE, rect, 2)  # Bordure bleue pour indiquer la portée de l'action

    #### DESSINS ####
    def flip_display(self):
        # Remplit l'écran en noir
        self.screen.fill(BLACK)

        # Affiche les terrains
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                a = x * CELL_SIZE
                b = y * CELL_SIZE
                self.screen.blit(TERRAIN_TYPES[self.terrain_grid[y][x]], (a, b))
        
        # Affiche les objets s'ils ne sont pas utilisés
        for object in self.objects:
            if not object.is_used:
                self.screen.blit(OBJECTS_IMAGES[object.type], (CELL_SIZE * object.x + CELL_SIZE/4 , CELL_SIZE * object.y + CELL_SIZE/4))
                self.screen.blit(OBJECTS_IMAGES[object.type], (CELL_SIZE * object.x + CELL_SIZE/4 , CELL_SIZE * object.y + CELL_SIZE/4))

        # Affiche les unités sur la grille
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

            if unit.is_selected:
                unit.draw_stats(self.screen)

                x = unit.x + self.selected_attack_position[0]
                y = unit.y + self.selected_attack_position[1]

                if unit.action_1_selected:
                    unit.draw_selected_stat(self.screen)
                    self.draw_range(unit, unit.skills[0].range)  # Affiche la portée de l'action 1

                    target = self.target_unit(x, y)

                    if target is None:
                        image = IMAGES['attack']
                    elif target.team == 'player':
                        image = IMAGES['ally']
                    elif target.team == 'enemy':
                        image = IMAGES['enemy']      

                    self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))


                if unit.action_2_selected:
                    unit.draw_selected_stat(self.screen)
                    self.draw_range(unit, unit.skills[1].range)  # Affiche la portée de l'action 2

                    target = self.target_unit(x, y)

                    if target is None:
                        image = IMAGES['attack']
                    elif target.team == 'player':
                        image = IMAGES['ally']
                    elif target.team == 'enemy':
                        image = IMAGES['enemy']      

                    self.screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

        # Affiche les équipes sur le côté droit de l'écran
        for unit in self.player_units:
            unit.draw_teams(self.screen)
        
        for ennemy in self.enemy_units:
            ennemy.draw_ennemies(self.screen)

        # Rafraîchit l'affichage
        pygame.display.flip()


#### MAIN ####
def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Lancement de la musique
    pygame.mixer.init()
    pygame.mixer.music.load("music\Astrub.mp3")
    pygame.mixer.music.play(-1)

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
    while game.player_units and game.enemy_units :
        game.handle_player_turn()
        game.handle_enemy_turn()


    result = "You have lost" if not game.player_units else "You have won"

    if result == "You have lost":
        print(result)
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music\lose_music.mp3")
        pygame.mixer.music.play(-1)

    elif result == "You have won":
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music\win_music.mp3")
        pygame.mixer.music.play(-1)

    while True:
        game_results = game.show_results(result)

if __name__ == "__main__":
    main()

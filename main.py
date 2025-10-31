"""
Life - The Game
A PyGame-based game where you play as a virus collecting cells while avoiding antibodies.
"""
import math
import random
import sys

import pygame

# Game constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 580
SCREEN_PLAYABLE_HEIGHT = 480
SPEED = 3
SPEED_PLAYER = 3.1
DIAGONAL_FACTOR = 0.7071217222732374245  # 1/sqrt(2) for diagonal movement

# Game state variables
life = 10
start_time = 0
time_played = 0
count_score = 0
score = 0
level = 1
map_loc = [[1, 1], [2, 1], [1, 2], [2, 2]]
ia_increment = 60
game_state = False


# Random positioning
def random_pos(initial=0):
    """Generate random position within screen boundaries."""
    pos_x = random.randint(0 + initial, SCREEN_WIDTH - initial)
    pos_y = random.randint(0 + initial, SCREEN_PLAYABLE_HEIGHT - initial)
    return int(pos_x), int(pos_y)


# Set map positioning
# Essa função divide o mapa em 4 partes:
#   [1,1], [2,1],
#   [1,2], [2,2]
# baseado na posição [x,y] de um objeto
def set_map_position(object_rect):
    """Divide the map into 4 parts based on object position."""
    map_position = [0, 0]

    if object_rect.x < SCREEN_WIDTH / 2:
        map_position[0] = 1
    else:
        map_position[0] = 2
    if object_rect.y < SCREEN_PLAYABLE_HEIGHT / 2:
        map_position[1] = 1
    else:
        map_position[1] = 2

    return map_position


#  Define valores aleatórios para X e Y baseado no posicionamento em blocos
#  no mapa.
def set_m_position_pixel(map_position):
    """Define random X and Y values based on block positioning on the map."""
    position = [0, 0]
    if map_position[0] == 1:
        position[0] = random.randint(0, int((SCREEN_WIDTH / 2) - 1))
    else:
        position[0] = random.randint(int(SCREEN_WIDTH / 2), SCREEN_WIDTH)
    if map_position[1] == 1:
        position[1] = random.randint(0, int((SCREEN_PLAYABLE_HEIGHT / 2) - 1))
    else:
        position[1] = random.randint(int(SCREEN_PLAYABLE_HEIGHT / 2), SCREEN_PLAYABLE_HEIGHT)
    return position


# Antibody movement
def antibody_movement(antibody_rect):
    """Move antibody towards the player position."""
    if player_rect.x > antibody_rect.x:
        antibody_rect.x = antibody_rect.x + 1
    if player_rect.y > antibody_rect.y:
        antibody_rect.y = antibody_rect.y + 1
    if player_rect.x < antibody_rect.x:
        antibody_rect.x = antibody_rect.x - 1
    if player_rect.y < antibody_rect.y:
        antibody_rect.y = antibody_rect.y - 1


# Antibody mechanics
def antibody_ia(antibody_rect, ai_increment):
    """Control antibody AI behavior based on distance to player."""
    # This logic it's great
    c_value = ((player_rect.x - antibody_rect.x) ** 2) + ((player_rect.y - antibody_rect.y) ** 2)
    distance = math.sqrt(c_value)

    if distance < ai_increment:
        antibody_movement(antibody_rect)


def antibody_animation():
    """Animate antibody sprite."""
    global antibody, antibody_index, antibody_sprites

    antibody_index += 0.1

    if antibody_index < len(antibody_sprites):
        antibody = antibody_sprites[int(antibody_index)]
    else:
        antibody_index = 0


# Cell movement
def cell_movement(cell_rect, dot_rect):
    """Move cell towards the dot with diagonal speed compensation."""
    global cell, cell_index, cell_sprites

    speed_cell = SPEED

    if dot_rect.x != cell_rect.x and dot_rect.y != cell_rect.y:
        speed_cell = SPEED * DIAGONAL_FACTOR

    if dot_rect.x > cell_rect.x:
        cell_rect.x = cell_rect.x + speed_cell
    if dot_rect.y > cell_rect.y:
        cell_rect.y = cell_rect.y + speed_cell
    if dot_rect.x < cell_rect.x:
        cell_rect.x = cell_rect.x - speed_cell
    if dot_rect.y < cell_rect.y:
        cell_rect.y = cell_rect.y - speed_cell

    cell_index += 0.1

    if cell_index < len(cell_sprites):
        cell = cell_sprites[int(cell_index)]
    else:
        cell_index = 0


# Show info
def display_info():
    """Display game information (life, time, score, level) on screen."""
    # Info text
    player_life_text = font_text.render(f'LIFE: {life}', False, 'Black').convert_alpha()
    player_life_rect = player_life_text.get_rect(topleft=(0, game_name_text_rect.bottom + 10))

    current_time_played = int(pygame.time.get_ticks() / 1000) - start_time

    player_time_played_text = font_text.render(
        f'    TIME: {current_time_played}', False, 'Black'
    ).convert_alpha()
    player_time_played_rect = player_time_played_text.get_rect(topleft=player_life_rect.topright)

    player_score_text = font_text.render(f'      SCORE: {score}', False, 'Black').convert_alpha()
    player_score_rect = player_score_text.get_rect(topleft=player_time_played_rect.topright)

    player_level_text = font_text.render(f'LEVEL: {level}', False, 'Black').convert_alpha()
    player_level_rect = player_level_text.get_rect(topleft=player_life_rect.bottomleft)

    screen.blit(player_life_text, player_life_rect)
    screen.blit(player_time_played_text, player_time_played_rect)
    screen.blit(player_score_text, player_score_rect)
    screen.blit(player_level_text, player_level_rect)


def player_animation():
    """Animate player sprite."""
    global player, player_index, player_sprites

    player_index += 0.1

    if player_index < len(player_sprites):
        player = player_sprites[int(player_index)]
    else:
        player_index = 0


# Initializing the screen
pygame.init()

# Tamanho da tela do jogo e Framerate
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Title of game
pygame.display.set_caption('Basic PyGame Program')

# Icon of game
icon = pygame.image.load('images/Life_Logo.png')
pygame.display.set_icon(icon)

# Font of game
font_title = pygame.font.Font('font/joystix monospace.ttf', 18)
font_text = pygame.font.Font('font/joystix monospace.ttf', 12)
font_game_over = pygame.font.Font('font/joystix monospace.ttf', 24)

# ----------------------------------------------

# Player | Virus
player_1 = pygame.image.load('images/Virus_1.png').convert_alpha()
player_2 = pygame.image.load('images/Virus_2.png').convert_alpha()
player_sprites = [player_1, player_2]
player_index = 1
player = player_sprites[player_index]
player_pos = random_pos()
player_rect = player.get_rect(center=player_pos)
player_path = [[0, 0], [0, 0]]

# antibody | Enemy
antibody_1 = pygame.image.load('images/Antibody_1.png').convert_alpha()
antibody_2 = pygame.image.load('images/Antibody_2.png').convert_alpha()
antibody_3 = pygame.image.load('images/Antibody_3.png').convert_alpha()
antibody_sprites = [antibody_1, antibody_2, antibody_3]
antibody_index = 0

antibody = antibody_sprites[antibody_index]

# Create list of antibody rectangles for easier management
antibody_rects = []
for i in range(6):
    antibody_pos = random_pos()
    antibody_rects.append(antibody.get_rect(center=antibody_pos))

# Keep individual references for backward compatibility
antibody_rect = antibody_rects[0]
antibody1_rect = antibody_rects[1]
antibody2_rect = antibody_rects[2]
antibody3_rect = antibody_rects[3]
antibody4_rect = antibody_rects[4]
antibody5_rect = antibody_rects[5]

# Cell | Objective
background = pygame.image.load('images/Background.png').convert_alpha()
background_pos = (0, 0)
background_rect = background.get_rect(topleft=background_pos)

cell_1 = pygame.image.load('images/Cell_1.png').convert_alpha()
cell_2 = pygame.image.load('images/Cell_2.png').convert_alpha()
cell_sprites = [cell_1, cell_2]
cell_index = 0

cell = cell_sprites[cell_index]

cell_pos = random_pos()
cell_rect = cell.get_rect(center=cell_pos)

dot = pygame.image.load('images/Dot.png').convert_alpha()
dot_pos = random_pos()
dot_rect = dot.get_rect(center=dot_pos)

# Main text
game_name_text = font_title.render('LIFE - THE GAME', False, 'Black').convert_alpha()
game_name_text_rect = game_name_text.get_rect(midtop=(SCREEN_WIDTH / 2, SCREEN_PLAYABLE_HEIGHT + 20))


# -----------------------------------------

# Main loop

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state:

        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_UP] and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            player_rect = player_rect.move(0, SPEED_PLAYER * DIAGONAL_FACTOR * -1)
        else:
            if keys[pygame.K_UP]:
                player_rect = player_rect.move(0, SPEED_PLAYER * -1)

        if keys[pygame.K_DOWN] and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            player_rect = player_rect.move(0, SPEED_PLAYER * DIAGONAL_FACTOR)
        else:
            if keys[pygame.K_DOWN]:
                player_rect = player_rect.move(0, SPEED_PLAYER)

        if keys[pygame.K_LEFT] and (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            player_rect = player_rect.move(SPEED_PLAYER * DIAGONAL_FACTOR * -1, 0)
        else:
            if keys[pygame.K_LEFT]:
                player_rect = player_rect.move(SPEED_PLAYER * -1, 0)

        if keys[pygame.K_RIGHT] and (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            player_rect = player_rect.move(SPEED_PLAYER * DIAGONAL_FACTOR, 0)
        else:
            if keys[pygame.K_RIGHT]:
                player_rect = player_rect.move(SPEED_PLAYER, 0)
    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            life = 10
            start_time = int(pygame.time.get_ticks() / 1000)
            time_played = int(pygame.time.get_ticks() / 1000) - start_time
            count_score = 0
            score = 0
            level = 1
            ia_increment = 60
            game_state = True

    if game_state:

        # Screen color
        screen.fill('White')
        screen.blit(background, background_rect)

        player_path_current = set_map_position(player_rect)

        if player_path_current != player_path[1]:
            player_path[0] = player_path[1]
            player_path[1] = player_path_current

        free_path = player_path_current
        aux = -1

        while free_path in (player_path[0], player_path[1]):
            aux = random.randint(0, 3)
            free_path = map_loc[aux]

        player_animation()
        antibody_animation()

        # Render Player, Cell and antibody
        screen.blit(player, player_rect)
        screen.blit(cell, cell_rect)
        for antibody_r in antibody_rects:
            screen.blit(antibody, antibody_r)
        screen.blit(dot, dot_rect)
        screen.blit(game_name_text, game_name_text_rect)
        display_info()

        if count_score == 10:
            level += 1
            count_score = 0
            ia_increment += 10
            life += 1
            display_info()

        # Collider Cell to Player
        if cell_rect.colliderect(player_rect):
            score += 1
            count_score += 1
            display_info()
            cell_pos = random_pos(32)
            cell_rect = cell.get_rect(center=cell_pos)
        else:
            # Calculate distance between Cell and Player
            c_value = ((cell_rect.x - player_rect.x) ** 2) + ((cell_rect.y - player_rect.y) ** 2)
            distance_cell = math.sqrt(c_value)

            # Calculate distance between Food and Player
            c_value = ((dot_rect.x - player_rect.x) ** 2) + ((dot_rect.y - player_rect.y) ** 2)
            distance_dot = math.sqrt(c_value)

            c_value = ((cell_rect.x - dot_rect.x) ** 2) + ((cell_rect.y - dot_rect.y) ** 2)
            distance_food_cell = math.sqrt(c_value)

        # Movimentando a Célula
        cell_movement(cell_rect, dot_rect)

        # Verificando se o alimento e o player estão no mesmo bloco
        # Se for verdadeiro o alimento será renderizado em um novo bloco
        if set_map_position(dot_rect) == set_map_position(player_rect):

            while free_path in (player_path[0], player_path[1]):
                aux = random.randint(0, 3)
                free_path = map_loc[aux]

            dot_pos = set_m_position_pixel(free_path)
            dot_rect = dot.get_rect(center=dot_pos)
            screen.blit(dot, dot_rect)

        # Collider Cell to Food
        if cell_rect.colliderect(dot_rect):
            while free_path in (player_path[0], player_path[1]):
                aux = random.randint(0, 3)
                free_path = map_loc[aux]

            dot_pos = set_m_position_pixel(free_path)
            dot_rect = dot.get_rect(center=dot_pos)
            screen.blit(dot, dot_rect)

        # Calculate distance between Cell and Player
        c_value = ((cell_rect.x - player_rect.x) ** 2) + ((cell_rect.y - player_rect.y) ** 2)
        distance_cell = math.sqrt(c_value)

        # Antibody Collider - refactored to use loop
        collision_detected = False
        for i, antibody_r in enumerate(antibody_rects):
            if antibody_r.colliderect(player_rect):
                life -= 1
                display_info()
                antibody_pos = random_pos()
                antibody_rects[i] = antibody.get_rect(center=antibody_pos)
                collision_detected = True
                break

        # Update individual references
        antibody_rect = antibody_rects[0]
        antibody1_rect = antibody_rects[1]
        antibody2_rect = antibody_rects[2]
        antibody3_rect = antibody_rects[3]
        antibody4_rect = antibody_rects[4]
        antibody5_rect = antibody_rects[5]

        if not collision_detected:
            for antibody_r in antibody_rects:
                antibody_ia(antibody_r, ia_increment)

        if life == 0:
            game_state = False

    else:
        # Screen color
        screen.fill('White')
        screen.blit(background, background_rect)

        if life == 0:

            game_over_text = font_game_over.render('GAME OVER', False, 'Black').convert_alpha()
            game_over_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_PLAYABLE_HEIGHT / 2)
            )
            screen.blit(game_over_text, game_over_rect)

        else:

            game_over_text = font_game_over.render(
                'LIFE - THE GAME', False, 'Black'
            ).convert_alpha()
            game_over_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_PLAYABLE_HEIGHT / 2)
            )
            screen.blit(game_over_text, game_over_rect)

        game_over_info_text = font_title.render(
            'PRESS SPACE TO START', False, 'Black'
        ).convert_alpha()
        game_over_info_rect = game_over_info_text.get_rect(
            center=(SCREEN_WIDTH / 2, (SCREEN_PLAYABLE_HEIGHT / 2) + 30)
        )
        screen.blit(game_over_info_text, game_over_info_rect)

    # Refreshing the screen
    pygame.display.update()
    clock.tick(60)

import pygame, random, time, math
from sys import exit

screen_width = 640
screen_height = 580
screen_playable_height = 480
speed = 3
speed_player = 3.1
life = 10
start_time = 0
time_played = 0
count_score = 0
score = 0
level = 1
map_loc = [[1,1],[2,1],[1,2],[2,2]]
onetime = 0
ia_increment = 60
game_state = False

# Random positioning
def random_pos(initial=0):
    posX = random.randint(0+initial,screen_width-initial)
    posY = random.randint(0+initial,screen_playable_height-initial)
    return int(posX), int(posY)

# Set map positioning
# Essa função divide o mapa em 4 partes:
#   [1,1], [2,1],
#   [1,2], [2,2]
# baseado na posição [x,y] de um objeto
def set_map_position(object_rect):
    map_position = [0,0]

    if object_rect.x < screen_width/2:
        map_position[0] = 1
    else:
        map_position[0] = 2
    if object_rect.y < screen_playable_height/2:
        map_position[1] = 1
    else:
        map_position[1] = 2

    return map_position

#  Define valores aleatórios para X e Y baseado no posicionamento em blocos
#  no mapa.
def set_m_position_pixel(map_position):
    position = [0,0]
    if map_position[0] == 1:
        position[0] = random.randint(0,int((screen_width/2)-1))
    else:
        position[0] = random.randint(int(screen_width/2),screen_width)
    if map_position[1] == 1:
        position[1] = random.randint(0,int((screen_playable_height/2)-1))
    else:
        position[1] = random.randint(int(screen_playable_height/2),screen_playable_height)
    return position

# Antibody movement
def antibody_movement(antibody_rect):
    
    if (player_rect.x > antibody_rect.x):
        antibody_rect.x = antibody_rect.x + 1
    if (player_rect.y > antibody_rect.y):
        antibody_rect.y = antibody_rect.y + 1
    if (player_rect.x < antibody_rect.x):
        antibody_rect.x = antibody_rect.x - 1
    if (player_rect.y < antibody_rect.y):
        antibody_rect.y = antibody_rect.y - 1


# Antibody mechanics
def antibody_ia(antibody_rect,ia_increment):

    # This logic it's great
    c_value = ((player_rect.x-antibody_rect.x)**2)+((player_rect.y-antibody_rect.y)**2)
    distance = math.sqrt(c_value)

    if distance < ia_increment:
         antibody_movement(antibody_rect)

def antibody_animation():

    global antibody, antibody_index, antibody_sprites
    
    antibody_index += 0.1

    if antibody_index < len(antibody_sprites):
        antibody = antibody_sprites[int(antibody_index)]
    else:
        antibody_index = 0

# Cell movement
def cell_movement(cell_rect,dot_rect):
    
    global cell, cell_index, cell_sprites
    speed_cell = speed

    if (dot_rect.x != cell_rect.x) and (dot_rect.y != cell_rect.y):
        speed_cell = speed*0.7071217222732374245

    if (dot_rect.x > cell_rect.x):
        cell_rect.x = cell_rect.x + speed_cell
    if (dot_rect.y > cell_rect.y):
        cell_rect.y = cell_rect.y + speed_cell
    if (dot_rect.x < cell_rect.x):
        cell_rect.x = cell_rect.x - speed_cell
    if (dot_rect.y < cell_rect.y):
        cell_rect.y = cell_rect.y - speed_cell

    cell_index += 0.1

    if cell_index < len(cell_sprites):
        cell = cell_sprites[int(cell_index)]
    else:
        cell_index = 0

# Show info
def display_info():
    # Info text
    player_life_text = font_text.render(f'LIFE: {life}',False, 'Black').convert_alpha()
    player_life_rect = player_life_text.get_rect(topleft = (0,game_name_text_rect.bottom+10))

    time_played = int(pygame.time.get_ticks()/1000) - start_time

    player_time_played_text = font_text.render(f'    TIME: {time_played}',False, 'Black').convert_alpha()
    player_time_played_rect = player_time_played_text.get_rect(topleft = (player_life_rect.topright))
    # print(f'{type(player_life_rect.topright[1]}')

    player_score_text = font_text.render(f'      SCORE: {score}',False, 'Black').convert_alpha()
    player_score_rect = player_score_text.get_rect(topleft = (player_time_played_rect.topright))

    player_level_text = font_text.render(f'LEVEL: {level}',False, 'Black').convert_alpha()
    player_level_rect = player_level_text.get_rect(topleft = (player_life_rect.bottomleft))

    screen.blit(player_life_text,player_life_rect)
    screen.blit(player_time_played_text,player_time_played_rect)
    screen.blit(player_score_text,player_score_rect)
    screen.blit(player_level_text,player_level_rect)


def player_animation():
    global player, player_index, player_sprites
    
    player_index += 0.1

    if player_index < len(player_sprites):
        player = player_sprites[int(player_index)]
    else:
        player_index = 0


# Initializing the screen
pygame.init()

# Tamanho da tela do jogo e Framerate
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Title of game
pygame.display.set_caption('Basic PyGame Program')

# Icon of game
icon = pygame.image.load('images/Life_Logo.png')
pygame.display.set_icon(icon)

# Font of game
font_title = pygame.font.Font('font/joystix monospace.ttf',18)
font_text = pygame.font.Font('font/joystix monospace.ttf',12)
font_game_over = pygame.font.Font('font/joystix monospace.ttf',24)

# ----------------------------------------------

# Player | Virus
player_1 = pygame.image.load('images/Virus_1.png').convert_alpha()
player_2 = pygame.image.load('images/Virus_2.png').convert_alpha()
player_sprites = [player_1,player_2]
player_index = 1
player = player_sprites[player_index]
player_pos = random_pos()
player_rect = player.get_rect(center = player_pos)
player_path = [[0,0],[0,0]]

# antibody | Enemy
antibody_1 = pygame.image.load('images/Antibody_1.png').convert_alpha()
antibody_2 = pygame.image.load('images/Antibody_2.png').convert_alpha()
antibody_3 = pygame.image.load('images/Antibody_3.png').convert_alpha()
antibody_sprites = [antibody_1,antibody_2,antibody_3]
antibody_index = 0

antibody = antibody_sprites[antibody_index]

antibody_pos = random_pos()
antibody_rect = antibody.get_rect(center = antibody_pos)

antibody1_pos = random_pos()
antibody1_rect = antibody.get_rect(center = antibody1_pos)

antibody2_pos = random_pos()
antibody2_rect = antibody.get_rect(center = antibody2_pos)

antibody3_pos = random_pos()
antibody3_rect = antibody.get_rect(center = antibody3_pos)

antibody4_pos = random_pos()
antibody4_rect = antibody.get_rect(center = antibody4_pos)

antibody5_pos = random_pos()
antibody5_rect = antibody.get_rect(center = antibody5_pos)


# Cell | Objective
background = pygame.image.load('images/Background.png').convert_alpha()
background_pos = (0,0)
background_rect = background.get_rect(topleft = background_pos)

cell_1 = pygame.image.load('images/Cell_1.png').convert_alpha()
cell_2 = pygame.image.load('images/Cell_2.png').convert_alpha()
cell_sprites = [cell_1,cell_2]
cell_index = 0

cell = cell_sprites[cell_index]

cell_pos = random_pos()
cell_rect = cell.get_rect(center = cell_pos)

dot = pygame.image.load('images/Dot.png').convert_alpha()
dot_pos = random_pos()
dot_rect = dot.get_rect(center = dot_pos)

# Main text
game_name_text = font_title.render('LIFE - THE GAME',False, 'Black').convert_alpha()
game_name_text_rect = game_name_text.get_rect(midtop = (screen_width/2,screen_playable_height + 20))

# # Info text
# player_life_text = font.render(f'{life}',False, 'Black').convert_alpha()
# player_life_text_pos = (int(250),int(481))

# player_time_played_text = font.render(f'{time_played}',False, 'Black').convert_alpha()
# player_time_played_text_pos = (int(250),int(501))

# player_score_text = font.render(f'{score}',False, 'Black').convert_alpha()
# player_score_text_pos = (int(250),int(521))

# player_level_text = font.render(f'{level}',False, 'Black').convert_alpha()
# player_level_text_pos = (int(300),int(481))


# -----------------------------------------

# Main loop

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_state:

        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_UP] and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            player_rect = player_rect.move(0,speed_player*0.7071217222732374245*-1)
        else:
            if keys[pygame.K_UP]:
                player_rect = player_rect.move(0,speed_player*-1)
        
        if keys[pygame.K_DOWN] and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            player_rect = player_rect.move(0,speed_player*0.7071217222732374245)
        else:
            if keys[pygame.K_DOWN]:
                player_rect = player_rect.move(0,speed_player)
        
        if keys[pygame.K_LEFT] and (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            player_rect = player_rect.move(speed_player*0.7071217222732374245*-1,0)
        else:
            if keys[pygame.K_LEFT]:
                player_rect = player_rect.move(speed_player*-1,0)
        
        if keys[pygame.K_RIGHT] and (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            player_rect = player_rect.move(speed_player*0.7071217222732374245,0)
        else:
            if keys[pygame.K_RIGHT]:
                player_rect = player_rect.move(speed_player,0)
    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            life = 10
            start_time = int(pygame.time.get_ticks()/1000)
            time_played = int(pygame.time.get_ticks()/1000) - start_time
            count_score = 0
            score = 0
            level = 1
            ia_increment = 60
            game_state = True


    if game_state:
        
        # Screen color
        screen.fill('White')
        screen.blit(background,background_rect)

        player_path_current = set_map_position(player_rect)

        if player_path_current != player_path[1]:
            player_path[0] = player_path[1]
            player_path[1] = player_path_current

        free_path = player_path_current
        aux = -1

        while free_path == player_path[0] or free_path == player_path[1]:
            aux = random.randint(0,3)
            free_path = map_loc[aux]

        player_animation()
        antibody_animation()
        
        # Render Player, Cell and antibody
        screen.blit(player, player_rect)
        screen.blit(cell, cell_rect)
        screen.blit(antibody,antibody_rect)
        screen.blit(antibody,antibody1_rect)
        screen.blit(antibody,antibody2_rect)
        screen.blit(antibody,antibody3_rect)
        screen.blit(antibody,antibody4_rect)
        screen.blit(antibody,antibody5_rect)
        screen.blit(dot,dot_rect)
        screen.blit(game_name_text,game_name_text_rect)
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
            count_score +=1
            display_info()
            cell_pos = random_pos(32)
            cell_rect = cell.get_rect(center = cell_pos)
        else:
            # Calculate distance between Cell and Player
            c_value = ((cell_rect.x-player_rect.x)**2)+((cell_rect.y-player_rect.y)**2)
            distance_cell = math.sqrt(c_value)

            # Calculate distance between Food and Player
            c_value = ((dot_rect.x-player_rect.x)**2)+((dot_rect.y-player_rect.y)**2)
            distance_dot = math.sqrt(c_value)

            c_value = ((cell_rect.x-dot_rect.x)**2)+((cell_rect.y-dot_rect.y)**2)
            distance_food_cell = math.sqrt(c_value)


        # Movimentando a Célula
        cell_movement(cell_rect,dot_rect)

        # Verificando se o alimento e o player estão no mesmo bloco
        # Se for verdadeiro o alimento será renderizado em um novo bloco
        if set_map_position(dot_rect) == set_map_position(player_rect):

            while free_path == player_path[0] or free_path == player_path[1]:
                aux = random.randint(0,3)
                free_path = map_loc[aux]

            dot_pos = set_m_position_pixel(free_path)
            dot_rect = dot.get_rect(center = dot_pos)
            screen.blit(dot,dot_rect)

        # Collider Cell to Food
        if cell_rect.colliderect(dot_rect):
            while free_path == player_path[0] or free_path == player_path[1]:
                aux = random.randint(0,3)
                free_path = map_loc[aux]
            
            dot_pos = set_m_position_pixel(free_path)
            dot_rect = dot.get_rect(center = dot_pos)
            screen.blit(dot,dot_rect)

            # Trecho não utilizado
            # # Calculate distance between Food and Player
            # c_value = ((dot_rect.x-player_rect.x)**2)+((dot_rect.y-player_rect.y)**2)
            # distance_dot = math.sqrt(c_value)
        
        # Calculate distance between Cell and Player
        c_value = ((cell_rect.x-player_rect.x)**2)+((cell_rect.y-player_rect.y)**2)
        distance_cell = math.sqrt(c_value)

        
        # Antibody Collider
        if antibody_rect.colliderect(player_rect):
            life -= 1
            display_info()
            antibody_pos = random_pos()
            antibody_rect = antibody.get_rect(center = antibody_pos)
        
        if antibody1_rect.colliderect(player_rect):
            life -= 1
            display_info()
            antibody1_pos = random_pos()
            antibody1_rect = antibody.get_rect(center = antibody1_pos)
        
        if antibody2_rect.colliderect(player_rect):
            life -= 1
            display_info()
            antibody2_pos = random_pos()
            antibody2_rect = antibody.get_rect(center = antibody2_pos)
        
        if antibody3_rect.colliderect(player_rect):
            life -= 1
            display_info()
            antibody3_pos = random_pos()
            antibody3_rect = antibody.get_rect(center = antibody3_pos)
        
        if antibody4_rect.colliderect(player_rect):
            life -= 1
            display_info()
            antibody4_pos = random_pos()
            antibody4_rect = antibody.get_rect(center = antibody4_pos)
        
        if antibody5_rect.colliderect(player_rect):
            life -= 1
            display_info()
            antibody5_pos = random_pos()
            antibody5_rect = antibody.get_rect(center = antibody5_pos)
        else:
            antibody_ia(antibody_rect,ia_increment)
            antibody_ia(antibody1_rect,ia_increment)
            antibody_ia(antibody2_rect,ia_increment)
            antibody_ia(antibody3_rect,ia_increment)
            antibody_ia(antibody4_rect,ia_increment)
            antibody_ia(antibody5_rect,ia_increment)

        if life == 0:
            game_state = False
        
    else:
        # Screen color
        screen.fill('White')
        screen.blit(background,background_rect)

        if life == 0:
            
            game_over_text = font_game_over.render(f'GAME OVER',False, 'Black').convert_alpha()
            game_over_rect = game_over_text.get_rect(center = (screen_width/2,screen_playable_height/2))
            screen.blit(game_over_text,game_over_rect)

        else:
            
            game_over_text = font_game_over.render(f'LIFE - THE GAME',False, 'Black').convert_alpha()
            game_over_rect = game_over_text.get_rect(center = (screen_width/2,screen_playable_height/2))
            screen.blit(game_over_text,game_over_rect)

        game_over_info_text = font_title.render(f'PRESS SPACE TO START',False, 'Black').convert_alpha()
        game_over_info_rect = game_over_info_text.get_rect(center = (screen_width/2,(screen_playable_height/2)+30))
        screen.blit(game_over_info_text,game_over_info_rect)


    # Refreshing the screen
    pygame.display.update()
    clock.tick(60)
import pygame, random, time


# Inicializando a tela
pygame.init()

# Tamanho da tela do jogo e Framerate
size_l = 640
size_h = 480
screen = pygame.display.set_mode((size_l, size_h))
clock = pygame.time.Clock()
# Título do jogo
pygame.display.set_caption("Basic PyGame Program")

# Ícone do jogo
icon = pygame.image.load("Life_Logo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("virus.png")
playerX = 320
playerY= 240

# Enemy
enemyImg = pygame.image.load("anticorps.png")
enemyX = -50
enemyY = -50

# Coin
coinImg = pygame.image.load("cell.png")
coinX = 100
coinY = 100


def random_X_coordenates():
    posX = random.randint(0,size_l-33)
    return int(posX)

def random_Y_coordenates():
    posY = random.randint(0,size_h-33)
    return int(posY)

def player(posX,posY):
    screen.blit(playerImg,(posX,posY))

def coin():
    posX = random_X_coordenates()
    posY = random_Y_coordenates()
    screen.blit(coinImg,(posX, posY))
    return posX,posY
    
def enemy():
    pass


# -----------------------------------------

# Loop para manter o jogo aberto

run = True
coin_time = 0
enemy_number = 0
flagX = True
flagY = True
score = 0
mov = [0,0]

while run:

    # Preenchimento via RGB
    screen.fill((250, 250, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 

        # Verificando se alguma tecla foi pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if playerX >= 0:
                    playerX -= 5
            if event.key == pygame.K_RIGHT:
                if playerX <= (639-32):
                    playerX += 5
            if event.key == pygame.K_UP:
                if playerY >= 0:
                    playerY -= 5
            if event.key == pygame.K_DOWN:
                if playerY <= (479-32):
                    playerY += 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX += 0
                playerY += 0
    
    player(playerX+mov[0],playerY+mov[1])
    
    screen.blit(enemyImg,(180,180))

    
    if coin_time == 0:
        posX, posY = coin()
        coin_time = 900
    
    # Lógica para movimento de rebatimento e renderização de células
    if posX >= 0 and posX < size_l-32 and flagX == True:
        posX += 0.5
        if posX > size_l-34-0.1:
            flagX = False
    if posX >= 0 and flagX == False:
        posX -= 0.5
        if posX < 0.9:
            flagX = True

    if posY >= 0 and posY < size_h-32 and flagY == True:
        posY += 0.5
        if posY > size_h-34-0.1:
            flagY = False
    if posY >= 0 and flagY == False:
        posY -= 0.5
        if posY < 0.9:
            flagY = True

    screen.blit(coinImg,(posX, posY))
    screen.blit(enemyImg,(posX-15, posY-15))

    if coin_time >= 0:
        coin_time -= 1
    
    # if enemy_number <= 4:
    #     enemy()

    # Colisão da célula no vírus
    if playerX >= posX - 30:
        # print("Cheguei IF1")
        if playerX <= posX + 30:
            # print("Cheguei IF2")
            if playerY >= posY - 25:
                # print("Cheguei IF3")
                if playerY <= posY + 25:
                    # print("Cheguei IF4")
                    score += 1
                    print(f"{score} célula(s) contaminada(s)!")
                    # Morte da célula
                    coin_time = 0
  
    # Teste com atualização randomica de cores no background
    # seguida por uma espera de meio segundo
    # screen.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    # time.sleep(0.2)

    # mov = [0,0]

    # Atualizando os dados exibidos em tela
    pygame.display.update()
    clock.tick(60)
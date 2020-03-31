import pygame, sys

## variáveis globais ##

FPS = 30

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BACKGROUND_COLOR = (255,255,255)
BACKGROUND_IMAGE = "assets/vialactea.png"
ICON_IMAGE = "assets/lander.png"
PLAYERSHIP_IMAGE = "assets/playership.png"
LASER_IMAGE = "assets/laser.png"
ALIENSHIP_IMAGE = "assets/alienship.png"
ALIENSHIP_NUMBER = 3
ALIENSHIP_SEPARACAO = 30

DISPLAYSURF = None

## MAIN ##

def main():
    global DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    pygame.display.set_caption("Space Invaders")
    game_icon = pygame.image.load(ICON_IMAGE).convert()
    game_bg = pygame.image.load(BACKGROUND_IMAGE).convert()
    game_bg = pygame.transform.scale(game_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_icon(game_icon)

    playership_x = 370
    playership_y = 480
    playership_mover = 0  
    playership_sprite = pygame.image.load(PLAYERSHIP_IMAGE)
    playership_largura = playership_sprite.get_rect().width

    laser_x = 370
    laser_y = 460
    laser_mover = 1
    laser_sprite = pygame.image.load(LASER_IMAGE)
    laser_state = "Espera"

    alienship_x_row1 = [] 
    alienship_y_row1 = [] 
    alienship_sprite_row1 = [] 
    alienship_direcao_row1 = [] 

    alienship_x_row2 = [] 
    alienship_y_row2 = [] 
    alienship_sprite_row2 = [] 
    alienship_direcao_row2 = [] 

    alienship_mover = 8
    alienship_largura = pygame.image.load(ALIENSHIP_IMAGE).get_rect().width

    for i in range(ALIENSHIP_NUMBER):
        alienship_sprite_row1.append(pygame.image.load(ALIENSHIP_IMAGE))   
        alienship_x_row1.append(50 + i*(alienship_largura+ALIENSHIP_SEPARACAO))
        alienship_y_row1.append(50)
        alienship_direcao_row1.append("Direita")

        alienship_sprite_row2.append(pygame.image.load(ALIENSHIP_IMAGE))   
        alienship_x_row2.append(50 + i*(alienship_largura+ALIENSHIP_SEPARACAO))
        alienship_y_row2.append(150)
        alienship_direcao_row2.append("Direita")

    ## Game loop
    while True: 
        DISPLAYSURF.fill(BACKGROUND_COLOR)
        DISPLAYSURF.blit(game_bg,(0,0))
        
        ## Movimento do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    playership_mover = -8
                if event.key == pygame.K_RIGHT:
                    playership_mover = 8
                if event.key == pygame.K_SPACE:
                    if laser_state == "Espera":
                        laser_state = "Atirando"
                        laser_x = playership_x + playership_largura/2                   
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    playership_mover = 0

        ## Movimento dos inimigos aliens
        for i in range(ALIENSHIP_NUMBER):     
            if alienship_x_row1[ALIENSHIP_NUMBER-1]>=688:
                alienship_mover = -8
                alienship_direcao_row1[i] = "Esquerda"
            elif alienship_x_row1[0]<=0:
                alienship_mover = 8
                alienship_direcao_row1[i] = "Direita"

            if alienship_x_row2[ALIENSHIP_NUMBER-1]>=688:
                alienship_mover = -8
                alienship_direcao_row2[i] = "Esquerda"
            elif alienship_x_row1[0]<=0:
                alienship_mover = 8
                alienship_direcao_row2[i] = "Direita"

        playership_x = movimento_jogador(playership_sprite,playership_x,playership_y,playership_mover)
        alienship_x_row1 = movimento_inimigos(alienship_sprite_row1,alienship_x_row1,alienship_y_row1,alienship_mover)
        alienship_x_row2 = movimento_inimigos(alienship_sprite_row2,alienship_x_row2,alienship_y_row2,alienship_mover)

        if laser_state == "Atirando":
            laser_state, laser_y = atira_laser(laser_sprite,laser_x,laser_y,laser_state)
            if teste_colisao(laser_sprite,alienship_sprite_row2):
                print("oi")


        pygame.display.update()  
        FPSCLOCK.tick(FPS)     

## FUNÇÕES ##      

def movimento_jogador(sprite,x,y,movimento):       
    x += movimento
    DISPLAYSURF.blit(sprite,(x,y))

    if x <= 0:
        x = 0
    elif x >= 688:
        x = 688

    return x

def atira_laser(sprite,x,y,state):
    y -= 50
    DISPLAYSURF.blit(sprite,(x-10,y))
    height = sprite.get_rect().height

    if y+height <= 0:
        y = 460
        state = "Espera"

    return state, y

def movimento_inimigos(sprite,x,y,movimento):  
    for i in range(ALIENSHIP_NUMBER):
        x[i] += movimento
        DISPLAYSURF.blit(sprite[i],(x[i],y[i]))  
      
    return x

def teste_colisao(sprite_laser,sprite_inimigo):
    for i in range(ALIENSHIP_NUMBER):
        return sprite_laser.Rect.colliderect(sprite_inimigo.Rect)


## MAIN ##

if __name__ == '__main__':
    main()

    
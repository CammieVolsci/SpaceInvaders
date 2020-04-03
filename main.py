import pygame, sys, jogador, inimigos

## variáveis globais ##

FPS = 30

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BACKGROUND_COLOR = (255,255,255)
BACKGROUND_IMAGE = "assets/vialactea.png"
ICON_IMAGE = "assets/lander.png"

ALIENSHIP_NUMBER = 3
ALIENSHIP_SEPARACAO = 30

DISPLAYSURF = None

## MAIN ##
def main():
    global DISPLAYSURF, ALIENSHIP_NUMBER

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    pygame.display.set_caption("Space Invaders")
    game_icon = pygame.image.load(ICON_IMAGE).convert()
    game_bg = pygame.image.load(BACKGROUND_IMAGE).convert()
    game_bg = pygame.transform.scale(game_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_icon(game_icon)

    player = jogador.playership()
    player_laser = jogador.laser()

    alien_row1 = []
    alien_row2 = [] 
    
    for i in range(ALIENSHIP_NUMBER):
        alien_row1.append(inimigos.alienship(50 + i*(100+ALIENSHIP_SEPARACAO),50))
        alien_row2.append(inimigos.alienship(50 + i*(100+ALIENSHIP_SEPARACAO),150))

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
                    player.mover = -8
                if event.key == pygame.K_RIGHT:
                    player.mover = 8
                if event.key == pygame.K_SPACE:
                    if player_laser.state == "Espera":
                        player_laser.state = "Atirando"
                        player_laser.x = player.x + player.width/2                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.mover = 0

        ## Movimento dos inimigos aliens
        for i in range(ALIENSHIP_NUMBER):     
            if alien_row1[ALIENSHIP_NUMBER-1].x>=688:
                alien_row1[i].mover = -0.8
                alien_row1[i].direcao = "Esquerda"
            elif alien_row1[0].x<=0:
                alien_row1[i].mover = 0.8
                alien_row1[i].direcao = "Direita"

            if alien_row2[ALIENSHIP_NUMBER-1].x>=688:
                alien_row2[i].mover = -0.8
                alien_row2[i].direcao = "Esquerda" 
            elif alien_row1[0].x<=0:
                alien_row2[i].mover = 0.8
                alien_row2[i].direcao = "Direita"

        player.movimento(DISPLAYSURF)

        for i in range(ALIENSHIP_NUMBER):
            alien_row1[i].movimento(DISPLAYSURF)
            alien_row2[i].movimento(DISPLAYSURF)

        if player_laser.state == "Atirando":
            player_laser.atira(DISPLAYSURF)
        
        for i in range(ALIENSHIP_NUMBER):   
            if alien_row1[i].rect != 0 and player_laser.teste_colisao(alien_row1[i]):
                alien_row1[i].kill()
                print("Colidiu 1")
                player_laser.reset(player.x,player.y)
            elif alien_row2[i].rect != 0 and player_laser.teste_colisao(alien_row2[i]):
                alien_row2[i].kill()
                print("Colidiu 2")
                player_laser.reset(player.x,player.y)

        pygame.display.update()  
        FPSCLOCK.tick(FPS)     

## MAIN ##

if __name__ == '__main__':
    main()


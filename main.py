import pygame, sys, jogador, inimigos

## variáveis globais ##
FPS = 30

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650

BACKGROUND_COLOR = (255,255,255)
BACKGROUND_IMAGE = "assets/vialactea.png"
ICON_IMAGE = "assets/lander.png"

ALIEN_NUMBER = 5
ALIEN_SEPARACAO = 5
ALIEN_TOTAL = 0

DISPLAYSURF = None

## MAIN ##
def main():
    global DISPLAYSURF, ALIEN_NUMBER

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    pygame.display.set_caption("Space Invaders")
    game_icon = pygame.image.load(ICON_IMAGE).convert()
    game_bg = pygame.image.load(BACKGROUND_IMAGE).convert()
    game_bg = pygame.transform.scale(game_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_icon(game_icon)

    frame_time = 0
    tiro_time  = 0

    player = jogador.playership()
    player_laser = jogador.laser()

    alien_row1 = []
    alien_row2 = [] 
    alien_row3 = []    
    
    for i in range(ALIEN_NUMBER):
        alien_row1.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),50,"assets/alien1.png","assets/alien2.png"))
        #alien_row2.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),130,"assets/alien1c.png","assets/alien2c.png"))
        #alien_row3.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),210,"assets/alien1e.png","assets/alien2e.png"))

    ## Game loop
    while True: 
        frame_time += FPSCLOCK.get_time()
        tiro_time  += FPSCLOCK.get_time()

        DISPLAYSURF.fill(BACKGROUND_COLOR)
        DISPLAYSURF.blit(game_bg,(0,0))

        if frame_time > 300:
            frame_time = 0

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
            
        player.movimento(DISPLAYSURF)

        ## Movimento dos inimigos aliens
        for i in range(ALIEN_NUMBER): 
            alien_row1[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, frame_time)
            #alien_row2[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, frame_time)
            #alien_row3[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, frame_time)

        if player_laser.state == "Atirando":
            player_laser.atira(DISPLAYSURF)
            for i in range(ALIEN_NUMBER):   
                if alien_row1[i].rect != 0 and player_laser.teste_colisao(alien_row1[i]):
                    alien_row1[i].kill()
                    player_laser.reset(player.x,player.y)
                #elif alien_row2[i].rect != 0 and player_laser.teste_colisao(alien_row2[i]):
                   # alien_row2[i].kill()
                  #  player_laser.reset(player.x,player.y) 
                #elif alien_row3[i].rect != 0 and player_laser.teste_colisao(alien_row3[i]):
                   # alien_row3[i].kill()
                   # player_laser.reset(player.x,player.y)

        if tiro_time > 1000:
            alien_row1[0].laser.append(inimigos.laser(alien_row1[0].x, alien_row1[0].y))
            alien_row1[0].tiro = 'Ativado'
            alien_row1[0].total_tiro += 1
            alien_row1[4].laser.append(inimigos.laser(alien_row1[4].x, alien_row1[4].y))
            alien_row1[4].tiro = 'Ativado'
            alien_row1[4].total_tiro += 1
            tiro_time = 0
        
        for i in range(ALIEN_NUMBER):
            if alien_row1[i].tiro == 'Ativado':
                for j in range(alien_row1[i].total_tiro):
                    alien_row1[i].laser[j].atira(DISPLAYSURF,WINDOW_HEIGHT)
                tiro_novo = []
                tira_total_novo = 0
                for j in range(alien_row1[i].total_tiro):
                    if alien_row1[i].laser[j].state == 'Atirando':
                        tiro_novo.append(alien_row1[i].laser[j])
                        tira_total_novo += 1
                alien_row1[i].laser = tiro_novo[:]
                alien_row1[i].total_tiro = tira_total_novo

        pygame.display.update()  
        FPSCLOCK.tick(FPS)     

## MAIN ##
if __name__ == '__main__':
    main()


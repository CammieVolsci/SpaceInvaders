import pygame, sys, jogador, inimigos

## variáveis globais ##
FPS = 30
FRAME_TIME = 0
TIRO_TIME = 0
DISPLAYSURF = None
FPSCLOCK = None

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650

BACKGROUND_COLOR = (255,255,255)
BACKGROUND_IMAGE = "assets/vialactea.png"
ICON_IMAGE = "assets/alien1c.png"

ALIEN_NUMBER = 5
ALIEN_SEPARACAO = 5
ALIEN_TOTAL = 0

## MAIN ##
def main():
    global DISPLAYSURF, FPSCLOCK, ALIEN_NUMBER, FRAME_TIME, TIRO_TIME

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Space Invaders")   
    game_icon = pygame.image.load(ICON_IMAGE).convert()
    game_bg = pygame.image.load(BACKGROUND_IMAGE).convert()
    game_bg = pygame.transform.scale(game_bg,(WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_icon(game_icon)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    player = jogador.playership()
    player_laser = jogador.laser()
    explosion = jogador.explosion()
    alien_row1 = []
    alien_row2 = [] 
    alien_row3 = []    
    
    for i in range(ALIEN_NUMBER):
        alien_row1.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),50,"assets/alien1.png","assets/alien2.png"))
        #alien_row2.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),130,"assets/alien1c.png","assets/alien2c.png"))
        #alien_row3.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),210,"assets/alien1e.png","assets/alien2e.png"))

    ## Game loop
    while True:        
        FRAME_TIME += FPSCLOCK.get_time()
        TIRO_TIME  += FPSCLOCK.get_time()
        player.tempo_invencivel += FPSCLOCK.get_time()
        pontuacao_txt = str(player.pontuacao) 
        gameOverSurf = BASICFONT.render('Game Over :< Pontuacao: ' + pontuacao_txt,True,(255,255,255))
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.center = (400, 325)  
        resetSurf = BASICFONT.render('Pressione R para reiniciar ',True,(255,255,255))
        resetRect = gameOverSurf.get_rect()
        resetRect.center = (400, 400)  

        DISPLAYSURF.fill(BACKGROUND_COLOR)
        DISPLAYSURF.blit(game_bg,(0,0))

        if FRAME_TIME > 300:
            FRAME_TIME = 0                 

        if TIRO_TIME > 1000:
            alien_row1[0].laser.append(inimigos.laser(alien_row1[0].x, alien_row1[0].y))
            alien_row1[0].tiro = 'Ativado'
            alien_row1[0].total_tiro += 1
            alien_row1[4].laser.append(inimigos.laser(alien_row1[4].x, alien_row1[4].y))
            alien_row1[4].tiro = 'Ativado'
            alien_row1[4].total_tiro += 1
            TIRO_TIME = 0      

        if player.vidas <= 0:
            player.dead = True
            DISPLAYSURF.blit(gameOverSurf,gameOverRect)
            DISPLAYSURF.blit(resetSurf,resetRect)          

        if player.invencivel and player.tempo_invencivel < 300:      
            explosion.explode(DISPLAYSURF)                 
        else:
            player.movimento(DISPLAYSURF)
            player.tempo_invencivel = 0
            player.invencivel = False

        movimento_jogador(player,player_laser,alien_row1)
        movimento_aliens(alien_row1)    
        atira_nos_aliens(player,player_laser,alien_row1)      
        alien_atira(alien_row1,player,explosion)                          

        pygame.display.update()  
        FPSCLOCK.tick(FPS)     


def movimento_jogador(player,player_laser,alien_row1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_jogo(player,alien_row1)
            if event.key == pygame.K_LEFT and not player.dead: 
                player.mover = -8
            if event.key == pygame.K_RIGHT and not player.dead:
                player.mover = 8
            if event.key == pygame.K_SPACE and not player.dead:
                if player_laser.state == "Espera":
                    player_laser.state = "Atirando"
                    player_laser.x = player.x + player.width/2                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.mover = 0

def movimento_aliens(alien_row1):
    global ALIEN_NUMBER, FRAME_TIME, DISPLAYSURF

    for i in range(ALIEN_NUMBER): 
        alien_row1[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME)
        #alien_row2[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME)
        #alien_row3[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME)

def atira_nos_aliens(player,player_laser,alien_row1):
    global DISPLAYSURF, ALIEN_NUMBER

    if player_laser.state == "Atirando":
        player_laser.atira(DISPLAYSURF)
        for i in range(ALIEN_NUMBER):   
            if alien_row1[i].rect != 0 and player_laser.teste_colisao(alien_row1[i]):
                alien_row1[i].kill()
                player.pontuacao += 50
                player_laser.reset(player.x,player.y)
            #elif alien_row2[i].rect != 0 and player_laser.teste_colisao(alien_row2[i]):
                # alien_row2[i].kill()
                #  player_laser.reset(player.x,player.y) 
            #elif alien_row3[i].rect != 0 and player_laser.teste_colisao(alien_row3[i]):
                # alien_row3[i].kill()
                # player_laser.reset(player.x,player.y)

def alien_atira(alien_row1,player,explosion):
    global DISPLAYSURF, WINDOW_HEIGHT, ALIEN_NUMBER

    for i in range(ALIEN_NUMBER):
        if alien_row1[i].tiro == 'Ativado':
            for j in range(alien_row1[i].total_tiro):
                alien_row1[i].laser[j].atira(DISPLAYSURF,WINDOW_HEIGHT)
                if alien_row1[i].laser[j].teste_colisao(player) and (not player.invencivel and not player.dead):
                    alien_row1[i].laser[j].reset(alien_row1[i].x,alien_row1[i].y)
                    explosion.set_xy(player.x,player.y)
                    player.vidas -= 1 
                    player.invencivel = True                                                                                  
            tiro_novo = []
            tira_total_novo = 0
            for j in range(alien_row1[i].total_tiro):
                if alien_row1[i].laser[j].state == 'Atirando':
                    tiro_novo.append(alien_row1[i].laser[j])
                    tira_total_novo += 1
            alien_row1[i].laser = tiro_novo[:]
            alien_row1[i].total_tiro = tira_total_novo

def reset_jogo(player,alien_row1):
    global ALIEN_NUMBER

    alien_row1.clear()
    player.pontuacao = 0
    player.vidas = 5
    player.dead = False
    player.invencivel = False
    player.tempo_invencivel = 0

    for i in range(ALIEN_NUMBER):
        alien_row1.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),50,"assets/alien1.png","assets/alien2.png"))

## MAIN ##
if __name__ == '__main__':
    main()


import datetime, pygame, random, sys
import cenario, jogador, inimigos

## variáveis globais ##
FPS = 30
FRAME_TIME = 0
TIRO_TIME = 0
DISPLAYSURF = None
FPSCLOCK = None

WHITE = (255,255,255)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650
BACKGROUND_IMAGE = "assets/vialactea.png"
ICON_IMAGE = "assets/alien1c.png"

ALIEN_NUMBER = 5
ALIEN_SEPARACAO = 5
ALIEN_TOTAL = ALIEN_NUMBER * 3
SHIELD_SIZE = 20

## MAIN ##
def main():
    global DISPLAYSURF, FPSCLOCK, ALIEN_NUMBER, ALIEN_TOTAL, FRAME_TIME, TIRO_TIME, SHIELD_SIZE

    pygame.init()
    random.seed(datetime.time())
    pygame.display.set_caption("Space Invaders")  

    FPSCLOCK = pygame.time.Clock()   
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 14)
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    game_icon = pygame.image.load(ICON_IMAGE).convert()
    pygame.display.set_icon(game_icon)
    game_bg = pygame.image.load(BACKGROUND_IMAGE).convert()
    game_bg = pygame.transform.scale(game_bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

    resetSurf = SMALLFONT.render('Pressione R para reiniciar ',True,WHITE)
    resetRect = resetSurf.get_rect()
    resetRect.center = (700, 20)

    player = jogador.playership()
    player_laser = jogador.laser()
    explosion = jogador.explosion()
    
    shield1 = []
    shield2 = []
    shield3 = []

    alien_row1 = []
    alien_row2 = [] 
    alien_row3 = []    
    
    for i in range(ALIEN_NUMBER):
        alien_row1.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),50,"assets/alien1.png","assets/alien2.png"))
        alien_row2.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),130,"assets/alien1c.png","assets/alien2c.png"))
        alien_row3.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),210,"assets/alien1e.png","assets/alien2e.png"))

    for i in range(SHIELD_SIZE):
        shield1.append(cenario.shield(50 + i*10,450))
        shield2.append(cenario.shield(300 + i*10,450))
        shield3.append(cenario.shield(550 + i*10,450))

    ## Game loop
    while True:        
        FRAME_TIME += FPSCLOCK.get_time()
        TIRO_TIME  += FPSCLOCK.get_time()
        player.tempo_invencivel += FPSCLOCK.get_time()
        pontuacao_txt = str(player.pontuacao) 
        vidas_txt = str(player.vidas)

        gameOverSurf = BASICFONT.render('Game Over :< Pontuacao: ' + pontuacao_txt,True,WHITE)
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.center = (400, 325)  
          
        pontuacaoSurf = SMALLFONT.render('Score: ' + pontuacao_txt,True,WHITE)
        pontuacaoRect = pontuacaoSurf.get_rect()
        pontuacaoRect.center = (50,20)

        vidasSurf = SMALLFONT.render('Life: ' + vidas_txt,True,WHITE)
        vidasRect = vidasSurf.get_rect()
        vidasRect.center = (140,20)

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(game_bg,(0,0))
        DISPLAYSURF.blit(pontuacaoSurf,pontuacaoRect)
        DISPLAYSURF.blit(vidasSurf,vidasRect)
        DISPLAYSURF.blit(resetSurf,resetRect) 

        for i in range(SHIELD_SIZE):
            shield1[i].desenha_escudo(DISPLAYSURF)
            shield2[i].desenha_escudo(DISPLAYSURF)                   
            shield3[i].desenha_escudo(DISPLAYSURF)     

        if FRAME_TIME > 300:
            FRAME_TIME = 0                 

        if TIRO_TIME > 2000:
            posicao = random.randint(0,4) 
            if  alien_row3[posicao].status == True:
                alien_row3[posicao].laser.append(inimigos.laser(alien_row3[posicao].x,alien_row3[posicao].y))
                alien_row3[posicao].tiro = 'Ativado'
                alien_row3[posicao].total_tiro += 1
                TIRO_TIME = 0   
            elif alien_row2[posicao].status == True:
                alien_row2[posicao].laser.append(inimigos.laser(alien_row2[posicao].x,alien_row2[posicao].y))
                alien_row2[posicao].tiro = 'Ativado'
                alien_row2[posicao].total_tiro += 1 
                TIRO_TIME = 0   
            elif alien_row1[posicao].status == True:
                alien_row1[posicao].laser.append(inimigos.laser(alien_row1[posicao].x,alien_row1[posicao].y))
                alien_row1[posicao].tiro = 'Ativado'
                alien_row1[posicao].total_tiro += 1
                TIRO_TIME = 0                           

        if player.vidas <= 0:
            player.dead = True
            DISPLAYSURF.blit(gameOverSurf,gameOverRect)     

        if ALIEN_TOTAL <= 0:
            reset_jogo(player,alien_row1,alien_row2,alien_row3,shield1,shield2,shield3)
            ALIEN_TOTAL = ALIEN_NUMBER * 3

        if player.invencivel and player.tempo_invencivel < 300:      
            explosion.explode(DISPLAYSURF)                 
        else:
            player.movimento(DISPLAYSURF)
            player.tempo_invencivel = 0
            player.invencivel = False
    
        colisao_escudo(player,player_laser,alien_row1,alien_row2,alien_row3,shield1,shield2,shield3)
        movimento_jogador(player,player_laser,alien_row1,alien_row2,alien_row3,shield1,shield2,shield3)     
        movimento_aliens(alien_row1,alien_row2,alien_row3)      
        tiros_do_jogador(player,player_laser,alien_row1,alien_row2,alien_row3)      
        tiros_dos_aliens(alien_row1,alien_row2,alien_row3,player,explosion)   
                               
        pygame.display.update()  
        FPSCLOCK.tick(FPS)     

def movimento_jogador(player, player_laser, alien_row1, alien_row2, alien_row3, shield1, shield2, shield3):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_jogo(player, alien_row1, alien_row2, alien_row3, shield1, shield2, shield3)
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

def movimento_aliens(alien_row1, alien_row2, alien_row3):
    global ALIEN_NUMBER, FRAME_TIME, DISPLAYSURF, ALIEN_TOTAL   

    for i in range(ALIEN_NUMBER): 
        if ALIEN_TOTAL > 10 and ALIEN_TOTAL <= 15:
            alien_row1[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 4)
            alien_row2[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 4)
            alien_row3[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 4)
        if ALIEN_TOTAL > 5 and ALIEN_TOTAL <= 10:
            alien_row1[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 5)
            alien_row2[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 5)
            alien_row3[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 5)
        if ALIEN_TOTAL > 2 and ALIEN_TOTAL <= 5:
            alien_row1[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 6)
            alien_row2[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 6)
            alien_row3[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 6)
        if ALIEN_TOTAL == 1 or ALIEN_TOTAL == 2:
            alien_row1[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 7)
            alien_row2[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 7)
            alien_row3[i].movimento(DISPLAYSURF, ALIEN_SEPARACAO, i, ALIEN_NUMBER, FRAME_TIME, 7)

def tiros_do_jogador(player, player_laser, alien_row1, alien_row2, alien_row3):
    global DISPLAYSURF, ALIEN_NUMBER, ALIEN_TOTAL

    if player_laser.state == "Atirando":
        player_laser.atira(DISPLAYSURF)
        for i in range(ALIEN_NUMBER):   
            if alien_row1[i].rect != 0 and player_laser.teste_colisao(alien_row1[i]):
                alien_row1[i].kill()
                player.pontuacao += 50
                ALIEN_TOTAL -= 1
                player_laser.reset(player.x,player.y)                
            elif alien_row2[i].rect != 0 and player_laser.teste_colisao(alien_row2[i]):
                alien_row2[i].kill()
                player.pontuacao += 50
                ALIEN_TOTAL -= 1
                player_laser.reset(player.x,player.y) 
            elif alien_row3[i].rect != 0 and player_laser.teste_colisao(alien_row3[i]):
                alien_row3[i].kill()
                player.pontuacao += 50
                ALIEN_TOTAL -= 1
                player_laser.reset(player.x,player.y)

def tiros_dos_aliens(alien_row1, alien_row2, alien_row3, player,explosion):
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

        if alien_row2[i].tiro == 'Ativado':
            for j in range(alien_row2[i].total_tiro):
                alien_row2[i].laser[j].atira(DISPLAYSURF,WINDOW_HEIGHT)
                if alien_row2[i].laser[j].teste_colisao(player) and (not player.invencivel and not player.dead):
                    alien_row2[i].laser[j].reset(alien_row2[i].x,alien_row2[i].y)
                    explosion.set_xy(player.x,player.y)
                    player.vidas -= 1 
                    player.invencivel = True   
            tiro_novo = []
            tira_total_novo = 0
            for j in range(alien_row2[i].total_tiro):
                if alien_row2[i].laser[j].state == 'Atirando':
                    tiro_novo.append(alien_row2[i].laser[j])
                    tira_total_novo += 1
            alien_row2[i].laser = tiro_novo[:]
            alien_row2[i].total_tiro = tira_total_novo

        if alien_row3[i].tiro == 'Ativado':
            for j in range(alien_row3[i].total_tiro):
                alien_row3[i].laser[j].atira(DISPLAYSURF,WINDOW_HEIGHT)
                if alien_row3[i].laser[j].teste_colisao(player) and (not player.invencivel and not player.dead):
                    alien_row3[i].laser[j].reset(alien_row3[i].x,alien_row3[i].y)
                    explosion.set_xy(player.x,player.y)
                    player.vidas -= 1 
                    player.invencivel = True                                                                           
            tiro_novo = []
            tira_total_novo = 0                    
            for j in range(alien_row3[i].total_tiro):
                if alien_row3[i].laser[j].state == 'Atirando':
                    tiro_novo.append(alien_row3[i].laser[j])
                    tira_total_novo += 1                      
            alien_row3[i].laser = tiro_novo[:]
            alien_row3[i].total_tiro = tira_total_novo

def colisao_escudo(player, player_laser, alien_row1, alien_row2, alien_row3, shield1, shield2, shield3):
    global ALIEN_NUMBER, SHIELD_SIZE

    for i in range(SHIELD_SIZE):
        if shield1[i].rect != 0 and player_laser.teste_colisao(shield1[i]):
            shield1[i].kill()
            player_laser.reset(player.x,player.y)          
        for j in range(ALIEN_NUMBER):          
            for k in range(alien_row3[j].total_tiro):
                if shield1[i].rect != 0 and alien_row3[j].laser[k].teste_colisao(shield1[i]):
                    shield1[i].kill()
                    alien_row3[j].laser[k].reset(alien_row3[j].x,alien_row3[j].y)
            for k in range(alien_row2[j].total_tiro):
                if shield1[i].rect != 0 and alien_row2[j].laser[k].teste_colisao(shield1[i]):
                    shield1[i].kill()
                    alien_row2[j].laser[k].reset(alien_row2[j].x,alien_row2[j].y)
            for k in range(alien_row1[j].total_tiro):
                if shield1[i].rect != 0 and alien_row1[j].laser[k].teste_colisao(shield1[i]):
                    shield1[i].kill()
                    alien_row1[j].laser[k].reset(alien_row1[j].x,alien_row1[j].y)
        
        if shield2[i].rect != 0 and player_laser.teste_colisao(shield2[i]):
            shield2[i].kill()
            player_laser.reset(player.x,player.y)          
        for j in range(ALIEN_NUMBER):          
            for k in range(alien_row3[j].total_tiro):
                if shield2[i].rect != 0 and alien_row3[j].laser[k].teste_colisao(shield2[i]):
                    shield2[i].kill()
                    alien_row3[j].laser[k].reset(alien_row3[j].x,alien_row3[j].y)
            for k in range(alien_row2[j].total_tiro):
                if shield2[i].rect != 0 and alien_row2[j].laser[k].teste_colisao(shield2[i]):
                    shield2[i].kill()
                    alien_row2[j].laser[k].reset(alien_row2[j].x,alien_row2[j].y)
            for k in range(alien_row1[j].total_tiro):
                if shield2[i].rect != 0 and alien_row1[j].laser[k].teste_colisao(shield2[i]):
                    shield2[i].kill()
                    alien_row1[j].laser[k].reset(alien_row1[j].x,alien_row1[j].y)

        if shield3[i].rect != 0 and player_laser.teste_colisao(shield3[i]):
            shield3[i].kill()
            player_laser.reset(player.x,player.y)          
        for j in range(ALIEN_NUMBER):          
            for k in range(alien_row3[j].total_tiro):
                if shield3[i].rect != 0 and alien_row3[j].laser[k].teste_colisao(shield3[i]):
                    shield3[i].kill()
                    alien_row3[j].laser[k].reset(alien_row3[j].x,alien_row3[j].y)
            for k in range(alien_row2[j].total_tiro):
                if shield3[i].rect != 0 and alien_row2[j].laser[k].teste_colisao(shield3[i]):
                    shield3[i].kill()
                    alien_row2[j].laser[k].reset(alien_row2[j].x,alien_row2[j].y)
            for k in range(alien_row1[j].total_tiro):
                if shield3[i].rect != 0 and alien_row1[j].laser[k].teste_colisao(shield3[i]):
                    shield3[i].kill()
                    alien_row1[j].laser[k].reset(alien_row1[j].x,alien_row1[j].y)

def reset_jogo(player, alien_row1, alien_row2, alien_row3, shield1, shield2, shield3):
    global ALIEN_NUMBER, ALIEN_SEPARACAO

    if ALIEN_NUMBER > 0:
        player.pontuacao = 0
        player.vidas = 5

    player.dead = False
    player.invencivel = False
    player.tempo_invencivel = 0

    alien_row1.clear()
    alien_row2.clear()
    alien_row3.clear()   

    shield1.clear()
    shield2.clear()
    shield3.clear()

    for i in range(ALIEN_NUMBER):
        alien_row1.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),50,"assets/alien1.png","assets/alien2.png"))
        alien_row2.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),130,"assets/alien1c.png","assets/alien2c.png"))
        alien_row3.append(inimigos.alien(50 + i*(100+ALIEN_SEPARACAO),210,"assets/alien1e.png","assets/alien2e.png"))

    for i in range(SHIELD_SIZE):
        shield1.append(cenario.shield(50 + i*10,450))
        shield2.append(cenario.shield(300 + i*10,450))
        shield3.append(cenario.shield(550 + i*10,450))

## MAIN ##
if __name__ == '__main__':
    main()


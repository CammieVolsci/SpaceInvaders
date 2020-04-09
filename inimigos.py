import pygame

LASER_IMAGE = "assets/laser2.png"

class alien(pygame.sprite.Sprite):

    def __init__(self,x,y,alien_image1,alien_image2):
        self.x = x
        self.y = y
        self.mover = 5
        self.direcao = "Direita"
        self.image1 = pygame.image.load(alien_image1)
        self.image1 = pygame.transform.scale(self.image1,(50,36))
        self.image2 = pygame.image.load(alien_image2)
        self.image2 = pygame.transform.scale(self.image2,(50,36))
        self.rect = self.image1.get_rect()     
        self.laser = []
        self.tiro = 'Desativado'
        self.total_tiro = 0

    def movimento(self,screen,distancia,i,total, time_frame):       
        self.x += self.mover

        if self.x + (total-1-i)*(100+distancia) >=688:
            self.mover = -5
            self.direcao = "Esquerda"
        elif self.x - i*(100+distancia) <=0:
            self.mover = 5
            self.direcao = "Direita"

        if self.image1 != 0 or self.image2 != 0:
            if time_frame > 150:
                screen.blit(self.image1,(self.x,self.y))
            else:
                screen.blit(self.image2,(self.x,self.y)) 
            self.rect.x = self.x
            self.rect.y = self.y        

    def kill(self):
        self.image1 = 0
        self.image2 = 0
        self.mover = 0 
        self.direcao = 0
        self.x = 0
        self.y = 0
        self.rect = 0
   
class laser(pygame.sprite.Sprite):
    
    def __init__(self,alien_x,alien_y):
        super().__init__()
        self.x = alien_x
        self.y = alien_y
        self.state = 'Atirando'
        self.image = pygame.image.load(LASER_IMAGE)
        self.image = pygame.transform.scale(self.image,(10,25))
        self.rect = self.image.get_rect()
        self.height = self.image.get_rect().height

    def atira(self,screen,window_height):
        self.y += 5
        if(self.image != 0):      
            self.rect.x = self.x
            self.rect.y = self.y
            screen.blit(self.image,(self.x,self.y))   

        if self.y + self.height >= window_height:
            self.kill()
            self.state = 'Parado'      

    def reset(self,x,y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def teste_colisao(self,sprite):
        if(self.image!=0):
            return self.rect.colliderect(sprite.rect)

    def kill(self):
        self.image = 0
        self.x = 0
        self.y = 0
        self.rect = 0
        self.height = 0
        self.state = 0
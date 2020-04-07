import pygame

BLACK = (0,0,0)

class alien(pygame.sprite.Sprite):

    def __init__(self,x,y,alien_image1, alien_image2):
        self.x = x
        self.y = y
        self.mover = 5
        self.direcao = "Direita"
        self.image1 = pygame.image.load(alien_image1)
        self.image2 = pygame.image.load(alien_image2)
        self.rect = self.image1.get_rect()     

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
            
            #pygame.draw.rect(screen,BLACK,self.rect)          

    def kill(self):
        self.image1 = 0
        self.image2 = 0
        self.mover = 0 
        self.direcao = 0
        self.x = 0
        self.y = 0
        self.rect = 0
   
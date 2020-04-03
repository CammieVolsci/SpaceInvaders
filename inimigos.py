import pygame

ALIENSHIP_IMAGE = "assets/alienship.png"
BLACK = (0,0,0)

class alienship(pygame.sprite.Sprite):

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.mover = 0.8
        self.direcao = "Direita"
        self.image = pygame.image.load(ALIENSHIP_IMAGE)  
        self.rect = self.image.get_rect()        

    def movimento(self,screen):        
        self.x += self.mover

        if self.image != 0:
            screen.blit(self.image,(self.x,self.y)) 
            self.rect.x = self.x
            self.rect.y = self.y
            
            pygame.draw.rect(screen,BLACK,self.rect)          

    def kill(self):
        self.image = 0
        self.mover = 0 
        self.direcao = 0
        self.x = 0
        self.y = 0
        self.rect = 0

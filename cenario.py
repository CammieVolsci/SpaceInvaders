import pygame

SHIELD_IMAGE = "assets/shield_part.png"

class shield():

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(SHIELD_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def desenha_escudo(self,screen):
        if(self.image != 0):
            screen.blit(self.image,(self.x,self.y))

    def kill(self):
        self.image = 0
        self.x = 0
        self.y = 0
        self.rect = 0
        
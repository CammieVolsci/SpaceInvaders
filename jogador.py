import pygame

PLAYERSHIP_IMAGE = "assets/playership.png"
LASER_IMAGE = "assets/laser.png"

class playership(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.x = 390
        self.y = 550
        self.mover = 0
        self.image = pygame.image.load(PLAYERSHIP_IMAGE)    
        self.image = pygame.transform.scale(self.image,(84,50))  
        self.rect = self.image.get_rect() 
        self.width = self.image.get_rect().width     

    def movimento(self,screen):       
        self.x += self.mover
        screen.blit(self.image,(self.x,self.y))

        if self.x <= 0:
            self.x = 0
        elif self.x >= 688:
            self.x = 688

        self.rect.x = self.x
        self.rect.y = self.y         

class laser(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.x = 370
        self.y = 480
        self.state = "Espera"
        self.image = pygame.image.load(LASER_IMAGE)
        self.image = pygame.transform.scale(self.image,(10,25))
        self.rect = self.image.get_rect()
        self.height = self.image.get_rect().height

    def atira(self,screen):
        self.y -= 50       
        screen.blit(self.image,(self.x-10,self.y))   

        if self.y + self.height <= 0:
            self.y = 460
            self.state = "Espera"
        
        self.rect.x = self.x
        self.rect.y = self.y  

    def reset(self,x,y):
        self.state = "Espera"
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def teste_colisao(self,sprite):
        if(self.image!=0):
            return self.rect.colliderect(sprite.rect)
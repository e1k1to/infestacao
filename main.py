#Lucca Eiki Amarante Millian - 10390794

import pygame
from pygame.locals import *

all_sprites = pygame.sprite.Group()
inimigos = []
inimigos_mortos = []

pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Infestação')

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.position = pygame.math.Vector2(screen_width // 2, screen_height // 2)
        self.speed = 5
        
        self.image = pygame.image.load('mira.png')
        self.image = pygame.transform.scale(self.image, (200,200)) 
        self.rect = self.image.get_rect()
        self.rect.center = self.position
  
    def update(self):
        keys = pygame.key.get_pressed()
            
        # Movimentação
        if (keys[K_LEFT] or keys[K_a]) and self.position.x > 0:
            self.position.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.position.x < screen_width:
            self.position.x += self.speed
        if (keys[K_UP] or keys[K_w]) and self.position.y > 0:
            self.position.y -= self.speed
        if (keys[K_DOWN] or keys[K_s]) and self.position.y < screen_height:
            self.position.y += self.speed

        if keys[K_SPACE]:
            self.shootproj(self.position.x, self.position.y)

        # Atualiza a posição do retângulo da nave
        xcentro = self.rect.center[0]
        ycentro = self.rect.center[1]
        
        for inimigo in inimigos:
            if(xcentro > inimigo.rect.left and xcentro < inimigo.rect.right and ycentro > inimigo.rect.top and ycentro < inimigo.rect.bottom):
                inimigo.morte()
                inimigos.remove(inimigo)
                inimigos_mortos.append(inimigos)
        
        self.rect.center = self.position

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Inimigo, self).__init__()
        self.position = pygame.math.Vector2(x,y)
        self.speed = 3
        
        self.image = pygame.image.load('formiga.png')
        self.image = pygame.transform.scale(self.image, (50,50)) 
        self.rect = self.image.get_rect()
        self.rect.center = self.position
  
    def update(self):
        # Atualiza a posição do retângulo da nave
        self.rect.center = self.position

    def morte(self):
        self.image = pygame.image.load('formiga_morta.png')
        self.image = pygame.transform.scale(self.image, (50,50))


def main():
    clock = pygame.time.Clock()
    cursor = Cursor()
    all_sprites.add(cursor)
    
    inimigos.append(Inimigo(100,200))
    inimigos.append(Inimigo(200,300))
    inimigos.append(Inimigo(300,400))
    for inimigo in inimigos:
        all_sprites.add(inimigo)
    #bg = pygame.image.load("fundo.png")
    #bg = pygame.transform.scale(bg, (screen_width, screen_height))

    running = True
    timer = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        all_sprites.update()
      
        screen.fill((255,255,255))  # Preenche o fundo de branco
        #screen.blit(bg, (0, scrolly-screen_height)) #tem q ver isso ai
        #screen.blit(bg, (0, scrolly)) #tem q ver isso ai
      
        all_sprites.draw(screen)
        clk = pygame.time.Clock().tick()
          
        pygame.display.flip()

        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
  main()


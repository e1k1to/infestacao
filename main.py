#Lucca Eiki Amarante Millian - 10390794

"""
códigos de pause
1- continuar
2- voltar ao main menu
"""

import pygame
from pygame.locals import *

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
inimigos = []
inimigos_mortos = []
game_menu = True

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

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, scale):
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.center=(x,y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                action = True
        
        screen.blit(self.img, (self.rect.x, self.rect.y))
        return action

def pause():
    borras = pygame.Surface((screen_width, screen_height), flags=pygame.SRCALPHA)
    borras.fill((75,75,75,100))
    screen.blit(borras, (0,0))

    butao_continue = pygame.image.load("butao_continua.png")
    if Button(500, 200, butao_continue, 1).draw():
        return 1 #volta pro jogo 

    butao_quit = pygame.image.load("butao_quit.png")
    if Button(500, 300, butao_quit, 1).draw():
        return 2 #volta pro menu

def prim_fase():
    game_paused = False
    
    cursor = Cursor()
    
    all_sprites.add(cursor)
    inimigos.append(Inimigo(100,200))
    inimigos.append(Inimigo(200,300))
    inimigos.append(Inimigo(300,400))
    for inimigo in inimigos:
        all_sprites.add(inimigo)
    
    running = True
    timer = 0
    while running:
        screen.fill((255,255,255))  # Preenche o fundo de branco
        all_sprites.draw(screen)
        
        if game_paused:
            id = pause()
            if id == 1:
                game_paused = False
            elif id == 2:
                running = False
                pygame.time.delay(100)
            
        else:
            all_sprites.update()

        clk = pygame.time.Clock().tick()
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
    return

def main():
    bg = pygame.image.load("fundo.png")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    pygame.display.set_caption("Menu")
    botao_jogar = pygame.image.load("butao_jogar.png")
    botao_sair = pygame.image.load("butao_quit.png")
    botao_config = pygame.image.load("butao_config.png")
    
    running_menu = True

    while running_menu:
        screen.blit(bg, (0,0))
        if Button(500, 200, botao_jogar, 1).draw():
            prim_fase()
        
        if Button(500, 400, botao_config, 1).draw(): 
            running_menu = False

        if Button(500, 600, botao_sair, 1).draw(): 
            running_menu = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False

        pygame.display.update()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
  main()


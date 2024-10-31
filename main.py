#Lucca Eiki Amarante Millian - 10390794

"""
códigos de pause
1- continuar
2- voltar ao main menu
"""


import pygame
from pygame.locals import *

pontuacao = 0 

volume = 0.2
sens = 5
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

def inverteCores(img):
    inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
    inv.fill((255,255,255,255))
    inv.blit(img, (0,0), None, BLEND_RGB_SUB)
    return inv

def drawText(texto, tamanho, fontName, x, y, cor):
    font = pygame.font.Font(fontName, tamanho)
    text_surface = font.render(texto, True, cor)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    screen.blit(text_surface,text_rect)

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__()
        self.position = pygame.math.Vector2(screen_width // 2, (screen_height // 4)*3)
        global sens
        self.speed = sens
        
        self.image = pygame.image.load('imagens/mira.png')
        self.image = pygame.transform.scale(self.image, (200,200)) 
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.somRecarga = pygame.mixer.Sound('audios/arma.mp3')
        self.ultimoTiro = pygame.time.get_ticks()
        self.cooldown = 1000
  
    def update(self):
        keys = pygame.key.get_pressed()
        
        x = self.rect.center[0]
        y = self.rect.center[1]

        if x > screen_width//2:
            self.position.x -= 2
        if x+1 < screen_width//2:
            self.position.x += 2
        if y > screen_height//4*3:
            self.position.y -= 2
        if y < screen_height//4*3:
            self.position.y += 2

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
            if(xcentro > inimigo.rect.left 
               and xcentro < inimigo.rect.right 
               and ycentro > inimigo.rect.top 
               and ycentro < inimigo.rect.bottom
               and pygame.time.get_ticks() - self.ultimoTiro >= self.cooldown
               ): 
                self.ultimoTiro = pygame.time.get_ticks()
                if inimigo.morte():
                    inimigos_mortos.append(inimigo.tipo) # pode ser usado pra calcular pontos dps
                    inimigos.remove(inimigo)
                self.somRecarga.set_volume(volume)
                self.somRecarga.play()
        
        self.rect.center = self.position

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super(Inimigo, self).__init__()
        self.position = pygame.math.Vector2(x,y)
        self.morta = False
        self.alpha = 255
        self.valor = 0
        self.hits = 0
        self.angle = 1

        if (tipo == 'formiga'):
            self.tipo = 'formiga'
            self.valor = 5
            self.image = pygame.image.load('imagens/formiga.png')
            self.image = pygame.transform.scale(self.image, (50,50)) 
            self.speed = 3
            self.maxhits = 1
        
        if (tipo == 'barata'):
            self.tipo = 'barata'
            self.valor = 10
            self.image = pygame.image.load('imagens/formiga.png')
            self.image = pygame.transform.scale(self.image, (60,60)) 
            self.speed = 5
            self.maxhits = 2
        
        if (tipo == 'escorpiao'):
            self.tipo = 'escorpiao'
            self.valor = 20
            self.image = pygame.image.load('imagens/formiga.png')
            self.image = pygame.transform.scale(self.image, (80,80)) 
            self.speed = 10
            self.maxhits = 3
        
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.somMorte = pygame.mixer.Sound('audios/smash.mp3')
        self.image = pygame.transform.rotate(self.image, 180)

  

    def update(self):
        # Atualiza a posição do retângulo da nave
        #self.angle += 1
        #self.image = pygame.transform.rotate(self.image, self.angle) #KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKk

        #self.position.x += self.speed
        if self.morta:
            self.alpha -= 0.05
            self.image.fill((255,255,255,self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        if self.alpha <= 250:
            self.kill()
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def morte(self):
        global volume
        self.somMorte.set_volume(volume)
        self.somMorte.play()

        self.hits += 1

        if self.hits == self.maxhits:
            self.image = pygame.image.load('imagens/formiga_morta.png')
            self.image = pygame.transform.scale(self.image, (50,50))
            self.morta = True
            return True
        return False

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, scale):
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.center=(x,y)
        self.clicked = False
        self.teste = False

    def draw(self):
        action = False
        evento = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.img = inverteCores(self.img)
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                action = True
                pygame.time.delay(150)
        screen.blit(self.img, (self.rect.x, self.rect.y))
        return action
        

def pause():
    borras = pygame.Surface((screen_width, screen_height), flags=pygame.SRCALPHA)
    borras.fill((75,75,75,100))
    screen.blit(borras, (0,0))

    butao_continue = pygame.image.load("imagens/butao_continua.png")
    if Button(500, 200, butao_continue, 1).draw():
        return 1 #volta pro jogo 

    butao_quit = pygame.image.load("imagens/butao_quit.png")
    if Button(500, 300, butao_quit, 1).draw():
        return 2 #volta pro menu


def prim_fase():
    pontuacao = 0
    game_paused = False
    
    cursor = Cursor()
    
    all_sprites.add(cursor)
    inimigos.append(Inimigo(100,200, 'formiga'))
    inimigos.append(Inimigo(200,300, 'barata'))
    inimigos.append(Inimigo(300,400, 'escorpiao'))
    for inimigo in inimigos:
        all_sprites.add(inimigo)
    
    running = True
    while running:
        screen.fill((255,255,255))  # Preenche o fundo de branco
        all_sprites.draw(screen)
        
        if game_paused:
            id = pause()
            if id == 1:
                game_paused = False
            elif id == 2:
                all_sprites.remove(cursor)
                cursor.kill()
                for inimigo in inimigos:
                    inimigo.kill()
                running = False
            
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

def setVolume(volumeNovo):
    global volume
    volume = (volumeNovo/100)

def setSensibility(novaSens):
    global sens
    sens = novaSens

def menuConfig():
    running = True
    global volume
    vlm = volume*100
    global sens
    while running:
        screen.fill((128,128,128))  # Preenche o fundo de branco
        volume_down = pygame.image.load("imagens/voldown.png")
        volume_up = pygame.image.load("imagens/volup.png")
        botao_sair = pygame.image.load("imagens/butao_quit.png")
        botao_config = pygame.image.load("imagens/butao_config.png")
        
        running_menu = True
        

        drawText(f"Volume = {int(vlm)}", 80, 'fonts/AnonymousPro-Regular.ttf', 500, 100, (255,255,255))
        
        drawText(f"Sensibilidade = {int(sens)}", 80, 'fonts/AnonymousPro-Regular.ttf', 500, 400, (255,255,255))

        if Button(600, 250, volume_up, 1).draw():
            if vlm >= 100:
                pass
            else:
                vlm += 5
            setVolume(vlm)
            pygame.mixer.music.set_volume((vlm/100)-0.10)
        if Button(400, 250, volume_down, 1).draw():
            if vlm <= 0:
                pass
            else:
                    vlm -= 5
            setVolume(vlm)
            pygame.mixer.music.set_volume((vlm/100)-0.10)
        
        if Button(600, 550, volume_up, 1).draw():
            if sens >= 10:
                pass
            else:
                sens += 1
        if Button(400, 550, volume_down, 1).draw():
            if sens <= 3:
                pass
            else:
                sens -= 1

        if Button(500, 725, botao_sair, 1).draw(): 
            running = False
                
        clk = pygame.time.Clock().tick()
        clock.tick(60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    return

#def setVolume(valor):



def main():
    global volume
    bg = pygame.image.load("imagens/fundo.png")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    font = 'fonts/AnonymousPro-Regular.ttf'
    pygame.display.set_caption("Menu")
    botao_jogar = pygame.image.load("imagens/butao_jogar.png")
    botao_sair = pygame.image.load("imagens/butao_quit.png")
    botao_config = pygame.image.load("imagens/butao_config.png")

    pygame.mixer.init()
    pygame.mixer.music.load("audios/musica.mp3")
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play()

    #pygame.mixer.Sound.set_volume(20)
    
    running_menu = True

    while running_menu:
        screen.blit(bg, (0,0))
        #drawText("HAHAHAHAHAHAHA", 24, font, 100, 100, (255,255,255))

        if Button(500, 200, botao_jogar, 1).draw():
            prim_fase()
        
        if Button(500, 400, botao_config, 1).draw(): 
            menuConfig()

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


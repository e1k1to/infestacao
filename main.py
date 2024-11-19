#Lucca Eiki Amarante Millian - 10390794

"""
códigos de pause
1- continuar
2- voltar ao main menu
"""


import pygame
from pygame.locals import *
from random import randint, choice

volume = 0.2
sens = 7
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
inimigos = []
inimigos_mortos = []
inimigos_fila = []
inimigos_perdidos = []
posicoes = ['D','E']
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
    def __init__(self, x, y, tipo, direcao):
        super(Inimigo, self).__init__()
        self.position = pygame.math.Vector2(x,y)
        self.morta = False
        self.alpha = 255
        self.valor = 0
        self.hits = 0
        self.movendo = False
        self.angle = 1
        self.direcao = direcao #D ou E

        if (tipo == 'formiga'):
            self.tipo = 'formiga'
            self.valor = 5
            self.image = pygame.image.load('imagens/formiga.png')
            self.image = pygame.transform.scale(self.image, (70,70)) 
            self.speed = 3
            self.maxhits = 1
        
        if (tipo == 'barata'):
            self.tipo = 'barata'
            self.valor = 10
            self.image = pygame.image.load('imagens/barata.png')
            self.image = pygame.transform.scale(self.image, (80,80)) 
            self.speed = 2
            self.maxhits = 2
        
        if (tipo == 'escorpiao'):
            self.tipo = 'escorpiao'
            self.valor = 20
            self.image = pygame.image.load('imagens/escorpiao.png')
            self.image = pygame.transform.scale(self.image, (100,100)) 
            self.speed = 1
            self.maxhits = 3
        
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.somMorte = pygame.mixer.Sound('audios/smash.mp3')

        if direcao == "D":
            self.image = pygame.transform.rotate(self.image, 315)

        elif direcao == "E" and tipo == 'escorpiao':
            self.image = pygame.transform.rotate(self.image, 315)
            self.image = pygame.transform.flip(self.image,True,False)

        else:
            self.image = pygame.transform.rotate(self.image, 135)

    def movimentar(self):
        self.movendo = True

    def update(self):
        # Atualiza a posição do retângulo da nave
        #self.angle += 1
        #self.image = pygame.transform.rotate(self.image, self.angle) #KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKk
        
        x, y = self.position

        if(x > screen_width+100 or x < -100):
            self.kill()
            inimigos.remove(self)

        if not self.morta and self.movendo:
            if self.direcao == "D":
                self.position.x += self.speed
            else:
                self.position.x -= self.speed

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
            if self.tipo == 'formiga':
                self.image = pygame.image.load('imagens/formiga_morta.png')
                self.image = pygame.transform.scale(self.image, (70,70)) 
                if self.direcao == 'D':
                    self.image = pygame.transform.rotate(self.image, 315)
                else:
                    self.image = pygame.transform.rotate(self.image, 135)

            if self.tipo == 'barata':
                self.image = pygame.image.load('imagens/barata_morta.png')
                self.image = pygame.transform.scale(self.image, (80,80)) 
                if self.direcao == 'D':
                    self.image = pygame.transform.rotate(self.image, 315)
                else:
                    self.image = pygame.transform.rotate(self.image, 135)

            if self.tipo == 'escorpiao':
                self.image = pygame.image.load('imagens/escorpiao_morto.png')
                self.image = pygame.transform.scale(self.image, (100,100)) 
                self.image = pygame.transform.rotate(self.image, 315)
                if self.direcao == 'E':
                    self.image = pygame.transform.flip(self.image,True,False)

            self.morta = True
            return True
        return False

    def morterapida(self):
        self.kill()

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
    if Button(500, 250, butao_continue, 1).draw():
        return 1 #volta pro jogo 

    butao_quit = pygame.image.load("imagens/butao_quit.png")
    if Button(500, 500, butao_quit, 1).draw():
        return 2 #volta pro menu

def mostra_resultados(fase):
    texto_resultado = ''
    global inimigos_mortos
    soma_pontos = 0
    for i in inimigos_mortos:
        if i == 'formiga':
            soma_pontos += 20
        elif i == 'barata':
            soma_pontos += 50
        else:
            soma_pontos += 100
    running = True
    if fase == 1:
        if soma_pontos >= 180:
            texto_resultado = "Pontuação Perfeita"
        elif soma_pontos >= 120:
            texto_resultado = "Pontuação Boa"
        else:
            texto_resultado = "Pontuação Baixa"
    elif fase == 2:
        if soma_pontos >= 270:
            texto_resultado = "Pontuação Perfeita"
        elif soma_pontos >= 190:
            texto_resultado = "Pontuação Boa"
        else:
            texto_resultado = "Pontuação Baixa"

    else:
        if soma_pontos >= 630:
            texto_resultado = "Pontuação Perfeita"
        elif soma_pontos >= 400:
            texto_resultado = "Pontuação Boa"
        else:
            texto_resultado = "Pontuação Baixa"

    global volume
    vlm = volume*100
    global sens
    while running:
        screen.fill((128,128,128))  # Preenche o fundo de branco
        drawText(f"Pontuação = {soma_pontos}", 80, 'fonts/AnonymousPro-Regular.ttf', 500, 300, (255,255,255))
        drawText(texto_resultado, 80, 'fonts/AnonymousPro-Regular.ttf', 500, 400, (255,255,255))
        prox_fase = pygame.image.load("imagens/butao_proxfase.png")
        botao_sair = pygame.image.load("imagens/butao_quit.png")
        running_menu = True
        
        if(fase < 3):
            if Button(500, 600, prox_fase, 1).draw():
                if(fase == 1):
                    running = False
                    segu_fase()
                if(fase == 2):
                    running = False
                    terc_fase()
                

        if fase < 3:
            if Button(500, 725, botao_sair, 1).draw():
                running = False
        else:
            if Button(500, 500, botao_sair, 1).draw():
                pygame.time.delay(150)
                running = False
                if fase == 3:
                    running = False
                    game_story = True

                    while game_story:
                        screen.fill((128,128,128))  # Preenche o fundo de branco
                        drawText(f"Boa tarde, senhor José.", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 100, (255,255,255))
                        drawText(f"Agradeço fortemente sua ajuda na remoção das", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 150, (255,255,255))
                        drawText(f"pragas da minha casa, o senhor realmente é", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 200, (255,255,255))
                        drawText(f"o melhor no que faz! Caso as pragas voltem,", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 250, (255,255,255))
                        drawText(f"já sei quem devo chamar!", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 300, (255,255,255))
                        drawText(f"Assinado: James.", 40, 'fonts/AnonymousPro-Regular.ttf', 700, 475, (255,255,255))
                        continua = pygame.image.load("imagens/butao_continua.png")

                        if Button(500, 650, continua, 1).draw():
                            game_story = False
                            running = False

                        clock.tick(60)
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    game_story = False
                
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
    #formiga, barata, escorpiao

def prim_fase():
    global inimigos_mortos
    inimigos_mortos = []
    total_inimigos = 9
    imgbg = pygame.image.load('imagens/mesa.png').convert_alpha()
    game_paused = False

    game_story = True

    while game_story:
        screen.fill((128,128,128))  # Preenche o fundo de branco
        drawText(f"Boa tarde, senhor José.", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 100, (255,255,255))
        drawText(f"Tenho enfrentado problemas com diferentes", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 150, (255,255,255))
        drawText(f"tipos de pragas, minhas fontes me disseram", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 200, (255,255,255))
        drawText(f"que você é o melhor exterminador de pragas", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 250, (255,255,255))
        drawText(f"cidade.", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 300, (255,255,255))
        drawText(f"Estarei contando com sua ajuda.", 40, 'fonts/AnonymousPro-Regular.ttf', 500, 375, (255,255,255))
        drawText(f"Assinado: James.", 40, 'fonts/AnonymousPro-Regular.ttf', 700, 475, (255,255,255))
        continua = pygame.image.load("imagens/butao_continua.png")

        if Button(500, 650, continua, 1).draw():
            game_story = False

        clock.tick(60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            

    cursor = Cursor()
    
    #todos inimigos
    for i in range(total_inimigos):
        dir_atual = choice(['D','E'])
        range_x = []
        range_y = [300,400,500,600,700]
        if (dir_atual == 'D'):
            range_x = [-99,-10]
            inimigos.append(Inimigo(randint(range_x[0], range_x[1]),choice(range_y),'formiga',dir_atual))
        else:
            range_x = [screen_width+10,screen_width+99]
            inimigos.append(Inimigo(randint(range_x[0], range_x[1]),choice(range_y),'formiga',dir_atual))

    all_sprites.add(cursor)
    for inimigo in inimigos:
        all_sprites.add(inimigo)
    
    gotms = [False, False, False]
    running = True
    while running:
        bg = screen.blit(imgbg,[0,0])
        #screen.fill((255,255,255))  # Preenche o fundo de branco
        all_sprites.draw(screen)
        
        if not gotms[0]: #wave 1
            for i in range(3):
                inimigos[i].movimentar()
            gotms[0] = True

        if len(inimigos) == total_inimigos-3 and not gotms[1]: #wave 2
            for i in range(3):
                inimigos[i].movimentar()
            gotms[1] = True
        
        if len(inimigos) == total_inimigos-6 and not gotms[2]: #wave 3
            for i in range(3):
                inimigos[i].movimentar()
            gotms[2] = True

        if game_paused:
            ids = pause()
            if ids == 1:
                game_paused = False
            elif ids == 2:
                all_sprites.remove(cursor)
                cursor.kill()
                for i in range(len(inimigos)-1,-1,-1):
                    inimigos[i].morterapida()
                    inimigos.pop(i)
                pygame.time.delay(150)
                return
            
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

        #and pygame.time.get_ticks() - self.ultimoTiro >= self.cooldown

        if not inimigos: #ou seja, ja nao tem ninguem vivo ou prestes a spawnar
            somVitoria = pygame.mixer.Sound('audios/vitoria.mp3') #som para fim de fase
            somVitoria.set_volume(volume) #som para fim de fase
            somVitoria.play() #som para fim de fase
            all_sprites.remove(cursor)
            cursor.kill()
            mostra_resultados(1) #acho a boa
            running = False
            return

def segu_fase():
    global inimigos_mortos
    inimigos_mortos = []
    total_inimigos = 12
    imgbg = pygame.image.load('imagens/banheiro.png').convert_alpha()
    imgbg = pygame.transform.scale(imgbg, (screen_width, screen_height))
    game_paused = False
    
    gotms = []

    cursor = Cursor()
    
    #todos inimigos
    for i in range(total_inimigos-1):
        dir_atual = choice(['D','E'])
        range_x = []
        range_y = [300,400,500,600,700]
        if (dir_atual == 'D'):
            range_x = [-99,-10]
            inimigos.append(Inimigo(randint(range_x[0], range_x[1]),choice(range_y),'formiga',dir_atual))
        else:
            range_x = [screen_width+10,screen_width+99]
            inimigos.append(Inimigo(randint(range_x[0], range_x[1]),choice(range_y),'formiga',dir_atual))

    inimigos.append(Inimigo(-50,400,'barata','D'))

    all_sprites.add(cursor)
    for inimigo in inimigos:
        all_sprites.add(inimigo)
    
    for i in range(4): #waves
        gotms.append(False)
    running = True
    while running:
        bg = screen.blit(imgbg,[0,0])
        #screen.fill((255,255,255))  # Preenche o fundo de branco
        all_sprites.draw(screen)
        
        if not gotms[0]: #wave 1
            for i in range(3):
                inimigos[i].movimentar()
            gotms[0] = True

        if len(inimigos) == total_inimigos-3 and not gotms[1]: #wave 2
            for i in range(3):
                inimigos[i].movimentar()
            gotms[1] = True
        
        if len(inimigos) == total_inimigos-6 and not gotms[2]: #wave 3
            for i in range(3):
                inimigos[i].movimentar()
            gotms[2] = True
        
        if len(inimigos) == total_inimigos-9 and not gotms[3]: #wave 4
            for i in range(3):
                inimigos[i].movimentar()
            gotms[2] = True

        if game_paused:
            ids = pause()
            if ids == 1:
                game_paused = False
            elif ids == 2:
                all_sprites.remove(cursor)
                cursor.kill()
                for i in range(len(inimigos)-1,-1,-1):
                    inimigos[i].morterapida()
                    inimigos.pop(i)
                pygame.time.delay(150)
                return
            
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

        #and pygame.time.get_ticks() - self.ultimoTiro >= self.cooldown

        if not inimigos: #ou seja, ja nao tem ninguem vivo ou prestes a spawnar
            somVitoria = pygame.mixer.Sound('audios/vitoria.mp3') #som para fim de fase
            somVitoria.set_volume(volume) #som para fim de fase
            somVitoria.play() #som para fim de fase
            all_sprites.remove(cursor)
            cursor.kill()
            mostra_resultados(2) #acho a boa
            running = False
            return

def terc_fase():
    global inimigos_mortos
    inimigos_mortos = []
    total_inimigos = 15 # 3 baratas e 3 escorpioes
    imgbg = pygame.image.load('imagens/jardim.png').convert_alpha()
    imgbg = pygame.transform.scale(imgbg, (screen_width, screen_height))
    baratas = 3
    game_paused = False

    gotms = []

    cursor = Cursor()
    
    #todos inimigos
    for i in range(total_inimigos-6):
        bixo = 'formiga'
        dir_atual = choice(['D','E'])
        range_x = []
        range_y = [300,400,500,600,700]
        if (dir_atual == 'D'):
            range_x = [-80,-30]
            inimigos.append(Inimigo(randint(range_x[0], range_x[1]),choice(range_y), bixo, dir_atual))
        else:
            range_x = [screen_width+30,screen_width+80]
            inimigos.append(Inimigo(randint(range_x[0], range_x[1]),choice(range_y), bixo, dir_atual))
    
    inimigos.append(Inimigo(-50,400,'barata','D'))
    inimigos.append(Inimigo(-50,100,'barata','D'))
    inimigos.insert(8,Inimigo(-50,200,'barata','D'))
    inimigos.append(Inimigo(-60,400,'escorpiao','D'))
    inimigos.append(Inimigo(-99,200,'escorpiao','D'))
    inimigos.append(Inimigo(screen_width+60,300,'escorpiao','E'))

    all_sprites.add(cursor)
    for inimigo in inimigos:
        all_sprites.add(inimigo)
    
    for i in range(5): #waves
        gotms.append(False)

    running = True
    while running:
        bg = screen.blit(imgbg,[0,0])
        #screen.fill((255,255,255))  # Preenche o fundo de branco
        all_sprites.draw(screen)
        
        if not gotms[0]: #wave 1
            for i in range(3):
                inimigos[i].movimentar()
            gotms[0] = True

        if len(inimigos) == total_inimigos-3 and not gotms[1]: #wave 2
            for i in range(3):
                inimigos[i].movimentar()
            gotms[1] = True
        
        if len(inimigos) == total_inimigos-6 and not gotms[2]: #wave 3
            for i in range(3):
                inimigos[i].movimentar()
            gotms[2] = True
        
        if len(inimigos) == total_inimigos-9 and not gotms[3]: #wave 4
            for i in range(3):
                inimigos[i].movimentar()
            gotms[3] = True
        
        if len(inimigos) == total_inimigos-12 and not gotms[4]: #wave 5
            for i in range(3):
                inimigos[i].movimentar()
            gotms[4] = True

        if game_paused:
            ids = pause()
            if ids == 1:
                game_paused = False
            elif ids == 2:
                all_sprites.remove(cursor)
                cursor.kill()
                for i in range(len(inimigos)-1,-1,-1):
                    inimigos[i].morterapida()
                    inimigos.pop(i)
                pygame.time.delay(150)
                return
            
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

        if not inimigos: #ou seja, ja nao tem ninguem vivo ou prestes a spawnar
            somVitoria = pygame.mixer.Sound('audios/vitoria.mp3') #som para fim de fase
            somVitoria.set_volume(volume) #som para fim de fase
            somVitoria.play() #som para fim de fase
            all_sprites.remove(cursor)
            cursor.kill()
            mostra_resultados(3) #acho a boa
            running = False
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
            #terc_fase()
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


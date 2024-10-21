import time
import pygame
import os
import random

#Alterações Grupo 2
from PIL import Image, ImageSequence

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'caixao.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.jpg')))
IMAGEM_BACKGROUND = pygame.image.load(os.path.join('imgs','background_cemiterio.png'))
IMAGEM_VIDA0 = pygame.image.load(os.path.join('imgs', 'vida0.png'))
IMAGEM_VIDA1 = pygame.image.load(os.path.join('imgs', 'vida1.png'))
IMAGEM_VIDA2 = pygame.image.load(os.path.join('imgs', 'vida2.png'))
IMAGEM_VIDA3 = pygame.image.load(os.path.join('imgs', 'vida3.png'))
IMAGEM_GAME_OVER = pygame.image.load(os.path.join('imgs', 'gameover.png'))
IMAGEM_PONTUACAO = pygame.image.load(os.path.join('imgs', 'pontuacao2.png'))
IMAGEM_MENOR_PONTUACAO = pygame.transform.scale(IMAGEM_PONTUACAO, (180, 35))
IMAGEM_RECORDE = pygame.image.load(os.path.join('imgs', 'recorde-img.png'))
IMAGEM_MENOR_RECORDE = pygame.transform.scale(IMAGEM_RECORDE, (180, 35))

# Alteração Grupo 3
pygame.mixer.init()
musica_de_fundo = pygame.mixer.music.load(os.path.join('sons', 'this-is-halloween-172354.mp3'))
pygame.mixer.music.set_volume(0.3)
musica_de_fundo_do_jogo = pygame.mixer.Sound('./sons/StockTune-Creepy Crawly Capers_1729035356.mp3')
som_contagem = pygame.mixer.Sound(os.path.join('sons', 'smw_kick.wav'))
som_pulo = pygame.mixer.Sound(os.path.join('sons', 'mixkit-player-jumping-in-a-video-game-2043.wav'))
som_colisão = pygame.mixer.Sound(os.path.join('sons', 'mixkit-arcade-fast-game-over-233.wav'))
som_gameOver = pygame.mixer.Sound(os.path.join('sons', 'mixkit-evil-dwarf-laugh-421.wav'))
som_pulo.set_volume(0.2)
som_colisão.set_volume(0.3)
som_gameOver.set_volume(0.8)

def contagem(seconds, tela):
    while seconds >= 0:
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        font = pygame.font.SysFont('arial', 74)
        if seconds == 0:
            text = font.render('GO!', True, (255, 255, 255))
        else:
            text = font.render(str(seconds), True, (255, 255, 255))
        tela.blit(text, (TELA_LARGURA // 2 - text.get_width() // 2, TELA_ALTURA // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)
        seconds -= 1
        som_contagem.play()

def load_gif(filename):
    gif = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert('RGBA')
        pygame_surface = pygame.image.frombuffer(
            frame.tobytes(), frame.size, frame.mode
        )
        frames.append(pygame.transform.scale2x(pygame_surface))
    return frames

IMAGENS_CORVO = load_gif(os.path.join('imgs', 'crow.gif'))

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 40)
FONTE_PONTOS_FINAIS = pygame.font.SysFont('arial', 65)

class Passaro:
    IMGS = IMAGENS_CORVO
    ROTACAO_MAXIMA = 5  # Limitar rotação horizontal (próximo de 0º)
    VELOCIDADE_ROTACAO = 2  # Suavizar a velocidade de rotação
    VELOCIDADE_MAXIMA = 10  # Limitar a velocidade de queda
    VELOCIDADE_PULO = -6  # Velocidade de pulo
    GRAVIDADE = 0.8  # Suavizar a gravidade
    TEMPO_ANIMACAO = 5
    TEMPO_INVENCIBILIDADE = 60

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0  # Iniciar sem inclinação
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]
        self.invencivel = False
        self.tempo_invencivel = 0

    def pular(self):
        self.velocidade = self.VELOCIDADE_PULO
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = self.GRAVIDADE * (self.tempo ** 2) + self.velocidade * self.tempo

        # Limitar o deslocamento máximo para que a queda seja suave
        if deslocamento > self.VELOCIDADE_MAXIMA:
            deslocamento = self.VELOCIDADE_MAXIMA
        elif deslocamento < 0:  # Se estiver subindo, deslocamento negativo
            deslocamento -= 2

        self.y += deslocamento

        # Manter a rotação horizontal e suave (perto de 0º)
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA  # Leve inclinação para cima
        else:
            if self.angulo > 0:  # Limitar para manter na horizontal
                self.angulo -= self.VELOCIDADE_ROTACAO

        # Atualizar invencibilidade
        if self.invencivel:
            self.tempo_invencivel -= 1
            if self.tempo_invencivel <= 0:
                self.invencivel = False

    def desenhar(self, tela):
        self.contagem_imagem += 1

        # Animação do pássaro
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Efeito de piscar para invencibilidade
        if self.invencivel and self.tempo_invencivel % 10 < 5:
            return  # Não desenha o pássaro durante o "piscar"

        # Rotação do pássaro
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 300
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 400)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos, vidas):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    if vidas == 3:
        tela.blit(IMAGEM_VIDA3, (10, 10))
    elif vidas == 2:
        tela.blit(IMAGEM_VIDA2, (10, 10))
    elif vidas == 1:
        tela.blit(IMAGEM_VIDA1, (10, 10))

    chao.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    pygame.display.update()

#equipe 4

recorde = 0
class bater:
    def mostrar_recorde(pontos, tela):
        global recorde
        if pontos > recorde:
            recorde = pontos

        tela.blit(IMAGEM_MENOR_RECORDE, (155, 490))
        pontuacao_recorde = FONTE_PONTOS_FINAIS.render(f"{recorde}", 1, (255, 255, 255))
        tela.blit(pontuacao_recorde, (230, 529))

    def exibir_game_over(tela, pontos):
        tela.blit(IMAGEM_VIDA0,(10,10))
        tela.blit(IMAGEM_GAME_OVER, (1, 220))
        tela.blit(IMAGEM_MENOR_PONTUACAO, (150, 350))

        pontuacao = FONTE_PONTOS_FINAIS.render(f"{pontos}", 1, (255, 255, 255))
        tela.blit(pontuacao, (230, 388))

        y = 620
        x = 110
        texto_reiniciar = ['Pressione espaço','para reiniciar']
        for linha in texto_reiniciar:
            texto_reiniciar = FONTE_PONTOS.render(linha, True, (255, 255, 255))
            tela.blit(texto_reiniciar, (x, y))
            y += 40
            x += 30

        pygame.display.update()
        pygame.time.delay(400) 
    
        # Loop para manter a tela de Game Over até que a tecla de espaço seja pressionada 
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE: 
                        main()
                        return

def contagem(seconds, tela):
    while seconds >= 0:
        tela.blit(IMAGEM_BACKGROUND, (0, 0))
        font = pygame.font.SysFont('arial', 74)
        if seconds == 0:
            text = font.render('GO!', True, (255, 255, 255))
        else:
            text = font.render(str(seconds), True, (255, 255, 255))
        tela.blit(text, (TELA_LARGURA // 2 - text.get_width() // 2, TELA_ALTURA // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)
        seconds -= 1
        som_contagem.play()

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(700)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()
    vidas = 3
    musica_de_fundo_do_jogo.play(-1)
 
    rodando = False
    jogo_pausado = False  # Variável para controlar o estado de pausa
    pygame.mixer.music.set_volume(0.5)
     
    #// alteraçôes Grupo 1 
    #imagem de fundo da tela inicial
    imagem_fundo_tela = pygame.image.load('./imgs/background_inicial.png')
    imagem_fundo_tela_re = pygame.transform.scale(imagem_fundo_tela, (TELA_LARGURA, TELA_ALTURA))

    #Adicionando música de fundo
    pygame.mixer.init()

    volume_inicio = 0.1
    musica_de_fundo_do_jogo.set_volume(volume_inicio)
    
    #configuraçôes da barra de progresso
    progresso_barra = 20
    largura_barra = 200
    tela_inicio = True

    while tela_inicio:
        #adicionando tela de fundo
        tela.blit(imagem_fundo_tela_re, (0,0))

      
        #adicionando butao de play
        botao_play_img = pygame.image.load('./imgs/botão_play_.png')
        botao_play_re =pygame.transform.scale(botao_play_img, (150,100))
        botao_play_posicao =botao_play_re.get_rect(center=(250,370))
        tela.blit(botao_play_re, botao_play_posicao)


        #adicionando botão quit
        botao_quit_img = pygame.image.load('./imgs/botão_exit_.png')
        botao_quit_re =pygame.transform.scale(botao_quit_img, (150,100))
        botao_quit_posicao =botao_quit_re.get_rect(center=(250,490))
        tela.blit(botao_quit_re, botao_quit_posicao)

        #definindo botao de aumentar volume
        botao_volume_mais = pygame.image.load('./imgs/botao_volume_positivo.png')
        botao_volume_mais_re = pygame.transform.scale(botao_volume_mais, (50,50))
        botao_volume_mias_posi =botao_volume_mais_re.get_rect(center=(260,700))
        tela.blit(botao_volume_mais_re,botao_volume_mias_posi)

        #definindo botao de diminuir volume
        botao_volume_menos = pygame.image.load('./imgs/botao_volume_negativo.png')
        botao_volume_menos_re = pygame.transform.scale(botao_volume_menos, (50,50))
        botao_volume_menos_posi = botao_volume_menos_re.get_rect(center=(20, 700))
        tela.blit(botao_volume_menos_re, botao_volume_menos_posi)

        # definindo barra de volume
        barra_volume = pygame.draw.rect(tela, (255,255,255), (40,690, largura_barra, 20))
        pygame.draw.rect(tela, (153,204,50), (40,690, progresso_barra, 20))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                tela_inicio = False
                pygame.quit()
                quit()
            #evento de click do botao play
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_play_posicao.collidepoint(evento.pos):
                    musica_de_fundo_do_jogo.stop()
                    tela_inicio = False
                    contagem(3, tela)
                    rodando = True
                    pygame.mixer.music.play(-1)

            #evento de click do botão quit
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_quit_posicao.collidepoint(evento.pos):
                    tela_inicio = False
                    rodando = False
           

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_volume_mias_posi.collidepoint(pygame.mouse.get_pos()):
                    if volume_inicio < 1:
                        volume_inicio += 0.10
                        musica_de_fundo_do_jogo.set_volume(volume_inicio)
                        
                        if progresso_barra < largura_barra:
                            progresso_barra += 20
                            pygame.time.delay(1)

                if botao_volume_menos_posi.collidepoint(pygame.mouse.get_pos()):
                    if volume_inicio > 0:
                        volume_inicio -= 0.10
                        musica_de_fundo_do_jogo.set_volume(volume_inicio)

                        if progresso_barra > 0:      
                            progresso_barra -= 20
                            pygame.time.delay(1)

                        elif progresso_barra == 0:
                            volume_inicio = 0.0


            pygame.display.update()
    
    while rodando:
        relogio.tick(30)       

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not jogo_pausado:
                    for passaro in passaros:
                        passaro.pular()
                        som_pulo.play()
                if evento.key == pygame.K_p:  # Tecla para pausar/despausar
                    jogo_pausado = not jogo_pausado
                    if not jogo_pausado:  # Se despausar, contar 2 segundos
                        contagem(2, tela)

        if jogo_pausado:
            # Exibir a mensagem de "PAUSE"
            font = pygame.font.SysFont('arial', 74)
            text = font.render('PAUSE', True, (255, 255, 255))
            tela.blit(IMAGEM_BACKGROUND, (0, 0))
            tela.blit(text, (TELA_LARGURA // 2 - text.get_width() // 2, TELA_ALTURA // 2 - text.get_height() // 2))
            pygame.display.flip()
            continue  # Não faz nenhuma atualização do jogo enquanto pausado

        for passaro in passaros:
            passaro.mover()
            chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for passaro in passaros:
                if cano.colidir(passaro) and not passaro.invencivel:
                    # Som de colisão e perda de vida
                    som_colisão.play()
                    vidas -= 1
                    if vidas == 0:
                        pygame.mixer.music.stop()
                        som_gameOver.play()
                    passaro.invencivel = True  # Passaro fica invencível
                    passaro.tempo_invencivel = passaro.TEMPO_INVENCIBILIDADE  # Reinicia o tempo de invencibilidade


                if not cano.passou and cano.x < passaro.x:
                    cano.passou = True
                    adicionar_cano = True
                cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

# Alteração Grupo 5
        if adicionar_cano:
            pontos += 5 # A pontuação aumenta de 5 em cinco
            canos.append(Cano(600))
            
            if pontos % 50 == 0:  # Aumenta a velocidade a cada 50 pontos
                Cano.VELOCIDADE += 3 # Velocidade aumentada em 3 a cada 50 pontos dados

        for cano in remover_canos:
            canos.remove(cano)
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                vidas-= 1
                pygame.mixer.music.stop()
                som_gameOver.play()

        if vidas == 0:
            bater.mostrar_recorde(pontos, tela)
            bater.exibir_game_over(tela, pontos)

        desenhar_tela(tela, passaros, canos, chao, pontos, vidas)

if __name__ == '__main__':
    main()

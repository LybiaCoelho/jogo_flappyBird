 #Biblioteca principal utilizada para o desenvolvimento de jogos em Python.
import pygame
import os #Biblioteca que fornece uma maneira de usar funcionalidades dependentes do sistema operacional, 
                #como manipulação de caminhos de arquivo neste caso.
                
import random #Biblioteca utilizada para gerar números aleatórios, 
                 #usada aqui para gerar alturas aleatórias para os canos.
                 
import pygame.mixer #Módulo da biblioteca pygame usado para lidar com reprodução de áudio.

import time #Biblioteca utilizada para operações relacionadas ao tempo, neste caso, 
               #sendo utilizada para pausar a execução do programa.
               
# Definindo as dimensões da tela e a dificuldade inicial
TELA_LARGURA = 500
TELA_ALTURA = 800
DIFICULDADE = 5
# Carregando as imagens e sons necessários
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEM_GAMEOVER = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'gameover.png')))
IMAGEM_LOGO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'logo.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]
# Inicializando a fonte para exibir a pontuação
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

# Inicializando o mixer para reprodução de áudio
pygame.mixer.init()
pygame.mixer.music.load('play/musicfundo.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Função para tocar música de "game over"    
def tocar_musica_game_over():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('play/musicgameover.mp3')
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_volume(0.5)
    
# Definindo a classe do Passaro
class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    
 # Inicializando os atributos do pássaro
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]
        self.visivel = True
 # Método para fazer o pássaro pular
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
# Método para mover o pássaro
    def mover(self):
        self.tempo += 1 # Incrementa o tempo para o cálculo do deslocamento
         # Calcula o deslocamento vertical do pássaro usando uma função quadrática
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
# Limita o deslocamento máximo para evitar movimentos excessivos para baixo
        if deslocamento > 16:
            deslocamento = 16
# Se o deslocamento for negativo, ajusta para uma queda mais rápida           
        elif deslocamento < 0:
            deslocamento -= 2
# Atualiza a posição vertical do pássaro
        self.y += deslocamento
# Ajusta o ângulo de rotação do pássaro com base no deslocamento
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
# Verifica se o pássaro está visível   
        if self.visivel:
# Incrementa a contagem de imagens para a animação do pássaro       
            self.contagem_imagem += 1
# Seleciona a imagem do pássaro com base na contagem de animação
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
# Verifica se o pássaro está em uma posição de mergulho
            if self.angulo <= -80:
                self.imagem = self.IMGS[1]
                self.contagem_imagem = self.TEMPO_ANIMACAO*2
# Rotaciona a imagem do pássaro de acordo com o ângulo
            imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
# Obtém o centro da imagem original para posicionamento adequado após rotação           
            pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
# Obtém o retângulo da imagem rotacionada           
            retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
# Desenha a imagem rotacionada na tela          
            tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
    # Cria e retorna uma máscara de colisão a partir da superfície da imagem do pássaro
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 300  # Distância padrão entre os canos
    VELOCIDADE = 5   # Velocidade de movimento dos canos

    def __init__(self, x, dificuldade):
        
        self.x = x # Posição horizontal do cano
        self.altura = 0 # Altura do cano
        self.pos_topo = 0 # Posição do topo do cano
        self.pos_base = 0 # Posição da base do cano
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)  # Imagem do cano invertida para o topo
        self.CANO_BASE = IMAGEM_CANO # Imagem do cano para a base
        self.passou = False # Indica se o pássaro já passou por este cano
        self.definir_altura(dificuldade) # Inicializa a altura do cano com base na dificuldade

    def definir_altura(self, dificuldade):
# Gera uma altura aleatória entre 50 e 450, ajustada pela dificuldade
        self.altura = random.randrange(50, 450) + (dificuldade * 10)
# Calcula a posição do topo do cano com base na altura e na altura do topo da imagem do cano
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
# Calcula a posição da base do cano com base na altura e na distância padrão entre os canos
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
# Atualiza a posição horizontal do cano subtraindo sua velocidade
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
# Desenha a imagem do topo do cano na posição (x, pos_topo) na tela
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
 # Desenha a imagem da base do cano na posição (x, pos_base) na tela
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
# Obtém a máscara de pixels do passaro
        passaro_mask = passaro.get_mask()
        
# Obtém as máscaras de pixels do topo e da base do cano
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)
        
# Calcula as distâncias entre os pixels do passaro e do topo/base do cano
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
# Verifica se há sobreposição de pixels entre as máscaras do passaro e do topo/base do cano
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
 # Se houver sobreposição de pixels entre o passaro e o topo/base do cano, retorna True (houve colisão)
        if base_ponto or topo_ponto:
            return True
# Se não houver sobreposição, retorna False (não houve colisão)        
        else:
            return False

class Chao:
 # Define a velocidade do chão
    VELOCIDADE = 5
# Obtém a largura da imagem do chão
    LARGURA = IMAGEM_CHAO.get_width()
# Atribui a imagem do chão à variável IMAGEM
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
    # Inicializa a posição vertical do chão
        self.y = y
    # Inicializa as posições horizontais do chão para criar o efeito de movimento
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
    # Move as posições horizontais do chão de acordo com a velocidade
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
     # Verifica se a primeira imagem do chão saiu completamente da tela e a reposiciona
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
     # Verifica se a segunda imagem do chão saiu completamente da tela e a reposiciona
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
     # Desenha as duas imagens do chão em movimento  
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos, game_over, nivel,tela_titulo):
# Desenha o fundo da tela
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
# Verifica se é a tela de título   
    if tela_titulo:
# Desenha o logotipo no centro da tela
        tela.blit(IMAGEM_LOGO, ((TELA_LARGURA - IMAGEM_LOGO.get_width()) // 2, (TELA_ALTURA - IMAGEM_LOGO.get_height()) // 2))
# Atualiza a tela para exibir o logotipo
        pygame.display.update()
# Inicializa o mixer de áudio do pygame
        pygame.mixer.init()
 # Aguarda por 1 segundo para exibir o logotipo
        time.sleep(1)
    
# Loop para desenhar cada passaro na tela, caso esteja visível   
    for passaro in passaros:
        if passaro.visivel:
            passaro.desenhar(tela)
# Loop para desenhar cada cano na tela
    for cano in canos:
        cano.desenhar(tela)
# Verifica se o jogo está no estado de "game over"
    if game_over:
# Se estiver no estado de "game over", exibe a imagem de game over no centro da tela
        tela.blit(IMAGEM_GAMEOVER, ((TELA_LARGURA - IMAGEM_GAMEOVER.get_width()) // 2, (TELA_ALTURA - IMAGEM_GAMEOVER.get_height()) // 2))
    else:
 # Se não estiver no estado de "game over", exibe a pontuação e o nível na tela
        texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
        tela.blit(texto_pontos, (TELA_LARGURA - 10 - texto_pontos.get_width(), 10))
        
        texto_nivel = FONTE_PONTOS.render(f"Nível: {nivel}", 1, (255, 255, 255))
        tela.blit(texto_nivel, (10, 10))
# Desenha o chão na tela
        chao.desenhar(tela)
        
# Atualiza a tela para refletir as mudanças
    pygame.display.update()

def reiniciar_jogo():
 # Cria um objeto da classe Passaro com posição inicial (230, 350)
    passaro = Passaro(230, 350)
# Cria um objeto da classe Chao com posição inicial 730
    chao = Chao(730)
 # Cria um objeto da classe Cano com posição inicial 700 e dificuldade DIFICULDADE
    cano = Cano(700, DIFICULDADE)
 # Retorna uma lista contendo o passaro, chao, uma lista com o cano, pontuação inicial (0) e False indicando que o jogo não está no estado de "game over"
    return [passaro], chao, [cano], 0, False

def main():
# Declaração de uma variável global DIFICULDADE
    global DIFICULDADE
# Inicia a reprodução contínua da música de fundo
    pygame.mixer.music.play(-1)
# Chama a função reiniciar_jogo para obter os elementos iniciais do jogo
    passaros, chao, canos, pontos, game_over = reiniciar_jogo()
# Cria a tela do jogo com as dimensões especificadas 
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
# Inicializa o nível do jogo como 1
    nivel = 1
 # Cria um objeto Clock para controlar a taxa de quadros por segundo (FPS)
    relogio = pygame.time.Clock()
# Define a variável tela_titulo como True, indicando que o jogo está no estado de tela de título
    tela_titulo = True

    rodando = True
    while rodando:
# Limita o loop para rodar a uma taxa de 30 quadros por segundo
        relogio.tick(30)
# Verifica os eventos do pygame
        for evento in pygame.event.get():
# Verifica se o evento é do tipo QUIT (fechar a janela)
        
             if evento.type == pygame.QUIT:
# Define a variável 'rodando' como False para encerrar o loop                 
                rodando = False
                pygame.quit() # Encerra o pygame
                quit() # Encerra o programa
             elif evento.type == pygame.KEYDOWN:
# Verifica se a tecla pressionada é a tecla de espaço
                if game_over and evento.key == pygame.K_SPACE:
# Se o jogo terminou e a tecla de espaço foi pressionada,
# # interrompe a música atual
                    pygame.mixer.music.stop()
# Carrega a música de fundo novamente                   
                    pygame.mixer.music.load('play/musicfundo.mp3')
# Inicia a reprodução da música de fundo em um loop infinito
                    pygame.mixer.music.play(-1)
 # Reinicia o jogo obtendo novas instâncias de passaro, chao, canos e zerando os pontos e a flag de game_over
                    passaros, chao, canos, pontos, game_over = reiniciar_jogo()

                    nivel = 1  # Reinicia o nível ao reiniciar o jogo
# Reinicia o nível ao reiniciar o jogo
                    tela_titulo = True

                elif not game_over and evento.key == pygame.K_SPACE:
# Verifica se o jogo não terminou e a tecla de espaço foi pressionada
                    for passaro in passaros:
# Para cada passaro na lista de passaros
                        passaro.pular()  # Chama o método pular() do passaro, fazendo-o pular
# Define a variável tela_titulo como False, indicando que o título do jogo não deve ser exibido
                        tela_titulo = False

# Verifica se o jogo não terminou
        if not game_over:
# Para cada passaro na lista de passaros
            for passaro in passaros:
# Chama o método mover() do passaro, movendo-o
                passaro.mover()
# Chama o método mover() do chao, movendo-o
            chao.mover()

        adicionar_cano = False # Variável que indica se deve ser adicionado um novo cano
        remover_canos = [] # Lista para armazenar canos que devem ser removidos
# Itera sobre a lista de canos
        for cano in canos:
# Itera sobre a lista de passaros usando enumerate para obter índice e valor
            for i, passaro in enumerate(passaros):
# Verifica se há colisão entre o cano e o passaro
                if cano.colidir(passaro):
                    game_over = True # Define o estado do jogo como game over
                    passaro.visivel = False # Torna o passaro invisível
                    tocar_musica_game_over() # Toca a música de game over
 # Verifica se o passaro ultrapassou o cano
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True # Marca que o passaro passou pelo cano
                    adicionar_cano = True # Indica que um novo cano deve ser adicionado
            cano.mover() # Move o cano
# Verifica se o cano saiu da tela
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano) # Adiciona o cano à lista de remoção

        if adicionar_cano: # Verifica se um novo cano deve ser adicionado
            pontos += 1 # Incrementa a pontuação
            if pontos % 5 == 0: # Verifica se a pontuação é um múltiplo de 5
                nivel += 1  # Aumenta o nível a cada 5 pontos
            canos.append(Cano(600, DIFICULDADE))  # Adiciona um novo cano à lista de canos

        for i, passaro in enumerate(passaros): # Loop sobre os pássaros na lista
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
# Verifica se a parte inferior ou superior do pássaro ultrapassou os limites
                game_over = True # Define a variável game_over como True
                passaro.visivel = False # Torna o pássaro invisível
                tocar_musica_game_over()  # Chama a função para tocar a música de game over

# Chama a função desenhar_tela para renderizar a tela do jogo com os parâmetros necessários
        desenhar_tela(tela, passaros, canos, chao, pontos, game_over, nivel,tela_titulo)
# Verifica se o script está sendo executado como o programa principal
if __name__ == '__main__':
# Chama a função main() para iniciar o loop principal do jogo e executar a lógica do jogo
    main()
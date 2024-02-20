import pygame
import os
import random
import pygame.mixer

# Restante do código...

pygame.mixer.init()
pygame.mixer.music.load('play/musicfundo.mp3')
pygame.mixer.music.set_volume(0.5)

def main():
    pygame.mixer.music.play(-1)  # -1 faz a música de fundo repetir indefinidamente

    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    game_over = False
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if game_over and evento.key == pygame.K_SPACE:
                    # Reiniciar o jogo
                    pygame.mixer.music.stop()  # Pára a música de fundo quando o jogo termina
                    pygame.mixer.music.play(-1)  # Reinicia a música de fundo
                    for passaro in passaros:
                        passaro.visivel = True
                    passaros = [Passaro(230, 350)]
                    chao = Chao(730)
                    canos = [Cano(700)]
                    pontos = 0
                    game_over = False
                elif not game_over and evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # Restante do código...

        if game_over:
            pygame.mixer.music.stop()  # Pára a música de fundo quando o jogo termina
            pygame.mixer.music.load('play/musicgameover.mp3')
            pygame.mixer.music.play(0)  # O argumento 0 faz a música de game over tocar uma vez
            pygame.mixer.music.set_volume(0.5)       

        desenhar_tela(tela, passaros, canos, chao, pontos, game_over)

if __name__ == '__main__':
    main()
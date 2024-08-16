import pygame
import random
import sys

# Iniciando o pygame
pygame.init()

# Configurações da tela
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird")

# Cores
green = (0, 255, 0)
dark_green = (0, 200, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

# Carregando as imagens
bird_image = pygame.image.load('Flappy.png')
bird_image = pygame.transform.scale(bird_image, (50, 30))  # Ajuste o tamanho se necessário

sky_background = pygame.image.load('sky_image.png')
sky_background = pygame.transform.scale(sky_background, (screen_width, screen_height))

congratsback = pygame.image.load('congratsback.png')  # Imagem de fundo para a tela de comemoração
congratsback = pygame.transform.scale(congratsback, (screen_width, screen_height))

bird_width = bird_image.get_width()
bird_height = bird_image.get_height()
bird_x = 50
bird_y = 300
bird_y_change = 0
gravity = 0.7  # Gravidade que faz o pássaro cair

# Configurações dos canos
pipe_width = 70
pipe_height = random.randint(150, 450)
pipe_x = 400
pipe_x_change = -4
gap = 200
pipe_count = 0  # Contador de canos passados

# Função para desenhar o passarinho
def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

# Função para desenhar os canos
def draw_pipes(pipe_x, pipe_height, gap):
    # Desenha o cano superior
    pygame.draw.rect(screen, green, [pipe_x, 0, pipe_width, pipe_height])
    pygame.draw.rect(screen, dark_green, [pipe_x + 5, 0, pipe_width - 10, pipe_height])  # Efeito de borda

    # Desenhar o cano inferior
    pygame.draw.rect(screen, green, [pipe_x, pipe_height + gap, pipe_width, screen_height - pipe_height - gap])
    pygame.draw.rect(screen, dark_green, [pipe_x + 5, pipe_height + gap, pipe_width - 10, screen_height - pipe_height - gap])  # Efeito de borda

# Função para desenhar o botão de start
def draw_start_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, white)
    button_rect = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
    pygame.draw.rect(screen, blue, button_rect)
    screen.blit(text, (button_rect.x + 20, button_rect.y + 10))
    return button_rect

# Função para desenhar a linha de chegada
def draw_finish_line():
    pygame.draw.rect(screen, blue, [pipe_x, 0, pipe_width, screen_height])

# Função para mostrar mensagem de parabéns
def show_congratulations():
    screen.blit(congratsback, (0, 0))  # Desenha o fundo
    font = pygame.font.Font(None, 48)
    text = font.render("Congratulations!", True, blue)
    screen.blit(text, (screen_width // 2 - 150, screen_height // 2 - 25))
    pygame.display.update()
    pygame.time.wait(2500)  # Aguarde 2.5 segundos antes de fechar
    pygame.quit()
    sys.exit()

# Função para mostrar a contagem regressiva
def countdown(seconds):
    font = pygame.font.Font(None, 48)
    for i in range(seconds, 0, -1):
        screen.blit(sky_background, (0, 0))  # Usa a mesma imagem de fundo do céu
        text = font.render(str(i), True, black)
        screen.blit(text, (screen_width // 2 - 10, screen_height // 2 - 25))
        pygame.display.update()
        pygame.time.wait(1000) 

# Função para mostrar a tela de game over
def show_game_over():
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, blue)
    screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 25))
    pygame.display.update()
    pygame.time.wait(3000) 
    pygame.quit()
    sys.exit()

# Loop principal do jogo
def game_loop():
    global bird_y, bird_y_change, pipe_x, pipe_height, pipe_count

    # Controle do jogo
    game_over = False
    game_started = False
    clock = pygame.time.Clock()

    while not game_over:
        screen.blit(sky_background, (0, 0))

        if not game_started:
            start_button = draw_start_button()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        countdown(3)  # Inicia a contagem de 3 segundos
                        game_started = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_y_change = -18  # O quanto o pássaro sobe ao pressionar a barra de espaço
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        bird_y_change = 0  # Para de subir quando solta a barra de espaço

            # Gravidade
            bird_y_change += gravity
            bird_y += bird_y_change

            # Movimento dos canos
            pipe_x += pipe_x_change

            # Verificar se o cano saiu da tela
            if pipe_x < -pipe_width:
                pipe_x = screen_width
                pipe_height = random.randint(150, 450)
                pipe_count += 1  # Incrementa o contador de canos passados

            
            draw_bird(bird_x, bird_y)
            if pipe_count < 10:
                draw_pipes(pipe_x, pipe_height, gap)
            else:
                draw_finish_line()

            # O jogador chegou à linha de chegada
            if pipe_count == 10 and pipe_x < bird_x + bird_width:
                show_congratulations()

            # Colisões
            if bird_y < 0 or bird_y > screen_height - bird_height:
                show_game_over()
            if (pipe_x < bird_x + bird_width and pipe_x + pipe_width > bird_x):
                if pipe_count < 10 and (bird_y < pipe_height or bird_y + bird_height > pipe_height + gap):
                    show_game_over()

            pygame.display.update()
            clock.tick(60)

    pygame.quit()
    sys.exit()

game_loop()

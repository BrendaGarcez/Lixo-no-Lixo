import pygame

pygame.init()

# Configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Créditos com Barra de Rolagem Bonita")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_ESCURO = (50, 50, 50)
AZUL = (70, 130, 180)

# Fonte e texto
fonte = pygame.font.Font(None, 36)
creditos_texto = [
    "Créditos:",
    "Programador: João Silva",
    "Designer: Maria Oliveira",
    "Músicas: Pedro Santos",
    "Testadores: Ana, Bruno, Carla",
    "Agradecimentos especiais:",
    "   - Comunidade Pygame",
    "   - Família e Amigos",
    "",
    "Feito com ❤️ usando Python e Pygame",
]
linha_altura = 50  # Espaçamento entre linhas

# Superfície maior para os créditos
altura_creditos = len(creditos_texto) * linha_altura
creditos_surface = pygame.Surface((largura_tela, altura_creditos))

# Variáveis de rolagem
scroll_y = 0
scroll_velocidade = 5

# Dimensões da barra de rolagem
barra_largura = 15
barra_x = largura_tela - barra_largura - 10  # Margem direita
barra_altura = altura_tela * (altura_tela / altura_creditos)  # Altura proporcional
barra_y = 0  # Posição inicial da barra

# Trilho da barra
trilho_x = barra_x
trilho_largura = barra_largura
trilho_altura = altura_tela

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Controle da rolagem com o mouse ou teclado
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:  # Rolagem para cima
                scroll_y = max(scroll_y - scroll_velocidade, 0)
            elif evento.button == 5:  # Rolagem para baixo
                scroll_y = min(scroll_y + scroll_velocidade, altura_creditos - altura_tela)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:  # Tecla para cima
                scroll_y = max(scroll_y - scroll_velocidade, 0)
            elif evento.key == pygame.K_DOWN:  # Tecla para baixo
                scroll_y = min(scroll_y + scroll_velocidade, altura_creditos - altura_tela)

    # Preencher a superfície dos créditos
    creditos_surface.fill(PRETO)
    for i, linha in enumerate(creditos_texto):
        texto = fonte.render(linha, True, BRANCO)
        creditos_surface.blit(texto, (50, i * linha_altura))

    # Atualizar a posição da barra de rolagem
    barra_y = (scroll_y / altura_creditos) * altura_tela

    # Renderizar a tela principal
    tela.fill(CINZA_ESCURO)  # Cor de fundo
    tela.blit(creditos_surface, (0, -scroll_y))  # Deslocar o conteúdo

    # Desenhar o trilho da barra de rolagem
    pygame.draw.rect(tela, PRETO, (trilho_x, 0, trilho_largura, trilho_altura))

    # Desenhar a barra de rolagem (com bordas arredondadas)
    pygame.draw.rect(tela, AZUL, (barra_x, barra_y, barra_largura, barra_altura), border_radius=8)

    pygame.display.flip()

pygame.quit()

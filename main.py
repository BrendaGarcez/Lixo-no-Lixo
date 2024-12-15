import pygame  # Importando biblioteca
import botao  # Importando a classe Botao

pygame.init()  # Inicializa os módulos do pygame

# Resolução da tela
telaLargura = 1100
telaAltura = 720
tela = pygame.display.set_mode((telaLargura, telaAltura))  # Configuração da tela
pygame.display.set_caption("Lixo_No_Lixo")  # Nome do jogo

# Estado do jogo
estadoJogo = "menu"  # situação atual do jogo, para rastrear as telas
rodando = True  # Controla se o programa deve continuar rodando

# Função para criar botões
def criarBotao(x, y, imagem, imagemAlterada):
    imagem = pygame.image.load(imagem).convert_alpha()
    imagemAlterada = pygame.image.load(imagemAlterada).convert_alpha()
    return botao.Botao(x, y, imagem, imagemAlterada)

# Função para as fases
def iniciarFases():
    global estadoJogo
    fasesBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")
    tela.blit(fasesBackground,(0,0))

    # Criando botões para as fases
    fase1Botao = criarBotao(80, 200, "imagens/GUI/botaoFases/botaoZoo0.png", "imagens/GUI/botaoFases/botaoZoo1.png")
    fase2Botao = criarBotao(580, 200, "imagens/GUI/botaoFases/botaoSala0.png", "imagens/GUI/botaoFases/botaoSala1.png")
    fase3Botao = criarBotao(400, 450, "imagens/GUI/botaoFases/botaoPraia0.png", "imagens/GUI/botaoFases/botaoPraia1.png")
    voltarBotao = criarBotao(100, 600, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    run = True
    while run:
        tela.blit(fasesBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()#arrumar para clique e não quando le está precionado

        # Atualizar e desenhar botões
        fase1Botao.atualizarImagem(posicaoMouse)
        fase2Botao.atualizarImagem(posicaoMouse)
        fase3Botao.atualizarImagem(posicaoMouse)
        voltarBotao.atualizarImagem(posicaoMouse)

        fase1Botao.desenharBotao(tela)
        fase2Botao.desenharBotao(tela)
        fase3Botao.desenharBotao(tela)
        voltarBotao.desenharBotao(tela)

        # Verificar cliques
        if fase1Botao.clicarBotao(tela):
            print("Fase 1 selecionada")
            estadoJogo = "fase1"
            run = False
        if fase2Botao.clicarBotao(tela):
            print("Fase 2 selecionada")
            estadoJogo = "fase2"
            run = False
        if fase3Botao.clicarBotao(tela):
            print("Fase 3 selecionada")
            estadoJogo = "fase3"
            run = False
        if voltarBotao.clicarBotao(tela):
            print("Voltar clicado")
            estadoJogo = "menu"
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

        pygame.display.update()

# Função para o menu principal
def menuPrincipal():
    global estadoJogo
    menuBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")

    # Criando botões do menu
    jogarBotao = criarBotao(295, 130, "imagens/GUI/botaoJogar/jogar0.png", "imagens/GUI/botaoJogar/jogar1.png")
    sairBotao = criarBotao(390, 370, "imagens/GUI/botaoSair/sair0.png", "imagens/GUI/botaoSair/sair1.png")

    run = True
    while run:
        tela.blit(menuBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        # Atualizar e desenhar botões
        jogarBotao.atualizarImagem(posicaoMouse)
        sairBotao.atualizarImagem(posicaoMouse)

        jogarBotao.desenharBotao(tela)
        sairBotao.desenharBotao(tela)

        # Verificar cliques
        if jogarBotao.clicarBotao(tela):
            print("Jogar clicado")
            estadoJogo = "jogando"
            run = False
        if sairBotao.clicarBotao(tela):
            print("Sair clicado")
            global rodando
            rodando = False
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                run = False

        pygame.display.update()

# Loop principal do jogo
while rodando:
    if estadoJogo == "menu":
        menuPrincipal()
    elif estadoJogo == "jogando":
        iniciarFases()
    elif estadoJogo == "fase1":
        menuPrincipal()
    elif estadoJogo == "fase2":
        menuPrincipal()
    elif estadoJogo == "fase3":
        iniciarFases()

# Finaliza o pygame
pygame.quit()

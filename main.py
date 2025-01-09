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

def abrirConfiguracoes():

    global estadoJogo
    configuracoesBackground = pygame.image.load("imagens/GUI/Backgrounds/configuracoesBackground.jpg")
    tela.blit(configuracoesBackground, (0, 0))
    somAtivo = True  # Estado inicial do som (ligado)
    volume = 0.5

    somLigadoBotao = criarBotao(400, 200, "imagens/GUI/botaoSom/ligado0.png", "imagens/GUI/botaoSom/ligado1.png")
    somDesligadoBotao = criarBotao(400, 200, "imagens/GUI/botaoSom/desligado0.png", "imagens/GUI/botaoSom/desligado1.png")
    aumentarVolumeBotao = criarBotao(400, 300, "imagens/GUI/botaoSom/aumentar0.png", "imagens/GUI/botaoSom/aumentar1.png")
    diminuirVolumeBotao = criarBotao(400, 400, "imagens/GUI/botaoSom/diminuir0.png", "imagens/GUI/botaoSom/diminuir1.png")
    # Criar botão de voltar
    voltarBotao = criarBotao(100, 600, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    run = True
    while run:
        tela.blit(configuracoesBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        # Atualizar e desenhar botões
        if somAtivo:
            somLigadoBotao.atualizarImagem(posicaoMouse)
            somLigadoBotao.desenharBotao(tela)
        else:
            somDesligadoBotao.atualizarImagem(posicaoMouse)
            somDesligadoBotao.desenharBotao(tela)

        aumentarVolumeBotao.atualizarImagem(posicaoMouse)
        diminuirVolumeBotao.atualizarImagem(posicaoMouse)
        voltarBotao.atualizarImagem(posicaoMouse)

        aumentarVolumeBotao.desenharBotao(tela)
        diminuirVolumeBotao.desenharBotao(tela)
        voltarBotao.desenharBotao(tela)

        # Exibir nível de volume na tela
        fonte = pygame.font.Font(None, 36)
        textoVolume = fonte.render(f"Volume: {int(volume * 100)}%", True, (255, 255, 255))
        tela.blit(textoVolume, (500, 500))

        # Verificar cliques nos botões
        if somAtivo and somLigadoBotao.clicarBotao(tela):
            print("Som desligado")
            somAtivo = False
            pygame.mixer.music.pause()  # Pausa a música
        elif not somAtivo and somDesligadoBotao.clicarBotao(tela):
            print("Som ligado")
            somAtivo = True
            pygame.mixer.music.unpause()  # Retoma a música

        if aumentarVolumeBotao.clicarBotao(tela):
            if volume < 1.0:
                volume += 0.1
                volume = round(volume, 1)  # Limita o volume em 1 casa decimal
                pygame.mixer.music.set_volume(volume)
                print(f"Aumentando volume para {int(volume * 100)}%")

        if diminuirVolumeBotao.clicarBotao(tela):
            if volume > 0.0:
                volume -= 0.1
                volume = round(volume, 1)
                pygame.mixer.music.set_volume(volume)
                print(f"Diminuindo volume para {int(volume * 100)}%")

        if voltarBotao.clicarBotao(tela):
            print("Voltando ao menu principal")
            estadoJogo = "menu"
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

        pygame.display.update()

def abrirCreditos():
    global estadoJogo
    creditosBackground = pygame.image.load("imagens/GUI/Backgrounds/creditos.jpg")
    voltarBotao = criarBotao(40, 50, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    linhas_creditos = [
            "                             Desenvolvido por:   ",
            "Brenda Amanda da Silva Garcez",
            "Nicole Louise Matias Jamuchewski",
            "João Rafael Modreira Anhaia",
            "Ilustrações por:",
            "Maria Souza",
            "Lucas Santos",
            "                             Obrigado por jogar!",
        ]

    fonte = pygame.font.Font(None, 40)  # Fonte para os textos
    cor_texto = (255, 255, 255)         # Cor do texto
    espacamento = 50                    # Espaçamento entre linhas

    largura_quadro = 700                # Largura do quadrado marrom
    altura_quadro = 350                 # Altura do quadrado marrom
    posicao_quadro = (200, 220)         # Posição do quadrado marrom
    
    # Altura total do conteúdo
    altura_conteudo = len(linhas_creditos) * espacamento
    deslocamento = 0  # Controla a rolagem do conteúdo

    run = True
    while run:
        tela.blit(creditosBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        voltarBotao.desenharBotao(tela)

         # Desenhar os textos dentro do quadrado marrom com rolagem
        superficie_creditos = pygame.Surface((largura_quadro, altura_conteudo), pygame.SRCALPHA)
        superficie_creditos.fill((131, 69, 31))  # Cor de fundo do quadrado

        for i, linha in enumerate(linhas_creditos):
            texto = fonte.render(linha, True, cor_texto)
            superficie_creditos.blit(texto, (20, i * espacamento))
        
        recorte = superficie_creditos.subsurface((0, deslocamento, largura_quadro, altura_quadro))
        tela.blit(recorte, posicao_quadro)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Rolar para cima
                    deslocamento = max(deslocamento - 20, 0)
                elif event.button == 5:  # Rolar para baixo
                    deslocamento = min(deslocamento + 20, altura_conteudo - altura_quadro)

        if voltarBotao.clicarBotao(tela):
            print("Voltando ao menu principal")
            estadoJogo = "menu"
            run = False

        pygame.display.update()

# Função para as fases
def iniciarFases():
    global estadoJogo
    fasesBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")
    tela.blit(fasesBackground,(0,0))

    # Criando botões para as fases
    fase1Botao = criarBotao(80, 200, "imagens/GUI/botaoFases/botaoZoo0.png", "imagens/GUI/botaoFases/botaoZoo1.png")
    fase2Botao = criarBotao(580, 200, "imagens/GUI/botaoFases/botaoSala0.png", "imagens/GUI/botaoFases/botaoSala1.png")
    fase3Botao = criarBotao(400, 450, "imagens/GUI/botaoFases/botaoPraia0.png", "imagens/GUI/botaoFases/botaoPraia1.png")
    voltarBotao = criarBotao(100, 620, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

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

def fase1():
    global estadoJogo
    fase1Background = pygame.image.load("imagens/fase1/imagemZoologico.jpg")

    voltarBotao = criarBotao(40, 50, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(900, 130, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    
    run = True
    while run:
        tela.blit(fase1Background, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        
        if voltarBotao.clicarBotao(tela):
            print("Voltar clicado")
            estadoJogo = "jogando"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            print("Configurações clicado")
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

        # Atualiza a tela
        pygame.display.update()

def fase2():
    global estadoJogo
    fase1Background = pygame.image.load("imagens/fase2/imagemSaladeAula.jpg")

    voltarBotao = criarBotao(40, 50, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(900, 130, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")

    run = True
    while run:
        tela.blit(fase1Background, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        
        if voltarBotao.clicarBotao(tela):
            print("Voltar clicado")
            estadoJogo = "jogando"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            print("Configurações clicado")
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

        # Atualiza a tela
        pygame.display.update()

def fase3():
    global estadoJogo
    fase1Background = pygame.image.load("imagens/fase3/imagemPraia.jpg")

    voltarBotao = criarBotao(40, 50, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(900, 130, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")

    run = True
    while run:
        tela.blit(fase1Background, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        
        if voltarBotao.clicarBotao(tela):
            print("Voltar clicado")
            estadoJogo = "jogando"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            print("Configurações clicado")
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

        # Atualiza a tela
        pygame.display.update()

# Função para o menu principal
def menuPrincipal():
    global estadoJogo
    menuBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")

    # Criando botões do menu
    jogarBotao = criarBotao(295, 130, "imagens/GUI/botaoJogar/jogar0.png", "imagens/GUI/botaoJogar/jogar1.png")
    configuracoesBotao = criarBotao(900, 625, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    sairBotao = criarBotao(390, 370, "imagens/GUI/botaoSair/sair0.png", "imagens/GUI/botaoSair/sair1.png")
    creditosBotao = criarBotao(820, 620, "imagens/GUI/botaoConfiguracoes/info0.png", "imagens/GUI/botaoConfiguracoes/info1.png")  

    run = True
    while run:
        tela.blit(menuBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        # Atualizar e desenhar botões
        jogarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)
        sairBotao.atualizarImagem(posicaoMouse)
        creditosBotao.atualizarImagem(posicaoMouse)

        jogarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        sairBotao.desenharBotao(tela)
        creditosBotao.desenharBotao(tela)

        # Verificar cliques
        if jogarBotao.clicarBotao(tela):
            print("Jogar clicado")
            estadoJogo = "jogando"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            print("Configurações clicado")
            abrirConfiguracoes()
        if creditosBotao.clicarBotao(tela):  # Detecta clique no botão de créditos
            print("Créditos clicado")
            abrirCreditos()

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
        fase1()
    elif estadoJogo == "fase2":
        fase2()
    elif estadoJogo == "fase3":
        fase3()

# Finaliza o pygame
pygame.quit()

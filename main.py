import pygame  # Importando biblioteca
import botao  # Importando a classe Botao
import botaoObjetos
import image
import random
import math
import time

pygame.init()  # Inicializa os módulos do pygame
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Muda o cursor para a mão
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

def criarBotaoImagens(x, y, imagem, imagemAlterada):
    imagem = pygame.image.load(imagem).convert_alpha()
    imagemAlterada = pygame.image.load(imagemAlterada).convert_alpha()
    
    # Redimensionar as imagens
    largura, altura = 200, 120  # Exemplo de tamanho, ajuste conforme necessário
    imagem = pygame.transform.scale(imagem, (largura, altura))
    imagemAlterada = pygame.transform.scale(imagemAlterada, (largura, altura))
    
    return botaoObjetos.BotaoObjetos(x, y, imagem, imagemAlterada)

import pygame

def abrirConfiguracoes():
    pygame.mixer.init()
    pygame.mixer.music.load("sons/musicafundo.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Música toca em loop

    som_click = pygame.mixer.Sound("sons/mouseclick.wav")
    som_click.set_volume(0.7)

    configuracoesBackground = pygame.image.load("imagens/GUI/Backgrounds/configuracoesBackground.jpg")
    tela.blit(configuracoesBackground, (0, 0))
    somAtivo = True  # Estado inicial do som
    volume = 0.5

    somLigadoBotao = criarBotao(510, 200, "imagens/GUI/botaoSom/ligado0.png", "imagens/GUI/botaoSom/ligado1.png")
    somDesligadoBotao = criarBotao(510, 200, "imagens/GUI/botaoSom/desligado0.png", "imagens/GUI/botaoSom/desligado1.png")
    voltarBotao = criarBotao(20, 650, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    run = True
    while run:
        tela.blit(configuracoesBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()
        cliqueMouse = pygame.mouse.get_pressed()

        # Atualizar e desenhar botões
        if somAtivo:
            somLigadoBotao.atualizarImagem(posicaoMouse)
            somLigadoBotao.desenharBotao(tela)
        else:
            somDesligadoBotao.atualizarImagem(posicaoMouse)
            somDesligadoBotao.desenharBotao(tela)

        voltarBotao.atualizarImagem(posicaoMouse)
        voltarBotao.desenharBotao(tela)

        # Barra de volume
        barra_x, barra_y = 400, 300
        barra_largura, barra_altura = 300, 10
        pygame.draw.rect(tela, (100, 100, 100), (barra_x, barra_y, barra_largura, barra_altura))  # Fundo da barra
        pygame.draw.rect(tela, (139, 69, 19), (barra_x, barra_y, int(volume * barra_largura), barra_altura))  # Barra de volume
        pygame.draw.circle(tela, (139, 50, 17), (barra_x + int(volume * barra_largura), barra_y + barra_altura // 2), 10)  # Indicador do volume

        if cliqueMouse[0] and barra_x <= posicaoMouse[0] <= barra_x + barra_largura and barra_y - 10 <= posicaoMouse[1] <= barra_y + barra_altura + 10:
            volume = (posicaoMouse[0] - barra_x) / barra_largura
            volume = max(0, min(volume, 1))
            pygame.mixer.music.set_volume(volume)

        # Texto do volume
        fonte = pygame.font.Font(None, 36)
        texto_volume = f"Volume: {int(volume * 100)}%"
        texto_renderizado = fonte.render(texto_volume, True, (255, 255, 255))
        tela.blit(texto_renderizado, (barra_x + barra_largura + 20, barra_y - 10))

        # Verificar cliques
        if somAtivo and somLigadoBotao.clicarBotao(tela):
            somAtivo = False
            pygame.mixer.music.pause()
            som_click.play()  # Som de clique
        elif not somAtivo and somDesligadoBotao.clicarBotao(tela):
            somAtivo = True
            pygame.mixer.music.unpause()
            som_click.play()  # Som de clique

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

        pygame.display.update()




def abrirInstrucoes():
    global estadoJogo
    instrucoesBackground = pygame.image.load("imagens/GUI/Backgrounds/instrucoesBackground.jpg")
    voltarBotao = criarBotao(40, 50, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(900, 50, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    fase1Botao = criarBotao(20, 250, "imagens/fase1/faseBotao1.png", "imagens/fase1/faseBotao1.png")
    fase2Botao = criarBotao(20, 370, "imagens/fase2/faseBotao2.png", "imagens/fase2/faseBotao2.png")
    fase3Botao = criarBotao(20, 490, "imagens/fase3/faseBotao3.png", "imagens/fase3/faseBotao3.png")

    instrucoes_texto = [
        "",
        "Bem-vindo ao jogo!",
        "",
        "Instruções:",
        "- Utilize as setas do teclado para movimentar o personagem.",
        "- Colete os itens correspondentes para marcar pontos.",
        "- Evite os obstáculos para não perder vidas.",
        "- Use o botão de 'Pause' para pausar o jogo.",
        "",
        "Boa sorte e divirta-se!",
    ]

    fonte = pygame.font.Font("sons/tipografia/LuckiestGuy-Regular.ttf", 20)
    cor_texto = (255, 255, 255)
    espacamento = 40

    largura_quadro = 670
    altura_quadro = 480
    posicao_quadro = (330, 180)

    altura_conteudo = len(instrucoes_texto) * espacamento
    deslocamento = 0  # Posição inicial
    clicando_na_barra = False

    barra_largura = 15
    barra_altura = max(30, altura_quadro * (altura_quadro / max(altura_conteudo, altura_quadro)))
    barra_x = posicao_quadro[0] + largura_quadro - barra_largura - 5

    run = True
    while run:
        tela.blit(instrucoesBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        voltarBotao.desenharBotao(tela)

        configuracoesBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.desenharBotao(tela)

        fase1Botao.atualizarImagem(posicaoMouse)
        fase1Botao.desenharBotao(tela)
        fase2Botao.atualizarImagem(posicaoMouse)
        fase2Botao.desenharBotao(tela)
        fase3Botao.atualizarImagem(posicaoMouse)
        fase3Botao.desenharBotao(tela)

        # Superfície para instruções
        superficie_instrucoes = pygame.Surface((largura_quadro, max(altura_conteudo, altura_quadro)), pygame.SRCALPHA)
        superficie_instrucoes.fill((131, 69, 31))  # Fundo do quadro

        # Renderizar o texto com contorno
        for i, linha in enumerate(instrucoes_texto):
            texto_contorno = fonte.render(linha, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento = fonte.render(linha, True, cor_texto)  # Texto branco
            x, y = 20, i * espacamento
            # Desenhar contorno
            superficie_instrucoes.blit(texto_contorno, (x - 1, y))
            superficie_instrucoes.blit(texto_contorno, (x + 1, y))
            superficie_instrucoes.blit(texto_contorno, (x, y - 1))
            superficie_instrucoes.blit(texto_contorno, (x, y + 1))
            # Desenhar texto principal
            superficie_instrucoes.blit(texto_preenchimento, (x, y))

        # Garantir que o deslocamento esteja dentro dos limites
        deslocamento = max(0, min(deslocamento, altura_conteudo - altura_quadro))

        # Recorte da parte visível
        recorte = superficie_instrucoes.subsurface((0, deslocamento, largura_quadro, altura_quadro))
        tela.blit(recorte, posicao_quadro)

        # Barra de rolagem
        trilho_x = barra_x
        trilho_altura = altura_quadro
        pygame.draw.rect(tela, (50, 50, 50), (trilho_x, posicao_quadro[1], barra_largura, trilho_altura))  # Trilho
        barra_y = posicao_quadro[1] + (deslocamento / max(altura_conteudo, 1)) * altura_quadro
        pygame.draw.rect(tela, (70, 130, 180), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)  # Barra

        # Verificar cliques nos botões
        if voltarBotao.clicarBotao(tela):
            print("Voltando ao menu principal")
            estadoJogo = "menu"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            print("Configurações clicado")
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    if trilho_x <= posicaoMouse[0] <= trilho_x + barra_largura and barra_y <= posicaoMouse[1] <= barra_y + barra_altura:
                        clicando_na_barra = True

                elif event.button == 4:  # Rolar para cima
                    deslocamento = max(deslocamento - 20, 0)
                elif event.button == 5:  # Rolar para baixo
                    deslocamento = min(deslocamento + 20, altura_conteudo - altura_quadro)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicando_na_barra = False

            elif event.type == pygame.MOUSEMOTION:
                if clicando_na_barra:
                    deslocamento = max(0, min(altura_conteudo - altura_quadro,
                                              (event.pos[1] - posicao_quadro[1]) * (altura_conteudo / altura_quadro)))

        pygame.display.update()



def abrirCreditos():
    global estadoJogo
    creditosBackground = pygame.image.load("imagens/GUI/Backgrounds/creditos.jpg")
    voltarBotao = criarBotao(20, 650, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    linhas_creditos = [
        "                                  Desenvolvido por:   ",
        "- Brenda Amanda da Silva Garcez",
        "- João Rafael Moreira Anhaia",
        "- Matheus Vinícius dos Santos Sachinski",
        "- Nicole Louise Matias Jamuchewski",
        "- Pedro Victor A. M. L. Maciel",

        "                                   Ilustrações por:",
        "- Nomes",
        "                                         Fontes por:",
        "- 'Luckiest' Guy por Astigmatic (Google Fonts)",
        "                             Obrigado por jogar!",
    ]

    fonte = pygame.font.Font("sons/tipografia/LuckiestGuy-Regular.ttf", 26)  # 40 é o tamanho da fonte
    cor_texto = (255, 255, 255)  # Cor do texto
    espacamento = 50  # Espaçamento entre linhas

    largura_quadro = 700  # Largura do quadrado marrom
    altura_quadro = 350  # Altura do quadrado marrom
    posicao_quadro = (200, 220)  # Posição do quadrado marrom

    configuracoesBotao = criarBotao(930, 50, "imagens/GUI/botaoConfiguracoes/configuracoes0.png",
                                    "imagens/GUI/botaoConfiguracoes/configuracoes1.png")

    # Altura total do conteúdo
    altura_conteudo = len(linhas_creditos) * espacamento
    deslocamento = 0  # Controla a rolagem do conteúdo

    barra_largura = 15
    barra_altura = max(30, altura_quadro * (altura_quadro / altura_conteudo))  # Altura proporcional mínima
    barra_x = posicao_quadro[0] + largura_quadro - barra_largura - 5  # Margem lateral direita do quadro
    barra_y = posicao_quadro[1]  # Posição inicial da barra
    trilho_x = barra_x
    trilho_altura = altura_quadro

    clicando_na_barra = False

    run = True
    while run:
        tela.blit(creditosBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        configuracoesBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.desenharBotao(tela)
        voltarBotao.atualizarImagem(posicaoMouse)
        voltarBotao.desenharBotao(tela)

        # Desenhar os textos dentro do quadrado marrom com rolagem
        superficie_creditos = pygame.Surface((largura_quadro, altura_conteudo), pygame.SRCALPHA)
        superficie_creditos.fill((131, 69, 31))  # Cor de fundo do quadrado

        for i, linha in enumerate(linhas_creditos):
            # Renderizar o texto de contorno
            texto_contorno = fonte.render(linha, True, (0, 0, 0))  # Preto para o contorno
            texto_preenchimento = fonte.render(linha, True, cor_texto)  # Texto branco

            x = 20  # Posição horizontal
            y = i * espacamento  # Posição vertical

            # Desenhar contorno (4 lados)
            superficie_creditos.blit(texto_contorno, (x - 1, y))  # Esquerda
            superficie_creditos.blit(texto_contorno, (x + 1, y))  # Direita
            superficie_creditos.blit(texto_contorno, (x, y - 1))  # Cima
            superficie_creditos.blit(texto_contorno, (x, y + 1))  # Baixo

            # Desenhar texto principal
            superficie_creditos.blit(texto_preenchimento, (x, y))

        recorte = superficie_creditos.subsurface((0, deslocamento, largura_quadro, altura_quadro))
        tela.blit(recorte, posicao_quadro)

        pygame.draw.rect(tela, (50, 50, 50), (trilho_x, posicao_quadro[1], barra_largura, trilho_altura))

        # Atualizar posição da barra de rolagem
        barra_y = posicao_quadro[1] + (deslocamento / altura_conteudo) * altura_quadro

        # Desenhar a barra de rolagem
        pygame.draw.rect(tela, (236, 155, 94), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)

        if voltarBotao.clicarBotao(tela):
            print("Voltando ao menu principal")
            estadoJogo = "menu"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            print("Configurações clicado")
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

            # Clique do mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    if trilho_x <= posicaoMouse[0] <= trilho_x + barra_largura and barra_y <= posicaoMouse[1] <= barra_y + barra_altura:
                        clicando_na_barra = True

                elif event.button == 4:  # Rolar para cima
                    deslocamento = max(deslocamento - 20, 0)
                elif event.button == 5:  # Rolar para baixo
                    deslocamento = min(deslocamento + 20, altura_conteudo - altura_quadro)

            # Soltar o clique do mouse
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Clique esquerdo
                    clicando_na_barra = False

            # Movimento do mouse
            elif event.type == pygame.MOUSEMOTION:
                if clicando_na_barra:
                    # Atualizar a posição do deslocamento com base no movimento do mouse
                    deslocamento = max(0, min(altura_conteudo - altura_quadro,
                                              (event.pos[1] - posicao_quadro[1]) * (altura_conteudo / altura_quadro)))

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
    voltarBotao = criarBotao(20, 650, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

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

    voltarBotao = criarBotao(20, 650, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(940, 660, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    
    # Configurações para o texto do temporizador
    fonte = pygame.font.Font("sons/tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Configurações para objetos
    largura_tela, altura_tela = tela.get_size()
    centro_x = largura_tela // 3 + 30
    centro_y = altura_tela // 2 - 20
    raio_x = largura_tela // 3 + 40
    raio_y = altura_tela // 4
    distancia_minima = 140  # Distância mínima entre objetos

    # Lista de imagens
    imagensCorretas = [
        "imagens/fase1/corretas/bichoquecomecupim.png",
        "imagens/fase1/corretas/capibara.png",
        "imagens/fase1/corretas/coala.png",
        "imagens/fase1/corretas/elefante.png",
        "imagens/fase1/corretas/esquilo.png",
        "imagens/fase1/corretas/gamba.png",
        "imagens/fase1/corretas/panda.png",
        "imagens/fase1/corretas/panda2.png",
        "imagens/fase1/corretas/passaro.png",
        "imagens/fase1/corretas/pescoco.png",
        "imagens/fase1/corretas/raposa.png",
        "imagens/fase1/corretas/renatogarcia.png",
    ]

    imagensIncorretas = [
        "imagens/fase1/incorretas/caixa.png",
        "imagens/fase1/incorretas/copoamassado.png",
        "imagens/fase1/incorretas/frauda.png",
        "imagens/fase1/incorretas/garrafa.png",
        "imagens/fase1/incorretas/garrafapet1.png",
        "imagens/fase1/incorretas/garrafapet2.png",
        "imagens/fase1/incorretas/latinha.png",
        "imagens/fase1/incorretas/latinha2.png",
        "imagens/fase1/incorretas/lixojoão.png",
        "imagens/fase1/incorretas/papel.png",
        "imagens/fase1/incorretas/sacodepapel.png",
    ]

    # Selecionando aleatoriamente 6 imagens corretas e 4 incorretas
    imagensCorretasSelecionadas = random.sample(imagensCorretas, 6)  # Seleciona 6 imagens corretas aleatórias
    imagensIncorretasSelecionadas = random.sample(imagensIncorretas, 4)  # Seleciona 4 imagens incorretas aleatórias

    objetos = []

    imagensCorretasClicadas = 0  # Contador de imagens corretas clicadas
    imagensIncorretasClicadas = 0  # Contador de imagens incorretas clicadas

    jogoGanhou = False  # variável para rastrear se o jogo foi vencido
    jogoPerdeu = False  # variável para rastrear se o jogo foi perdido

    objetosSelecionados = []  # Lista para armazenar objetos selecionados

    # Definir o número de vidas
    vidas = 3  # O jogo começa com 3 vidas
    vida_imagens = [
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/0vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/1vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/2vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/3vidas.png"), (220, 60))
    ]

    # Função auxiliar para posicionar objetos
    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        while imagens_selecionadas:
            imagem = imagens_selecionadas.pop(0)
            
            posicao_valida = False
            tentativa = 0
            while not posicao_valida and tentativa < 100:  # Limite de tentativas para evitar loop infinito
                tentativa += 1
                
                # Gerar posição aleatória
                x = random.randint(centro_x - raio_x, centro_x + raio_x)
                y = random.randint(centro_y - raio_y, centro_y + raio_y)
                
                posicao_valida = True  # Assume que a posição é válida inicialmente
                
                # Verifica se está longe o suficiente de outros objetos
                for obj in objetos:
                    distancia = math.sqrt((x - obj["x"])**2 + (y - obj["y"])**2)
                    if distancia < distancia_minima:
                        posicao_valida = False
                        break

            if posicao_valida:
                # Cria o botão para o objeto
                botao = criarBotaoImagens(x, y, imagem, imagem)
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0})
            else:
                print(f"Falha ao posicionar objeto após {tentativa} tentativas: {imagem}")


    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

    # Calcular a posição centralizada para o botão de confirmar na parte inferior
    largura_botao_confirmar = 56  # Tamanho estimado do botão (ajuste conforme necessário)
    altura_botao_confirmar = 56    # Altura estimada do botão (ajuste conforme necessário)
    x_botao_confirmar = (largura_tela - 60 - largura_botao_confirmar) // 2  # Centraliza na horizontal
    y_botao_confirmar = altura_tela - altura_botao_confirmar - 35      # Posiciona perto da parte inferior
    
    # Criar o botão de confirmar no centro inferior da tela
    confirmarBotao = criarBotao(x_botao_confirmar, y_botao_confirmar, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

     # Configurações do temporizador
    tempo_inicial = 120  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa
    
    run = True
    while run:
        tela.blit(fase1Background, (0, 0))
        if jogoPerdeu:
            tela.blit(pygame.image.load("imagens/fase1/perdeuZoologico.jpg"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        elif jogoGanhou:
            tela.blit(pygame.image.load("imagens/fase1/ganhouZoologico.jpg"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        else:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicializado) // 1000
            tempo_restante = max(tempo_inicial - tempo_decorrido, 0)

            if tempo_restante == 0:
                jogoPerdeu = True

        # Exibir as vidas
        tela.blit(vida_imagens[vidas], (140, 640))  # Exibe a imagem das vidas no canto superior esquerdo
        # Configurações para o texto de "VIDAS"
        texto_vidas = "VIDAS"
        texto_vidas_contorno = fonte.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
        texto_vidas_preenchimento = fonte.render(texto_vidas, True, cor_texto)  # Texto branco

        # Posição do texto "VIDAS" ajustada
        posicao_vidas = (largura_tela // 4 - texto_vidas_contorno.get_width() // 1.32, altura_tela - 34)

        # Desenhar o texto com contorno
        tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
        tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
        tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
        tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

        # Desenhar o texto preenchido no centro
        tela.blit(texto_vidas_preenchimento, posicao_vidas)
        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
            erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
            
            # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
            texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

            # Renderizando o texto para mostrar no centro da tela
            texto_contorno_conclusao = fonte.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_conclusao = fonte.render(texto_conclusao, True, cor_texto)  # Texto branco
            posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2)  # Centraliza o texto

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

        # Exibir o temporizador
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        texto_tempo = f"TEMPO: {minutos:02}:{segundos:02}"

        texto_contorno_tempo = fonte.render(texto_tempo, True, (0, 0, 0))  # Contorno preto
        texto_preenchimento_tempo = fonte.render(texto_tempo, True, cor_texto)  # Texto branco
        posicao_tempo = (780, 130)  # Posição abaixo do contador de objetos

        # Desenhar o texto com contorno
        tela.blit(texto_contorno_tempo, (posicao_tempo[0] - 1, posicao_tempo[1]))
        tela.blit(texto_contorno_tempo, (posicao_tempo[0] + 1, posicao_tempo[1]))
        tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] - 1))
        tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] + 1))

        # Desenhar o texto preenchido no centro
        tela.blit(texto_preenchimento_tempo, posicao_tempo)

        # Renderiza o texto do contador com contorno
        texto_contorno = fonte.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, (0, 0, 0))  # Preto para o contorno
        texto_preenchimento = fonte.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, cor_texto)  # Cor original

        posicao_texto = (120, 130)  # Posição no canto superior esquerdo

        # Desenhar o texto com deslocamento para criar o contorno
        tela.blit(texto_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
        tela.blit(texto_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

        # Desenhar o texto preenchido no centro
        tela.blit(texto_preenchimento, posicao_texto)

        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)
        confirmarBotao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do botão de confirmar

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        confirmarBotao.desenharBotao(tela)  # Desenha o botão de confirmar

        # Atualizar e desenhar objetos com movimento
        for obj in objetos:
            botao = obj["botao"]
            botao.atualizarImagem(posicaoMouse)
            botao.desenharBotao(tela)

        # Verificar clique nos objetos
        for obj in objetos:
            if obj["botao"].clicarBotao(tela):
                # Substituir o objeto selecionado
                if objetosSelecionados:
                    print(f"Objeto {objetosSelecionados[0]['tipo']} desmarcado.")
                    objetosSelecionados.clear()  # Limpa a seleção atual

                objetosSelecionados.append(obj)  # Seleciona o novo objeto
                print(f"Objeto {obj['tipo']} selecionado na posição ({obj['x']}, {obj['y']})!")

        # Verificar clique no botão de confirmar
        if confirmarBotao.clicarBotao(tela):
            for obj in objetosSelecionados:
                if obj["tipo"] == "correto":
                    imagensCorretasClicadas += 1
                    if imagensCorretasClicadas == 6:  # Clicou em todas as imagens corretas
                        jogoGanhou = True
                elif obj["tipo"] == "incorreto":
                    imagensIncorretasClicadas += 1
                    vidas -= 1  # Perde uma vida a cada erro
                    if vidas == 0:
                        jogoPerdeu = True
                objetos.remove(obj)  # Remove o objeto selecionado
            objetosSelecionados.clear()  # Limpa a lista de objetos selecionados
            print("Seleção confirmada. Você pode selecionar outro objeto.")



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

    voltarBotao = criarBotao(20, 650, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(940, 660, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    
    # Configurações para o texto do temporizador
    fonte = pygame.font.Font("sons/tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Configurações para objetos
    largura_tela, altura_tela = tela.get_size()
    centro_x = largura_tela // 3 + 30
    centro_y = altura_tela // 2 - 20
    raio_x = largura_tela // 3 + 40
    raio_y = altura_tela // 4
    distancia_minima = 140  # Distância mínima entre objetos

    # Inicializa a fonte para o texto do contador
    fonte = pygame.font.Font("sons/tipografia/LuckiestGuy-Regular.ttf", 36)  # 'None' usa a fonte padrão; 36 é o tamanho 
    cor_texto = (255, 255, 255)  # Cor do texto (branco)

    # Lista de imagens
    imagensCorretas = [
        "imagens/fase2/corretas/banana.png",
        "imagens/fase2/corretas/copoamassado.png",
        "imagens/fase2/corretas/frauda.png",
        "imagens/fase2/corretas/garrafa.png",
        "imagens/fase2/corretas/latinha.png",
        "imagens/fase2/corretas/latinha2.png",
        "imagens/fase2/corretas/lixojoão.png",
        "imagens/fase2/corretas/maçacomida.png",
        "imagens/fase2/corretas/sacodepapel.png",
    ]

    imagensIncorretas = [
        "imagens/fase2/incorretas/borra.png",
        "imagens/fase2/incorretas/estojo.png",
        "imagens/fase2/incorretas/livros.png",
        "imagens/fase2/incorretas/objetoescolar.png",
        "imagens/fase2/incorretas/regua.png",
    ]

    # Selecionando aleatoriamente 6 imagens corretas e 4 incorretas
    imagensCorretasSelecionadas = random.sample(imagensCorretas, 6)  # Seleciona 6 imagens corretas aleatórias
    imagensIncorretasSelecionadas = random.sample(imagensIncorretas, 4)  # Seleciona 4 imagens incorretas aleatórias

    objetos = []

    imagensCorretasClicadas = 0  # Contador de imagens corretas clicadas
    imagensIncorretasClicadas = 0  # Contador de imagens incorretas clicadas

    jogoGanhou = False  # variável para rastrear se o jogo foi vencido
    jogoPerdeu = False  # variável para rastrear se o jogo foi perdido

    objetosSelecionados = []  # Lista para armazenar objetos selecionados

    # Definir o número de vidas
    vidas = 3  # O jogo começa com 3 vidas
    vida_imagens = [
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/0vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/1vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/2vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/3vidas.png"), (220, 60))
    ]

    # Função auxiliar para posicionar objetos
    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        while imagens_selecionadas:
            imagem = imagens_selecionadas.pop(0)
            
            posicao_valida = False
            tentativa = 0
            while not posicao_valida and tentativa < 100:  # Limite de tentativas para evitar loop infinito
                tentativa += 1
                
                # Gerar posição aleatória
                x = random.randint(centro_x - raio_x, centro_x + raio_x)
                y = random.randint(centro_y - raio_y, centro_y + raio_y)
                
                posicao_valida = True  # Assume que a posição é válida inicialmente
                
                # Verifica se está longe o suficiente de outros objetos
                for obj in objetos:
                    distancia = math.sqrt((x - obj["x"])**2 + (y - obj["y"])**2)
                    if distancia < distancia_minima:
                        posicao_valida = False
                        break

            if posicao_valida:
                # Cria o botão para o objeto
                botao = criarBotaoImagens(x, y, imagem, imagem)
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0})
            else:
                print(f"Falha ao posicionar objeto após {tentativa} tentativas: {imagem}")


    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

    # Calcular a posição centralizada para o botão de confirmar na parte inferior
    largura_botao_confirmar = 200  # Tamanho estimado do botão (ajuste conforme necessário)
    altura_botao_confirmar = 50    # Altura estimada do botão (ajuste conforme necessário)
    x_botao_confirmar = (largura_tela - 60 - largura_botao_confirmar) // 2  # Centraliza na horizontal
    y_botao_confirmar = altura_tela - altura_botao_confirmar - 35      # Posiciona perto da parte inferior
    
    # Criar o botão de confirmar no centro inferior da tela
    confirmarBotao = criarBotao(x_botao_confirmar, y_botao_confirmar, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

     # Configurações do temporizador
    tempo_inicial = 120  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa

    run = True
    while run:
        tela.blit(fase1Background, (0, 0))
        if jogoPerdeu:
            tela.blit(pygame.image.load("imagens/fase2/perdeuSaladeAula.jpg"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        elif jogoGanhou:
            tela.blit(pygame.image.load("imagens/fase2/ganhouSaladeAula.jpg"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        else:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicializado) // 1000
            tempo_restante = max(tempo_inicial - tempo_decorrido, 0)

            if tempo_restante == 0:
                jogoPerdeu = True

         # Exibir as vidas
        tela.blit(vida_imagens[vidas], (140, 640))  # Exibe a imagem das vidas no canto superior esquerdo
        # Configurações para o texto de "VIDAS"
        texto_vidas = "VIDAS"
        texto_vidas_contorno = fonte.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
        texto_vidas_preenchimento = fonte.render(texto_vidas, True, cor_texto)  # Texto branco

        # Posição do texto "VIDAS" ajustada
        posicao_vidas = (largura_tela // 4 - texto_vidas_contorno.get_width() // 1.32, altura_tela - 34)

        # Desenhar o texto com contorno
        tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
        tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
        tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
        tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

        # Desenhar o texto preenchido no centro
        tela.blit(texto_vidas_preenchimento, posicao_vidas)

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
            erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
            
            # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
            texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

            # Renderizando o texto para mostrar no centro da tela
            texto_contorno_conclusao = fonte.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_conclusao = fonte.render(texto_conclusao, True, cor_texto)  # Texto branco
            posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2)  # Centraliza o texto

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

        # Exibir o temporizador
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        texto_tempo = f"TEMPO: {minutos:02}:{segundos:02}"

        texto_contorno_tempo = fonte.render(texto_tempo, True, (0, 0, 0))  # Contorno preto
        texto_preenchimento_tempo = fonte.render(texto_tempo, True, cor_texto)  # Texto branco
        posicao_tempo = (780, 130)  # Posição abaixo do contador de objetos

        # Desenhar o texto com contorno
        tela.blit(texto_contorno_tempo, (posicao_tempo[0] - 1, posicao_tempo[1]))
        tela.blit(texto_contorno_tempo, (posicao_tempo[0] + 1, posicao_tempo[1]))
        tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] - 1))
        tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] + 1))

        # Desenhar o texto preenchido no centro
        tela.blit(texto_preenchimento_tempo, posicao_tempo)

        # Renderiza o texto do contador com contorno
        texto_contorno = fonte.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, (0, 0, 0))  # Preto para o contorno
        texto_preenchimento = fonte.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, cor_texto)  # Cor original

        posicao_texto = (120, 130)  # Posição no canto superior esquerdo

        # Desenhar o texto com deslocamento para criar o contorno
        tela.blit(texto_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
        tela.blit(texto_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

        # Desenhar o texto preenchido no centro
        tela.blit(texto_preenchimento, posicao_texto)

        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)
        confirmarBotao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do botão de confirmar

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        confirmarBotao.desenharBotao(tela)  # Desenha o botão de confirmar

        # Atualizar e desenhar objetos com movimento
        for obj in objetos:
            botao = obj["botao"]
            botao.atualizarImagem(posicaoMouse)
            botao.desenharBotao(tela)

        # Verificar clique nos objetos
        for obj in objetos:
            if obj["botao"].clicarBotao(tela):
                # Substituir o objeto selecionado
                if objetosSelecionados:
                    print(f"Objeto {objetosSelecionados[0]['tipo']} desmarcado.")
                    objetosSelecionados.clear()  # Limpa a seleção atual

                objetosSelecionados.append(obj)  # Seleciona o novo objeto
                print(f"Objeto {obj['tipo']} selecionado na posição ({obj['x']}, {obj['y']})!")

        # Verificar clique no botão de confirmar
        if confirmarBotao.clicarBotao(tela):
            for obj in objetosSelecionados:
                if obj["tipo"] == "correto":
                    imagensCorretasClicadas += 1
                    if imagensCorretasClicadas == 6:  # Clicou em todas as imagens corretas
                        jogoGanhou = True
                elif obj["tipo"] == "incorreto":
                    imagensIncorretasClicadas += 1
                    vidas -= 1  # Perde uma vida a cada erro
                    if vidas == 0:
                        jogoPerdeu = True
                objetos.remove(obj)  # Remove o objeto selecionado
            objetosSelecionados.clear()  # Limpa a lista de objetos selecionados
            print("Seleção confirmada. Você pode selecionar outro objeto.")


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
    jogarBotao = criarBotao(400, 300, "imagens/GUI/botaoJogar/jogar0.png", "imagens/GUI/botaoJogar/jogar1.png")
    configuracoesBotao = criarBotao(900, 50, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    instrucoesBotao = criarBotao(400, 425, "imagens/GUI/botaoInicio/instrucoes1.png", "imagens/GUI/botaoInicio/instrucoes01.png")
    sairBotao = criarBotao(40, 50, "imagens/GUI/botaoSair/sair0.png", "imagens/GUI/botaoSair/sair1.png")
    creditosBotao = criarBotao(1000, 640, "imagens/GUI/botaoConfiguracoes/info0.png", "imagens/GUI/botaoConfiguracoes/info1.png")  

    run = True
    while run:
        tela.blit(menuBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        # Atualizar e desenhar botões
        jogarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)
        instrucoesBotao.atualizarImagem(posicaoMouse)
        sairBotao.atualizarImagem(posicaoMouse)
        creditosBotao.atualizarImagem(posicaoMouse)

        jogarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        instrucoesBotao.desenharBotao(tela)
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
            run = False

        if instrucoesBotao.clicarBotao(tela):
            print("Instruções clicado")
            abrirInstrucoes()
            run = False

        if creditosBotao.clicarBotao(tela):  # Detecta clique no botão de créditos
            print("Créditos clicado")
            abrirCreditos()
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
    print(f"Estado do jogo: {estadoJogo}")  # Imprime o estado atual do jogo

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

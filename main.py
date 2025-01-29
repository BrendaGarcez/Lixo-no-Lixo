from moviepy import VideoFileClip
import pygame  # Importando biblioteca
import botao  # Importando a classe Botao
import botaoObjetos
import sys
import random
import math
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk



pygame.init()  # Inicializa os módulos do pygame
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Muda o cursor para a mão
# Resolução da tela
telaLargura = 1100
telaAltura = 720
tela = pygame.display.set_mode((telaLargura, telaAltura))  # Configuração da tela
pygame.display.set_caption("Lixo_No_Lixo")  # Nome do jogo

som_click = pygame.mixer.Sound("sons/somClickMouse/mouseclick.wav")
som_click.set_volume(0.2)
clock = pygame.time.Clock()
somAtivo = True  # Estado inicial do som
musica_atual = None
pygame.mixer.init()

estadoJogo = "menu"  # situação atual do jogo, para rastrear as telas
rodando = True  # Controla se o programa deve continuar rodando

jogoConcluido = False
pontuacao_fase1 = 0
pontuacao_fase2 = 0
pontuacao_fase3 = 0

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

def criarBotaoImagensFASE3(x, y, imagem, imagemAlterada):
    imagem = pygame.image.load(imagem).convert_alpha()
    imagemAlterada = pygame.image.load(imagemAlterada).convert_alpha()
    
    # Redimensionar as imagens
    largura, altura = 160, 100  # Exemplo de tamanho, ajuste conforme necessário
    imagem = pygame.transform.scale(imagem, (largura, altura))
    imagemAlterada = pygame.transform.scale(imagemAlterada, (largura, altura))
    
    return botaoObjetos.BotaoObjetos(x, y, imagem, imagemAlterada)

def exibir_nome_objeto(obj):
    # Definir a fonte para o nome do objeto
    fonte_nome = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 24)
    nome_objeto = obj["nome"]  # Usa o nome extraído da imagem
    cor_texto = (255, 255, 255)  # Cor do texto (branco)

    # Renderizar o nome com contorno e preenchimento
    texto_nome_contorno = fonte_nome.render(nome_objeto, True, (0, 0, 0))  # Contorno preto
    texto_nome_preenchimento = fonte_nome.render(nome_objeto, True, cor_texto)  # Texto branco

    # Posicionar o nome logo acima do objeto
    posicao_nome = (obj["x"] + 100 - texto_nome_preenchimento.get_width() // 2, obj["y"] + 5)

    # Desenhar o texto com contorno
    tela.blit(texto_nome_contorno, (posicao_nome[0] - 1, posicao_nome[1]))
    tela.blit(texto_nome_contorno, (posicao_nome[0] + 1, posicao_nome[1]))
    tela.blit(texto_nome_contorno, (posicao_nome[0], posicao_nome[1] - 1))
    tela.blit(texto_nome_contorno, (posicao_nome[0], posicao_nome[1] + 1))

    # Desenhar o texto preenchido
    tela.blit(texto_nome_preenchimento, posicao_nome)


# Função para verificar se o botão foi clicado
def verificar_clique_botao(x, y, largura, altura):
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if x <= mouse_pos[0] <= x + largura and y <= mouse_pos[1] <= y + altura:
        if mouse_pressed[0]:  # Se o botão esquerdo do mouse foi pressionado
            return True
    return False

def mostrarVideo(video_path, video_width, video_height, imagem_fundo_path, audio_path):
    # Abrir o vídeo com OpenCV
    cap = cv2.VideoCapture(video_path)
    
    # Inicializar o mixer do Pygame para áudio
    pygame.mixer.init()

    posicaoMouse = pygame.mouse.get_pos()

    # Criar o botão de voltar
    voltarBotao = criarBotao(477.5 , 520,"imagens/GUI/imagensExtra/botaoPular0.png", "imagens/GUI/imagensExtra/botaoPular1.png")
    avatarBotao = criarBotao(786, 485, "imagens/GUI/imagensExtra/avatar.png", "imagens/GUI/imagensExtra/avatar.png")
     
    if not cap.isOpened():
        print("Erro ao abrir o vídeo:", video_path)
        return

    # Carregar a imagem de fundo
    fundo_imagem = pygame.image.load(imagem_fundo_path)

    # Carregar e tocar o áudio
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1, 0.0)  # Tocar o áudio de forma contínua (-1) desde o início (0.0)

    # Calcular a posição central do vídeo na tela
    x_center = (telaLargura - video_width) // 2
    y_center = (telaAltura - video_height) // 2

    # Posição e tamanho do botão de "Voltar"
    botao_largura, botao_altura = 145, 47

    # Loop principal do vídeo
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # Verificar se o botão foi clicado
        if verificar_clique_botao(477.5 , 520, botao_largura, botao_altura):
            print("Botão de voltar clicado!")
            run = False
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Voltar ao início do vídeo

        # Ler o próximo frame do vídeo
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler frame!")
            break

        # Redimensionar o frame para o tamanho definido (video_width x video_height)
        frame = cv2.resize(frame, (video_width, video_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Renderizar o fundo da fase (imagem de fundo)
        tela.blit(fundo_imagem, (0, 0))  # Colocar a imagem de fundo

        # Renderizar o vídeo no centro da tela
        tela.blit(frame_surface, (x_center, y_center))

        # Atualizar a posição do mouse
        posicaoMouse = pygame.mouse.get_pos()
        
        avatarBotao.desenharBotao(tela)
        # Verificar se o mouse está sobre o botão e alterar a imagem para o hover
        if 200 <= posicaoMouse[0] <= 200 + botao_largura and 660 <= posicaoMouse[1] <= 660 + botao_altura:
            voltarBotao.desenharBotao(tela)  # Desenhar o botão hover
        else:
            voltarBotao.desenharBotao(tela)
        
        pygame.display.update()
        pygame.time.Clock().tick(30)

    # Parar o áudio quando o vídeo terminar
    pygame.mixer.music.stop()

    # Liberar os recursos do vídeo
    cap.release()





def tocar_musica(nova_musica): # FUNÇÃO DA MÚSICA DE FUNDO
    global musica_atual
    if musica_atual != nova_musica:  # Só troca se a música for diferente
        pygame.mixer.music.stop()  # Para a música atual
        pygame.mixer.music.load(nova_musica)  # Carrega a nova música
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # Toca em loop
        musica_atual = nova_musica  # Atualiza a música atual
        
def tocar_efeito_sonoro(efeito):
    efeito_sonoro = pygame.mixer.Sound(efeito)
    efeito_sonoro.play()  # Toca o efeito sonoro sem parar a música de fundo


def confirmar_saida(tela):
    # Dimensões da janela de confirmação
    largura = 400
    altura = 150
    fonte = pygame.font.SysFont(None, 36)

    # Cria um retângulo centralizado para a janela de diálogo
    janela_rect = pygame.Rect(
        (tela.get_width() - largura) // 2, 
        (tela.get_height() - altura) // 2, 
        largura, altura
    )

    # Botões "Sim" e "Não"
    sim_botao = pygame.Rect(janela_rect.x + 100, janela_rect.y + 80, 80, 40)
    nao_botao = pygame.Rect(janela_rect.x + 220, janela_rect.y + 80, 80, 40)

    while True:
        # Preenche a tela de fundo
        pygame.draw.rect(tela, (120, 64, 8), janela_rect)
        pygame.draw.rect(tela, (0, 0, 0), janela_rect, 2)

        # Texto da janela
        texto = fonte.render("Deseja realmente sair?", True, (255, 255, 255))
        tela.blit(texto, (janela_rect.x + 68, janela_rect.y + 20))

        # Botões "Sim" e "Não"
        pygame.draw.rect(tela, (0, 200, 0), sim_botao)
        pygame.draw.rect(tela, (200, 0, 0), nao_botao)

        texto_sim = fonte.render("Sim", True, (255, 255, 255))
        texto_nao = fonte.render("Não", True, (255, 255, 255))
        tela.blit(texto_sim, (sim_botao.x + 20, sim_botao.y + 5))
        tela.blit(texto_nao, (nao_botao.x + 20, nao_botao.y + 5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if sim_botao.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if nao_botao.collidepoint(event.pos):
                    return  # Retorna ao jogo
                
def abrirConfiguracoes():
    global somAtivo

    configuracoesBackground = pygame.image.load("imagens/GUI/Backgrounds/configuracoesBackground.jpg")
    tela.blit(configuracoesBackground, (0, 0))

    volume = pygame.mixer.music.get_volume()  # Obter o volume atual

    largura_tela, altura_tela = tela.get_size()  # Dimensões da tela
    largura_imagem, altura_imagem = 96, 96  # Tamanho das imagens dos botões

    # Calcula as posições para centralizar as imagens
    som_x = (largura_tela - largura_imagem) // 2
    som_y = (altura_tela - altura_imagem) // 2 - 50

    somLigadoBotao = criarBotao(som_x, som_y, "imagens/GUI/botaoSom/ligado0.png", "imagens/GUI/botaoSom/ligado1.png")
    somDesligadoBotao = criarBotao(som_x, som_y, "imagens/GUI/botaoSom/desligado0.png", "imagens/GUI/botaoSom/desligado1.png")
    voltarBotao = criarBotao(20, 660, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    sairBotao = criarBotao(som_x - 20, 560,"imagens/GUI/botaoSair/Sair0.png", "imagens/GUI/botaoSair/Sair1.png")

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
        sairBotao.atualizarImagem(posicaoMouse)
        sairBotao.desenharBotao(tela)

        # Barra de volume centralizada horizontalmente
        barra_x, barra_y = (largura_tela - 300) // 2, som_y + altura_imagem + 50
        barra_largura, barra_altura = 300, 10
        pygame.draw.rect(tela, (100, 100, 100), (barra_x, barra_y, barra_largura, barra_altura))  # Fundo da barra
        pygame.draw.rect(tela, (139, 69, 19), (barra_x, barra_y, int(volume * barra_largura), barra_altura))  # Barra de volume
        pygame.draw.circle(tela, (139, 50, 17), (barra_x + int(volume * barra_largura), barra_y + barra_altura // 2), 10)  # Indicador do volume

        if cliqueMouse[0] and barra_x <= posicaoMouse[0] <= barra_x + barra_largura and barra_y - 10 <= posicaoMouse[1] <= barra_y + barra_altura + 10:
            volume = (posicaoMouse[0] - barra_x) / barra_largura
            volume = max(0, min(volume, 1))
            pygame.mixer.music.set_volume(volume)  # Atualiza o volume

        # Texto do volume abaixo da barra
        fonte = pygame.font.Font(None, 36)
        texto_volume = f"Volume: {int(volume * 100)}%"
        texto_renderizado = fonte.render(texto_volume, True, (255, 255, 255))
        texto_rect = texto_renderizado.get_rect(center=(barra_x + barra_largura // 2, barra_y + barra_altura + 30))
        tela.blit(texto_renderizado, texto_rect.topleft)

        # Verificar cliques
        if somAtivo and somLigadoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            somAtivo = False
            pygame.mixer.music.pause()
        elif not somAtivo and somDesligadoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            somAtivo = True
            pygame.mixer.music.unpause()

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            run = False  
        
        if sairBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            confirmar_saida(tela)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def abrirConfiguracoesFases():
    global somAtivo
    global estadoJogo

    configuracoesBackground = pygame.image.load("imagens/GUI/Backgrounds/configuracoesBackground.jpg")
    tela.blit(configuracoesBackground, (0, 0))

    volume = pygame.mixer.music.get_volume()  # Obter o volume atual

    largura_tela, altura_tela = tela.get_size()  # Dimensões da tela
    largura_imagem, altura_imagem = 96, 96  # Tamanho das imagens dos botões

    # Calcula as posições para centralizar as imagens
    som_x = (largura_tela - largura_imagem) // 2
    som_y = (altura_tela - altura_imagem) // 2 - 110

    somLigadoBotao = criarBotao(som_x, som_y, "imagens/GUI/botaoSom/ligado0.png", "imagens/GUI/botaoSom/ligado1.png")
    somDesligadoBotao = criarBotao(som_x, som_y, "imagens/GUI/botaoSom/desligado0.png", "imagens/GUI/botaoSom/desligado1.png")
    voltarBotao = criarBotao(som_x - 275, 540, "imagens/GUI/botaoVoltar/continuar0.png", "imagens/GUI/botaoVoltar/continuar1.png")
    sairBotao = criarBotao(som_x - 105, 540,"imagens/GUI/botaoSair/Sair0.png", "imagens/GUI/botaoSair/Sair1.png")
    menuBotao = criarBotao(som_x + 65, 540,"imagens/GUI/botaoInicio/botaoHome.png", "imagens/GUI/botaoInicio/botaoHome.png")
    fasesBotao = criarBotao(som_x + 235, 540,"imagens/GUI/botaoFases/botaoFases.png", "imagens/GUI/botaoFases/botaoFases.png")

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
        sairBotao.atualizarImagem(posicaoMouse)
        sairBotao.desenharBotao(tela)
        menuBotao.atualizarImagem(posicaoMouse)
        menuBotao.desenharBotao(tela)
        fasesBotao.atualizarImagem(posicaoMouse)
        fasesBotao.desenharBotao(tela)

        # Barra de volume centralizada horizontalmente
        barra_x, barra_y = (largura_tela - 300) // 2, som_y + altura_imagem + 50
        barra_largura, barra_altura = 300, 10
        pygame.draw.rect(tela, (100, 100, 100), (barra_x, barra_y, barra_largura, barra_altura))  # Fundo da barra
        pygame.draw.rect(tela, (139, 69, 19), (barra_x, barra_y, int(volume * barra_largura), barra_altura))  # Barra de volume
        pygame.draw.circle(tela, (139, 50, 17), (barra_x + int(volume * barra_largura), barra_y + barra_altura // 2), 10)  # Indicador do volume

        if cliqueMouse[0] and barra_x <= posicaoMouse[0] <= barra_x + barra_largura and barra_y - 10 <= posicaoMouse[1] <= barra_y + barra_altura + 10:
            volume = (posicaoMouse[0] - barra_x) / barra_largura
            volume = max(0, min(volume, 1))
            pygame.mixer.music.set_volume(volume)  # Atualiza o volume

        # Texto do volume abaixo da barra
        fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 25)
        texto_volume = f"Volume: {int(volume * 100)}%"
        texto_renderizado = fonte.render(texto_volume, True, (255, 255, 255))
        texto_rect = texto_renderizado.get_rect(center=(barra_x + barra_largura // 2, barra_y + barra_altura + 30))
        tela.blit(texto_renderizado, texto_rect.topleft)

        # Verificar cliques nos botões
        if somAtivo and somLigadoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            somAtivo = False
            pygame.mixer.music.pause()
        elif not somAtivo and somDesligadoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            somAtivo = True
            pygame.mixer.music.unpause()

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            run = False  # Sai do loop para voltar para a tela anterior

        if sairBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            confirmar_saida(tela)  # Chama a função para confirmar a saída

        if menuBotao.clicarBotao(tela):
            som_click.play()  
            menuPrincipal()  
            run = False  
            return  

        if fasesBotao.clicarBotao(tela):
            som_click.play()  
            iniciarFases()  
            run = False  
            return  

        # Controle de eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)


def abrirInstrucoes():
    global estadoJogo
    instrucoesBackground = pygame.image.load("imagens/GUI/Backgrounds/instrucoesBackground.jpg")
    voltarBotao = criarBotao(40, 50, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(900, 50, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    fase1Botao = criarBotao(20, 250, "imagens/fase1/faseBotao1.png", "imagens/fase1/faseBotao1.png")
    fase2Botao = criarBotao(20, 370, "imagens/fase2/faseBotao2.png", "imagens/fase2/faseBotao2.png")
    fase3Botao = criarBotao(20, 490, "imagens/fase3/faseBotao3.png", "imagens/fase3/faseBotao3.png")

    # Textos das fases
    texto_fase1 = [
        "",
        "                           Bem-vindo à Fase 1!",
        " Nesta fase estamos no zoológico,",
        " O zoológico é um lugar que protege os ",
        " animais que não podem estar na cidade,",
        " voce pode ajudar a identificar quais ",
        " são os animais que devem ir para suas",
        " jaulas?",
        "",
        " Objetivo:",
        " - Selecione os animais.",
        " - Evite os lixos.",
        "",
        " Boa sorte!"
    ]
    texto_fase2 = [
        "",
        "                           Bem-vindo à Fase 2!",
        " Nesta fase estamos na sala de aula,",
        " Alguem espalhou lixo pela sala inteira!",
        " Não podemos deixar a sala suja ",
        " desse jeito, selecione todos",
        " os objetos que nao deveria estar na",
        " sala de aula",
        "",
        " Objetivo:",
        " - Selecione o Lixo!",
        " - Evite os que pertence a Sala de Aula.",
        "",
        " Boa sorte!"
    ]
    texto_fase3 = [
        "",
        "                           Bem-vindo à Fase 3!",
        " Nesta fase estamos na praia,",
        " Alguem espalhou lixo pela praia toda!",
        " Não podemos deixar tudo se misturar ",
        " dessa forma, arraste todos os objetos ",
        " que nao deveriam estar na praia ",
        " para o lixo, e os nossos itens de ",
        " praia para a cesta de praia!",
        "",
        " Objetivo:",
        " - Arraste o lixo para a área do lixo",
        " na tela.",
        " - Arraste os itens de praia para a área ",
        " da cesta na tela.",
        "",
        " Boa sorte!"
    ]

    texto_atual = [
        "",
        "                           Bem-vindo ao Jogo!",
        " Informações Gerais: ",
        " - Informe seu nome para sua pontuação ",
        " ficar salva",
        " - Clique nos itens para ouvir o nome ",
        " deles",
        " - Passe o mouse por cima dos itens ",
        " para saber o nome deles"
    ]

    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 30)
    cor_texto = (255, 255, 255)
    espacamento = 40

    largura_quadro = 670
    altura_quadro = 480
    posicao_quadro = (330, 180)

    altura_conteudo = len(texto_atual) * espacamento
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
        superficie_instrucoes = pygame.Surface((largura_quadro, max(len(texto_atual) * espacamento, altura_quadro)), pygame.SRCALPHA)
        superficie_instrucoes.fill((131, 69, 31))  # Fundo do quadro

        # Renderizar o texto
        for i, linha in enumerate(texto_atual):
            texto_contorno = fonte.render(linha, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento = fonte.render(linha, True, cor_texto)  # Texto branco
            x, y = 20, i * espacamento
            superficie_instrucoes.blit(texto_contorno, (x - 1, y))
            superficie_instrucoes.blit(texto_contorno, (x + 1, y))
            superficie_instrucoes.blit(texto_contorno, (x, y - 1))
            superficie_instrucoes.blit(texto_contorno, (x, y + 1))
            superficie_instrucoes.blit(texto_preenchimento, (x, y))

        deslocamento = max(0, min(deslocamento, len(texto_atual) * espacamento - altura_quadro))
        recorte = superficie_instrucoes.subsurface((0, deslocamento, largura_quadro, altura_quadro))
        tela.blit(recorte, posicao_quadro)

        # Barra de rolagem
        trilho_x = barra_x
        trilho_altura = altura_quadro
        pygame.draw.rect(tela, (50, 50, 50), (trilho_x, posicao_quadro[1], barra_largura, trilho_altura))
        barra_y = posicao_quadro[1] + (deslocamento / max(len(texto_atual) * espacamento, 1)) * altura_quadro
        pygame.draw.rect(tela, (70, 130, 180), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)

        # Verificar cliques nos botões
        if voltarBotao.clicarBotao(tela):
            som_click.play()
            estadoJogo = "menu"
            run = False

        if configuracoesBotao.clicarBotao(tela):
            som_click.play()
            abrirConfiguracoes()

        if fase1Botao.clicarBotao(tela):
            som_click.play()
            texto_atual = texto_fase1  # Atualiza texto para Fase 1
            deslocamento = 0  # Reseta o deslocamento

        if fase2Botao.clicarBotao(tela):
            som_click.play()
            texto_atual = texto_fase2  # Atualiza texto para Fase 2
            deslocamento = 0

        if fase3Botao.clicarBotao(tela):
            som_click.play()
            texto_atual = texto_fase3  # Atualiza texto para Fase 3
            deslocamento = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                confirmar_saida(tela)
                rodando = False
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if trilho_x <= posicaoMouse[0] <= trilho_x + barra_largura and barra_y <= posicaoMouse[1] <= barra_y + barra_altura:
                        clicando_na_barra = True

                elif event.button == 4:
                    deslocamento = max(deslocamento - 20, 0)
                elif event.button == 5:
                    deslocamento = min(deslocamento + 20, len(texto_atual) * espacamento - altura_quadro)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicando_na_barra = False

            elif event.type == pygame.MOUSEMOTION:
                if clicando_na_barra:
                    deslocamento = max(0, min(len(texto_atual) * espacamento - altura_quadro,
                                              (event.pos[1] - posicao_quadro[1]) * (len(texto_atual) * espacamento / altura_quadro)))
             

        pygame.display.update()

def abrirCreditos():
    global estadoJogo
    creditosBackground = pygame.image.load("imagens/GUI/Backgrounds/creditos.jpg")
    voltarBotao = criarBotao(20, 660, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    linhas_creditos = [
        "Lixo no lixo é um jogo educativo criado para ",
        "ajudar na conscientização sobre a poluição.",
        "Este jogo ajuda a lembrarmos que se deve",
        "jogar lixo no chão para não danificar o ",
        "meio ambiente!",
        "Combinando com esse tema, também podemos",
        "ajudar os jogadores a saberem quais",
        "objetos pertencem aos lugares como:", 
        " - Zoológico,",
        " - Sala de aula,",
        " - Praia.",
        "",
        "Lembre-se: sempre jogue o LIXO NO LIXO!",
        "",
        "Jogo produzido por:",
        "- Brenda Amanda da Silva Garcez",
        "- Nicole Louise Matias Jamuchewski",
        "- João Rafael Moreira Anhaia",
        "- Matheus Vinícius dos Santos Sachinski",
        "- Pedro Victor A. M. L. Maciel",
        "                                  Desenvolvimento   ",
        "- Brenda Amanda da Silva Garcez",
        "- Matheus Vinícius dos Santos Sachinski",
        "                                   Ilustrações",
        "- João Rafael Moreira Anhaia",
        "- Nicole Louise Matias Jamuchewski",
        "                                   Audio e Vídeo",
        "- Brenda Amanda da Silva Garcez",
        "- Matheus Vinícius dos Santos Sachinski",
        "- Nicole Louise Matias Jamuchewski",
        "                                   Documentação",
        "- Pedro Victor A. M. L. Maciel",
        "                                         Fontes por:",
        "- 'Luckiest' Guy por Astigmatic (Google Fonts)",
        "                             Obrigado por jogar!",
    ]

    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 26)  # 40 é o tamanho da fonte
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
            som_click.play()  # Som de clique
            print("Voltando ao menu principal")
            estadoJogo = "menu"
            run = False
        if configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                confirmar_saida(tela)
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

def relatorio():
    global estadoJogo, pontuacao_fase1, pontuacao_fase2, pontuacao_fase3

    # Carregar o fundo
    fasesBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")
    tela.blit(fasesBackground, (0, 0))

    # Botões
    voltarBotao = criarBotao(20, 660, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(940, 660, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")

    # Fonte para exibir o texto
    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Cor branca
    cor_contorno = (0, 0, 0)  # Cor preta para o contorno
    largura_tela = tela.get_width()  # Largura da tela
    altura_fase = 320  # Altura para exibir o texto das fases
    altura_pontuacao = altura_fase + 40  # Altura para exibir as pontuações

    # Fases e pontuações
    fases = ["FASE 1", "FASE 2", "FASE 3"]
    pontuacoes = [pontuacao_fase1, pontuacao_fase2, pontuacao_fase3] 

    # Posições horizontais
    posicoes_x = [
        largura_tela // 6,  # Esquerda
        largura_tela // 2,  # Centro
        largura_tela * 5 // 6  # Direita
    ]

    run = True
    while run:
        tela.blit(fasesBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        # Desenhar os botões
        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)

        # Exibir as fases e pontuações com contorno
        for i, fase in enumerate(fases):
            # Renderizar textos
            texto_fase = fonte.render(fase, True, cor_texto)
            texto_fase_contorno = fonte.render(fase, True, cor_contorno)
            texto_pontuacao = fonte.render(f"Pontuação: {pontuacoes[i]}", True, cor_texto)
            texto_pontuacao_contorno = fonte.render(f"Pontuação: {pontuacoes[i]}", True, cor_contorno)

            # Posições calculadas
            x_fase = posicoes_x[i] - texto_fase.get_width() // 2
            y_fase = altura_fase
            x_pontuacao = posicoes_x[i] - texto_pontuacao.get_width() // 2
            y_pontuacao = altura_pontuacao

            # Desenhar contorno para o texto da fase
            tela.blit(texto_fase_contorno, (x_fase - 1, y_fase))
            tela.blit(texto_fase_contorno, (x_fase + 1, y_fase))
            tela.blit(texto_fase_contorno, (x_fase, y_fase - 1))
            tela.blit(texto_fase_contorno, (x_fase, y_fase + 1))

            # Desenhar o texto preenchido da fase
            tela.blit(texto_fase, (x_fase, y_fase))

            # Desenhar contorno para o texto da pontuação
            tela.blit(texto_pontuacao_contorno, (x_pontuacao - 1, y_pontuacao))
            tela.blit(texto_pontuacao_contorno, (x_pontuacao + 1, y_pontuacao))
            tela.blit(texto_pontuacao_contorno, (x_pontuacao, y_pontuacao - 1))
            tela.blit(texto_pontuacao_contorno, (x_pontuacao, y_pontuacao + 1))

            # Desenhar o texto preenchido da pontuação
            tela.blit(texto_pontuacao, (x_pontuacao, y_pontuacao))

        # Verificar cliques nos botões
        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "menu"
            run = False

        if configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoes()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)


    
# Função para as fases
def iniciarFases():
    global estadoJogo
    fasesBackground = pygame.image.load("imagens/GUI/Backgrounds/fasesBackground.jpg")
    tela.blit(fasesBackground,(0,0))
    
    largura_tela = tela.get_width()

    if somAtivo:
        tocar_musica("sons/musicaMenu/musicafundo.mp3")
        
    margem_lateral = (largura_tela - (2 * 430)) // 3  # Espaço entre as bordas e os botões
    posicao_fase1 = (margem_lateral, 200)  # Primeiro botão na parte superior esquerda
    posicao_fase2 = (margem_lateral + 430 + margem_lateral, 200)  # Segundo botão na parte superior direita
    posicao_fase3 = ((largura_tela - 430) // 2, 450)  # Terceiro botão centralizado abaixo
    posicao_voltar = (20, 660)  # Botão voltar no canto inferior esquerdo

    # Criando botões para as fases
    fase1Botao = criarBotao(posicao_fase1[0] + 5, posicao_fase1[1], "imagens/GUI/botaoFases/botaoZoo0.png", "imagens/GUI/botaoFases/botaoZoo1.png")
    fase2Botao = criarBotao(posicao_fase2[0], posicao_fase2[1], "imagens/GUI/botaoFases/botaoSala0.png", "imagens/GUI/botaoFases/botaoSala1.png")
    fase3Botao = criarBotao(posicao_fase3[0]+ 15, posicao_fase3[1], "imagens/GUI/botaoFases/botaoPraia0.png", "imagens/GUI/botaoFases/botaoPraia1.png")
    voltarBotao = criarBotao(posicao_voltar[0], posicao_voltar[1], "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
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
            som_click.play()  # Som de clique
            print("Fase 1 selecionada")
            estadoJogo = "fase1"
            run = False
            return "fase1"
        elif fase2Botao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Fase 2 selecionada")
            estadoJogo = "fase2"
            run = False
            return "fase2"
        elif fase3Botao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Fase 3 selecionada")
            estadoJogo = "fase3"
            run = False
            return "fase3"
        elif voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "menu"
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def fase1():
    global estadoJogo, jogoConcluido, pontuacao_fase1
    pontuacao_fase1 = 0
    jogoConcluido = False
    fase1Background = pygame.image.load("imagens/fase1/imagemZoologico.png")
     

    mostrarVideo("video/fase1.mp4", 600, 300, "imagens/fase1/imagemTutorialZoo.png", "sons/tutorial/fase1.wav")

    # Verificar som
    if somAtivo:
        tocar_musica("sons/musicaZoo/fundoZoo.mp3")  # Toca a primeira música

    voltarBotao = criarBotao(20, 660, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(940, 660, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    
    # Configurações para o texto do temporizador
    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
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
        "imagens/fase1/corretas/Tamanduá.png",
        "imagens/fase1/corretas/Capivara.png",
        "imagens/fase1/corretas/Preguiça.png",
        "imagens/fase1/corretas/Elefante.png",
        "imagens/fase1/corretas/Esquilo.png",
        "imagens/fase1/corretas/Gambá.png",
        "imagens/fase1/corretas/Panda.png",
        "imagens/fase1/corretas/Panda .png",
        "imagens/fase1/corretas/Pássaro.png",
        "imagens/fase1/corretas/Girafa.png",
        "imagens/fase1/corretas/Raposa.png",
        "imagens/fase1/corretas/Cervo.png",
    ]

    imagensIncorretas = [
        "imagens/fase1/incorretas/Caixa.png",
        "imagens/fase1/incorretas/Copo Amassado.png",
        "imagens/fase1/incorretas/Fralda.png",
        "imagens/fase1/incorretas/Garrafa de Vidro.png",
        "imagens/fase1/incorretas/Garrafa Pet.png",
        "imagens/fase1/incorretas/Garrafa Pet .png",
        "imagens/fase1/incorretas/Latinha.png",
        "imagens/fase1/incorretas/Latinha .png",
        "imagens/fase1/incorretas/Lixo.png",
        "imagens/fase1/incorretas/Papel.png",
        "imagens/fase1/incorretas/Saco de Papel.png",
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

    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        while imagens_selecionadas:
            imagem = imagens_selecionadas.pop(0)
            
            # Extrair o nome do arquivo da imagem (sem extensão)
            nome_objeto = imagem.split("/")[-1].split(".")[0].replace("_", " ").capitalize()

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
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0, "nome": nome_objeto})
            else:
                print(f"Falha ao posicionar objeto após {tentativa} tentativas: {imagem}")

    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

    # Calcular a posição centralizada para o botão de confirmar na parte inferior
    largura_botao_confirmar = 56  # Tamanho estimado do botão (ajuste conforme necessário)
    altura_botao_confirmar = 56    # Altura estimada do botão (ajuste conforme necessário)
    x_botao_confirmar = (largura_tela - 65 - largura_botao_confirmar) // 2  # Centraliza na horizontal
    y_botao_confirmar = altura_tela - altura_botao_confirmar - 25     # Posiciona perto da parte inferior
    
    # Criar o botão de confirmar no centro inferior da tela
    confirmarBotao = criarBotao(x_botao_confirmar, y_botao_confirmar, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

     # Configurações do temporizador
    tempo_inicial = 120  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa
    
    mostrar_informacoes = True
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

        if not jogoGanhou and not jogoPerdeu:
            # Exibir as vidas
            tela.blit(vida_imagens[vidas], (220, 640))  # Exibe a imagem das vidas no canto superior esquerdo
            # Configurações para o texto de "VIDAS"
            texto_vidas = "VIDAS"
            texto_vidas_contorno = fonte.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
            texto_vidas_preenchimento = fonte.render(texto_vidas, True, cor_texto)  # Texto branco

            # Posição do texto "VIDAS" ajustada
            posicao_vidas = (largura_tela // 3.85 - texto_vidas_contorno.get_width() // 80, altura_tela - 34)

            # Desenhar o texto com contorno
            tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_vidas_preenchimento, posicao_vidas)

        # Adicionar o botão "Tentar Novamente" para as telas de vitória e derrota
        botaoTentarNovamente = criarBotao(
            402,  # Centraliza horizontalmente
            350,  # Posiciona um pouco abaixo do texto
            "imagens/GUI/botaoTentarnovamente/tentarnovamente.png",
            "imagens/GUI/botaoTentarnovamente/tentarnovamente1.png"
        )

        # Criar o botão de "Próxima Fase"
        proximaFaseBotao = criarBotao(
            410,  # Centraliza horizontalmente
            460,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoProximaFase/proximafase0.png",  # Imagem do botão
            "imagens/GUI/botaoProximaFase/proximafase1.png"  # Imagem do botão (hover)
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao = criarBotao(
            405,  # Centraliza horizontalmente
            550,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        voltarMenuBotao2 = criarBotao(
            405,  # Centraliza horizontalmente
            460,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            jogoConcluido = True
            mostrar_informacoes = False
            if jogoGanhou:
                if pontuacao_fase1 == 6:
                    pontuacao_fase1 = 10
                elif pontuacao_fase1 == 5:
                    pontuacao_fase1 = 9
                elif pontuacao_fase1 == 4:
                    pontuacao_fase1 = 8
                # Exibir o botão de "Próxima Fase" na tela de vitória
                proximaFaseBotao.atualizarImagem(posicaoMouse)
                proximaFaseBotao.desenharBotao(tela)

                # Desenhar o botão "Voltar ao Menu"
                voltarMenuBotao.atualizarImagem(posicaoMouse)
                voltarMenuBotao.desenharBotao(tela)

                # Verificar clique no botão "Voltar ao Menu"
                if voltarMenuBotao.clicarBotao(tela):
                    som_click.play()  # Tocar som de clique
                    print("Botão 'Voltar ao Menu' clicado.")
                    estadoJogo = "menu"  # Voltar para o menu
                    run = False  # Sai do loop atual
                    menuPrincipal()  # Chama a função do menu principa

            if jogoPerdeu:
                pontuacao_fase1 = 0
                # Desenhar o botão "Voltar ao Menu"
                voltarMenuBotao2.atualizarImagem(posicaoMouse)
                voltarMenuBotao2.desenharBotao(tela)

                # Verificar clique no botão "Voltar ao Menu"
                if voltarMenuBotao2.clicarBotao(tela):
                    som_click.play()  # Tocar som de clique
                    print("Botão 'Voltar ao Menu' clicado.")
                    estadoJogo = "menu"  # Voltar para o menu
                    run = False  # Sai do loop atual
                    menuPrincipal()  # Chama a função do menu principa

            # Verificar clique no botão "Próxima Fase"
            if proximaFaseBotao.clicarBotao(tela):
                som_click.play()  # Tocar som de clique
                print("Botão 'Próxima Fase' clicado.")
                estadoJogo = "fase2"  # Mudar o estado do jogo para a fase 2
                run = False  # Sai do loop atual
                fase2()  # Chama a função para a próxima fase (fase2)
                
            # Desenhar o botão "Tentar Novamente"
            botaoTentarNovamente.atualizarImagem(posicaoMouse)
            botaoTentarNovamente.desenharBotao(tela)

            # Verificar clique no botão "Tentar Novamente"
            if botaoTentarNovamente.clicarBotao(tela):
                som_click.play()  # Tocar o som de clique
                print("Botão 'Tentar Novamente' clicado.")
                run = False  # Sai do loop atual
                fase1()  # Reinicia a fase

            tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
            erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
            
            # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
            texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

            # Renderizando o texto para mostrar no centro da tela
            texto_contorno_conclusao = fonte.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_conclusao = fonte.render(texto_conclusao, True, cor_texto)  # Texto branco
            posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 50)  # Centraliza o texto

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

        if mostrar_informacoes:
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

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)

        # Apenas processa o botão confirmar se o jogo ainda não foi ganho ou perdido
        if not jogoGanhou and not jogoPerdeu:
            confirmarBotao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do botão de confirmar
            confirmarBotao.desenharBotao(tela)  # Desenha o botão de confirmar

        # Atualizar e desenhar objetos com movimento
        for obj in objetos:
            botao = obj["botao"]
            botao.atualizarImagem(posicaoMouse)
            botao.desenharBotao(tela)

            # Verifica se o mouse está sobre o objeto (hover)
            if botao.rect.collidepoint(posicaoMouse):  # Verifica se o mouse está sobre o botão
                exibir_nome_objeto(obj)  # Exibe o nome do objeto acima dele

        # Verificar clique nos objetos
        for obj in objetos:
            if obj["botao"].clicarBotao(tela):
                som_click.play()  # Som de clique
                # Substituir o objeto selecionado
                if objetosSelecionados:
                    print(f"Objeto {objetosSelecionados[0]['tipo']} desmarcado.")
                    objetosSelecionados.clear()  # Limpa a seleção atual

                objetosSelecionados.append(obj)  # Seleciona o novo objeto
                print(f"Objeto {obj['tipo']} selecionado na posição ({obj['x']}, {obj['y']})!")

        # Verificar clique no botão de confirmar
        if confirmarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            for obj in objetosSelecionados:
                if obj["tipo"] == "correto":
                    imagensCorretasClicadas += 1
                    pontuacao_fase1 += 1
                    if imagensCorretasClicadas == 6:  # Clicou em todas as imagens corretas
                        jogoGanhou = True
                    # Tocar som de resposta certa
                    tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3")
                elif obj["tipo"] == "incorreto":
                    imagensIncorretasClicadas += 1
                    pontuacao_fase1 -= 1
                    vidas -= 1  # Perde uma vida a cada erro
                    if vidas == 0:
                        jogoPerdeu = True
                    # Tocar som de resposta errada
                    tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3")
                objetos.remove(obj)  # Remove o objeto selecionado
            objetosSelecionados.clear()  # Limpa a lista de objetos selecionados
            print("Seleção confirmada. Você pode selecionar outro objeto.")

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "jogando"
            if jogoConcluido == False:
                pontuacao_fase1 = 0
            run = False

        elif configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoesFases()
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def fase2():
    global estadoJogo, jogoConcluido, pontuacao_fase2
    pontuacao_fase2 = 0
    jogoConcluido = False
    fase1Background = pygame.image.load("imagens/fase2/imagemSaladeAula.png")

    mostrarVideo("video/fase2.mp4", 600, 300, "imagens/fase2/imagemTutorialSala.png", "sons/tutorial/fase2.wav")

    # Verificar som
    if somAtivo:
        tocar_musica("sons/musicaSala/fundoSala.mp3")  # Toca a primeira música

    voltarBotao = criarBotao(20, 660, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(940, 660, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    
    # Configurações para o texto do temporizador
    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Configurações para objetos
    largura_tela, altura_tela = tela.get_size()
    centro_x = largura_tela // 3 + 30
    centro_y = altura_tela // 2 - 20
    raio_x = largura_tela // 3 + 40
    raio_y = altura_tela // 4
    distancia_minima = 140  # Distância mínima entre objetos

    # Inicializa a fonte para o texto do contador
    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)  # 'None' usa a fonte padrão; 36 é o tamanho 
    cor_texto = (255, 255, 255)  # Cor do texto (branco)

    # Lista de imagens
    imagensCorretas = [
        "imagens/fase2/corretas/Banana.png",
        "imagens/fase2/corretas/Copo Amassado.png",
        "imagens/fase2/corretas/Fralda.png",
        "imagens/fase2/corretas/Garrafa de Vidro.png",
        "imagens/fase2/corretas/Latinha.png",
        "imagens/fase2/corretas/Latinha .png",
        "imagens/fase2/corretas/Lixo.png",
        "imagens/fase2/corretas/Maçã Comida.png",
        "imagens/fase2/corretas/Saco de Papel.png",
    ]

    imagensIncorretas = [
        "imagens/fase2/incorretas/Borracha.png",
        "imagens/fase2/incorretas/Estojo.png",
        "imagens/fase2/incorretas/Caderno.png",
        "imagens/fase2/incorretas/Mochila.png",
        "imagens/fase2/incorretas/Caneta.png",
        "imagens/fase2/incorretas/Apontador.png",
        "imagens/fase2/incorretas/Lápis.png",
        "imagens/fase2/incorretas/Tesoura.png",

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
            
            # Extrair o nome do arquivo da imagem (sem extensão)
            nome_objeto = imagem.split("/")[-1].split(".")[0].replace("_", " ").capitalize()

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
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0, "nome": nome_objeto})
            else:
                print(f"Falha ao posicionar objeto após {tentativa} tentativas: {imagem}")


    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

    # Calcular a posição centralizada para o botão de confirmar na parte inferior
    largura_botao_confirmar = 56  # Tamanho estimado do botão (ajuste conforme necessário)
    altura_botao_confirmar = 56    # Altura estimada do botão (ajuste conforme necessário)
    x_botao_confirmar = (largura_tela - 65 - largura_botao_confirmar) // 2  # Centraliza na horizontal
    y_botao_confirmar = altura_tela - altura_botao_confirmar - 25     # Posiciona perto da parte inferior
    
    # Criar o botão de confirmar no centro inferior da tela
    confirmarBotao = criarBotao(x_botao_confirmar, y_botao_confirmar, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

     # Configurações do temporizador
    tempo_inicial = 120  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa

    run = True
    mostrar_informacoes = True

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

        if not jogoGanhou and not jogoPerdeu:
            # Exibir as vidas
            tela.blit(vida_imagens[vidas], (220, 640))  # Exibe a imagem das vidas no canto superior esquerdo
            # Configurações para o texto de "VIDAS"
            texto_vidas = "VIDAS"
            texto_vidas_contorno = fonte.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
            texto_vidas_preenchimento = fonte.render(texto_vidas, True, cor_texto)  # Texto branco

            # Posição do texto "VIDAS" ajustada
            posicao_vidas = (largura_tela // 3.85 - texto_vidas_contorno.get_width() // 80, altura_tela - 34)

            # Desenhar o texto com contorno
            tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_vidas_preenchimento, posicao_vidas)

         # Adicionar o botão "Tentar Novamente" para as telas de vitória e derrota
        botaoTentarNovamente = criarBotao(
            402,  # Centraliza horizontalmente
            350,  # Posiciona um pouco abaixo do texto
            "imagens/GUI/botaoTentarnovamente/tentarnovamente.png",
            "imagens/GUI/botaoTentarnovamente/tentarnovamente1.png"
        )

        # Criar o botão de "Próxima Fase"
        proximaFaseBotao = criarBotao(
            410,  # Centraliza horizontalmente
            460,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoProximaFase/proximafase0.png",  # Imagem do botão
            "imagens/GUI/botaoProximaFase/proximafase1.png"  # Imagem do botão (hover)
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao = criarBotao(
            405,  # Centraliza horizontalmente
            550,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        voltarMenuBotao2 = criarBotao(
            405,  # Centraliza horizontalmente
            460,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            jogoConcluido = True
            mostrar_informacoes = False
            if jogoGanhou:
                if pontuacao_fase2 == 6:
                    pontuacao_fase2 = 10
                elif pontuacao_fase2 == 5:
                    pontuacao_fase2 = 9
                elif pontuacao_fase2 == 4:
                    pontuacao_fase2 = 8
                # Exibir o botão de "Próxima Fase" na tela de vitória
                proximaFaseBotao.atualizarImagem(posicaoMouse)
                proximaFaseBotao.desenharBotao(tela)

                # Desenhar o botão "Voltar ao Menu"
                voltarMenuBotao.atualizarImagem(posicaoMouse)
                voltarMenuBotao.desenharBotao(tela)

                # Verificar clique no botão "Voltar ao Menu"
                if voltarMenuBotao.clicarBotao(tela):
                    som_click.play()  # Tocar som de clique
                    print("Botão 'Voltar ao Menu' clicado.")
                    estadoJogo = "menu"  # Voltar para o menu
                    run = False  # Sai do loop atual
                    menuPrincipal()  # Chama a função do menu principa

            if jogoPerdeu:
                pontuacao_fase2 = 0
                # Desenhar o botão "Voltar ao Menu"
                voltarMenuBotao2.atualizarImagem(posicaoMouse)
                voltarMenuBotao2.desenharBotao(tela)

                # Verificar clique no botão "Voltar ao Menu"
                if voltarMenuBotao2.clicarBotao(tela):
                    som_click.play()  # Tocar som de clique
                    print("Botão 'Voltar ao Menu' clicado.")
                    estadoJogo = "menu"  # Voltar para o menu
                    run = False  # Sai do loop atual
                    menuPrincipal()  # Chama a função do menu principa

            # Verificar clique no botão "Próxima Fase"
            if proximaFaseBotao.clicarBotao(tela):
                som_click.play()  # Tocar som de clique
                print("Botão 'Próxima Fase' clicado.")
                estadoJogo = "fase2"  # Mudar o estado do jogo para a fase 2
                run = False  # Sai do loop atual
                fase3()  # Chama a função para a próxima fase (fase2)
                
            # Desenhar o botão "Tentar Novamente"
            botaoTentarNovamente.atualizarImagem(posicaoMouse)
            botaoTentarNovamente.desenharBotao(tela)

            # Verificar clique no botão "Tentar Novamente"
            if botaoTentarNovamente.clicarBotao(tela):
                som_click.play()  # Tocar o som de clique
                print("Botão 'Tentar Novamente' clicado.")
                run = False  # Sai do loop atual
                fase2()  # Reinicia a fase

            tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
            erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
            
            # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
            texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

            # Renderizando o texto para mostrar no centro da tela
            texto_contorno_conclusao = fonte.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_conclusao = fonte.render(texto_conclusao, True, cor_texto)  # Texto branco
            posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 50)  # Centraliza o texto

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

        if mostrar_informacoes:
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

        # Apenas processa o botão confirmar se o jogo ainda não foi ganho ou perdido
        if not jogoGanhou and not jogoPerdeu:
            confirmarBotao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do botão de confirmar
            confirmarBotao.desenharBotao(tela)  # Desenha o botão de confirmar
        
        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)

        # Atualizar e desenhar objetos com movimento
        for obj in objetos:
            botao = obj["botao"]
            botao.atualizarImagem(posicaoMouse)
            botao.desenharBotao(tela)

            # Verifica se o mouse está sobre o objeto (hover)
            if botao.rect.collidepoint(posicaoMouse):  # Verifica se o mouse está sobre o botão
                exibir_nome_objeto(obj)  # Exibe o nome do objeto acima dele

        # Verificar clique nos objetos
        for obj in objetos:
            if obj["botao"].clicarBotao(tela):
                som_click.play()  # Som de clique
                # Substituir o objeto selecionado
                if objetosSelecionados:
                    print(f"Objeto {objetosSelecionados[0]['tipo']} desmarcado.")
                    objetosSelecionados.clear()  # Limpa a seleção atual

                objetosSelecionados.append(obj)  # Seleciona o novo objeto
                print(f"Objeto {obj['tipo']} selecionado na posição ({obj['x']}, {obj['y']})!")

        # Verificar clique no botão de confirmar
        if confirmarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            for obj in objetosSelecionados:
                if obj["tipo"] == "correto":
                    imagensCorretasClicadas += 1
                    pontuacao_fase2 += 1
                    if imagensCorretasClicadas == 6:  # Clicou em todas as imagens corretas
                        jogoGanhou = True
                    # Tocar som de resposta certa
                    tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3")
                elif obj["tipo"] == "incorreto":
                    imagensIncorretasClicadas += 1
                    pontuacao_fase2 -= 1
                    vidas -= 1  # Perde uma vida a cada erro
                    if vidas == 0:
                        jogoPerdeu = True
                    # Tocar som de resposta errada
                    tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3")
                objetos.remove(obj)  # Remove o objeto selecionado
            objetosSelecionados.clear()  # Limpa a lista de objetos selecionados
            print("Seleção confirmada. Você pode selecionar outro objeto.")

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "jogando"
            if jogoConcluido == False:
                pontuacao_fase2 = 0
            run = False

        elif configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoesFases()
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def fase3():
    global estadoJogo, jogoConcluido, pontuacao_fase3
    pontuacao_fase3 = 0
    jogoConcluido = False
    fase1Background = pygame.image.load("imagens/fase3/imagemPraia.jpg")

    mostrarVideo("video/fase3.mp4", 600, 300, "imagens/fase3/imagemTutorialPraia.png", "sons/tutorial/fase3.wav")

    # Verificar som
    if somAtivo:
        tocar_musica("sons/musicaPraia/fundoPraia.mp3")  # Toca a primeira música

    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(940, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    
    # Configurações para o texto do temporizador
    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Configurações para objetos
    largura_tela, altura_tela = tela.get_size()
    centro_x = largura_tela // 3 + 30
    centro_y = altura_tela // 2 - 80
    raio_x = largura_tela // 3 + 10
    raio_y = altura_tela // 4 - 20
    distancia_minima = 120  # Distância mínima entre objetos

    # Lista de imagens
    imagensCorretas = [
        "imagens/fase3/corretas/Balde de Areia.png",
        "imagens/fase3/corretas/Cadeira de Praia.png",
        "imagens/fase3/corretas/Coco.png",
        "imagens/fase3/corretas/Coqueiro.png",
        "imagens/fase3/corretas/Guarda Sol.png",
        "imagens/fase3/corretas/Objetos de Praia.png",
        "imagens/fase3/corretas/Óculos de Praia.png",
        "imagens/fase3/corretas/Toalha de Praia.png",
    ]

    imagensIncorretas = [
        "imagens/fase3/incorretas/Banana.png",
        "imagens/fase3/incorretas/Caixa.png",
        "imagens/fase3/incorretas/Copo Amassado.png",
        "imagens/fase3/incorretas/Fralda.png",
        "imagens/fase3/incorretas/Garrafa de Vidro.png",
        "imagens/fase3/incorretas/Garrafa Pet.png",
        "imagens/fase3/incorretas/Latinha.png",
        "imagens/fase3/incorretas/Latinha .png",
        "imagens/fase3/incorretas/Lixo.png",
        "imagens/fase3/incorretas/Papel.png",
        "imagens/fase3/incorretas/Maçã Comida.png",
        "imagens/fase3/incorretas/Papel.png",
        "imagens/fase3/incorretas/Saco de Papel.png",
    ]

    # Selecionando aleatoriamente 6 imagens corretas e 4 incorretas
    imagensCorretasSelecionadas = random.sample(imagensCorretas, 5)  # Seleciona 6 imagens corretas aleatórias
    imagensIncorretasSelecionadas = random.sample(imagensIncorretas, 5)  # Seleciona 4 imagens incorretas aleatórias

    objetos = []

    imagensCorretasClicadas = 0  # Contador de imagens corretas clicadas
    imagensIncorretasClicadas = 0  # Contador de imagens incorretas clicadas
    todasImagens = 0
    jogoGanhou = False  # variável para rastrear se o jogo foi vencido
    jogoPerdeu = False  # variável para rastrear se o jogo foi perdido

    # Definir o número de vidas
    vidas = 3  # O jogo começa com 3 vidas
    vida_imagens = [
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/0vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/1vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/2vidas.png"), (220, 60)),
        pygame.transform.scale(pygame.image.load("imagens/GUI/vidas/3vidas.png"), (220, 60))
    ]

    # Carregar as imagens das áreas
    imagem_area_PRAIA = pygame.image.load("imagens/fase3/areas/areaPRAIA.png")
    imagem_area_LIXO = pygame.image.load("imagens/fase3/areas/areaLIXO.png")

    # Obter o tamanho original das imagens
    tamanho_area_PRAIA = imagem_area_PRAIA.get_rect().size
    tamanho_area_LIXO = imagem_area_LIXO.get_rect().size

    # Fator de escala para diminuir o tamanho
    fator_escala = 0.5

    # Calcular o novo tamanho das imagens
    novo_tamanho_area_PRAIA = (int(tamanho_area_PRAIA[0] * fator_escala), int(tamanho_area_PRAIA[1] * fator_escala))
    novo_tamanho_area_LIXO = (int(tamanho_area_LIXO[0] * fator_escala), int(tamanho_area_LIXO[1] * fator_escala))

    # Escalar as imagens
    imagem_area_PRAIA = pygame.transform.scale(imagem_area_PRAIA, novo_tamanho_area_PRAIA)
    imagem_area_LIXO = pygame.transform.scale(imagem_area_LIXO, novo_tamanho_area_LIXO)

    # Posicionar as áreas na tela
    posicao_area_PRAIA = (largura_tela - novo_tamanho_area_PRAIA[0] - 40, altura_tela - novo_tamanho_area_PRAIA[1] - 20)
    posicao_area_LIXO = (40, altura_tela - novo_tamanho_area_LIXO[1] - 20)

    # Criar os objetos de área (Rect) para facilitar a colisão
    rect_area_PRAIA = pygame.Rect(posicao_area_PRAIA, novo_tamanho_area_PRAIA)
    rect_area_LIXO = pygame.Rect(posicao_area_LIXO, novo_tamanho_area_LIXO)

    # Função para verificar se o objeto está dentro da área da praia
    def colisao_com_area_PRAIA(objeto):
        # Criar o retângulo do objeto (assumindo que o objeto tem a posição 'x' e 'y' e a imagem do botão)
        rect_objeto = pygame.Rect(objeto["x"], objeto["y"], objeto["botao"].imagem.get_width(), objeto["botao"].imagem.get_height())
        
        # Verificar se o objeto está completamente dentro da área da praia
        if rect_area_PRAIA.colliderect(rect_objeto):
            return True
        return False

    # Função para verificar se o objeto está dentro da área do lixo
    def colisao_com_area_LIXO(objeto):
        # Criar o retângulo do objeto (assumindo que o objeto tem a posição 'x' e 'y' e a imagem do botão)
        rect_objeto = pygame.Rect(objeto["x"], objeto["y"], objeto["botao"].imagem.get_width(), objeto["botao"].imagem.get_height())
        
        # Verificar se o objeto está completamente dentro da área do lixo
        if rect_area_LIXO.colliderect(rect_objeto):
            return True
        return False


    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        while imagens_selecionadas:
            imagem = imagens_selecionadas.pop(0)
            
            # Extrair o nome do arquivo da imagem (sem extensão)
            nome_objeto = imagem.split("/")[-1].split(".")[0].replace("_", " ").capitalize()

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

                # Verifica se está longe o suficiente das áreas de "correto" e "errado"
                distancia_area_correta = math.sqrt((x - posicao_area_PRAIA[0])**2 + (y - posicao_area_PRAIA[1])**2)
                distancia_area_errada = math.sqrt((x - posicao_area_LIXO[0])**2 + (y - posicao_area_LIXO[1])**2)
                
                if distancia_area_correta < distancia_minima or distancia_area_errada < distancia_minima:
                    posicao_valida = False  # Se o objeto estiver muito perto das áreas, a posição é inválida

            if posicao_valida:
                # Cria o botão para o objeto
                botao = criarBotaoImagensFASE3(x, y, imagem, imagem)
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0, "nome": nome_objeto})
            else:
                print(f"Falha ao posicionar objeto após {tentativa} tentativas: {imagem}")

    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

     # Configurações do temporizador
    tempo_inicial = 120  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa
    
    # Variáveis para controle de arrasto
    arrastando_objeto = None  # O objeto que está sendo arrastado
    deslocamento_x = 0
    deslocamento_y = 0

    mostrar_informacoes = True
    run = True
    while run:
        tela.blit(fase1Background, (0, 0))
        if jogoPerdeu:
            tela.blit(pygame.image.load("imagens/fase3/perdeuPraia.jpg"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        elif jogoGanhou:
            tela.blit(pygame.image.load("imagens/fase3/ganhouPraia.jpg"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        else:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicializado) // 1000
            tempo_restante = max(tempo_inicial - tempo_decorrido, 0)

            if tempo_restante == 0:
                jogoPerdeu = True

        # Apenas processa o botão confirmar se o jogo ainda não foi ganho ou perdido
        if not jogoGanhou and not jogoPerdeu:
            # No loop principal, substituir o desenho dos retângulos pelas imagens
            tela.blit(imagem_area_PRAIA, posicao_area_PRAIA)  # Exibir a área errada
            tela.blit(imagem_area_LIXO, posicao_area_LIXO)  # Exibir a área correta
        
        if not jogoGanhou and not jogoPerdeu:
            # Exibir as vidas
            tela.blit(vida_imagens[vidas], (440, 640))  # Exibe a imagem das vidas no canto superior esquerdo
            # Configurações para o texto de "VIDAS"
            texto_vidas = "VIDAS"
            texto_vidas_contorno = fonte.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
            texto_vidas_preenchimento = fonte.render(texto_vidas, True, cor_texto)  # Texto branco

            # Posição do texto "VIDAS" ajustada
            posicao_vidas = (largura_tela // 2 - texto_vidas_contorno.get_width() + 65 // 1.32, altura_tela - 34)

            # Desenhar o texto com contorno
            tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
            tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_vidas_preenchimento, posicao_vidas)

        # Adicionar o botão "Tentar Novamente" para as telas de vitória e derrota
        botaoTentarNovamente = criarBotao(
            402,  # Centraliza horizontalmente
            350,  # Posiciona um pouco abaixo do texto
            "imagens/GUI/botaoTentarnovamente/tentarnovamente.png",
            "imagens/GUI/botaoTentarnovamente/tentarnovamente1.png"
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao = criarBotao(
            405,  # Centraliza horizontalmente
            469,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            mostrar_informacoes = False
            jogoConcluido = True
            
            if jogoPerdeu:
                pontuacao_fase3 = 0    
            voltarMenuBotao.atualizarImagem(posicaoMouse)
            voltarMenuBotao.desenharBotao(tela)

            # Verificar clique no botão "Voltar ao Menu"
            if voltarMenuBotao.clicarBotao(tela):
                som_click.play()  # Tocar som de clique
                print("Botão 'Voltar ao Menu' clicado.")
                estadoJogo = "menu"  # Voltar para o menu
                run = False  # Sai do loop atual
                menuPrincipal()  # Chama a função do menu principa

            # Desenhar o botão "Tentar Novamente"
            botaoTentarNovamente.atualizarImagem(posicaoMouse)
            botaoTentarNovamente.desenharBotao(tela)

            # Verificar clique no botão "Tentar Novamente"
            if botaoTentarNovamente.clicarBotao(tela):
                som_click.play()  # Tocar o som de clique
                print("Botão 'Tentar Novamente' clicado.")
                run = False  # Sai do loop atual
                fase3()  # Reinicia a fase

            tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
            erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
            
            # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
            texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

            # Renderizando o texto para mostrar no centro da tela
            texto_contorno_conclusao = fonte.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_conclusao = fonte.render(texto_conclusao, True, cor_texto)  # Texto branco
            posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 50)  # Centraliza o texto

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
            tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

        if mostrar_informacoes:
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
            texto_contorno = fonte.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/10", True, (0, 0, 0))  # Preto para o contorno
            texto_preenchimento = fonte.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/10", True, cor_texto)  # Cor original

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

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "jogando"
            if jogoConcluido == False:
                pontuacao_fase3 = 0
            run = False

        if configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoesFases()
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                confirmar_saida(tela)

            # Quando o mouse é pressionado (click) e um objeto é clicado
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica se o botão pressionado é o esquerdo
                    posicaoMouse = pygame.mouse.get_pos()
                    som_click.play()  # Tocar o som de clique

                    for obj in objetos:
                        if obj["botao"].rect.collidepoint(posicaoMouse):  # Verifica se o mouse clicou no objeto
                            arrastando_objeto = obj  # Inicia o arraste do objeto
                            deslocamento_x = posicaoMouse[0] - obj["x"]  # Calcula o deslocamento
                            deslocamento_y = posicaoMouse[1] - obj["y"]

            # Durante o movimento do mouse, se estiver arrastando
            elif event.type == pygame.MOUSEMOTION:
                if arrastando_objeto and pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo está pressionado
                    posicaoMouse = pygame.mouse.get_pos()
                    # Atualiza a posição do objeto e o texto associado ao objeto
                    arrastando_objeto["x"] = posicaoMouse[0] - deslocamento_x
                    arrastando_objeto["y"] = posicaoMouse[1] - deslocamento_y

            # Quando o mouse é solto, para o arraste
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Verifica se o botão solto é o esquerdo
                    if arrastando_objeto:
                        # Verifica se o objeto foi colocado na área correta ou incorreta
                        if colisao_com_area_PRAIA(arrastando_objeto):
                            if arrastando_objeto["tipo"] == "correto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensCorretasClicadas += 1  # Incrementa a pontuação de objetos corretos
                                pontuacao_fase3 += 1
                                todasImagens += 1
                                tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3")
                            elif arrastando_objeto["tipo"] == "incorreto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensIncorretasClicadas += 1  # Incrementa a pontuação de objetos incorretos
                                todasImagens += 1
                                vidas -= 1
                                if vidas == 0:
                                    jogoPerdeu = True
                                tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3")
                        elif colisao_com_area_LIXO(arrastando_objeto):
                            if arrastando_objeto["tipo"] == "correto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensIncorretasClicadas += 1  # Incrementa a pontuação de objetos incorretos
                                todasImagens += 1
                                vidas -= 1
                                if vidas == 0:
                                    jogoPerdeu = True
                                tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3")
                            elif arrastando_objeto["tipo"] == "incorreto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensCorretasClicadas += 1  # Incrementa a pontuação de objetos corretos
                                pontuacao_fase3 += 1
                                todasImagens += 1
                                tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3")

                        if imagensCorretasClicadas == 10:
                            jogoGanhou = True
                        elif imagensCorretasClicadas >= 5 and todasImagens == 10:
                            jogoGanhou = True
                        elif imagensCorretasClicadas < 5 and todasImagens == 10:
                            jogoPerdeu = True

                        # Para o arraste ao soltar o botão do mouse
                        arrastando_objeto = None
            
        # Atualizar e desenhar os objetos com as novas posições
        for obj in objetos:
            botao = obj["botao"]
            botao.rect.topleft = (obj["x"], obj["y"])  # Atualiza a posição do objeto gráfico
            botao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do objeto (se necessário)
            botao.desenharBotao(tela)  # Desenha o objeto na nova posição

            # Verifica se o mouse está sobre o objeto (hover)
            if botao.rect.collidepoint(posicaoMouse):
                exibir_nome_objeto(obj)  # Exibe o nome do objeto acima dele
            
            # Atualiza a tela
        pygame.display.update() 
        clock.tick(60)
        
# Função para o menu principal
def menuPrincipal():
    global estadoJogo
    menuBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")

    if somAtivo:
        tocar_musica("sons/musicaMenu/musicafundo.mp3")  # Toca a primeira música

    # Criando botões do menu
    jogarBotao = criarBotao(400, 300, "imagens/GUI/botaoJogar/jogar0.png", "imagens/GUI/botaoJogar/jogar1.png")
    configuracoesBotao = criarBotao(900, 50, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    instrucoesBotao = criarBotao(410, 425, "imagens/GUI/botaoInicio/instrucoes1.png", "imagens/GUI/botaoInicio/instrucoes01.png")
    sairBotao = criarBotao(40, 50, "imagens/GUI/botaoSair/sair0.png", "imagens/GUI/botaoSair/sair1.png")
    creditosBotao = criarBotao(1000, 640, "imagens/GUI/botaoConfiguracoes/info0.png", "imagens/GUI/botaoConfiguracoes/info1.png")  
    pontuacaoBotao = criarBotao(402, 550, "imagens/GUI/botaoPontuacao/pontuacao0.png", "imagens/GUI/botaoPontuacao/pontuacao1.png")
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
        pontuacaoBotao.atualizarImagem(posicaoMouse)

        jogarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        instrucoesBotao.desenharBotao(tela)
        sairBotao.desenharBotao(tela)
        creditosBotao.desenharBotao(tela)
        pontuacaoBotao.desenharBotao(tela)

        # Verificar cliques
        if jogarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Jogar clicado")
            estadoJogo = "jogando"
            run = False
            
        if configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoes()
            run = False

        if instrucoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Instruções clicado")
            abrirInstrucoes()
            run = False

        if creditosBotao.clicarBotao(tela):  # Detecta clique no botão de créditos
            som_click.play()  # Som de clique
            print("Créditos clicado")
            abrirCreditos()
            run = False

        if sairBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Sair clicado")
            confirmar_saida(tela)
            global rodando
            rodando = True
            run = False

        if pontuacaoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("relatório clicado")
            relatorio()
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

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

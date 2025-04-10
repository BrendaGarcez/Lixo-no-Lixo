from turtle import Screen
import pygame  # Importando biblioteca
import botao  # Importando a classe Botao
import botaoObjetos
import sys
import random
import cv2
import json
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


pygame.init()  # Inicializa os módulos do pygame
pygame.mixer.init()

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Muda o cursor para a mão
# Resolução da tela
telaLargura = 1100
telaAltura = 720
tela = pygame.display.set_mode((telaLargura, telaAltura))  # Configuração da tela
pygame.display.set_caption("Lixo_No_Lixo")  # Nome do jogo

som_click = pygame.mixer.Sound("sons/somClickMouse/mouseclick.wav")
som_click.set_volume(0.2)

som_dica = pygame.mixer.Sound("sons/somDicaLampada/dica.mp3")

clock = pygame.time.Clock()
somAtivo = True  # Estado inicial do som
musica_atual = None
volume = 0.21

estadoJogo = "menu"  # situação atual do jogo, para rastrear as telas
rodando = True  # Controla se o programa deve continuar rodando
fase_ativa = False

jogoConcluido = False
pontuacao_fase1 = 0
pontuacao_fase2 = 0
pontuacao_fase3 = 0
nome_jogador = ""

# Adicionar variáveis globais para controlar o estado da lâmpada e o objeto selecionado
lampada_acesa = False
objeto_circulado = None
ultimo_objeto_confirmado = None  # Variável para armazenar o último objeto clicado

# Função para desenhar o círculo vermelho ao redor do objeto
def desenhar_circulo_redondo(objeto):
    x, y = objeto["x"], objeto["y"]
    pygame.draw.circle(tela, (255, 0, 0), (x + 80, y + 60), 60, 5)  # Ajuste o valor de 50, 50 e o raio conforme necessário

def desenhar_circulo_area(x, y):
    pygame.draw.circle(tela, (255, 0, 0), (x, y), 100, 5)  # Ajuste o valor de 50, 50 e o raio conforme necessário

# Função para criar botões
def criarBotao(x, y, imagem, imagemAlterada):
    imagem = pygame.image.load(imagem).convert_alpha()
    imagemAlterada = pygame.image.load(imagemAlterada).convert_alpha()
    return botao.Botao(x, y, imagem, imagemAlterada)

def criarBotaoImagens(x, y, imagem, imagemAlterada):
    imagem = pygame.image.load(imagem).convert_alpha()
    imagemAlterada = pygame.image.load(imagemAlterada).convert_alpha()
    
    # Redimensionar as imagens
    largura, altura = 180, 100  # Exemplo de tamanho, ajuste conforme necessário
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

cooldown_som = 0.7  # Cooldown de 0.8 segundos
ultimo_som_tocado = 0  # Inicializa o tempo do último som

def falar_nome_objeto(obj):
    """Toca o som do nome do objeto, respeitando o cooldown."""
    global ultimo_som_tocado

    caminho_som = f"sons/audioNomeObjetos/{obj['nome']}.mp3"
    tempo_atual = time.time()

    if (tempo_atual - ultimo_som_tocado > cooldown_som):  # Verifica cooldown
        if os.path.exists(caminho_som):
            som_nome = pygame.mixer.Sound(caminho_som)  # Carregar o som
            som_nome.set_volume(0.5)  # Define o volume para 50%
            som_nome.play()  # Tocar o som do nome do objeto
            ultimo_som_tocado = tempo_atual  # Atualiza o tempo do último som tocado

def exibir_nome_objeto(obj):
    """Exibe o nome do objeto acima dele e chama a função para falar o nome."""
    fonte_nome = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 24)
    nome_objeto = obj["nome"]  # Nome do objeto
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

"""Para relatório"""
def carregar_dados_jogadores():
    """Carrega os dados do arquivo JSON e garante que seja um dicionário válido."""
    try:
        with open("jogadores.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            if not isinstance(dados, dict):  # Garante que o arquivo tenha um dicionário
                return {"jogadores": []}
            return dados
    except FileNotFoundError:
        return {"jogadores": []}  # Retorna estrutura padrão se o arquivo não existir
    except json.JSONDecodeError:
        print("Erro ao carregar o JSON. O arquivo pode estar corrompido.")
        return {"jogadores": []}

def salvar_dados_jogadores(dados):
    """Salva os dados no arquivo JSON."""
    with open("jogadores.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def buscar_jogador(nome):
    """Busca um jogador pelo nome no JSON."""
    dados = carregar_dados_jogadores()
    jogadores = dados.get("jogadores", [])

    for jogador in jogadores:
        if jogador.get("nome") == nome:
            return jogador
    return None

def adicionar_jogador(nome):
    """Adiciona um novo jogador ao arquivo JSON."""
    if not nome.strip():  # Verifica se o nome está vazio
        print("O nome do jogador não pode ser vazio.")
        return

    dados = carregar_dados_jogadores()

    if buscar_jogador(nome):
        print(f"O jogador {nome} já está registrado.")
        return

    novo_jogador = {
        "nome": nome,
        "fases": []  # Lista de fases jogadas
    }
    dados["jogadores"].append(novo_jogador)
    salvar_dados_jogadores(dados)
    print(f"O jogador {nome} foi adicionado com sucesso!")

def atualizar_pontuacao_fase(nome, fase, pontuacao, tempo):
    """Atualiza a pontuação e tempo de uma fase de um jogador."""
    dados = carregar_dados_jogadores()
    jogadores = dados.get("jogadores", [])

    jogador = None
    for j in jogadores:
        if j["nome"] == nome:
            jogador = j
            break

    if jogador is None:
        print(f"Jogador {nome} não encontrado.")
        return

    # Verifica se a fase já existe
    fase_existente = False
    for f in jogador.get("fases", []):
        if f["fase"] == fase:
            f["pontuacao"] = pontuacao
            f["tempo"] = tempo
            fase_existente = True
            break

    # Se a fase não existe, adiciona uma nova entrada
    if not fase_existente:
        jogador.setdefault("fases", []).append({
            "fase": fase,
            "pontuacao": pontuacao,
            "tempo": tempo
        })

    # Salva as alterações no arquivo
    salvar_dados_jogadores(dados)
    print(f"Pontuação e tempo da fase {fase} atualizados para {nome}.")


def verificar_clique_botao(x, y, largura, altura):
    """Verifica se houve clique dentro de um botão, dado sua posição e tamanho."""
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if x <= mouse_pos[0] <= x + largura and y <= mouse_pos[1] <= y + altura:
        if mouse_pressed[0]:  # Se o botão esquerdo do mouse foi pressionado
            return True
    return False

def pedir_nome():
    """Solicita o nome do jogador via input no Pygame."""
    global nome_jogador, estadoJogo, somAtivo

    fonte_titulo = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 50)  # Fonte do título
    fonte_nome = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 30)  # Fonte menor para o nome

    texto = ""
    input_ativo = True

    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    confirmarBotao = criarBotao(470, 345, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

    # Variáveis para controle de repetição de teclas
    key_repeat_delay = 0.5  # Tempo de espera antes de começar a repetir
    key_repeat_interval = 0.05  # Intervalo de repetição
    last_key_time = 0
    key_repeating = None

    while input_ativo:
        # Define o novo background
        menu_background = pygame.image.load("imagens/GUI/Backgrounds/nomeBackground.png")
        tela.blit(menu_background, (0, 0))

        botao_largura, botao_altura = 147, 48

        # Exibe o título "Informe seu nome"
        texto_titulo = "Informe seu nome"
        texto_contorno = fonte_titulo.render(texto_titulo, True, (0, 0, 0))  # Contorno preto
        texto_preenchido = fonte_titulo.render(texto_titulo, True, (255, 255, 255))  # Texto branco
        posicao_titulo = (323, 200)

        tela.blit(texto_contorno, (posicao_titulo[0] - 1, posicao_titulo[1]))
        tela.blit(texto_contorno, (posicao_titulo[0] + 1, posicao_titulo[1]))
        tela.blit(texto_contorno, (posicao_titulo[0], posicao_titulo[1] - 1))
        tela.blit(texto_contorno, (posicao_titulo[0], posicao_titulo[1] + 1))
        tela.blit(texto_preenchido, posicao_titulo)

        # Calcular a largura do texto para centralizar
        largura_nome = fonte_nome.size(texto)[0]
        posicao_nome_x = (tela.get_width() - largura_nome) // 2
        posicao_nome_y = 300

        # Exibe o nome digitado com contorno
        texto_contorno = fonte_nome.render(texto, True, (0, 0, 0))  # Contorno preto
        texto_preenchido = fonte_nome.render(texto, True, (255, 255, 255))  # Texto branco

        tela.blit(texto_contorno, (posicao_nome_x - 1, posicao_nome_y))  # Esquerda
        tela.blit(texto_contorno, (posicao_nome_x + 1, posicao_nome_y))  # Direita
        tela.blit(texto_contorno, (posicao_nome_x, posicao_nome_y - 1))  # Cima
        tela.blit(texto_contorno, (posicao_nome_x, posicao_nome_y + 1))  # Baixo
        tela.blit(texto_preenchido, (posicao_nome_x, posicao_nome_y))  # Texto final branco

        # Atualizar os botões
        posicaoMouse = pygame.mouse.get_pos()
        voltarBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.atualizarImagem(posicaoMouse)
        confirmarBotao.atualizarImagem(posicaoMouse)

        voltarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        confirmarBotao.desenharBotao(tela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and texto.strip():
                    nome_jogador = texto.strip()
                    som_click.play()
                    input_ativo = False
                elif event.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]  # Remove a última letra
                    key_repeating = pygame.K_BACKSPACE
                    last_key_time = time.time()
                elif len(texto) < 22:
                    texto += event.unicode  # Adiciona o caractere digitado
                    key_repeating = event.key
                    last_key_time = time.time()

            if event.type == pygame.KEYUP:
                if event.key == key_repeating:
                    key_repeating = None

            # Verifica clique nos botões
            if verificar_clique_botao(20, 20, botao_largura, botao_altura):
                som_click.play()
                print("Voltar clicado")
                print(estadoJogo)
                estadoJogo = "menu"
                input_ativo = False
                return menuPrincipal()

            elif verificar_clique_botao(936, 20, botao_largura, botao_altura):
                som_click.play()
                print("Configurações clicado")
                abrirConfiguracoes()

            elif verificar_clique_botao(470, 345, botao_largura, botao_altura) and texto.strip():
                nome_jogador = texto.strip()
                som_click.play()
                print("Nome confirmado!")
                input_ativo = False

        # Lógica para repetição de teclas
        if key_repeating is not None and time.time() - last_key_time > key_repeat_delay:
            if key_repeating == pygame.K_BACKSPACE:
                texto = texto[:-1]  # Remove a última letra
            elif len(texto) < 22:
                texto += pygame.key.name(key_repeating)  # Adiciona o caractere digitado
            last_key_time = time.time() - (key_repeat_delay - key_repeat_interval)

        pygame.display.update()

    print(f"Nome do jogador: {nome_jogador}")


def salvar_pontuacao(nome_jogador, fase, pontuacao, tempo):
    """Salva a pontuação de uma fase de um jogador."""
    dados = carregar_dados_jogadores()
    jogadores = dados.get("jogadores", [])

    jogador = None
    for j in jogadores:
        if j["nome"] == nome_jogador:
            jogador = j
            break

    if jogador:
        # Atualiza a pontuação da fase correspondente
        fase_existente = False
        for p in jogador["fases"]:
            if p["fase"] == fase:
                p["pontuacao"] = pontuacao
                p["tempo"] = tempo
                fase_existente = True
                break
        
        if not fase_existente:
            jogador["fases"].append({
                "fase": fase,
                "pontuacao": pontuacao,
                "tempo": tempo
            })
    else:
        # Se o jogador não existir, cria um novo
        novo_jogador = {
            "nome": nome_jogador,
            "fases": [
                {"fase": fase, "pontuacao": pontuacao, "tempo": tempo}
            ]
        }
        dados["jogadores"].append(novo_jogador)

    salvar_dados_jogadores(dados)

    print(f"Pontuação salva: {nome_jogador} - Fase {fase} - {pontuacao} pontos - {tempo:.2f} segundos")

def mostrarVideo(video_path, video_width, video_height, imagem_fundo_path, audio_path, audio_normal_jogo):
    global somAtivo
    # Abrir o vídeo com OpenCV
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    fps_video = cap.get(cv2.CAP_PROP_FPS) or 30

    # Inicializar o mixer do Pygame para áudio
    posicaoMouse = pygame.mouse.get_pos()

    # Criar o botão de pular
    pularBotao = criarBotao(477.5, 520, "imagens/GUI/botaoPularTutorial/botaoPular0.png", "imagens/GUI/botaoPularTutorial/botaoPular1.png")

    # Carregar a imagem do avatar (substitui o botão)
    avatarImagem = pygame.image.load("imagens/GUI/imagensExtra/avatarTeste.png")
    avatarImagem = pygame.transform.scale(avatarImagem, (294, 498))  # Ajuste o tamanho conforme necessário

    if not cap.isOpened():
        print("Erro ao abrir o vídeo:", video_path)
        return

    # Carregar a imagem de fundo
    fundo_imagem = pygame.image.load(imagem_fundo_path)

    # Carregar e tocar o áudio do tutorial
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1, 0.0)

    # Calcular a posição central do vídeo na tela
    x_center = (telaLargura - video_width) // 2
    y_center = (telaAltura - video_height) // 2

    # Posição e tamanho do botão de "Pular"
    botao_largura, botao_altura = 145, 47

    # Definir a fonte para o texto
    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 40)
    texto_1 = "Assista o"
    texto_2 = "tutorial"
    cor_texto = (255, 255, 255)  # Cor do texto (branco)
    cor_contorno = (0, 0, 0)  # Cor do contorno (preto)

    clock = pygame.time.Clock()
    run = True
    while run:
        posicaoMouse = pygame.mouse.get_pos()
        pularBotao.atualizarImagem(posicaoMouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                confirmar_saida(tela)

        # Verificar se o botão foi clicado
        if verificar_clique_botao(477.5, 520, botao_largura, botao_altura):
            som_click.play()  # Som de clique
            print("Botão de pular clicado!")
            pygame.mixer.music.stop()  # Parar a música do tutorial
            if somAtivo:
                pygame.mixer.music.load(audio_normal_jogo)  # Carregar o áudio normal do jogo
                pygame.mixer.music.play(-1, 0.0)  # Reproduzir o áudio normal do jogo
            run = False

        # Ler o próximo frame do vídeo
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler frame!")
            pygame.mixer.music.stop()  # Parar a música ao terminar o vídeo
            break


        frame = cv2.resize(frame, (video_width, video_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        tela.blit(fundo_imagem, (0, 0))
        tela.blit(frame_surface, (x_center, y_center))

        # Desenhar a imagem do avatar na tela (posição x=0, y=420)
        tela.blit(avatarImagem, (0, 260))

        # Desenhar o texto com contorno
        # Desenhar o contorno para o texto superior (Assista o)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    contorno_1 = fonte.render(texto_1, True, cor_contorno)
                    tela.blit(contorno_1, (76 + dx, 300 + dy))  # Ajuste a posição conforme necessário

        # Desenhar o texto superior
        texto_surf_1 = fonte.render(texto_1, True, cor_texto)
        tela.blit(texto_surf_1, (76, 300))  # Ajuste a posição conforme necessário

        # Desenhar o contorno para o texto inferior (tutorial)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    contorno_2 = fonte.render(texto_2, True, cor_contorno)
                    tela.blit(contorno_2, (76 + dx, 350 + dy))  # Ajuste a posição conforme necessário

        # Desenhar o texto inferior
        texto_surf_2 = fonte.render(texto_2, True, cor_texto)
        tela.blit(texto_surf_2, (76, 350))  # Ajuste a posição conforme necessário

        pularBotao.desenharBotao(tela)

        pygame.display.update()
        clock.tick(fps_video)

    cap.release()

def tocar_musica(nova_musica): # FUNÇÃO DA MÚSICA DE FUNDO
    global musica_atual, volume
    if musica_atual != nova_musica:  # Só troca se a música for diferente
        pygame.mixer.music.stop()  # Para a música atual
        pygame.mixer.music.load(nova_musica)  # Carrega a nova música
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # Toca em loop
        musica_atual = nova_musica  # Atualiza a música atual
        
def tocar_efeito_sonoro(efeito, volume=0.5):
    efeito_sonoro = pygame.mixer.Sound(efeito)
    efeito_sonoro.set_volume(volume)  # Define o volume do efeito (0.0 a 1.0)
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
    global somAtivo, volume

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
    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
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

        # Fonte e texto do volume
        fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
        texto_volume = f"Volume: {int(volume * 100)}%"

        # Renderizar texto com contorno preto
        texto_contorno = fonte.render(texto_volume, True, (0, 0, 0))  # Cor do contorno preta
        texto_preenchimento = fonte.render(texto_volume, True, (255, 255, 255))  # Texto branco

        # Posição do texto
        posicao_texto = (barra_x + barra_largura // 2 - texto_contorno.get_width() // 2, 
                        barra_y + barra_altura + 30)

        # Desenhar o contorno do texto
        tela.blit(texto_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
        tela.blit(texto_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

        # Desenhar o texto preenchido por cima
        tela.blit(texto_preenchimento, posicao_texto)

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
            run = False  # Sai do loop para voltar para a tela anterior
        
        if sairBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            confirmar_saida(tela)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def abrirConfiguracoesFases():
    global fase_ativa, somAtivo, estadoJogo, volume
    

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
    continuarBotao = criarBotao(som_x - 275, 540, "imagens/GUI/botaoVoltar/continuar0.png", "imagens/GUI/botaoVoltar/continuar1.png")
    sairBotao = criarBotao(som_x + 235, 540,"imagens/GUI/botaoSair/Sair0.png", "imagens/GUI/botaoSair/Sair1.png")
    menuBotao = criarBotao(som_x + 65, 540,"imagens/GUI/botaoInicio/botaoHome.png", "imagens/GUI/botaoInicio/botaoHome.png")
    fasesBotao = criarBotao(som_x - 105, 540,"imagens/GUI/botaoFases/botaoFases.png", "imagens/GUI/botaoFases/botaoFases.png")

    run = True
    while run:
        tela.blit(configuracoesBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()
        cliqueMouse = pygame.mouse.get_pressed()
        # Atualizar e desenhar botões
        if somAtivo:
            if estadoJogo == "fase1":
                tocar_musica("sons/musicaZoo/fundoZoo.mp3")  # Toca a primeira música
            elif estadoJogo == "fase2":
                tocar_musica("sons/musicaSala/fundoSala.mp3")  # Toca a primeira música
            elif estadoJogo == "fase3":
                tocar_musica("sons/musicaPraia/fundoPraia.mp3")  # Toca a primeira música

            somLigadoBotao.atualizarImagem(posicaoMouse)
            somLigadoBotao.desenharBotao(tela)
        else:
            somDesligadoBotao.atualizarImagem(posicaoMouse)
            somDesligadoBotao.desenharBotao(tela)

        continuarBotao.atualizarImagem(posicaoMouse)
        continuarBotao.desenharBotao(tela)
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

        # Fonte e texto do volume
        fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
        texto_volume = f"Volume: {int(volume * 100)}%"

        # Renderizar texto com contorno preto
        texto_contorno = fonte.render(texto_volume, True, (0, 0, 0))  # Cor do contorno preta
        texto_preenchimento = fonte.render(texto_volume, True, (255, 255, 255))  # Texto branco

        # Posição do texto
        posicao_texto = (barra_x + barra_largura // 2 - texto_contorno.get_width() // 2, 
                        barra_y + barra_altura + 30)

        # Desenhar o contorno do texto
        tela.blit(texto_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
        tela.blit(texto_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
        tela.blit(texto_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

        # Desenhar o texto preenchido por cima
        tela.blit(texto_preenchimento, posicao_texto)

        # Verificar cliques nos botões
        if somAtivo and somLigadoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            somAtivo = False
            pygame.mixer.music.pause()
        elif not somAtivo and somDesligadoBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            somAtivo = True
            pygame.mixer.music.unpause()

        if continuarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            run = False  # Sai do loop para voltar para a tela anterior

        if sairBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            confirmar_saida(tela)  # Chama a função para confirmar a saída

        if menuBotao.clicarBotao(tela):
            som_click.play()  
            menuPrincipal()  
            run = False 
            fase_ativa = False
            return  

        if fasesBotao.clicarBotao(tela):
            som_click.play()  
            iniciarFases()  
            run = False  
            fase_ativa = False
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
    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    fase1Botao = criarBotao(20, 250, "imagens/fase1/faseBotao1.png", "imagens/fase1/faseBotao1.png")
    fase2Botao = criarBotao(20, 370, "imagens/fase2/faseBotao2.png", "imagens/fase2/faseBotao2.png")
    fase3Botao = criarBotao(20, 490, "imagens/fase3/faseBotao3.png", "imagens/fase3/faseBotao3.png")

    # Textos das fases
    texto_fase1 = [
        "",
        "                           Bem-vindo à Fase 1!",
        "",
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
        "",
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
        "",
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

    def calcular_altura_barra(texto):
        altura_conteudo = len(texto) * espacamento
        barra_altura = max(30, (altura_quadro ** 2) / max(altura_conteudo, altura_quadro))
        return altura_conteudo, barra_altura

    altura_conteudo, barra_altura = calcular_altura_barra(texto_atual)
    deslocamento = 0
    clicando_na_barra = False
    offset_y = 0  # Armazena a posição relativa do clique na barra

    barra_largura = 15
    barra_x = posicao_quadro[0] + largura_quadro - barra_largura - 5
    trilho_x = barra_x
    trilho_altura = altura_quadro

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
        superficie_instrucoes.fill((131, 69, 31))

        for i, linha in enumerate(texto_atual):
            texto_img = fonte.render(linha, True, cor_texto)
            superficie_instrucoes.blit(texto_img, (20, i * espacamento))

        deslocamento = max(0, min(deslocamento, altura_conteudo - altura_quadro))
        recorte = superficie_instrucoes.subsurface((0, deslocamento, largura_quadro, altura_quadro))
        tela.blit(recorte, posicao_quadro)

        # Barra de rolagem
        pygame.draw.rect(tela, (50, 50, 50), (trilho_x, posicao_quadro[1], barra_largura, trilho_altura))
        barra_y = posicao_quadro[1] + (deslocamento / (altura_conteudo - altura_quadro)) * (altura_quadro - barra_altura)
        pygame.draw.rect(tela, (236, 155, 94), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)

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
            altura_conteudo, barra_altura = calcular_altura_barra(texto_fase1)  # Atualiza altura da barra
            deslocamento = 0  # Reseta o deslocamento

        if fase2Botao.clicarBotao(tela):
            som_click.play()
            texto_atual = texto_fase2  # Atualiza texto para Fase 2
            altura_conteudo, barra_altura = calcular_altura_barra(texto_fase2)  # Atualiza altura da barra
            deslocamento = 0

        if fase3Botao.clicarBotao(tela):
            som_click.play()
            texto_atual = texto_fase3  # Atualiza texto para Fase 3
            altura_conteudo, barra_altura = calcular_altura_barra(texto_fase3)  # Atualiza altura da barra
            deslocamento = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global rodando
                rodando = False
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if barra_x <= posicaoMouse[0] <= barra_x + barra_largura:
                        if barra_y <= posicaoMouse[1] <= barra_y + barra_altura:
                            clicando_na_barra = True
                            offset_y = posicaoMouse[1] - barra_y
                        elif posicao_quadro[1] <= posicaoMouse[1] <= posicao_quadro[1] + altura_quadro:
                            nova_pos = (posicaoMouse[1] - posicao_quadro[1]) / altura_quadro
                            deslocamento = nova_pos * (altura_conteudo - altura_quadro)

                elif event.button == 4:
                    deslocamento = max(deslocamento - 20, 0)
                elif event.button == 5:
                    deslocamento = min(deslocamento + 20, altura_conteudo - altura_quadro)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicando_na_barra = False

            elif event.type == pygame.MOUSEMOTION:
                if clicando_na_barra:
                    nova_pos = event.pos[1] - posicao_quadro[1] - offset_y
                    nova_pos = max(0, min(nova_pos, altura_quadro - barra_altura))
                    deslocamento = (nova_pos / (altura_quadro - barra_altura)) * (altura_conteudo - altura_quadro)

        pygame.display.update()

def abrirCreditos():
    global estadoJogo
    creditosBackground = pygame.image.load("imagens/GUI/Backgrounds/creditos.jpg")
    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")

    linhas_creditos = [
        "Lixo no lixo é um jogo educativo criado para ",
        "ajudar na conscientização sobre a poluição.",
        "Este jogo ajuda a lembrarmos que não se deve",
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
        "- João Rafael Moreira Anhaia",
        "- Matheus Vinícius dos Santos Sachinski",
        "- Nicole Louise Matias Jamuchewski",
        "- Pedro Victor A. M. L. Maciel",
        "                                  Desenvolvimento   ",
        "- Brenda Amanda da Silva Garcez",
        "- Matheus Vinícius dos Santos Sachinski",
        "                                   Ilustrações",
        "- Brenda Amanda da Silva Garcez",
        "- João Rafael Moreira Anhaia",
        "- Matheus Vinícius dos Santos Sachinski",
        "- Nicole Louise Matias Jamuchewski",
        "                                  Áudio e Vídeo",
        "- Brenda Amanda da Silva Garcez",
        "- João Rafael Moreira Anhaia",
        "- Nicole Louise Matias Jamuchewski",

        "                                   Documentação",
        "- Brenda Amanda da Silva Garcez",
        "- Pedro Victor A. M. L. Maciel",
        "                                     Fontes por:",
        "- 'Luckiest' Guy por Astigmatic (Google Fonts)",
        "                             Obrigado por jogar!",
    ]

    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 26)  # 40 é o tamanho da fonte
    cor_texto = (255, 255, 255)  # Cor do texto
    espacamento = 50  # Espaçamento entre linhas

    largura_quadro = 700  # Largura do quadrado marrom
    altura_quadro = 350  # Altura do quadrado marrom
    posicao_quadro = (200, 220)  # Posição do quadrado marrom

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

def enviar_email(email_usuario, mensagem):
    try:
        remetente = "jogosdevmk@gmail.com"  # Substitua pelo seu e-mail
        senha = "ijhj wfbb fchq wwjd"  # Substitua pela sua senha
        destinatario = "jogosdevmk@gmail.com"  # E-mail de suporte
        #tyhj anlg csxw wzrn
        # Configurar o e-mail
        mensagem_email = MIMEMultipart()
        mensagem_email['From'] = remetente
        mensagem_email['To'] = destinatario
        mensagem_email['Subject'] = "Mensagem de Suporte"
        
        corpo = f"Email do Usuário: {email_usuario}\n\nMensagem:\n{mensagem}"
        mensagem_email.attach(MIMEText(corpo, 'plain'))

        # Enviar o e-mail
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem_email)
        servidor.quit()

        print("E-mail enviado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

def abrirSuporte():
    global estadoJogo
    pygame.init()

    # Configuração da janela
    largura_tela, altura_tela = 1100, 720
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Suporte")

    suporteBackground = pygame.image.load("imagens/GUI/Backgrounds/suporteBackground.png")
    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    confirmarBotao = criarBotao(473, 500, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

    # Mensagens de suporte
    textoSuporte = [
        "Se tiver alguma duvida ou sugestão entre em contato!",
        "email: jogosdevmk@gmail.com",
        "Obrigado por jogar!",
    ]

    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 26)
    input_fonte = pygame.font.Font(None, 32)
    cor_texto = (255, 255, 255)
    cor_input = (50, 50, 50)
    cor_input_ativo = (200, 200, 200)

    # Campos de entrada centralizados
    campo_email = pygame.Rect((largura_tela - 400) // 2, 350, 400, 40)
    campo_mensagem = pygame.Rect((largura_tela - 400) // 2, 450, 400, 40)

    email_usuario = ""
    mensagem = ""
    ativo_email = False
    ativo_mensagem = False

    def limitar_texto(texto, fonte, largura_max):
        while fonte.size(texto)[0] > largura_max:
            texto = texto[1:]  # Remove o primeiro caractere se exceder a largura
        return texto

    run = True
    while run:
        tela.blit(suporteBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        voltarBotao.atualizarImagem(posicaoMouse)
        confirmarBotao.atualizarImagem(posicaoMouse)
        voltarBotao.desenharBotao(tela)
        confirmarBotao.desenharBotao(tela)

        # Renderizar as mensagens de suporte centralizadas
        y_offset = 150
        for linha in textoSuporte:
            texto = fonte.render(linha, True, cor_texto)
            texto_rect = texto.get_rect(center=(largura_tela // 2, y_offset))
            tela.blit(texto, texto_rect.topleft)
            y_offset += 40

        # Renderizar textos dos campos de entrada centralizados
        texto_email = fonte.render("Seu e-mail:", True, cor_texto)
        texto_email_rect = texto_email.get_rect(center=(largura_tela // 2, 320))
        tela.blit(texto_email, texto_email_rect.topleft)

        texto_mensagem = fonte.render("Sua mensagem:", True, cor_texto)
        texto_mensagem_rect = texto_mensagem.get_rect(center=(largura_tela // 2, 420))
        tela.blit(texto_mensagem, texto_mensagem_rect.topleft)

        # Renderizar campos de entrada
        pygame.draw.rect(tela, cor_input_ativo if ativo_email else cor_input, campo_email)
        pygame.draw.rect(tela, cor_input_ativo if ativo_mensagem else cor_input, campo_mensagem)

        texto_email_usuario = input_fonte.render(limitar_texto(email_usuario, input_fonte, campo_email.width - 10), True, (255, 255, 255))
        texto_mensagem_usuario = input_fonte.render(limitar_texto(mensagem, input_fonte, campo_mensagem.width - 10), True, (255, 255, 255))

        tela.blit(texto_email_usuario, (campo_email.x + 5, campo_email.y + 5))
        tela.blit(texto_mensagem_usuario, (campo_mensagem.x + 5, campo_mensagem.y + 5))

        if voltarBotao.clicarBotao(tela):
            print("Voltando ao menu principal")
            estadoJogo = "menu"
            run = False
        if confirmarBotao.clicarBotao(tela):
            if email_usuario.strip() and mensagem.strip():  # Verifica se os campos não estão vazios
                sucesso = enviar_email(email_usuario, mensagem)
                if sucesso:
                    print("E-mail enviado com sucesso!")
                    email_usuario = ""
                    mensagem = ""
                else:
                    print("Erro ao enviar o e-mail. Tente novamente.")
            else:
                print("Preencha todos os campos antes de enviar.")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se clicou dentro dos campos de entrada
                if campo_email.collidepoint(event.pos):
                    ativo_email = True
                    ativo_mensagem = False  # Desativa o outro campo
                elif campo_mensagem.collidepoint(event.pos):
                    ativo_mensagem = True
                    ativo_email = False  # Desativa o outro campo
                else:
                    ativo_email = False
                    ativo_mensagem = False  # Desativa ambos se clicar fora

            if event.type == pygame.KEYDOWN:
                if ativo_email:
                    if event.key == pygame.K_BACKSPACE:
                        email_usuario = email_usuario[:-1]  # Remove o último caractere
                    elif event.key == pygame.K_RETURN:
                        ativo_email = False  # Sai do campo ao pressionar Enter
                    else:
                        email_usuario += event.unicode  # Adiciona caracteres

                if ativo_mensagem:
                    if event.key == pygame.K_BACKSPACE:
                        mensagem = mensagem[:-1]  # Remove o último caractere
                    elif event.key == pygame.K_RETURN:
                        ativo_mensagem = False  # Sai do campo ao pressionar Enter
                    else:
                        mensagem += event.unicode  # Adiciona caracteres

        pygame.display.flip()


def calculoDaPontuacao():
    global estadoJogo
    creditosBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")
    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")

    linhas_creditos = [
        "Como funciona a pontuação:",
        "- É com base nas vidas restantes durante a fase",
        "ou seja:",
        "3 corações = 0 erros",
        "2 corações = 1 erro",
        "1 coração = 2 erros",
        "0 corações = 3 erros ",
    ]

    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 26)  # 40 é o tamanho da fonte
    cor_texto = (255, 255, 255)  # Cor do texto
    espacamento = 50  # Espaçamento entre linhas

    largura_quadro = 700  # Largura do quadrado marrom
    altura_quadro = 350  # Altura do quadrado marrom
    posicao_quadro = (200, 220)  # Posição do quadrado marrom

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

        # Desenhar o contorno do quadro
        pygame.draw.rect(tela, (255, 189, 140), (posicao_quadro[0] - 5, posicao_quadro[1] - 5, largura_quadro + 10, altura_quadro + 10), 5)  # Contorno preto, espessura 5px

        recorte = superficie_creditos.subsurface((0, deslocamento, largura_quadro, altura_quadro))
        tela.blit(recorte, posicao_quadro)

        pygame.draw.rect(tela, (50, 50, 50), (trilho_x, posicao_quadro[1], barra_largura, trilho_altura))

        # Atualizar posição da barra de rolagem
        barra_y = posicao_quadro[1] + (deslocamento / altura_conteudo) * altura_quadro

        # Desenhar a barra de rolagem
        pygame.draw.rect(tela, (236, 155, 94), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltando")
            abrirRelatorio()
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

def abrirRelatorio(ultimo_jogador=None):
    global estadoJogo
    relatorioBackground = pygame.image.load("imagens/GUI/Backgrounds/relatorioBackground.png")
    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    calculoPontuacao = criarBotao(990, 620, "imagens/GUI/botaoConfiguracoes/info0.png", "imagens/GUI/botaoConfiguracoes/info1.png")

    # Carregar as imagens das vidas e redimensioná-las
    tamanho_imagem = (120, 30)  # Defina o tamanho desejado para as imagens
    vidas_imagens = {
        0: pygame.transform.scale(pygame.image.load("imagens/GUI/vidasRelatorio/0vidas.png"), tamanho_imagem),
        1: pygame.transform.scale(pygame.image.load("imagens/GUI/vidasRelatorio/1vida.png"), tamanho_imagem),
        2: pygame.transform.scale(pygame.image.load("imagens/GUI/vidasRelatorio/2vidas.png"), tamanho_imagem),
        3: pygame.transform.scale(pygame.image.load("imagens/GUI/vidasRelatorio/3vidas.png"), tamanho_imagem)
    }

    # Função para mapear pontuação para vidas
    def pontuacao_para_vidas(pontuacao):
        if pontuacao == 10:
            return 3
        elif pontuacao == 9:
            return 2
        elif pontuacao == 8:
            return 1
        else:
            return 0

    dados = carregar_dados_jogadores()
    jogadores = dados.get("jogadores", [])
    if jogadores:
        jogadores.insert(0, jogadores.pop())

    fonte = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 26)
    fonte2 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 18)
    cor_texto = (255, 255, 255)
    cor_ultimo = (255, 0, 0)
    espacamento = 50

    largura_quadro = 640
    altura_quadro = 350
    posicao_quadro = ((1020 - largura_quadro) // 2, (720 - altura_quadro) // 2)

    colunas = ["Jogador", "Fase 1", "Fase 2", "Fase 3"]
    largura_colunas = [200, 150, 150, 150]

    altura_conteudo = (len(jogadores) + 1) * espacamento
    deslocamento = 0

    barra_largura = 15
    barra_altura = max(30, altura_quadro * (altura_quadro / max(altura_conteudo, altura_quadro)))
    barra_x = posicao_quadro[0] + largura_quadro - barra_largura + 80
    trilho_x = barra_x
    trilho_altura = altura_quadro

    clicando_na_barra = False
    mouse_inicial = 0

    run = True
    while run:
        tela.blit(relatorioBackground, (0, 0))
        posicaoMouse = pygame.mouse.get_pos()

        configuracoesBotao.atualizarImagem(posicaoMouse)
        configuracoesBotao.desenharBotao(tela)

        voltarBotao.atualizarImagem(posicaoMouse)
        voltarBotao.desenharBotao(tela)

        calculoPontuacao.atualizarImagem(posicaoMouse)
        calculoPontuacao.desenharBotao(tela)

        superficie_relatorio = pygame.Surface((largura_quadro, altura_conteudo), pygame.SRCALPHA)
        superficie_relatorio.fill((255, 189, 140))

        # Desenhar cabeçalho
        y_atual = 20
        pygame.draw.line(superficie_relatorio, (120, 84, 8), (0, y_atual - 10), (largura_quadro, y_atual - 10), 3)

        x_atual = 0
        for i, coluna in enumerate(colunas):
            pygame.draw.line(superficie_relatorio, (120, 64, 8), (x_atual, y_atual - 10), (x_atual, y_atual + espacamento - 10), 2)
            cor_cabecalho = (255, 215, 0) if i == 0 else (102, 51, 0)

            texto_contorno = fonte.render(coluna, True, (102, 51, 0))
            texto_preenchimento = fonte.render(coluna, True, cor_cabecalho)

            superficie_relatorio.blit(texto_contorno, (x_atual + 10, y_atual))
            superficie_relatorio.blit(texto_preenchimento, (x_atual + 10, y_atual))
            x_atual += largura_colunas[i]

        y_atual += espacamento

        # Desenhar tabela com os jogadores
        for index, jogador in enumerate(jogadores):
            nome = jogador["nome"]
            fases = jogador.get("fases", [])
            cor_atual = cor_ultimo if nome == ultimo_jogador else cor_texto

            pygame.draw.line(superficie_relatorio, (120, 64, 8), (0, y_atual - 10), (largura_quadro, y_atual - 10), 2)
            
            x_atual = 0
            for i, coluna in enumerate(colunas):
                pygame.draw.line(superficie_relatorio, (120, 64, 8), (x_atual, y_atual - 10), (x_atual, y_atual + espacamento - 10), 2)

                if i == 0:
                    texto = f"{nome}"
                    texto_contorno = fonte.render(texto, True, (120, 84, 6))
                    texto_preenchimento = fonte.render(texto, True, cor_atual)
                    superficie_relatorio.blit(texto_contorno, (x_atual + 10, y_atual))
                    superficie_relatorio.blit(texto_preenchimento, (x_atual + 10, y_atual))
                else:
                    fase = next((f for f in fases if f['fase'] == i), None)
                    if fase:
                        pontuacao = fase['pontuacao']
                        vidas = pontuacao_para_vidas(pontuacao)
                        imagem_vidas = vidas_imagens[vidas]
                        superficie_relatorio.blit(imagem_vidas, (x_atual + 15, y_atual))
                    else:
                        texto = "Não concluída"
                        texto_contorno = fonte2.render(texto, True, (120, 84, 6))
                        texto_preenchimento = fonte2.render(texto, True, cor_texto)
                        superficie_relatorio.blit(texto_contorno, (x_atual + 10, y_atual))
                        superficie_relatorio.blit(texto_preenchimento, (x_atual + 10, y_atual))
                
                x_atual += largura_colunas[i]

            y_atual += espacamento

            # Verificar se é o último jogador (para desenhar a linha final da tabela e borda da última coluna)
            if index == len(jogadores) - 1:
                # Linha final horizontal
                pygame.draw.line(superficie_relatorio, (0, 0, 0), (0, y_atual - 10), (largura_quadro, y_atual - 10), 3)

                # Borda da última coluna
                x_atual = sum(largura_colunas)  # Posição da última coluna
                pygame.draw.line(superficie_relatorio, (120, 64, 8), (x_atual, y_atual - 10), (x_atual, y_atual), 2)

        # Desenho da linha final da última coluna (Fase 3)
        pygame.draw.line(superficie_relatorio, (120, 64, 8), (0, y_atual - 10), (largura_quadro, y_atual - 10), 3)

        deslocamento = max(0, min(deslocamento, altura_conteudo - altura_quadro))
        altura_recorte = min(altura_quadro, altura_conteudo - deslocamento)
        recorte = superficie_relatorio.subsurface((0, deslocamento, largura_quadro, altura_recorte))        
        tela.blit(recorte, (posicao_quadro[0], posicao_quadro[1]))

        pygame.draw.rect(tela, (200, 200, 200), (trilho_x, posicao_quadro[1], barra_largura, trilho_altura))
        barra_y = posicao_quadro[1] + (deslocamento / max(1, altura_conteudo - altura_quadro)) * (altura_quadro - barra_altura)
        pygame.draw.rect(tela, (120, 84, 8), (barra_x, barra_y, barra_largura, barra_altura), border_radius=5)

        if calculoPontuacao.clicarBotao(tela):
            som_click.play()
            run = False
            calculoDaPontuacao()

        if voltarBotao.clicarBotao(tela):
            som_click.play()
            estadoJogo = "menu"
            run = False

        if configuracoesBotao.clicarBotao(tela):
            som_click.play()
            abrirConfiguracoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and trilho_x <= posicaoMouse[0] <= trilho_x + barra_largura:
                    if barra_y <= posicaoMouse[1] <= barra_y + barra_altura:
                        clicando_na_barra = True
                        mouse_inicial = event.pos[1]
                    elif posicaoMouse[1] < barra_y:
                        deslocamento = max(deslocamento - altura_quadro, 0)
                    elif posicaoMouse[1] > barra_y + barra_altura:
                        deslocamento = min(deslocamento + altura_quadro, max(0, altura_conteudo - altura_quadro))
                elif event.button == 4:
                    deslocamento = max(deslocamento - 20, 0)
                elif event.button == 5:
                    deslocamento = min(deslocamento + 20, max(0, altura_conteudo - altura_quadro))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicando_na_barra = False
            elif event.type == pygame.MOUSEMOTION and clicando_na_barra:
                deslocamento += (event.pos[1] - mouse_inicial) * (altura_conteudo / altura_quadro)
                mouse_inicial = event.pos[1]

        pygame.display.update()

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
    posicao_voltar = (20, 20)  # Botão voltar no canto inferior esquerdo

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

def fase1(nome_jogador):
    global estadoJogo, jogoConcluido, pontuacao_fase1, fase_ativa, somAtivo, objeto_circulado, lampada_acesa, ultimo_objeto_clicado
    pontuacao_fase1 = 0
    jogoConcluido = False
    fase1Background = pygame.image.load("imagens/fase1/imagemZoologico.png")

    largura_tela, altura_tela = tela.get_size()

    mostrarVideo("video/fase1.mp4", 600, 300, "imagens/fase1/imagemTutorialZoo.png", "sons/tutorial/fase1.wav", "sons/musicaZoo/fundoZoo.mp3")
    
    # Verificar som
    if somAtivo:
        tocar_musica("sons/musicaZoo/fundoZoo.mp3")  # Toca a primeira música

    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    botaoTutorial = criarBotao(936, 660, "imagens/GUI/botaoTutorial/botaoTutorial0.png", "imagens/GUI/botaoTutorial/botaoTutorial1.png")

    # Configurações para o texto do temporizador
    fonte1 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Lista de imagens
    imagensCorretas = [
        "imagens/fase1/corretas/Tamanduá.png",
        "imagens/fase1/corretas/Capivara.png",
        "imagens/fase1/corretas/Preguiça.png",
        "imagens/fase1/corretas/Elefante.png",
        "imagens/fase1/corretas/Esquilo.png",
        "imagens/fase1/corretas/Gambá.png",
        "imagens/fase1/corretas/Panda.png",
        "imagens/fase1/corretas/Pássaro.png",
        "imagens/fase1/corretas/Girafa.png",
        "imagens/fase1/corretas/Raposa.png",
        "imagens/fase1/corretas/Cervo.png",
    ]

    imagensIncorretas = [
        "imagens/fase1/incorretas/Caixa de Papelão.png",
        "imagens/fase1/incorretas/Copo Descartável.png",
        "imagens/fase1/incorretas/Fralda Descartável.png",
        "imagens/fase1/incorretas/Garrafa de Vidro.png",
        "imagens/fase1/incorretas/Garrafa Pet.png",
        "imagens/fase1/incorretas/Lata Amassada.png",
        "imagens/fase1/incorretas/Lata.png",
        "imagens/fase1/incorretas/Saco de Lixo.png",
        "imagens/fase1/incorretas/Papel Amassado.png",
        "imagens/fase1/incorretas/Saco de Papel.png",
    ]

    # Sorteio pro senhor pássaro
    senhor_passaro = random.randint(1, 1000)
    #print(f"número sorteado: {senhor_passaro}")

    if senhor_passaro == 47:
        # Seleciona 5 imagens corretas e adiciona o "senhor pássaro"
        imagensCorretasSelecionadas = random.sample(imagensCorretas, 5)
        imagensCorretasSelecionadas.append("imagens/fase1/corretas/Pássaro .png")
    else:
        # Seleciona 6 imagens corretas normalmente
        imagensCorretasSelecionadas = random.sample(imagensCorretas, 6)

    # Seleciona 4 imagens incorretas
    imagensIncorretasSelecionadas = random.sample(imagensIncorretas, 4)

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

    objetos = []
    
    posicoes_fixas = [
        (80, 440), (287, 163), (500, 155), (700, 180),
        (837, 440), (100, 300), (438, 299), (674, 313),
        (326, 463), (563, 468)
    ]

    # Função para posicionar os objetos
    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        # Embaralha as imagens antes de atribuir às posições fixas
        random.shuffle(imagens_selecionadas)

        # Faz uma cópia das posições fixas disponíveis
        posicoes_disponiveis = posicoes_fixas.copy()

        for imagem in imagens_selecionadas:
            if len(posicoes_disponiveis) > 0:  # Verifica se há posições disponíveis
                # Extrair o nome do arquivo da imagem (sem extensão)
                nome_objeto = imagem.split("/")[-1].split(".")[0].replace("_", " ").capitalize()

                # Escolhe uma posição disponível
                posicao_escolhida = random.choice(posicoes_disponiveis)
                while any(objeto["x"] == posicao_escolhida[0] and objeto["y"] == posicao_escolhida[1] for objeto in objetos):
                    # Se a posição já estiver ocupada, escolhe outra posição
                    posicao_escolhida = random.choice(posicoes_disponiveis)

                # Remove a posição já utilizada
                posicoes_disponiveis.remove(posicao_escolhida)

                # Cria o botão para o objeto
                x, y = posicao_escolhida
                botao = criarBotaoImagensFASE3(x, y, imagem, imagem)
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0, "nome": nome_objeto})
            else:
                break  # Interrompe o loop se não houver mais posições disponíveis

    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")
    
    # Criar o botão de confirmar no centro inferior da tela
    confirmarBotao = criarBotao(470, 660, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")
    
    lampadaAcesaImagem = pygame.image.load("imagens/GUI/lampadas/lampadaAcesa.png")
    lampadaApagadaImagem = pygame.image.load("imagens/GUI/lampadas/lampadaApagada.png")
    lampada = criarBotao(980, 170, "imagens/GUI/lampadas/lampadaApagada.png", "imagens/GUI/lampadas/lampadaApagada.png")

     # Configurações do temporizador
    tempo_inicial = 300  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa
    
    mostrar_informacoes = True
    fase_ativa = True
    circulo = False
    som_da_lampada = False
    
    fonte2 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 25)  # Fonte padrão de tamanho 36
    cor_texto = (255, 255, 255)  # Cor do texto (branco)
    cor_contorno = (0, 0, 0)  # Cor do contorno (preto)
    tempo_perda = None

    while fase_ativa:
        if not jogoGanhou and not jogoPerdeu:
            if lampada_acesa:
                lampada.mudarImagem(lampadaAcesaImagem, lampadaAcesaImagem)
                if not som_da_lampada:
                    som_dica.play()  # Toca o som apenas se não foi tocado ainda
                    som_da_lampada = True  # Marca o som como tocado
            else:
                lampada.mudarImagem(lampadaApagadaImagem, lampadaApagadaImagem)
                som_da_lampada = False
        tela.blit(fase1Background, (0, 0))

        if not jogoGanhou and not jogoPerdeu:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicializado) // 1000
            tempo_restante = max(tempo_inicial - tempo_decorrido, 0)

            if tempo_restante == 0:
                jogoPerdeu = True
                lampada_acesa = False
                circulo = False
                objeto_circulado = None

        if not jogoGanhou and not jogoPerdeu:
            # Exibir as vidas
            tela.blit(vida_imagens[vidas], (20, 650))  # Exibe a imagem das vidas no canto superior esquerdo
            # Configurações para o texto de "VIDAS"
            texto_vidas = "VIDAS"
            texto_vidas_contorno = fonte1.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
            texto_vidas_preenchimento = fonte1.render(texto_vidas, True, cor_texto)  # Texto branco

            # Posição do texto "VIDAS" ajustada
            posicao_vidas = (largura_tela // 13 - texto_vidas_contorno.get_width() // 80, altura_tela - 30)

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
            300,  # Posiciona um pouco abaixo do texto
            "imagens/GUI/botaoTentarnovamente/tentarnovamente.png",
            "imagens/GUI/botaoTentarnovamente/tentarnovamente1.png"
        )

        fasesBotao = criarBotao(
            410,  # Centraliza horizontalmente
            410,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoFases/fasesBotao.png", 
            "imagens/GUI/botaoFases/fasesBotao.png" # adicionar imagem nova com cor
        )

        # Criar o botão de "Próxima Fase"
        proximaFaseBotao = criarBotao(
            410,  # Centraliza horizontalmente
            410,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoProximaFase/proximafase0.png",  # Imagem do botão
            "imagens/GUI/botaoProximaFase/proximafase1.png"  # Imagem do botão (hover)
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao = criarBotao(
            405,  # Centraliza horizontalmente
            510,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            jogoConcluido = True
            if jogoGanhou:
                tela.blit(pygame.image.load("imagens/fase1/ganhouZoologico.jpg"), (0, 0))
                objetos.clear()  # Limpa todos os objetos
                if pontuacao_fase1 == 6:
                    pontuacao_fase1 = 10
                elif pontuacao_fase1 == 5:
                    pontuacao_fase1 = 9
                elif pontuacao_fase1 == 4:
                    pontuacao_fase1 = 8
               
                mostrar_informacoes = False

                # Desenhar o botão "Tentar Novamente"
                botaoTentarNovamente.atualizarImagem(posicaoMouse)
                botaoTentarNovamente.desenharBotao(tela)

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
                    fase_ativa = False  # Sai do loop atual
                    lampada_acesa = False
                    menuPrincipal()  # Chama a função do menu principa
                salvar_pontuacao(nome_jogador, 1, pontuacao_fase1, tempo_decorrido)

                tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
                erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
                
                # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
                texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

                # Renderizando o texto para mostrar no centro da tela
                texto_contorno_conclusao = fonte1.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
                texto_preenchimento_conclusao = fonte1.render(texto_conclusao, True, cor_texto)  # Texto branco
                posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 120)  # Centraliza o texto

                # Desenhar o texto com contorno
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

                # Desenhar o texto preenchido no centro
                tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

            # Verifica se o jogo foi perdido
            if jogoPerdeu:
                # Filtra os objetos para pegar apenas os de tipo 'correto'
                objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]
                
                # Desenha o círculo em cada objeto correto
                for objeto in objetos_corretos:
                    desenhar_circulo_redondo(objeto)    

                # Exibir as vidas
                tela.blit(vida_imagens[vidas], (20, 650))  # Exibe a imagem das vidas no canto superior esquerdo
                # Configurações para o texto de "VIDAS"
                texto_vidas = "VIDAS"
                texto_vidas_contorno = fonte1.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
                texto_vidas_preenchimento = fonte1.render(texto_vidas, True, cor_texto)  # Texto branco

                # Posição do texto "VIDAS" ajustada
                posicao_vidas = (largura_tela // 13 - texto_vidas_contorno.get_width() // 80, altura_tela - 30)

                # Desenhar o texto com contorno
                tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
                tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
                tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
                tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

                # Desenhar o texto preenchido no centro
                tela.blit(texto_vidas_preenchimento, posicao_vidas)

                if tempo_perda is None:
                    # Armazena o tempo em que o jogo foi perdido
                    tempo_perda = pygame.time.get_ticks()

                # Calcula o tempo decorrido desde a perda
                tempo_decorrido = pygame.time.get_ticks() - tempo_perda

                # Verifica se o tempo de delay passou (2 segundos = 2000 ms)
                if tempo_decorrido >= 2000:
                    # Executa o código desejado após o delay
                    tela.blit(pygame.image.load("imagens/fase1/perdeuZoologico.png"), (0, 0))
                    objetos.clear()  # Limpa todos os objetos
                    pontuacao_fase1 = 0

                    mostrar_informacoes = False

                    # Desenhar o botão "Voltar ao Menu"
                    # Desenhar o botão "Tentar Novamente"
                    botaoTentarNovamente.atualizarImagem(posicaoMouse)
                    botaoTentarNovamente.desenharBotao(tela)

                    fasesBotao.atualizarImagem(posicaoMouse)
                    fasesBotao.desenharBotao(tela)

                    voltarMenuBotao.atualizarImagem(posicaoMouse)
                    voltarMenuBotao.desenharBotao(tela)

                    # Verificar clique no botão "Voltar ao Menu"
                    if voltarMenuBotao.clicarBotao(tela):
                        som_click.play()  # Tocar som de clique
                        print("Botão 'Voltar ao Menu' clicado.")
                        estadoJogo = "menu"  # Voltar para o menu
                        fase_ativa = False  # Sai do loop atual
                        lampada_acesa = False
                        menuPrincipal()  # Chama a função do menu principal

                    if fasesBotao.clicarBotao(tela):
                        som_click.play()
                        print("botao fases clicado")
                        estadoJogo = "jogando"
                        fase_ativa = False
                        lampada_acesa = False
                        iniciarFases()

                    salvar_pontuacao(nome_jogador, 1, pontuacao_fase1, tempo_decorrido)

                    tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
                    erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
                    
                    # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
                    texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

                    # Renderizando o texto para mostrar no centro da tela
                    texto_contorno_conclusao = fonte1.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
                    texto_preenchimento_conclusao = fonte1.render(texto_conclusao, True, cor_texto)  # Texto branco
                    posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 120)  # Centraliza o texto

                    # Desenhar o texto com contorno
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

                    # Desenhar o texto preenchido no centro
                    tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

            # Verificar clique no botão "Próxima Fase"
            if proximaFaseBotao.clicarBotao(tela):
                som_click.play()  # Tocar som de clique
                print("Botão 'Próxima Fase' clicado.")
                estadoJogo = "fase2"  # Mudar o estado do jogo para a fase 2
                fase_ativa = False  # Sai do loop atual
                lampada_acesa = False
                fase2(nome_jogador)  # Chama a função para a próxima fase (fase2)
                
            # Verificar clique no botão "Tentar Novamente"
            if botaoTentarNovamente.clicarBotao(tela):
                som_click.play()  # Tocar o som de clique
                print("Botão 'Tentar Novamente' clicado.")
                fase_ativa = False  # Sai do loop atual
                lampada_acesa = False
                fase1(nome_jogador)  # Reinicia a fase

        if mostrar_informacoes:
            # Exibir o temporizador
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            texto_tempo = f"TEMPO: {minutos:02}:{segundos:02}"

            texto_contorno_tempo = fonte1.render(texto_tempo, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_tempo = fonte1.render(texto_tempo, True, cor_texto)  # Texto branco
            posicao_tempo = (780, 130)  # Posição abaixo do contador de objetos

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_tempo, (posicao_tempo[0] - 1, posicao_tempo[1]))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0] + 1, posicao_tempo[1]))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] - 1))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_tempo, posicao_tempo)

            # Renderiza o texto do contador com contorno
            texto_contorno = fonte1.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, (0, 0, 0))  # Preto para o contorno
            texto_preenchimento = fonte1.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, cor_texto)  # Cor original

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
            botaoTutorial.atualizarImagem(posicaoMouse)
            botaoTutorial.desenharBotao(tela)
            
            confirmarBotao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do botão de confirmar
            confirmarBotao.desenharBotao(tela)  # Desenha o botão de confirmar

            lampada.atualizarImagem(posicaoMouse)
            lampada.desenharBotao(tela)

            if lampada_acesa:
                lampada.mudarImagem(lampadaAcesaImagem, lampadaAcesaImagem)
                
                # Verifica se o som já foi tocado
                if not som_da_lampada:
                    som_dica.play()  # Toca o som apenas se não foi tocado ainda
                    som_da_lampada = True  # Marca o som como tocado
                
                # Criar o texto "Dica" com contorno
                texto_dica_contorno = fonte2.render("Dica", True, cor_contorno)  # Contorno do texto
                texto_dica_preenchimento = fonte2.render("Dica", True, cor_texto)  # Texto preenchido com a cor original

                # Posicionamento do texto sobre a lâmpada
                posicao_texto = (lampada.rect.x + 10, lampada.rect.y + 100)

                # Desenhar o contorno do texto em 4 direções (esquerda, direita, cima, baixo)
                tela.blit(texto_dica_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
                tela.blit(texto_dica_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
                tela.blit(texto_dica_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
                tela.blit(texto_dica_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

                # Desenhar o texto preenchido sobre o contorno
                tela.blit(texto_dica_preenchimento, posicao_texto)

        # Verificar clique na lâmpada
        if lampada.clicarBotao(tela):
            if lampada_acesa:
                circulo = True
            som_click.play()  # Som de clique

            # Verifica se o último objeto confirmado foi incorreto
            if ultimo_objeto_confirmado and ultimo_objeto_confirmado["tipo"] == "incorreto":
                objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]  # Filtra objetos corretos
                if objetos_corretos:  # Se houver objetos corretos
                    objeto_circulado = random.choice(objetos_corretos)  # Circula um objeto correto aleatório
                lampada_acesa = False
        # Desenhar o círculo ao redor do objeto circulado
        if objeto_circulado and circulo:
            desenhar_circulo_redondo(objeto_circulado)

        # Atualizar e desenhar objetos com movimento
        for obj in objetos:
            botao = obj["botao"]
            botao.atualizarImagem(posicaoMouse)
            botao.desenharBotao(tela)
            if botao.rect.collidepoint(posicaoMouse):  # Verifica se o mouse está sobre o botão
                 exibir_nome_objeto(obj)
            else:
                obj["som_tocado"] = False  # Reseta para permitir que o som toque novamente
        
        # Verificar clique nos objetos
        for obj in objetos:
            if obj["botao"].clicarBotao(tela):
                som_click.play()  # Som de clique
                # Fala o som do nome do objeto
                falar_nome_objeto(obj)
                
                # Verifica se o objeto clicado é o mesmo que está circulado
                if lampada.clicarBotao(tela):
                    if lampada_acesa and objeto_circulado and obj == objeto_circulado:
                        lampada_acesa = False  # Apaga a lâmpada
                        objeto_circulado = None  # Remove o objeto circulado
                
                # Substituir o objeto selecionado
                if objetosSelecionados:
                    print(f"Objeto {objetosSelecionados[0]['tipo']} desmarcado.")
                    objetosSelecionados.clear()  # Limpa a seleção atual

                objetosSelecionados.append(obj)  # Seleciona o novo objeto
                print(f"Objeto {obj['tipo']} selecionado na posição ({obj['x']}, {obj['y']})!")
                ultimo_objeto_clicado = obj  # Atualiza o último objeto clicado

        # Verificar clique no botão de confirmar
        if confirmarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            lampada_acesa = False
            for obj in objetosSelecionados:
                if obj["tipo"] == "correto":
                    imagensCorretasClicadas += 1
                    pontuacao_fase1 += 1
                    if imagensCorretasClicadas == 6:  # Clicou em todas as imagens corretas
                        jogoGanhou = True
                    # Tocar som de resposta certa
                    tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3", volume=0.3)
                elif obj["tipo"] == "incorreto":
                    imagensIncorretasClicadas += 1
                    pontuacao_fase1 -= 1
                    vidas -= 1  # Perde uma vida a cada erro
                    if vidas == 0:
                        jogoPerdeu = True
                    # Tocar som de resposta errada
                    tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3", volume=0.4)
                    # Acender a lâmpada se o objeto confirmado for incorreto
                    lampada_acesa = True
                    objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]
                    if objetos_corretos:
                        objeto_circulado = random.choice(objetos_corretos)  # Circula um objeto correto

                objetos.remove(obj)  # Remove o objeto selecionado
            objetosSelecionados.clear()  # Limpa a lista de objetos selecionados
            print("Seleção confirmada. Você pode selecionar outro objeto.")
            circulo = False

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "jogando"
            if jogoConcluido == False:
                pontuacao_fase1 = 0
            fase_ativa = False
            lampada_acesa = False

        elif configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoesFases()
        
        elif botaoTutorial.clicarBotao(tela):
            som_click.play()
            print("tutorial clicado")
            mostrarVideo("video/fase1.mp4", 600, 300, "imagens/fase1/imagemTutorialZoo.png", "sons/tutorial/fase1.wav", "sons/musicaZoo/fundoZoo.mp3")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def fase2(nome_jogador):
    global estadoJogo, jogoConcluido, pontuacao_fase2, fase_ativa, somAtivo, objeto_circulado, lampada_acesa, ultimo_objeto_clicado
    pontuacao_fase2 = 0
    jogoConcluido = False
    fase2Background = pygame.image.load("imagens/fase2/imagemSaladeAula.jpg")

    mostrarVideo("video/fase2.mp4", 600, 300, "imagens/fase2/imagemTutorialSala.png", "sons/tutorial/fase2.wav", "sons/musicaSala/fundoSala.mp3")

    # Verificar som
    if somAtivo:
        tocar_musica("sons/musicaSala/fundoSala.mp3")  # Toca a primeira música

    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    botaoTutorial = criarBotao(936, 660, "imagens/GUI/botaoTutorial/botaoTutorial0.png", "imagens/GUI/botaoTutorial/botaoTutorial1.png")

    # Configurações para o texto do temporizador
    fonte1 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Configurações para objetos
    largura_tela, altura_tela = tela.get_size()
    
    # Lista de imagens
    imagensCorretas = [
        "imagens/fase2/corretas/Casca de Banana.png",
        "imagens/fase2/corretas/Copo Descartável.png",
        "imagens/fase2/corretas/Fralda Descartável.png",
        "imagens/fase2/corretas/Garrafa de Vidro.png",
        "imagens/fase2/corretas/Lata Amassada.png",
        "imagens/fase2/corretas/Lata.png",
        "imagens/fase2/corretas/Saco de Lixo.png",
        "imagens/fase2/corretas/Restos de Maçã.png",
        "imagens/fase2/corretas/Saco de Papel.png",
    ]

    imagensIncorretas = [
        "imagens/fase2/incorretas/Borracha.png",
        "imagens/fase2/incorretas/Estojo.png",
        "imagens/fase2/incorretas/Livro.png",
        "imagens/fase2/incorretas/Mochila.png",
        "imagens/fase2/incorretas/Caneta.png",
        "imagens/fase2/incorretas/Apontador.png",
        "imagens/fase2/incorretas/Lápis.png",
        "imagens/fase2/incorretas/Tesoura.png",
        "imagens/fase2/incorretas/Régua.png",
    ]

    # Selecionando aleatoriamente 6 imagens corretas e 4 incorretas
    imagensCorretasSelecionadas = random.sample(imagensCorretas, 6)  # Seleciona 6 imagens corretas aleatórias
    imagensIncorretasSelecionadas = random.sample(imagensIncorretas, 4)  # Seleciona 4 imagens incorretas aleatórias

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

    objetos = []
    
    posicoes_fixas = [
        (80, 440), (287, 163), (500, 155), (700, 180),
        (837, 440), (100, 300), (438, 299), (674, 313),
        (326, 463), (563, 468)
    ]

    # Função para posicionar os objetos
    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        # Embaralha as imagens antes de atribuir às posições fixas
        random.shuffle(imagens_selecionadas)

        # Faz uma cópia das posições fixas disponíveis
        posicoes_disponiveis = posicoes_fixas.copy()

        for imagem in imagens_selecionadas:
            if len(posicoes_disponiveis) > 0:  # Verifica se há posições disponíveis
                # Extrair o nome do arquivo da imagem (sem extensão)
                nome_objeto = imagem.split("/")[-1].split(".")[0].replace("_", " ").capitalize()

                # Escolhe uma posição disponível
                posicao_escolhida = random.choice(posicoes_disponiveis)
                while any(objeto["x"] == posicao_escolhida[0] and objeto["y"] == posicao_escolhida[1] for objeto in objetos):
                    # Se a posição já estiver ocupada, escolhe outra posição
                    posicao_escolhida = random.choice(posicoes_disponiveis)

                # Remove a posição já utilizada
                posicoes_disponiveis.remove(posicao_escolhida)

                # Cria o botão para o objeto
                x, y = posicao_escolhida
                botao = criarBotaoImagensFASE3(x, y, imagem, imagem)
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0, "nome": nome_objeto})
            else:
                break  # Interrompe o loop se não houver mais posições disponíveis

    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

    # Criar o  de confirmar no centro inferior da tela
    confirmarBotao = criarBotao(470, 660, "imagens/GUI/botaoConfirmar/confirmar1.png", "imagens/GUI/botaoConfirmar/confirmar2.png")

    lampadaAcesaImagem = pygame.image.load("imagens/GUI/lampadas/lampadaAcesa.png")
    lampadaApagadaImagem = pygame.image.load("imagens/GUI/lampadas/lampadaApagada.png")
    lampada = criarBotao(980, 170, "imagens/GUI/lampadas/lampadaApagada.png", "imagens/GUI/lampadas/lampadaApagada.png")

     # Configurações do temporizador
    tempo_inicial = 300  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa

    fase_ativa = True
    mostrar_informacoes = True
    circulo = False
    som_da_lampada = False

    fonte2 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 25)  # Fonte padrão de tamanho 36
    cor_texto = (255, 255, 255)  # Cor do texto (branco)
    cor_contorno = (0, 0, 0)  # Cor do contorno (preto)
    tempo_perda = None

    while fase_ativa:        
        if not jogoGanhou and not jogoPerdeu:
            if lampada_acesa:
                lampada.mudarImagem(lampadaAcesaImagem, lampadaAcesaImagem)
                if not som_da_lampada:
                    som_dica.play()  # Toca o som apenas se não foi tocado ainda
                    som_da_lampada = True  # Marca o som como tocado
            else:
                lampada.mudarImagem(lampadaApagadaImagem, lampadaApagadaImagem)
                som_da_lampada = False
                
        tela.blit(fase2Background, (0, 0))
        
        if not jogoGanhou and not jogoPerdeu:
            tempo_decorrido = (pygame.time.get_ticks() - tempo_inicializado) // 1000
            tempo_restante = max(tempo_inicial - tempo_decorrido, 0)

            if tempo_restante == 0:
                jogoPerdeu = True

        if not jogoGanhou and not jogoPerdeu:
            # Exibir as vidas
            tela.blit(vida_imagens[vidas], (20, 650))  # Exibe a imagem das vidas no canto superior esquerdo
            # Configurações para o texto de "VIDAS"
            texto_vidas = "VIDAS"
            texto_vidas_contorno = fonte1.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
            texto_vidas_preenchimento = fonte1.render(texto_vidas, True, cor_texto)  # Texto branco

            # Posição do texto "VIDAS" ajustada
            posicao_vidas = (largura_tela // 13 - texto_vidas_contorno.get_width() // 80, altura_tela - 30)

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
            300,  # Posiciona um pouco abaixo do texto
            "imagens/GUI/botaoTentarnovamente/tentarnovamente.png",
            "imagens/GUI/botaoTentarnovamente/tentarnovamente1.png"
        )

        fasesBotao = criarBotao(
            410,  # Centraliza horizontalmente
            410,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoFases/fasesBotao.png", 
            "imagens/GUI/botaoFases/fasesBotao.png"
        )

        # Criar o botão de "Próxima Fase"
        proximaFaseBotao = criarBotao(
            410,  # Centraliza horizontalmente
            410,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoProximaFase/proximafase0.png",  # Imagem do botão
            "imagens/GUI/botaoProximaFase/proximafase1.png"  # Imagem do botão (hover)
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao = criarBotao(
            405,  # Centraliza horizontalmente
            510,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            jogoConcluido = True
            if jogoGanhou:
                tela.blit(pygame.image.load("imagens/fase2/ganhouSaladeAula.jpg"), (0, 0))
                objetos.clear()  # Limpa todos os objetos
                if pontuacao_fase2 == 6:
                    pontuacao_fase2 = 10
                elif pontuacao_fase2 == 5:
                    pontuacao_fase2 = 9
                elif pontuacao_fase2 == 4:
                    pontuacao_fase2 = 8

                mostrar_informacoes = False

                # Desenhar o botão "Tentar Novamente"
                botaoTentarNovamente.atualizarImagem(posicaoMouse)
                botaoTentarNovamente.desenharBotao(tela)

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
                    fase_ativa = False  # Sai do loop atual
                    lampada_acesa = False
                    menuPrincipal()  # Chama a função do menu principa
                salvar_pontuacao(nome_jogador, 2, pontuacao_fase2, tempo_decorrido) 

                tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
                erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
                
                # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
                texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

                # Renderizando o texto para mostrar no centro da tela
                texto_contorno_conclusao = fonte1.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
                texto_preenchimento_conclusao = fonte1.render(texto_conclusao, True, cor_texto)  # Texto branco
                posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 120)  # Centraliza o texto

                # Desenhar o texto com contorno
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
                tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

                # Desenhar o texto preenchido no centro
                tela.blit(texto_preenchimento_conclusao, posicao_conclusao)

            if jogoPerdeu:
                # Filtra os objetos para pegar apenas os de tipo 'correto'
                objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]
                
                # Desenha o círculo em cada objeto correto
                for objeto in objetos_corretos:
                    desenhar_circulo_redondo(objeto)

                # Exibir as vidas
                tela.blit(vida_imagens[vidas], (20, 650))  # Exibe a imagem das vidas no canto superior esquerdo
                # Configurações para o texto de "VIDAS"
                texto_vidas = "VIDAS"
                texto_vidas_contorno = fonte1.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
                texto_vidas_preenchimento = fonte1.render(texto_vidas, True, cor_texto)  # Texto branco

                # Posição do texto "VIDAS" ajustada
                posicao_vidas = (largura_tela // 13 - texto_vidas_contorno.get_width() // 80, altura_tela - 30)

                # Desenhar o texto com contorno
                tela.blit(texto_vidas_contorno, (posicao_vidas[0] - 1, posicao_vidas[1]))
                tela.blit(texto_vidas_contorno, (posicao_vidas[0] + 1, posicao_vidas[1]))
                tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] - 1))
                tela.blit(texto_vidas_contorno, (posicao_vidas[0], posicao_vidas[1] + 1))

                # Desenhar o texto preenchido no centro
                tela.blit(texto_vidas_preenchimento, posicao_vidas)

                if tempo_perda is None:
                    # Armazena o tempo em que o jogo foi perdido
                    tempo_perda = pygame.time.get_ticks()

                # Calcula o tempo decorrido desde a perda
                tempo_decorrido = pygame.time.get_ticks() - tempo_perda

                # Verifica se o tempo de delay passou (2 segundos = 2000 ms)
                if tempo_decorrido >= 2000:
                # Desenhar o texto preenchido no centro
                    tela.blit(texto_vidas_preenchimento, posicao_vidas)
                    tela.blit(pygame.image.load("imagens/fase2/perdeuSaladeAula.png"), (0, 0))
                    objetos.clear()  # Limpa todos os objetos

                    pontuacao_fase2 = 0

                    mostrar_informacoes = False

                    # Desenhar o botão "Tentar Novamente"
                    botaoTentarNovamente.atualizarImagem(posicaoMouse)
                    botaoTentarNovamente.desenharBotao(tela)

                    fasesBotao.atualizarImagem(posicaoMouse)
                    fasesBotao.desenharBotao(tela)

                    # Desenhar o botão "Voltar ao Menu"
                    voltarMenuBotao.atualizarImagem(posicaoMouse)
                    voltarMenuBotao.desenharBotao(tela)

                    # Verificar clique no botão "Voltar ao Menu"
                    if voltarMenuBotao.clicarBotao(tela):
                        som_click.play()  # Tocar som de clique
                        print("Botão 'Voltar ao Menu' clicado.")
                        estadoJogo = "menu"  # Voltar para o menu
                        fase_ativa = False  # Sai do loop atual
                        lampada_acesa = False
                        menuPrincipal()  # Chama a função do menu principa

                    if fasesBotao.clicarBotao(tela):
                        som_click.play()
                        print("botao fases clicado")
                        estadoJogo = "jogando"
                        fase_ativa = False
                        lampada_acesa = False
                        iniciarFases()
                    salvar_pontuacao(nome_jogador, 2, pontuacao_fase2, tempo_decorrido)

                    tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
                    erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
                    
                    # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
                    texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

                    # Renderizando o texto para mostrar no centro da tela
                    texto_contorno_conclusao = fonte1.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
                    texto_preenchimento_conclusao = fonte1.render(texto_conclusao, True, cor_texto)  # Texto branco
                    posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 120)  # Centraliza o texto

                    # Desenhar o texto com contorno
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] - 1, posicao_conclusao[1]))
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0] + 1, posicao_conclusao[1]))
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] - 1))
                    tela.blit(texto_contorno_conclusao, (posicao_conclusao[0], posicao_conclusao[1] + 1))

                    # Desenhar o texto preenchido no centro
                    tela.blit(texto_preenchimento_conclusao, posicao_conclusao)
            # Verificar clique no botão "Próxima Fase"
            if proximaFaseBotao.clicarBotao(tela):
                som_click.play()  # Tocar som de clique
                print("Botão 'Próxima Fase' clicado.")
                estadoJogo = "fase2"  # Mudar o estado do jogo para a fase 2
                fase_ativa = False  # Sai do loop atual
                lampada_acesa = False
                fase3(nome_jogador)  # Chama a função para a próxima fase (fase2)

            # Verificar clique no botão "Tentar Novamente"
            if botaoTentarNovamente.clicarBotao(tela):
                som_click.play()  # Tocar o som de clique
                print("Botão 'Tentar Novamente' clicado.")
                fase_ativa = False  # Sai do loop atual4
                lampada_acesa = False
                fase2(nome_jogador)  # Reinicia a fase

        if mostrar_informacoes:
            # Exibir o temporizador
            minutos = tempo_restante // 60
            segundos = tempo_restante % 60
            texto_tempo = f"TEMPO: {minutos:02}:{segundos:02}"

            texto_contorno_tempo = fonte1.render(texto_tempo, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_tempo = fonte1.render(texto_tempo, True, cor_texto)  # Texto branco
            posicao_tempo = (780, 130)  # Posição abaixo do contador de objetos

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_tempo, (posicao_tempo[0] - 1, posicao_tempo[1]))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0] + 1, posicao_tempo[1]))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] - 1))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_tempo, posicao_tempo)

            # Renderiza o texto do contador com contorno
            texto_contorno = fonte1.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, (0, 0, 0))  # Preto para o contorno
            texto_preenchimento = fonte1.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/6", True, cor_texto)  # Cor original

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
            botaoTutorial.atualizarImagem(posicaoMouse)
            botaoTutorial.desenharBotao(tela)
            
            confirmarBotao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do botão de confirmar
            confirmarBotao.desenharBotao(tela)  # Desenha o botão de confirmar

            lampada.atualizarImagem(posicaoMouse)
            lampada.desenharBotao(tela)

            if lampada_acesa:
                lampada.mudarImagem(lampadaAcesaImagem, lampadaAcesaImagem)
                
                # Verifica se o som já foi tocado
                if not som_da_lampada:
                    som_dica.play()  # Toca o som apenas se não foi tocado ainda
                    som_da_lampada = True  # Marca o som como tocado
                
                # Criar o texto "Dica" com contorno
                texto_dica_contorno = fonte2.render("Dica", True, cor_contorno)  # Contorno do texto
                texto_dica_preenchimento = fonte2.render("Dica", True, cor_texto)  # Texto preenchido com a cor original

                # Posicionamento do texto sobre a lâmpada
                posicao_texto = (lampada.rect.x + 10, lampada.rect.y + 100)

                # Desenhar o contorno do texto em 4 direções (esquerda, direita, cima, baixo)
                tela.blit(texto_dica_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
                tela.blit(texto_dica_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
                tela.blit(texto_dica_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
                tela.blit(texto_dica_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

                # Desenhar o texto preenchido sobre o contorno
                tela.blit(texto_dica_preenchimento, posicao_texto)

        # Verificar clique na lâmpada
        if lampada.clicarBotao(tela):
            if lampada_acesa:
                circulo = True
            som_click.play()  # Som de clique

            # Verifica se o último objeto confirmado foi incorreto
            if ultimo_objeto_confirmado and ultimo_objeto_confirmado["tipo"] == "incorreto":
                objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]  # Filtra objetos corretos
                if objetos_corretos:  # Se houver objetos corretos
                    objeto_circulado = random.choice(objetos_corretos)  # Circula um objeto correto aleatório
                lampada_acesa = False  # Apaga a lâmpada após o clique
           
        # Desenhar o círculo ao redor do objeto circulado
        if objeto_circulado and circulo:
            desenhar_circulo_redondo(objeto_circulado)

        # Atualizar e desenhar objetos com movimento
        for obj in objetos:
            botao = obj["botao"]
            botao.atualizarImagem(posicaoMouse)
            botao.desenharBotao(tela)

            # Verifica se o mouse está sobre o objeto (hover)
            if botao.rect.collidepoint(posicaoMouse):  # Verifica se o mouse está sobre o botão
                exibir_nome_objeto(obj)
            else:
                obj["som_tocado"] = False  # Reseta para permitir que o som toque novamente
        # Verificar clique nos objetos

        # Verificar clique nos objetos
        for obj in objetos:
            if obj["botao"].clicarBotao(tela):
                som_click.play()  # Som de clique
                # Fala o som do nome do objeto
                falar_nome_objeto(obj)
                
                if lampada.clicarBotao(tela):
                    # Verifica se o objeto clicado é o mesmo que está circulado
                    if lampada_acesa and objeto_circulado and obj == objeto_circulado:
                        lampada_acesa = False  # Apaga a lâmpada
                        objeto_circulado = None  # Remove o objeto circulado
                
                # Substituir o objeto selecionado
                if objetosSelecionados:
                    print(f"Objeto {objetosSelecionados[0]['tipo']} desmarcado.")
                    objetosSelecionados.clear()  # Limpa a seleção atual

                objetosSelecionados.append(obj)  # Seleciona o novo objeto
                print(f"Objeto {obj['tipo']} selecionado na posição ({obj['x']}, {obj['y']})!")
                ultimo_objeto_clicado = obj  # Atualiza o último objeto clicado

        # Verificar clique no botão de confirmar
        if confirmarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            lampada_acesa = False
            for obj in objetosSelecionados:
                if obj["tipo"] == "correto":
                    imagensCorretasClicadas += 1
                    pontuacao_fase2 += 1
                    if imagensCorretasClicadas == 6:  # Clicou em todas as imagens corretas
                        jogoGanhou = True
                    # Tocar som de resposta certa
                    tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3", volume=0.3)
                elif obj["tipo"] == "incorreto":
                    imagensIncorretasClicadas += 1
                    pontuacao_fase2 -= 1
                    vidas -= 1  # Perde uma vida a cada erro
                    if vidas == 0:
                        jogoPerdeu = True
                    # Tocar som de resposta errada
                    tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3", volume=0.4)
                    # Acender a lâmpada se o objeto confirmado for incorreto
                    lampada_acesa = True
                    objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]
                    if objetos_corretos:
                        objeto_circulado = random.choice(objetos_corretos)  # Circula um objeto correto

                objetos.remove(obj)  # Remove o objeto selecionado
            objetosSelecionados.clear()  # Limpa a lista de objetos selecionados
            print("Seleção confirmada. Você pode selecionar outro objeto.")
            circulo = False

        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "jogando"
            if jogoConcluido == False:
                pontuacao_fase2 = 0
            fase_ativa = False
            lampada_acesa = False

        elif configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoesFases()

        elif botaoTutorial.clicarBotao(tela):
            som_click.play()
            print("tutorial clicado")
            mostrarVideo("video/fase2.mp4", 600, 300, "imagens/fase2/imagemTutorialSala.png", "sons/tutorial/fase2.wav", "sons/musicaSala/fundoSala.mp3")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmar_saida(tela)

        pygame.display.update()
        clock.tick(60)

def fase3(nome_jogador):
    global estadoJogo, jogoConcluido, pontuacao_fase3, fase_ativa, somAtivo,  objeto_circulado, lampada_acesa, ultimo_objeto_clicado
    pontuacao_fase3 = 0
    jogoConcluido = False
    fase3Background = pygame.image.load("imagens/fase3/imagemPraia.jpg")

    largura_tela, altura_tela = tela.get_size()

    mostrarVideo("video/fase3.mp4", 600, 300, "imagens/fase3/imagemTutorialPraia.png", "sons/tutorial/fase3.wav", "sons/musicaPraia/fundoPraia.mp3")

    # Verificar som
    if somAtivo:
        tocar_musica("sons/musicaPraia/fundoPraia.mp3")  # Toca a primeira música

    voltarBotao = criarBotao(20, 20, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    botaoTutorial = criarBotao(936, 660, "imagens/GUI/botaoTutorial/botaoTutorial0.png", "imagens/GUI/botaoTutorial/botaoTutorial1.png")

    # Configurações para o texto do temporizador
    fonte1 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 36)
    cor_texto = (255, 255, 255)  # Branco
    
    # Lista de imagens
    imagensCorretas = [
        "imagens/fase3/corretas/Balde de Areia.png",
        "imagens/fase3/corretas/Cadeira de Praia.png",
        "imagens/fase3/corretas/Coco.png",
        "imagens/fase3/corretas/Coqueiro.png",
        "imagens/fase3/corretas/Guarda Sol.png",
        "imagens/fase3/corretas/Bolsa de Praia.png",
        "imagens/fase3/corretas/Óculos de Sol.png",
        "imagens/fase3/corretas/Toalha.png",
    ]

    imagensIncorretas = [
        "imagens/fase3/incorretas/Casca de Banana.png",
        "imagens/fase3/incorretas/Copo Descartável.png",
        "imagens/fase3/incorretas/Fralda Descartável.png",
        "imagens/fase3/incorretas/Garrafa de Vidro.png",
        "imagens/fase3/incorretas/Garrafa Pet.png",
        "imagens/fase3/incorretas/Lata Amassada.png",
        "imagens/fase3/incorretas/Lata.png",
        "imagens/fase3/incorretas/Saco de Lixo.png",
        "imagens/fase3/incorretas/Papel Amassado.png",
        "imagens/fase3/incorretas/Restos de Maçã.png",
        "imagens/fase3/incorretas/Saco de Papel.png",
    ]

    # Selecionando aleatoriamente 6 imagens corretas e 4 incorretas
    imagensCorretasSelecionadas = random.sample(imagensCorretas, 5)  # Seleciona 6 imagens corretas aleatórias
    imagensIncorretasSelecionadas = random.sample(imagensIncorretas, 5)  # Seleciona 4 imagens incorretas aleatórias

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
    fator_escala = 0.4

    # Calcular o novo tamanho das imagens
    novo_tamanho_area_PRAIA = (int(tamanho_area_PRAIA[0] * fator_escala), int(tamanho_area_PRAIA[1] * fator_escala))
    novo_tamanho_area_LIXO = (int(tamanho_area_LIXO[0] * fator_escala), int(tamanho_area_LIXO[1] * fator_escala))

    # Escalar as imagens
    imagem_area_PRAIA = pygame.transform.scale(imagem_area_PRAIA, novo_tamanho_area_PRAIA)
    imagem_area_LIXO = pygame.transform.scale(imagem_area_LIXO, novo_tamanho_area_LIXO)

    # Posicionar as áreas na tela
    posicao_area_PRAIA = (largura_tela - novo_tamanho_area_PRAIA[0] - 40, altura_tela - novo_tamanho_area_PRAIA[1] - 20)
    posicao_area_LIXO = (30, altura_tela - novo_tamanho_area_LIXO[1] - 20)

    # Função para verificar se o objeto está dentro da área da praia
    def colisao_com_area_PRAIA(objeto):
        # Cria uma máscara para a área da praia
        mask_area_praia = pygame.mask.from_surface(imagem_area_PRAIA)
        
        # Cria uma máscara para o objeto
        rect_objeto = pygame.Rect(objeto["x"], objeto["y"], objeto["botao"].imagem.get_width(), objeto["botao"].imagem.get_height())
        mask_objeto = pygame.mask.from_surface(objeto["botao"].imagem)
        
        # Obter o deslocamento entre o objeto e a área da praia
        deslocamento = (rect_objeto.x - posicao_area_PRAIA[0], rect_objeto.y - posicao_area_PRAIA[1])
        
        # Verifica se as máscaras se sobrepõem
        if mask_area_praia.overlap(mask_objeto, deslocamento):
            return True
        return False

    def colisao_com_area_LIXO(objeto):
        # Cria uma máscara para a área do lixo
        mask_area_lixo = pygame.mask.from_surface(imagem_area_LIXO)
        
        # Cria uma máscara para o objeto
        rect_objeto = pygame.Rect(objeto["x"], objeto["y"], objeto["botao"].imagem.get_width(), objeto["botao"].imagem.get_height())
        mask_objeto = pygame.mask.from_surface(objeto["botao"].imagem)
        
        # Obter o deslocamento entre o objeto e a área do lixo
        deslocamento = (rect_objeto.x - posicao_area_LIXO[0], rect_objeto.y - posicao_area_LIXO[1])
        
        # Verifica se as máscaras se sobrepõem
        if mask_area_lixo.overlap(mask_objeto, deslocamento):
            return True
        return False

    objetos = []
    
    posicoes_fixas = [
        (89, 162), (287, 163), (500, 155), (679, 158),
        (837, 162), (222, 290), (438, 299), (674, 313),
        (326, 463), (563, 468)
    ]

    def posicionar_objetos(lista_imagens, tipo="correto"):
        imagens_selecionadas = lista_imagens  # Lista de imagens a posicionar

        # Embaralha as imagens antes de atribuir às posições fixas
        random.shuffle(imagens_selecionadas)

        # Faz uma cópia das posições fixas disponíveis
        posicoes_disponiveis = posicoes_fixas.copy()

        for imagem in imagens_selecionadas:
            if len(posicoes_disponiveis) > 0:  # Verifica se há posições disponíveis
                # Extrair o nome do arquivo da imagem (sem extensão)
                nome_objeto = imagem.split("/")[-1].split(".")[0].replace("_", " ").capitalize()

                # Escolhe uma posição disponível
                posicao_escolhida = random.choice(posicoes_disponiveis)
                while any(objeto["x"] == posicao_escolhida[0] and objeto["y"] == posicao_escolhida[1] for objeto in objetos):
                    # Se a posição já estiver ocupada, escolhe outra posição
                    posicao_escolhida = random.choice(posicoes_disponiveis)

                # Remove a posição já utilizada
                posicoes_disponiveis.remove(posicao_escolhida)

                # Atribuir a área com base no tipo
                area = "praia" if tipo == "correto" else "lixo"

                # Cria o botão para o objeto
                x, y = posicao_escolhida
                botao = criarBotaoImagensFASE3(x, y, imagem, imagem)
                objetos.append({"x": x, "y": y, "botao": botao, "tipo": tipo, "movimento": 0, "nome": nome_objeto, "area": area})
            else:
                break  # Interrompe o loop se não houver mais posições disponíveis

    # Posicionar objetos corretos e incorretos
    posicionar_objetos(imagensCorretasSelecionadas, "correto")
    posicionar_objetos(imagensIncorretasSelecionadas, "incorreto")

    lampadaAcesaImagem = pygame.image.load("imagens/GUI/lampadas/lampadaAcesa.png")
    lampadaApagadaImagem = pygame.image.load("imagens/GUI/lampadas/lampadaApagada.png")
    lampada = criarBotao(980, 170, "imagens/GUI/lampadas/lampadaApagada.png", "imagens/GUI/lampadas/lampadaApagada.png")

     # Configurações do temporizador
    tempo_inicial = 300  # Tempo inicial em segundos
    tempo_restante = tempo_inicial
    tempo_inicializado = pygame.time.get_ticks()  # Registrar o momento em que o temporizador começa
    
    # Variáveis para controle de arrasto
    arrastando_objeto = None  # O objeto que está sendo arrastado
    deslocamento_x = 0
    deslocamento_y = 0

    mostrar_informacoes = True
    fase_ativa = True
    circulo = False
    som_da_lampada = False

    fonte2 = pygame.font.Font("tipografia/LuckiestGuy-Regular.ttf", 25)  # Fonte padrão de tamanho 36
    cor_texto = (255, 255, 255)  # Cor do texto (branco)
    cor_contorno = (0, 0, 0)  # Cor do contorno (preto)

    while fase_ativa:
        if not jogoGanhou and not jogoPerdeu:
            if lampada_acesa:
                lampada.mudarImagem(lampadaAcesaImagem, lampadaAcesaImagem)
                if not som_da_lampada:
                    som_dica.play()  # Toca o som apenas se não foi tocado ainda
                    som_da_lampada = True  # Marca o som como tocado
            else:
                lampada.mudarImagem(lampadaApagadaImagem, lampadaApagadaImagem)
                som_da_lampada = False

        tela.blit(fase3Background, (0, 0))
        if jogoPerdeu:
            salvar_pontuacao(nome_jogador, 3, pontuacao_fase3, tempo_decorrido) 
            tela.blit(pygame.image.load("imagens/fase3/perdeuPraia.png"), (0, 0))
            objetos.clear()  # Limpa todos os objetos
        elif jogoGanhou:
            salvar_pontuacao(nome_jogador, 3, pontuacao_fase3, tempo_decorrido) 
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
            tela.blit(vida_imagens[vidas], (440, 650))  # Exibe a imagem das vidas no canto superior esquerdo
            # Configurações para o texto de "VIDAS"
            texto_vidas = "VIDAS"
            texto_vidas_contorno = fonte1.render(texto_vidas, True, (0, 0, 0))  # Contorno preto
            texto_vidas_preenchimento = fonte1.render(texto_vidas, True, cor_texto)  # Texto branco

            # Posição do texto "VIDAS" ajustada
            posicao_vidas = (largura_tela // 2 - texto_vidas_contorno.get_width() + 65 // 1.32, altura_tela - 30)

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
            300,  # Posiciona um pouco abaixo do texto
            "imagens/GUI/botaoTentarnovamente/tentarnovamente.png",
            "imagens/GUI/botaoTentarnovamente/tentarnovamente1.png"
        )

        fasesBotao = criarBotao(
            410,  # Centraliza horizontalmente
            410,  # Posiciona um pouco abaixo do botão "Tentar Novamente"
            "imagens/GUI/botaoFases/fasesBotao.png", 
            "imagens/GUI/botaoFases/fasesBotao.png" 
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao = criarBotao(
            405,  # Centraliza horizontalmente
            510,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Criar o botão de "Voltar ao Menu"
        voltarMenuBotao2 = criarBotao(
            405,  # Centraliza horizontalmente
            400,  # Posiciona um pouco abaixo do botão "Próxima Fase"
            "imagens/GUI/botaoVoltarMenu/voltaraomenu.png",  # Imagem do botão
            "imagens/GUI/botaoVoltarMenu/voltaraomenu1.png"  # Imagem do botão (hover)
        )

        # Se o jogo foi ganho ou perdido, exibe o tempo total e o número de objetos errados
        if jogoGanhou or jogoPerdeu:
            mostrar_informacoes = False
            jogoConcluido = True
            
            if jogoPerdeu:
                pontuacao_fase3 = 0    
                fasesBotao.atualizarImagem(posicaoMouse)
                fasesBotao.desenharBotao(tela)

                if fasesBotao.clicarBotao(tela):
                    som_click.play()
                    print("botao fases clicado")
                    estadoJogo = "jogando"
                    fase_ativa = False
                    lampada_acesa = False
                    iniciarFases()

                voltarMenuBotao.atualizarImagem(posicaoMouse)
                voltarMenuBotao.desenharBotao(tela)
                # Verificar clique no botão "Voltar ao Menu"
                if voltarMenuBotao.clicarBotao(tela):
                    som_click.play()  # Tocar som de clique
                    print("Botão 'Voltar ao Menu' clicado.")
                    estadoJogo = "menu"  # Voltar para o menu
                    fase_ativa = False  # Sai do loop atual
                    lampada_acesa = False
                    menuPrincipal()  # Chama a função do menu principal

            if jogoGanhou:
                voltarMenuBotao2.atualizarImagem(posicaoMouse)
                voltarMenuBotao2.desenharBotao(tela)
                # Verificar clique no botão "Voltar ao Menu"
                if voltarMenuBotao2.clicarBotao(tela):
                    som_click.play()  # Tocar som de clique
                    print("Botão 'Voltar ao Menu' clicado.")
                    estadoJogo = "menu"  # Voltar para o menu
                    fase_ativa = False  # Sai do loop atual
                    lampada_acesa = False
                    menuPrincipal()  # Chama a função do menu principal

            # Desenhar o botão "Tentar Novamente"
            botaoTentarNovamente.atualizarImagem(posicaoMouse)
            botaoTentarNovamente.desenharBotao(tela)

            # Verificar clique no botão "Tentar Novamente"
            if botaoTentarNovamente.clicarBotao(tela):
                som_click.play()  # Tocar o som de clique
                print("Botão 'Tentar Novamente' clicado.")
                fase_ativa = False  # Sai do loop atual
                lampada_acesa = False
                fase3(nome_jogador)  # Reinicia a fase

            tempo_total = tempo_inicial - tempo_restante  # Tempo total que o jogador levou
            erros = imagensIncorretasClicadas  # Número de objetos errados que o jogador clicou
            
            # Configurações para o texto a ser exibido (pode usar a mesma fonte que foi definida antes)
            texto_conclusao = f"Tempo: {tempo_total // 60:02}:{tempo_total % 60:02} | Erros: {erros}"

            # Renderizando o texto para mostrar no centro da tela
            texto_contorno_conclusao = fonte1.render(texto_conclusao, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_conclusao = fonte1.render(texto_conclusao, True, cor_texto)  # Texto branco
            posicao_conclusao = (largura_tela // 2 - texto_contorno_conclusao.get_width() // 2, altura_tela // 2 - 120)  # Centraliza o texto

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

            texto_contorno_tempo = fonte1.render(texto_tempo, True, (0, 0, 0))  # Contorno preto
            texto_preenchimento_tempo = fonte1.render(texto_tempo, True, cor_texto)  # Texto branco
            posicao_tempo = (710, 20)  # Posição abaixo do contador de objetos

            # Desenhar o texto com contorno
            tela.blit(texto_contorno_tempo, (posicao_tempo[0] - 1, posicao_tempo[1]))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0] + 1, posicao_tempo[1]))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] - 1))
            tela.blit(texto_contorno_tempo, (posicao_tempo[0], posicao_tempo[1] + 1))

            # Desenhar o texto preenchido no centro
            tela.blit(texto_preenchimento_tempo, posicao_tempo)

            # Renderiza o texto do contador com contorno
            texto_contorno = fonte1.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/10", True, (0, 0, 0))  # Preto para o contorno
            texto_preenchimento = fonte1.render(f"TOTAL DE OBJETOS: {imagensCorretasClicadas}/10", True, cor_texto)  # Cor original

            posicao_texto = (180, 20)  

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
       
        if not jogoGanhou and not jogoPerdeu:
            botaoTutorial.atualizarImagem(posicaoMouse)
            botaoTutorial.desenharBotao(tela)
        
            lampada.atualizarImagem(posicaoMouse)
            lampada.desenharBotao(tela)
            
            if lampada_acesa:
                lampada.mudarImagem(lampadaAcesaImagem, lampadaAcesaImagem)
                
                # Verifica se o som já foi tocado
                if not som_da_lampada:
                    som_dica.play()  # Toca o som apenas se não foi tocado ainda
                    som_da_lampada = True  # Marca o som como tocado
                                
                # Criar o texto "Dica" com contorno
                texto_dica_contorno = fonte2.render("Dica", True, cor_contorno)  # Contorno do texto
                texto_dica_preenchimento = fonte2.render("Dica", True, cor_texto)  # Texto preenchido com a cor original

                # Posicionamento do texto sobre a lâmpada
                posicao_texto = (lampada.rect.x + 10, lampada.rect.y + 100)

                # Desenhar o contorno do texto em 4 direções (esquerda, direita, cima, baixo)
                tela.blit(texto_dica_contorno, (posicao_texto[0] - 1, posicao_texto[1]))  # Esquerda
                tela.blit(texto_dica_contorno, (posicao_texto[0] + 1, posicao_texto[1]))  # Direita
                tela.blit(texto_dica_contorno, (posicao_texto[0], posicao_texto[1] - 1))  # Cima
                tela.blit(texto_dica_contorno, (posicao_texto[0], posicao_texto[1] + 1))  # Baixo

                # Desenhar o texto preenchido sobre o contorno
                tela.blit(texto_dica_preenchimento, posicao_texto)

       # Verificar clique na lâmpada
        if lampada.clicarBotao(tela):
            if lampada_acesa:
                circulo = True
            som_click.play()  # Som de clique

            # Verifica se o último objeto confirmado foi incorreto
            if ultimo_objeto_confirmado and ultimo_objeto_confirmado["tipo"] == "incorreto":
                objetos_incorretos = [obj for obj in objetos if obj["tipo"] == "incorreto"]  # Filtra objetos incorretos
                if objetos_incorretos:  # Se houver objetos incorretos
                    objeto_circulado = random.choice(objetos_incorretos)  # Circula um objeto incorreto aleatório
                lampada_acesa = False  # Apaga a lâmpada após o clique
            
            # Verifica se o último objeto confirmado foi correto
            if ultimo_objeto_confirmado and ultimo_objeto_confirmado["tipo"] == "correto":
                objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]  # Filtra objetos corretos
                if objetos_corretos:  # Se houver objetos corretos
                    objeto_circulado = random.choice(objetos_corretos)  # Circula um objeto correto aleatório
                lampada_acesa = False  # Apaga a lâmpada após o clique
                # Desenhar o círculo ao redor do objeto circulado

        # Verifica se há um objeto circulado e se o círculo deve ser desenhado
        if objeto_circulado and circulo:
            desenhar_circulo_redondo(objeto_circulado)

            # Desenha o círculo nas áreas correspondentes ao objeto selecionado
            if objeto_circulado["area"] == "praia":
                desenhar_circulo_area(955, 605)  # Circulando área praia
            elif objeto_circulado["area"] == "lixo":
                desenhar_circulo_area(130, 605)  # Circulando área lixo
                
        if voltarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Voltar clicado")
            estadoJogo = "jogando"
            if jogoConcluido == False:
                pontuacao_fase3 = 0
            fase_ativa = False
            lampada_acesa = False

        elif configuracoesBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Configurações clicado")
            abrirConfiguracoesFases()
        
        elif botaoTutorial.clicarBotao(tela):
            som_click.play()
            print("tutorial clicado")
            mostrarVideo("video/fase3.mp4", 600, 300, "imagens/fase3/imagemTutorialPraia.png", "sons/tutorial/fase3.wav", "sons/musicaPraia/fundoPraia.mp3")
        
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
                            # Fala o som do nome do objeto
                            falar_nome_objeto(obj)
                            arrastando_objeto = obj  # Inicia o arraste do objeto
                            deslocamento_x = posicaoMouse[0] - obj["x"]  # Calcula o deslocamento
                            deslocamento_y = posicaoMouse[1] - obj["y"]

                            if lampada.clicarBotao(tela):
                                # Verifica se o objeto clicado é o mesmo que está circulado
                                if lampada_acesa and objeto_circulado and obj == objeto_circulado:
                                    lampada_acesa = False  # Apaga a lâmpada
                                    objeto_circulado = None  # Remove o objeto circulado

            # Durante o movimento do mouse, se estiver arrastando
            elif event.type == pygame.MOUSEMOTION:
                if arrastando_objeto and pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo está pressionado
                    posicaoMouse = pygame.mouse.get_pos()
                    # Atualiza a posição do objeto e o texto associado ao objeto
                    arrastando_objeto["x"] = posicaoMouse[0] - deslocamento_x
                    arrastando_objeto["y"] = posicaoMouse[1] - deslocamento_y
                    print(f"Posição do objeto: X = {arrastando_objeto['x']}, Y = {arrastando_objeto['y']}")
            # Quando o mouse é solto, para o arraste
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Verifica se o botão solto é o esquerdo
                    if arrastando_objeto:
                        # Verifica se o objeto foi colocado na área correta ou incorreta
                        if colisao_com_area_PRAIA(arrastando_objeto):
                            lampada_acesa = False
                            if arrastando_objeto["tipo"] == "correto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensCorretasClicadas += 1  # Incrementa a pontuação de objetos corretos
                                pontuacao_fase3 += 1
                                todasImagens += 1
                                tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3", volume=0.3)
                            elif arrastando_objeto["tipo"] == "incorreto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensIncorretasClicadas += 1  # Incrementa a pontuação de objetos incorretos
                                todasImagens += 1
                                vidas -= 1
                                if vidas == 0:
                                    jogoPerdeu = True
                                lampada_acesa = True
                                tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3", volume=0.4)
                                objetos_incorretos = [obj for obj in objetos if obj["tipo"] == "incorreto"]
                                if objetos_incorretos:
                                    objeto_circulado = random.choice(objetos_incorretos)  # Circula um objeto correto
                        elif colisao_com_area_LIXO(arrastando_objeto):
                            lampada_acesa = False
                            if arrastando_objeto["tipo"] == "correto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensIncorretasClicadas += 1  # Incrementa a pontuação de objetos incorretos
                                todasImagens += 1
                                vidas -= 1
                                if vidas == 0:
                                    jogoPerdeu = True
                                lampada_acesa = True
                                tocar_efeito_sonoro("sons/somObjetoIncorreto/respostaErrada.mp3", volume=0.4)
                                objetos_corretos = [obj for obj in objetos if obj["tipo"] == "correto"]
                                if objetos_corretos:
                                    objeto_circulado = random.choice(objetos_corretos)  # Circula um objeto correto
                            elif arrastando_objeto["tipo"] == "incorreto":
                                objetos.remove(arrastando_objeto)  # Remove o objeto da lista
                                imagensCorretasClicadas += 1  # Incrementa a pontuação de objetos corretos
                                pontuacao_fase3 += 1
                                todasImagens += 1
                                tocar_efeito_sonoro("sons/somObjetoCorreto/respostaCerta.mp3", volume=0.3)

                        if imagensCorretasClicadas == 10:
                            jogoGanhou = True
                        elif imagensCorretasClicadas >= 5 and todasImagens == 10:
                            jogoGanhou = True
                        elif imagensCorretasClicadas < 5 and todasImagens == 10:
                            jogoPerdeu = True

                        # Para o arraste ao soltar o botão do mouse
                        arrastando_objeto = None
                        circulo = False
            
        # Atualizar e desenhar os objetos com as novas posições
        for obj in objetos:
            botao = obj["botao"]
            botao.rect.topleft = (obj["x"], obj["y"])  # Atualiza a posição do objeto gráfico
            botao.atualizarImagem(posicaoMouse)  # Atualiza a imagem do objeto (se necessário)
            botao.desenharBotao(tela)  # Desenha o objeto na nova posição

            # Verifica se o mouse está sobre o objeto (hover)
            if botao.rect.collidepoint(posicaoMouse):  # Verifica se o mouse está sobre o botão
                 exibir_nome_objeto(obj)
            else:
                obj["som_tocado"] = False  # Reseta para permitir que o som toque novamente
            
            # Atualiza a tela
        pygame.display.update() 
        clock.tick(60)
        
# Função para o menu principal
def menuPrincipal():
    global somAtivo
    global estadoJogo
    global menuBackground
    menuBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")

    if somAtivo:
        tocar_musica("sons/musicaMenu/musicafundo.mp3")  # Toca a primeira música

    # Criando botões do menu
    jogarBotao = criarBotao(400, 300, "imagens/GUI/botaoJogar/jogar0.png", "imagens/GUI/botaoJogar/jogar1.png")
    configuracoesBotao = criarBotao(936, 20, "imagens/GUI/botaoConfiguracoes/configuracoes0.png", "imagens/GUI/botaoConfiguracoes/configuracoes1.png")
    instrucoesBotao = criarBotao(400, 425, "imagens/GUI/botaoInicio/instrucoes1.png", "imagens/GUI/botaoInicio/instrucoes01.png")
    sairBotao = criarBotao(20, 20, "imagens/GUI/botaoSair/sair0.png", "imagens/GUI/botaoSair/sair1.png")
    creditosBotao = criarBotao(990, 620, "imagens/GUI/botaoConfiguracoes/info0.png", "imagens/GUI/botaoConfiguracoes/info1.png")
    suporteBotao = criarBotao(30, 620, "imagens/GUI/botaoConfiguracoes/suporte0.png", "imagens/GUI/botaoConfiguracoes/suporte1.png")  
    pontuacaoBotao = criarBotao(400, 550, "imagens/GUI/botaoPontuacao/pontuacao0.png", "imagens/GUI/botaoPontuacao/pontuacao1.png")
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
        suporteBotao.atualizarImagem(posicaoMouse)
        pontuacaoBotao.atualizarImagem(posicaoMouse)

        jogarBotao.desenharBotao(tela)
        configuracoesBotao.desenharBotao(tela)
        instrucoesBotao.desenharBotao(tela)
        sairBotao.desenharBotao(tela)
        creditosBotao.desenharBotao(tela)
        suporteBotao.desenharBotao(tela)
        pontuacaoBotao.desenharBotao(tela)

        # Verificar cliques
        if jogarBotao.clicarBotao(tela):
            som_click.play()  # Som de clique
            print("Jogar clicado")
            estadoJogo = "jogando"
            pedir_nome()  # Jogador digita o nome
            adicionar_jogador(nome_jogador)  # Salva no JSON
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
        
        if suporteBotao.clicarBotao(tela):  # Detecta clique no botão de créditos
            som_click.play()  # Som de clique
            print("Suporte Clicado")
            abrirSuporte()
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
            abrirRelatorio(nome_jogador)
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
        fase1(nome_jogador)
    elif estadoJogo == "fase2":
        fase2(nome_jogador)
    elif estadoJogo == "fase3":
        fase3(nome_jogador)
    

# Finaliza o pygame
pygame.quit()

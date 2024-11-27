import pygame # importando biblioteca
import botao

pygame.init() # inicializa os principais módulos (alguns dizem que é importante usar, outros não)

# Resolução
telaLargura = 1100
telaAltura = 720

tela = pygame.display.set_mode((telaLargura, telaAltura)) # variável tela recebe a resolução
pygame.display.set_caption("Lixo_No_Lixo") # nome do jogo

estadoJogo = "menu" # situação atual do jogo, para rastrear as telas

def criarBotao(x, y, imagem, imagemAlterada): # função para criar botões
    imagem = pygame.image.load(imagem).convert_alpha()
    imagemAlterada = pygame.image.load(imagemAlterada).convert_alpha()
    return botao.Botao(x, y, imagem, imagemAlterada)

def iniciarFases(): # função das fases (talvez precise mudar/colocar muita coisa aqui)
    fase1Background = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg")
    tela.blit(fase1Background, (0, 0))

def menuPrincipal(): # função jogo
    global estadoJogo

    # criando os botões do jogo
    jogarBotao = criarBotao(295, 130, "imagens/GUI/botaoJogar/jogar0.png", "imagens/GUI/botaoJogar/jogar1.png")
    sairBotao = criarBotao(390, 370, "imagens/GUI/botaoSair/sair0.png", "imagens/GUI/botaoSair/sair1.png")
    voltarBotao = criarBotao(800, 570, "imagens/GUI/botaoVoltar/voltar0.png", "imagens/GUI/botaoVoltar/voltar1.png")

    posicaoMouse = pygame.mouse.get_pos()

    run = True
    while run: 
        menuBackground = pygame.image.load("imagens/GUI/Backgrounds/menuBackground.jpg").convert_alpha() # backGround do menu
        tela.blit(menuBackground,(0, 0)) # coloca a imagem na tela

        posicaoMouse = pygame.mouse.get_pos()

        # mantem a imagem do botão atualizada de acordo com a posição do mouse do usuário
        jogarBotao.atualizarImagem(posicaoMouse) 
        sairBotao.atualizarImagem(posicaoMouse)
        voltarBotao.atualizarImagem(posicaoMouse)

        # lógica feia de if else para troca de dela (provável alteração no futuro?)
        if estadoJogo == "menu":
            # botões do menu
            jogarBotao.desenharBotao(tela)
            sairBotao.desenharBotao(tela)

            if jogarBotao.clicarBotao(tela): 
                print("Jogar clicado")
                estadoJogo = "jogando"

            if sairBotao.clicarBotao(tela):
                print("Sair clicado")
                run = False  

        if estadoJogo == "jogando":
            iniciarFases()
            #botões das fases
            voltarBotao.desenharBotao(tela)

            if voltarBotao.clicarBotao(tela):
                print("Voltar clicado")
                estadoJogo = "menu"
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
                pygame.quit()

        pygame.display.update() # atualiza a tela

# iniciar jogo
menuPrincipal()

    
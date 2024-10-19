import pygame # importando biblioteca
import botao

pygame.init() # inicializa os principais modulos (alguns dizem que é importante usar, outros não)

# Resolução
telaLargura = 1100
telaAltura = 720

tela = pygame.display.set_mode((telaLargura, telaAltura)) # variável tela recebe a resolução
pygame.display.set_caption("Lixo_No_Lixo") # nome do jogo

estadoJogo = "menu" # situação atual do jogo, para rastrear as telas

def criarBotao(x, y, caminhoImagem): # função para criar botões
    imagem = pygame.image.load(caminhoImagem).convert_alpha()
    return botao.Botao(x, y, imagem)

def iniciarFases():
    fase1Background = pygame.image.load("imagens/fase1/imagemFloresta.png")
    tela.blit(fase1Background, (0, 0))

def menuPrincipal(): # função jogo
    global estadoJogo

    # criando os botões do jogo
    jogarBotao = criarBotao(390, 110, "imagens/menu/menuJogar.png") 
    sairBotao = criarBotao(390, 370, "imagens/menu/menuSair.png")
    voltarBotao = criarBotao(800, 570, "imagens/menu/menuVoltar.png")

    run = True
    while run: 
        menuBackground = pygame.image.load("imagens/menu/menuBackground.png").convert_alpha() # backGround do menu
        tela.blit(menuBackground,(0, 0)) # coloca a imagem na tela

        # lógica feia de if else para troca de dela (provável alteração no futuro?)
        if estadoJogo == "menu": 
            if jogarBotao.clicarBotao(tela): 
                print("Jogar clicado")
                estadoJogo = "jogando"

            if sairBotao.clicarBotao(tela):
                print("Sair clicado")
                run = False  

        if estadoJogo == "jogando":
            iniciarFases()
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

    
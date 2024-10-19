import pygame # importando biblioteca
import botao

pygame.init() # inicializa os principais modulos (alguns dizem que é importante usar, outros não)

# Resolução
telaLargura = 1100
telaAltura = 720

tela = pygame.display.set_mode((telaLargura, telaAltura)) # variável tela recebe a resolução
pygame.display.set_caption("Lixo_No_Lixo") # nome do jogo

def menuPrincipal(): # função do menu
    menuBackground = pygame.image.load("imagens/menu/menuBackground.png") # variável menuImagem recebe o carregamento da imagem 
    jogarImagem = pygame.image.load("imagens/menu/menuJogar.png").convert_alpha()
    sairImagem = pygame.image.load("imagens/menu/menuSair.png").convert_alpha()
    
    # cria os objetos nas coordenadas + imagem passadas como parâmetro
    jogarBotao = botao.Botao(390, 110, jogarImagem) 
    sairBotao = botao.Botao(390, 370, sairImagem)

    tela.blit(menuBackground,(0, 0)) # coloca a imagem na tela
    
     # aqui usa a função do objeto Botao
    if jogarBotao.criarBotao(tela):
        print("Jogar clicado")

    if sairBotao.criarBotao(tela):
        print("Sair clicado")

    pygame.display.update() # atualiza a tela


def jogo(): # função jogo
    iniciar = True

    while iniciar:
        menuPrincipal()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iniciar = False  
    pygame.quit()
    
# iniciar jogo
jogo()

    
import pygame # importando biblioteca

pygame.init() # inicializa os principais modulos (alguns dizem que é importante usar, outros não)

# Resolução
telaLargura = 1100
telaAltura = 720

tela = pygame.display.set_mode((telaLargura, telaAltura)) # variável tela recebe a resolução
pygame.display.set_caption("Lixo_No_Lixo") # nome do jogo

def menuPrincipal(): # função do menu
    tela.fill((0, 0, 10)) # RGB

    menuImagem = pygame.image.load("imagens/menu/menu.png") # variável menuImagem recebe o carregamento da imagem 
    tela.blit(menuImagem,(0, 0)) # coloca a imagem na tela
    
    pygame.display.update() # atualiza a tela


def jogo(): # função jogo

    iniciar = True
    clock = pygame.time.Clock()

    menuPrincipal()

    while iniciar:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            iniciar = False  
            pygame.quit()
    
# iniciar jogo
jogo() # teste


    
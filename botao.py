import pygame

class Botao(): # objeto
    def __init__(self, x, y, image): # self = ele mesmo; x,y = coordenadas; image = imagem para o botão
        self.image = image
        self.rect = self.image.get_rect() # cria um retângulo para o objeto do tamanho da imagem, por isso get_rect
        self.rect.topleft = (x, y) # coordenadas para a posição que queremos o botão/imagem
        self.clicked = False # define o estado atual do botão como falso (não clicado)

    def criarBotao(self, tela): # mostrar botão na tela
        acao = False # variável para rastrear as ações dos clicks
        
        tela.blit(self.image, (self.rect.x, self.rect.y)) # coloca o botão na tela com as coordenadas do retângulo passadas

        posicaoMouse = pygame.mouse.get_pos() # variável recebe posição do mouse

        if self.rect.collidepoint(posicaoMouse): # verifica se o objeto "colidiu" com o mouse
            # verifica se algum click foi feito, >> [0] para click esquerdo, se fosse o direito seria [1] E se o estado do objeto está clicked False
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked: 
                self.clicked = True
                acao = True
        if pygame.mouse.get_pressed()[0] == 0: # se o botão não está sendo clicado
            self.clicked = False

        return acao    
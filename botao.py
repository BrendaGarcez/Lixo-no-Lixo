import pygame

class Botao(): # objeto
    def __init__(self, x, y, imagem, imagemAlterada): # self = ele mesmo; x, y = coordenadas; image = imagem para o botão (função init: método construtor)
        self.imagemOriginal = imagem
        self.imagemAlterada = imagemAlterada # imagem com highlight
        self.imagem = self.imagemOriginal # define a imagem do objeto original
        
        self.rect = self.imagem.get_rect() # cria um retângulo para o objeto do tamanho da imagem, por isso get_rect
        self.rect.topleft = (x, y) # coordenadas para a posição que queremos o botão/imagem
        self.clicked = False # define o estado atual do botão como falso (não clicado)

    def desenharBotao(self, tela):
        tela.blit(self.imagem, (self.rect.x, self.rect.y))
    
    def clicarBotao(self, tela): # mostrar/criar/clicar no botão na tela
        acao = False # variável para rastrear as ações dos clicks
        
        posicaoMouse = pygame.mouse.get_pos() # variável recebe posição do mouse

        if self.rect.collidepoint(posicaoMouse): # verifica se o objeto "colidiu" com o mouse
           
           # verifica se algum click foi feito, >> [0] para click esquerdo, se fosse o direito seria [1] E se o estado do objeto está clicked False
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked: 
                self.clicked = True
                acao = True
                
        if pygame.mouse.get_pressed()[0] == 0: 
            self.clicked = False 

        return acao 
    
    def atualizarImagem(self, posicaoMouse): # caso o mouse do usuário passar em cima troca a imagem 
        if self.rect.collidepoint(posicaoMouse):
            self.imagem = self.imagemAlterada
        else: # imagem volta ao original ao tirar o mouse de cima
            self.imagem = self.imagemOriginal 
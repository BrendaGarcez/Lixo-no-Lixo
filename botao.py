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
    
    def clicarBotao(self, tela):
        acao = False  # variável para rastrear as ações dos cliques
        posicaoMouse = pygame.mouse.get_pos()  # variável recebe a posição do mouse

        # Verifica se o mouse está dentro da área do botão
        if self.rect.collidepoint(posicaoMouse):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.clicked:  # Detecta o clique apenas uma vez
                        self.clicked = True
                        acao = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.clicked = False  # Reseta a flag ao liberar o mouse

        return acao

    
    def atualizarImagem(self, posicaoMouse): # caso o mouse do usuário passar em cima troca a imagem 
        if self.rect.collidepoint(posicaoMouse):
            self.imagem = self.imagemAlterada
        else: # imagem volta ao original ao tirar o mouse de cima
            self.imagem = self.imagemOriginal 
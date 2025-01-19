import pygame

class Botao():
    def __init__(self, x, y, imagem, imagemAlterada): 
        self.imagemOriginal = imagem
        self.imagemAlterada = imagemAlterada 
        self.imagem = self.imagemOriginal
        
        self.rect = self.imagem.get_rect() 
        self.rect.topleft = (x, y) 
        self.clicked = False 

    def desenharBotao(self, tela):
        tela.blit(self.imagem, (self.rect.x, self.rect.y))
    
    def clicarBotao(self, tela):
        acao = False  
        posicaoMouse = pygame.mouse.get_pos()  

        if self.rect.collidepoint(posicaoMouse):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.clicked:  
                        self.clicked = True
                        acao = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.clicked = False  

        return acao

    def atualizarImagem(self, posicaoMouse): 
        if self.rect.collidepoint(posicaoMouse):
            self.imagem = self.imagemAlterada
            # Aumenta a imagem (zoom) quando o mouse passa por cima
            largura, altura = self.imagem.get_size()
            self.imagem = pygame.transform.scale(self.imagem, (int(largura * 1.05), int(altura * 1.05)))  # Aumenta 20% do tamanho
        else:
            self.imagem = self.imagemOriginal
            largura, altura = self.imagem.get_size()
            self.imagem = pygame.transform.scale(self.imagem, (int(largura), int(altura)))  # Volta ao tamanho original

import pygame

class BotaoObjetos():
    def __init__(self, x, y, imagem, imagemAlterada): 
        self.imagemOriginal = imagem
        self.imagemAlterada = imagemAlterada 
        self.imagem = self.imagemOriginal 
        
        self.rect = self.imagem.get_rect() 
        self.rect.topleft = (x, y) 
        self.clicked = False 
        
        # Cria a máscara para o botão
        self.maskOriginal = pygame.mask.from_surface(self.imagemOriginal)
        self.maskAlterada = pygame.mask.from_surface(self.imagemAlterada)
        self.mask = self.maskOriginal  # Inicialmente, a máscara é a original

    def desenharBotao(self, tela):
        tela.blit(self.imagem, (self.rect.x, self.rect.y))
    
    def clicarBotao(self, tela):
        acao = False  
        posicaoMouse = pygame.mouse.get_pos()  

        # Verifica se o mouse está dentro da área do botão considerando a máscara (pixel-perfect)
        if self.rect.collidepoint(posicaoMouse):
            # Calcula a posição do mouse em relação ao retângulo do botão
            offset = (posicaoMouse[0] - self.rect.x, posicaoMouse[1] - self.rect.y)

            # Verifica se a posição do mouse está dentro da máscara do botão
            if self.mask.get_at(offset):  # Verifica se o pixel no offset está "ativo" na máscara
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
            # Calcula o offset do mouse e verifica se o pixel da máscara está ativo
            offset = (posicaoMouse[0] - self.rect.x, posicaoMouse[1] - self.rect.y)
            # Verifica se o offset está dentro dos limites da máscara
            largura, altura = self.mask.get_size()  # Obtém as dimensões da máscara
            if 0 <= offset[0] < largura and 0 <= offset[1] < altura:
                if self.mask.get_at(offset):  # Verifica pixel-perfect
                    self.imagem = self.imagemAlterada
                    self.mask = self.maskAlterada  # Atualiza a máscara para a versão alterada
                else:
                    self.imagem = self.imagemOriginal
                    self.mask = self.maskOriginal  # Volta para a máscara original
            else:
                # Se o offset estiver fora dos limites da máscara, volta à imagem original
                self.imagem = self.imagemOriginal
                self.mask = self.maskOriginal
        else:
            self.imagem = self.imagemOriginal
            self.mask = self.maskOriginal  # Volta para a máscara original

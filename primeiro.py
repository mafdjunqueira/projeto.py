import pygame
from pygame.locals import *
import random

pygame.init()

# Criar a janela
largura = 500
altura = 500
tamanho_tela = (largura, altura)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption('Corrida Feliz')

# Carregar imagem de capa
imagem_capa_original = pygame.image.load('START.png')
# Reduzir a imagem de capa para metade do tamanho original
largura_capa_original, altura_capa_original = imagem_capa_original.get_size()
nova_largura_capa = largura_capa_original // 1.55
nova_altura_capa = altura_capa_original // 1.55

# Redimensionar a imagem
imagem_capa = pygame.transform.scale(imagem_capa_original, (nova_largura_capa, nova_altura_capa))

# Exibir imagem de capa e aguardar entrada do usuário
exibindo_capa = True
while exibindo_capa:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()
        if evento.type == KEYDOWN:
            exibindo_capa = False

    # Centralizar a imagem na tela
    posicao_x = (largura - nova_largura_capa) // 2
    posicao_y = (altura - nova_altura_capa) // 2
    tela.fill((0, 0, 0))  # Preencher o fundo com preto (ou qualquer cor de fundo desejada)
    tela.blit(imagem_capa, (posicao_x, posicao_y))
    pygame.display.update()

# Loop para exibir a imagem de capa e aguardar entrada do usuário
exibindo_capa = True
while exibindo_capa:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
        if evento.type == KEYDOWN:
            exibindo_capa = False

    tela.blit(imagem_capa, ((largura - imagem_capa.get_width()) / 2, (altura - imagem_capa.get_height()) / 2))
    pygame.display.update()
  

# Cores
marrom = (139, 69, 19)
verde_escuro = (0, 100, 0)
vermelho = (200, 0, 0)
branco = (255, 255, 255)

# Tamanhos da pista e marcadores
largura_pista = 300
largura_marcador = 10
altura_marcador = 50

# Coordenadas das faixas
faixa_esquerda = 150
faixa_central = 250
faixa_direita = 350
faixas = [faixa_esquerda, faixa_central, faixa_direita]

# Pista e marcadores de borda
pista = (100, 0, largura_pista, altura)
marcador_borda_esquerda = (95, 0, largura_marcador, altura)
marcador_borda_direita = (395, 0, largura_marcador, altura)

# Para animar o movimento dos marcadores de faixa
movimento_marcador_faixa_y = 0

# Coordenadas iniciais do cavalo do jogador
cavalo_x = 250
cavalo_y = 400

# Configurações do frame
relogio = pygame.time.Clock()
fps = 120

# Configurações do jogo
fim_de_jogo = False
velocidade = 2
pontuacao = 0

# Carregar música
pygame.mixer.music.load('03-caipira-de-fato-joao-carreiro-172749.mp3')
pygame.mixer.music.play(-1)

# Classe Cavalo
class Cavalo(pygame.sprite.Sprite):
    def __init__(self, imagens, x, y):
        super().__init__()
        self.imagens = [pygame.transform.scale(img, (int(img.get_rect().width * 0.1), int(img.get_rect().height * 0.1))) for img in imagens]
        self.image = self.imagens[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.index_animacao = 0
        self.contador_animacao = 0

    def update(self):
        self.contador_animacao += 1
        if self.contador_animacao >= 10:
            self.contador_animacao = 0
            self.index_animacao = (self.index_animacao + 1) % len(self.imagens)
            self.image = self.imagens[self.index_animacao]

# Classe Colisao
class Colisao(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y):
        super().__init__()
        fator_escala_imagem =0.01
        nova_largura =  int(imagem.get_rect().width * fator_escala_imagem)
        nova_altura =   int(imagem.get_rect().height * fator_escala_imagem)
        self.image = pygame.transform.scale(imagem, (nova_largura, nova_altura))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Grupos de sprites
grupo_cavalo_jogador = pygame.sprite.Group()
grupo_cavalo = pygame.sprite.Group()
grupo_colisao = pygame.sprite.Group()
# Carregar as imagens de animação do cavalo do jogador
imagens_animacao_cavalo_jogador = []
for i in range(1, 5):
    imagem = pygame.image.load(f'cavalo{i}.png').convert_alpha()
    imagem.set_colorkey((0, 0, 0))  # Define a cor preta como transparente
    imagens_animacao_cavalo_jogador.append(imagem)

# Criar o cavalo do jogador com animação
cavalo_jogador = Cavalo(imagens_animacao_cavalo_jogador, cavalo_x, cavalo_y)
grupo_cavalo_jogador.add(cavalo_jogador)


imagens_animacao_cavalo_jogador = []
for i in range(1, 5):
    imagem = pygame.image.load(f'{i}.png').convert_alpha()
    imagem.set_colorkey((0, 0, 0))  # Define a cor preta como transparente
    imagens_animacao_cavalo_jogador.append(imagem)

# Carregar as imagens dos cavalos adversários
nomes_arquivos_imagens = ['Marrom.png', 'Rosa.png', 'Lilas.png', 'Verde.png','Azul.png']
imagens_cavalos = []
for nome_arquivo_imagem in nomes_arquivos_imagens:
    imagem = pygame.image.load(nome_arquivo_imagem).convert_alpha()
    imagem.set_colorkey((0, 0, 0))  # Define a cor preta como transparente
    imagens_cavalos.append(imagem)
# Carregar a imagem de colisão
imagem_colisao = pygame.image.load('colisão.png').convert_alpha()

# Loop do jogo
executando = True
while executando:
    relogio.tick(fps)
    
    for evento in pygame.event.get():
        if evento.type == QUIT:
            executando = False
        if evento.type == KEYDOWN:
            if evento.key == K_LEFT and cavalo_jogador.rect.center[0] > faixa_esquerda:
                cavalo_jogador.rect.x -= 100
            elif evento.key == K_RIGHT and cavalo_jogador.rect.center[0] < faixa_direita:
                cavalo_jogador.rect.x += 100

            for cavalo in grupo_cavalo:
                if pygame.sprite.collide_rect(cavalo_jogador, cavalo):
                    fim_de_jogo = True
                    if evento.key == K_LEFT:
                        cavalo_jogador.rect.left = cavalo.rect.right/2
                    elif evento.key == K_RIGHT:
                        cavalo_jogador.rect.right = cavalo.rect.left/2
                    rect_colisao = imagem_colisao.get_rect()
                    rect_colisao.center = [(cavalo_jogador.rect.center[0] + cavalo.rect.center[0]) //2, (cavalo_jogador.rect.center[1] + cavalo.rect.center[1]) //2]
                    colisao = Colisao(imagem_colisao, rect_colisao.center[0], rect_colisao.center[1])
                    grupo_colisao.add(colisao)

    tela.fill(verde_escuro)
    pygame.draw.rect(tela, marrom, pista)
    pygame.draw.rect(tela, verde_escuro, marcador_borda_esquerda)
    pygame.draw.rect(tela, verde_escuro, marcador_borda_direita)

    movimento_marcador_faixa_y += velocidade * 2
    if movimento_marcador_faixa_y >= altura_marcador * 2:
        movimento_marcador_faixa_y = 0
    for y in range(altura_marcador * -2, altura, altura_marcador * 2):
        pygame.draw.rect(tela, branco, (faixa_esquerda + 45, y + movimento_marcador_faixa_y, largura_marcador, altura_marcador))
        pygame.draw.rect(tela, branco, (faixa_central + 45, y + movimento_marcador_faixa_y, largura_marcador, altura_marcador))

    grupo_cavalo_jogador.update()
    grupo_cavalo_jogador.draw(tela)
    
    if len(grupo_cavalo) < 2:
        adicionar_cavalo = all(cavalo.rect.top >= cavalo.rect.height * 1.5 for cavalo in grupo_cavalo)
        if adicionar_cavalo:
            faixa = random.choice(faixas)
            imagem = random.choice(imagens_cavalos)
            cavalo = Cavalo([imagem], faixa, altura / -2)
            grupo_cavalo.add(cavalo)
    
    for cavalo in grupo_cavalo:
        cavalo.rect.y += velocidade
        if cavalo.rect.top >= altura:
            cavalo.kill()
            pontuacao += 1
            if pontuacao % 5 == 0:
                velocidade += 1

    grupo_cavalo.draw(tela)
    grupo_colisao.draw(tela)
    
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f'Pontuação: {pontuacao}', True, branco)
    tela.blit(texto, (10, 10))
    
    if pygame.sprite.spritecollide(cavalo_jogador, grupo_cavalo, True):
        fim_de_jogo = True
        rect_colisao = imagem_colisao.get_rect()
        rect_colisao.center = [cavalo_jogador.rect.center[0], cavalo_jogador.rect.top]
        colisao = Colisao(imagem_colisao, rect_colisao.center[0], rect_colisao.center[1])
        grupo_colisao.add(colisao)
   

    if fim_de_jogo:
        pygame.draw.rect(tela, vermelho, (0, 50, largura, 100))
        texto = fonte.render('Fim de jogo. Jogar novamente? (Digite S ou N)', True, branco)
        tela.blit(texto, (largura // 2 - texto.get_width() // 2, 75))
        pygame.display.update()
        
        while fim_de_jogo:
            relogio.tick(fps)
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    fim_de_jogo = False
                    executando = False
                if evento.type == KEYDOWN:
                    if evento.key == K_s:
                        fim_de_jogo = False
                        velocidade = 2
                        pontuacao = 0
                        grupo_cavalo.empty()
                        grupo_colisao.empty()
                        cavalo_jogador.rect.center = [cavalo_x, cavalo_y]
                    elif evento.key == K_n:
                        fim_de_jogo = False
                        executando = False
    
    pygame.display.update()

pygame.quit()

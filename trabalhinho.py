def ler_arquivo_pgm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        tipo_arquivo = arquivo.readline().strip()
        if tipo_arquivo != "P1":
            raise ValueError("O arquivo não é do tipo PGM P1")

        # Lê as dimensões da imagem (largura e altura)
        largura, altura = 0, 0
        for linha in arquivo:
            if not linha.strip():  # Ignora linhas em branco
                continue
            if linha.startswith('#'):  # Ignora comentários
                continue
            largura, altura = map(int, linha.split())
            break  # Encerra após a leitura da largura e altura

        # Lê os dados de intensidade (preto 1 ou branco 0), pixel por pixel
        dados_intensidade = []
        for linha in arquivo:
            # Ignora linhas em branco ou comentários
            if linha.strip() and not linha.startswith('#'):
                # Remove espaços em branco e quebra a linha em caracteres individuais
                valores = linha.strip()
                for valor in valores:
                    if valor.isdigit():  # Verifica se o caractere é um dígito
                        dados_intensidade.append(int(valor))

    return largura, altura, dados_intensidade


# Você dá os dados e ele salva no arquivo
def salvar_arquivo_pgm(nome_arquivo, largura, altura, dados_imagem):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('P1\n')
        arquivo.write(f"{largura} {altura}\n")

        # Escreve os dados da imagem
        for i in range(0, len(dados_imagem), largura):
            linha = " ".join(map(str, dados_imagem[i:i + largura]))
            arquivo.write(f"{linha}\n")
    print("Salva com sucesso")


# Nova função pra criar matriz
def lista_para_matriz(linhas, colunas, lista):
    if linhas * colunas != len(lista):
        raise ValueError("Tamanho da lista nao deixa criar a matriz")

    matriz = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            indice = i * colunas + j
            elemento = lista[indice]
            linha.append(elemento)
        matriz.append(linha)

    return matriz


# Função pra transformar uma matriz em uma lista
def cria_lista(matriz):
    lista = [item for sublista in matriz for item in sublista]
    return lista


# Pega os vizinhos do valor em matriz[i][j] (considerando máscara 3x3)
def pega_vizinhos(matriz, i, j):
    mascara = [matriz[i][j], matriz[i + 1][j], matriz[i + 1][j + 1], matriz[i - 1][j], matriz[i - 1][j + 1],
               matriz[i - 1][j - 1], matriz[i][j + 1], matriz[i][j - 1], matriz[i + 1][j - 1]]
    return mascara


# Aplica o filtro da mediana

# O filtro tá funcionando assim:
# 1. Lê a imagem que você quer aplicar o filtro
# 2. Cria uma matriz a partir do valor de "intensidade" encontrado na imagem
# 3. Cria uma matriz pra guardar os novos valores depois do filtro
# 4. Começa o loop em i = 1, j = 1 pegando os vizinhos
# 5. Ordena e pega o quarto elemento (mediana) e ja era
def filtro_mediana(largura, altura, intensidade):
    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    imagem_matriz_filtrada = lista_para_matriz(altura, largura, intensidade)

    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # print(f"{imagem_matriz[i][j]}: {i} {j}")
            mascara = pega_vizinhos(imagem_matriz, i, j)
            mascara.sort()
            imagem_matriz_filtrada[i][j] = mascara[4]

    imagem_matriz_filtrada = cria_lista(imagem_matriz_filtrada)
    return imagem_matriz_filtrada


def dilatacao(largura, altura, intensidade, elem):
    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    imagem_matriz_filtrada = lista_para_matriz(altura, largura, intensidade)
    qtde_linhas_elemento = len(elem)
    qtde_colunas_elemento = len(elem[0])

    # Loop pelos pixels da imagem, exceto a borda
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Se o pixel na imagem original estiver branco (valor 1)
            if imagem_matriz[i][j] == 1:
                # Aplica a dilatação usando o elemento estruturante
                for k in range(qtde_linhas_elemento):
                    for l in range(qtde_colunas_elemento):
                        # Atualiza os pixels na imagem filtrada com base no elemento estruturante
                        if elem[k][l] == 1:
                            # Define o pixel correspondente na imagem filtrada como branco (valor 1)
                            imagem_matriz_filtrada[i - 1 + k][j - 1 + l] = 1

    imagem_matriz_filtrada = cria_lista(imagem_matriz_filtrada)
    return imagem_matriz_filtrada


def erosao(largura, altura, intensidade, elem):
    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    imagem_matriz_filtrada = lista_para_matriz(altura, largura, intensidade)
    qtde_linhas_elemento = len(elem)
    qtde_colunas_elemento = len(elem[0])

    # Loop pelos pixels da imagem, exceto a borda
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Se o pixel na imagem original estiver braco (valor 1)
            if imagem_matriz[i][j] == 1:
                # Aplica erosão usando o elemento estruturante
                for k in range(qtde_linhas_elemento):
                    for l in range(qtde_colunas_elemento):
                        # Verifica se o pixel do elemento estruturante corresponde a um pixel branco na imagem
                        if elem[k][l] == 1 and imagem_matriz[i - 1 + k][j - 1 + l] != 1:
                            # Se algum dos pixels do elemento estruturante não corresponder a um pixel branco na imagem,
                            # o pixel na imagem filtrada é definido como preto (valor 0)
                            imagem_matriz_filtrada[i][j] = 0
                            break
                        else:
                            continue
                        break

    imagem_matriz_filtrada = cria_lista(imagem_matriz_filtrada)
    return imagem_matriz_filtrada


def abertura(largura, altura, intensidade, elem):
    e = erosao(largura, altura, intensidade, elem)
    r = dilatacao(largura, altura, e, elem)
    return r


def fechamento(largura, altura, intensidade, elem):
    d = dilatacao(largura, altura, intensidade, elem)
    r = erosao(largura, altura, d, elem)
    return r


def aplicar_negativo(largura, altura, dados_intensidade):
    imagem_matriz = lista_para_matriz(altura, largura, dados_intensidade)
    imagem_negativa = lista_para_matriz(altura, largura, dados_intensidade)

    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            imagem_negativa[i][j] = 1 - imagem_matriz[i][j]
    return cria_lista(imagem_negativa)
    # salvar_arquivo_pgm(nome_arquivo_saida, largura, altura, cria_lista(imagem_negativa))


# Calcula o valor do pixel dada uma máscara 3x3
def calcula_pixel(vizinhos, mascara):
    resultado = 0

    for i in range(3):
        for j in range(3):
            resultado += vizinhos[i][j] * mascara[i][j]

    if resultado < 0: return 0
    if resultado > 1: return 1
    return resultado


"""
Aplica o filtro Sobel somando os pixels de Sobel X e Sobel Y 
numa imagem final
"""


def sobel(largura, altura, intensidade):
    Gx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]

    Gy = [
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1],
    ]

    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    nova_imagem_matriz = [[0 for _ in range(largura)] for _ in range(altura)]

    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            vizinhos = lista_para_matriz(3, 3, pega_vizinhos(imagem_matriz, i, j))
            pixel_sobel_x = calcula_pixel(vizinhos, Gx)
            pixel_sobel_y = calcula_pixel(vizinhos, Gy)
            nova_imagem_matriz[i][j] = pixel_sobel_x or pixel_sobel_y
    return cria_lista(nova_imagem_matriz)


# Função para verificar se um elemento estruturante bate com a vizinhança
def verifica_elemento(imagem, i, j, elemento):
    for k in range(len(elemento)):
        for l in range(len(elemento[0])):
            if elemento[k][l] != imagem[i + k][j + l]:
                return False
    return True


# Função para contar palavras na imagem usando a transformada Hit or Miss
def contar_palavras(imagem, largura, altura):
    elemento_hit = [[1, 1], [0, 1]]  # Elemento estruturante para o início da palavra
    elemento_miss = [[0, 0], [1, 0]]  # Elemento estruturante para o fim da palavra

    imagem_matriz = lista_para_matriz(altura, largura, imagem)
    qtd_palavras = 0

    # Loop pela imagem
    for i in range(altura - 1):
        for j in range(largura - 1):
            # Verifica se o elemento Hit bate com a vizinhança
            if i < altura - 1 and j < largura - 1:
                if verifica_elemento(imagem_matriz, i, j, elemento_hit):
                    # Verifica se o elemento Miss bate com a vizinhança
                    if verifica_elemento(imagem_matriz, i, j + 1, elemento_miss):
                        qtd_palavras += 1

    return qtd_palavras


def soma_imagem(imagem1, imagem2, imagem_final):
    largura1, altura1, dados_intensidade1 = ler_arquivo_pgm(imagem1)
    imagem_matriz1 = lista_para_matriz(altura1, largura1, dados_intensidade1)
    largura2, altura2, dados_intensidade2 = ler_arquivo_pgm(imagem2)
    imagem_matriz2 = lista_para_matriz(altura2, largura2, dados_intensidade2)
    imagem_final_matriz = lista_para_matriz(altura1, largura1, dados_intensidade1)
    for i in range(1, altura1 - 1):
        for j in range(1, largura1 - 1):
            imagem_final_matriz[i][j] = imagem_matriz1[i][j] or imagem_matriz2[i][j]
    salvar_arquivo_pgm(imagem_final, largura1, altura1, cria_lista(imagem_final_matriz))


def imagem_terminada(imagem_entrada, imagem_saida, elem):
    largura, altura, intensidade = ler_arquivo_pgm(imagem_entrada)
    intensidade = filtro_mediana(largura, altura, intensidade)
    # for i in range(1):
    #     print(f"{i + 1}. iteração")
    #     img = dilatacao(largura, altura, intensidade, elem)
    #     intensidade = img
    # img = abertura(largura, altura, img, elem)
    img = filtro_mediana(largura, altura, intensidade)
    #com_sobel = sobel(largura, altura, img)
    #aplicar_negativo(largura, altura, com_sobel, imagem_saida)
    salvar_arquivo_pgm(imagem_saida, largura, altura, img)

def contar_linhas_texto(imagem):
    largura, altura, intensidade = ler_arquivo_pgm(imagem) 
    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    contador = 0
    linha_anterior_texto = False

    for i in range(1, altura - 1):
        linha = imagem_matriz[i]
        for j in range(1, largura - 1):
            pixel = linha[j]
            if pixel == 1:   # Verifica se há pelo menos um pixel de texto na linha
                if not linha_anterior_texto:  # Se a linha anterior não tinha texto e a linha atual tem, incrementa o contador
                    contador += 1
                linha_anterior_texto = True
                break  # Avança para a próxima linha
        else:
            linha_anterior_texto = False

    return contador

listaa = [0, 0, 0, 1, 1, 1, 0, 0, 0]
lista2 = [1,1,1,1,1,1]
elemento_estruturante = lista_para_matriz(2, 3, lista2)
imagem_terminada("ImagensTeste/lorem_s12_c03_noise.pbm", "ImagensTeste/escrever.pbm", elemento_estruturante)

total_linhas = contar_linhas_texto("ImagensTeste/escrever.pbm")
print(total_linhas)

# Aplicar abertura
# img = fechamento(l,a,it,elemento_estruturante)
# salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, it)
# l,a, it = ler_arquivo_pgm("ImagensTeste/lorem_s12_c02_noise.pbm")
# l, a, it = ler_arquivo_pgm("ImagensTeste/lorem_s12_c02_noise.pbm")
# Aplicar a dilatação
# imagem_nova = dilatacao(l, a, it,elemento_estruturante)

# imagem_dilatacao = dilatacao(l, a, it,elemento_estruturante)

# Aplicar a erosão
# imagem_erosao = erosao(l, a, it, elemento_estruturante)


# for i in range(10):
#     print(f"{i+1}. iteração")
#     l, a, it = ler_arquivo_pgm("ImagensTeste/escrever.pbm")
#     img = abertura(l, a, it, elemento_estruturante)
#     salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, img)

# Aplicar filtro da mediana
# imagem_filtrada = filtro_mediana("ImagensTeste/lorem_s12_c02_noise.pbm")

# Salvar a nova imagem
# salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, negativa)

# salvar_arquivo_pgm("ImagensTeste/imagem_filtrada.pbm", l, a, imagem_filtrada)


# l, a, it = ler_arquivo_pgm("ImagensTeste/imagem_filtrada.pbm")

# imagem_dilatacao = dilatacao(l, a, it,elemento_estruturante)
# imagem_erosao = erosao(l, a, it, elemento_estruturante)

# salvar_arquivo_pgm("ImagensTeste/imagem_dilatada.pbm", l, a, imagem_dilatacao)
# salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, imagem_erosao)

# print(intensidade)
# print(l)
# print(a)
# lorem_s12_c02_just.pbm, lorem_s12_c02_espacos_noise.pbm

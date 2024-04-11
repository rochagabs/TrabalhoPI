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


#Você dá os dados e ele salva no arquivo
def salvar_arquivo_pgm(nome_arquivo, largura, altura, dados_imagem):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('P1\n')
        arquivo.write(f"{largura} {altura}\n")
        
        # Escreve os dados da imagem
        for i in range(0, len(dados_imagem), largura):
            linha = " ".join(map(str, dados_imagem[i:i+largura]))
            arquivo.write(f"{linha}\n")
    print("Salva com sucesso")


# Nova função pra criar matriz
def lista_para_matriz(linhas,colunas,lista):
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
def pega_vizinhos(matriz,i,j):
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
def filtro_mediana(imagem):
    largura, altura, intensidade = ler_arquivo_pgm(imagem)
    imagem_matriz = lista_para_matriz(altura,largura,intensidade)
    imagem_matriz_filtrada = lista_para_matriz(altura,largura,intensidade)

    for i in range(1,altura-1):
        for j in range(1,largura-1):
            #print(f"{imagem_matriz[i][j]}: {i} {j}")
            mascara = pega_vizinhos(imagem_matriz,i,j)
            mascara.sort()
            imagem_matriz_filtrada[i][j] = mascara[4]

    imagem_matriz_filtrada = cria_lista(imagem_matriz_filtrada)
    return imagem_matriz_filtrada


def dilatacao(imagem, elemento_estruturante):
    largura, altura, intensidade = ler_arquivo_pgm(imagem)
    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    imagem_matriz_filtrada = lista_para_matriz(altura, largura, intensidade)
    qtde_linhas_elemento = len(elemento_estruturante)
    qtde_colunas_elemento = len(elemento_estruturante[0])

    # Loop pelos pixels da imagem, exceto a borda
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Se o pixel na imagem original estiver branco (valor 1)
            if imagem_matriz[i][j] == 1:
                # Aplica a dilatação usando o elemento estruturante
                for k in range(qtde_linhas_elemento):
                    for l in range(qtde_colunas_elemento):
                        # Atualiza os pixels na imagem filtrada com base no elemento estruturante
                        if elemento_estruturante[k][l] == 1:
                            # Define o pixel correspondente na imagem filtrada como branco (valor 1)
                            imagem_matriz_filtrada[i - 1 + k][j - 1 + l] = 1

    imagem_matriz_filtrada = cria_lista(imagem_matriz_filtrada)
    return imagem_matriz_filtrada

def erosao(imagem, elemento_estruturante):
    largura, altura, intensidade = ler_arquivo_pgm(imagem)
    imagem_matriz = lista_para_matriz(altura, largura, intensidade)
    imagem_matriz_filtrada = lista_para_matriz(altura, largura, intensidade)
    qtde_linhas_elemento = len(elemento_estruturante)
    qtde_colunas_elemento = len(elemento_estruturante[0])

    #Loop pelos pixels da imagem, exceto a borda
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            #Se o pixel na imagem original estiver braco (valor 1)
            if imagem_matriz[i][j] == 1:
                #Aplica erosão usando o elemento estruturante
                for k in range(qtde_linhas_elemento):
                    for l in range(qtde_colunas_elemento):
                        #Verifica se o pixel do elemento estruturante corresponde a um pixel branco na imagem
                        if elemento_estruturante[k][l] == 1 and imagem_matriz[i - 1 + k][j - 1 +l] != 1:
                            #Se algum dos pixels do elemento estruturante não corresponder a um pixel branco na imagem,
                            #o pixel na imagem filtrada é definido como preto (valor 0)
                            imagem_matriz_filtrada[i][j] = 0
                            break
                        else:
                            continue
                        break

    imagem_matriz_filtrada = cria_lista(imagem_matriz_filtrada)
    return imagem_matriz_filtrada


def abertura(largura, altura, intensidade, elem):
    e = erosao(largura,altura,intensidade,elem)
    r = dilatacao(largura,altura,e,elem)
    return r


def fechamento(largura, altura, intensidade, elem):
    d = dilatacao(largura,altura,intensidade,elem)
    r = erosao(largura,altura,d,elem)
    return r

def aplicar_negativo (nome_arquivo_entrada, nome_arquivo_saida):
    largura, altura, dados_intensidade = ler_arquivo_pgm(nome_arquivo_entrada)
    imagem_matriz = lista_para_matriz(altura,largura,dados_intensidade)
    imagem_negativa = lista_para_matriz(altura,largura,dados_intensidade)

    for i in range(1,altura-1):
        for j in range(1,largura-1):
            imagem_negativa[i][j] = 1-imagem_matriz[i][j]
    salvar_arquivo_pgm(nome_arquivo_saida, largura, altura, cria_lista(imagem_negativa))



#l,a,intensidade = ler_arquivo_pgm("ImagensTeste/lorem_s12_c02_noise.pbm")
l, a, it = ler_arquivo_pgm("ImagensTeste/lorem_s12_c02_noise.pbm")


listaa = [0, 0, 0, 0, 1, 1, 0, 0, 0]
elemento_estruturante = lista_para_matriz(3, 3, listaa)
#print(elemento_estruturante)

# Aplicar a dilatação
#imagem_nova = dilatacao(l, a, it,elemento_estruturante)
aplicar_negativo("ImagensTeste/lorem_s12_c02_noise.pbm",  "ImagensTeste/neg.pbm")
# for i in range(10):
#     l, a, it = ler_arquivo_pgm("ImagensTeste/escrever.pbm")
#     img = dilatacao(l, a, it, elemento_estruturante)
#     salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, img)

# Aplicar filtro da mediana
imagem_filtrada = filtro_mediana("ImagensTeste/lorem_s12_c02_noise.pbm")
salvar_arquivo_pgm("ImagensTeste/imagem_filtrada.pbm", l, a, imagem_filtrada)
# Salvar a nova imagem
#salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, negativa)

l, a, it = ler_arquivo_pgm("ImagensTeste/imagem_filtrada.pbm")

imagem_dilatacao = dilatacao("ImagensTeste/imagem_filtrada.pbm",elemento_estruturante)
imagem_erosao = erosao("ImagensTeste/imagem_filtrada.pbm", elemento_estruturante)

salvar_arquivo_pgm("ImagensTeste/imagem_dilatada.pbm", l, a, imagem_dilatacao)
salvar_arquivo_pgm("ImagensTeste/imagem_erudita.pbm", l, a, imagem_erosao)

#print(intensidade)
#print(l)
#print(a)
# lorem_s12_c02_just.pbm, lorem_s12_c02_espacos_noise.pbm

#print(f"Largura: {l}")
#print(f"Altura: {a}")
#print(f"Valor Máximo de Intensidade: {valor_maximo}")
#print(f"Dados de Intensidade: {intensidade}")
#print(type(intensidade))







# Exemplo de uso
#nome_arquivo_entrada = 'Figuras/lago_escuro.pgm'

# Lê a imagem do arquivo de entrada
#largura, altura, valor_maximo, dados_imagem = ler_arquivo_pgm(nome_arquivo_entrada)

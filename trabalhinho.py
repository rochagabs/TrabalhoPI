

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


#vc da os dados e ele salvo no arquivo
def salvar_arquivo_pgm(nome_arquivo, largura, altura, dados_imagem):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('P1\n')
        arquivo.write(f"{largura} {altura}\n")
        
        # Escreve os dados da imagem
        for i in range(0, len(dados_imagem), largura):
            linha = " ".join(map(str, dados_imagem[i:i+largura]))
            arquivo.write(f"{linha}\n")
    print("Salva com sucesso")




# Função pra transformar uma lista em uma matriz
# Função pra transformar uma lista em uma matriz
# def cria_matriz(linhas, colunas, lista):
#     matriz = []
#     for i in range(linhas):
#         lista_linhas = []
#         for j in range(colunas):
#             #print(i,j)
#             lista_linhas.append(lista[colunas * i + j])
#         matriz.append(lista_linhas)
#     return matriz


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


def cria_matriz(linhas, colunas, lista):
    matriz = []
    idx = 0
    for i in range(linhas):
        lista_linhas = []
        for j in range(colunas):
            #print(i,j)
            lista_linhas.append(lista[colunas * i + j])
            # Verifica se ainda há elementos na lista
            if idx < len(lista):
                #lista_linhas.append(lista[idx])
                idx += 1
            else:
                # Se a lista terminar antes da matriz, preenche com zero
                lista_linhas.append(0)
        matriz.append(lista_linhas)
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


def dilatacao(largura, altura, intensidade, elemento_estruturante):
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



#l,a,intensidade = ler_arquivo_pgm("ImagensTeste/lorem_s12_c02_noise.pbm")
l, a, it = ler_arquivo_pgm("ImagensTeste/lorem_s12_c02_noise.pbm")


listaa = [0, 0, 0, 0, 1, 1, 0, 0, 0]
elemento_estruturante = lista_para_matriz(3, 3, listaa)
print(elemento_estruturante)

# Aplicar a dilatação
imagem_nova = dilatacao(l, a, it,elemento_estruturante)

# for i in range(10):
#     l, a, it = ler_arquivo_pgm("ImagensTeste/escrever.pbm")
#     img = dilatacao(l, a, it, elemento_estruturante)
#     salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, img)

# Aplicar filtro da mediana
#imagem_nova = filtro_mediana("ImagensTeste/lorem_s12_c02_noise.pbm")

# Salvar a nova imagem
salvar_arquivo_pgm("ImagensTeste/escrever.pbm", l, a, imagem_nova)




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

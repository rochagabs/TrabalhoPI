def ler_arquivo_ppm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        # Lê a primeira linha para obter o tipo de arquivo (deve ser "P2" para PPM ASCII)
        tipo_arquivo = arquivo.readline().strip()
        if tipo_arquivo != "P2":
            raise ValueError("O arquivo não é do tipo P2 (PPM ASCII)")

        # Lê as dimensões da imagem (largura e altura)
        largura, altura = map(int, arquivo.readline().split())

        # Lê o valor máximo de intensidade (geralmente 255)
        valor_maximo = int(arquivo.readline().strip())

        # Lê os dados de intensidade pixel por pixel
        dados_intensidade = []
        for linha in arquivo:
            # Ignora linhas em branco ou comentários
            if linha.strip() and not linha.startswith('#'):
                dados_intensidade.extend(map(int, linha.split()))

    return largura, altura, valor_maximo, dados_intensidade


#print(f"Largura: {largura}")
#print(f"Altura: {altura}")
#print(f"Valor Máximo de Intensidade: {valor_maximo}")
#print(f"Dados de Intensidade: {dados_intensidade}")

def salvar_arquivo_ppm(nome_arquivo, largura, altura, valor_maximo, dados_imagem):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('P2\n')
        arquivo.write(f"{largura} {altura}\n")
        arquivo.write(f"{valor_maximo}\n")
        
        # Escreve os dados da imagem
        for i in range(0, len(dados_imagem), largura):
            linha = " ".join(map(str, dados_imagem[i:i+largura]))
            arquivo.write(f"{linha}\n")


def aplicar_negativo (nome_arquivo_entrada, nome_arquivo_saida):
     with open(nome_arquivo_entrada, 'r') as arquivo:
        # Lê a primeira linha para obter o tipo de arquivo (deve ser "P2" para PPM ASCII)
        tipo_arquivo = arquivo.readline().strip()
        if tipo_arquivo != "P2":
            raise ValueError("O arquivo não é do tipo P2 (PPM ASCII)")

        # Lê as dimensões da imagem (largura e altura)
        largura, altura = map(int, arquivo.readline().split())

        # Lê o valor máximo de intensidade (geralmente 255)
        valor_maximo = int(arquivo.readline().strip())

        # Lê os dados de intensidade pixel por pixel
        dados_intensidade = []
        for linha in arquivo:
            # Ignora linhas em branco ou comentários
            if linha.strip() and not linha.startswith('#'):
                dados_intensidade.extend(map(int, linha.split()))
     negativo = [255-i for i in dados_intensidade]
     salvar_arquivo_ppm(nome_arquivo_saida, largura, altura, valor_maximo, negativo)


def calcular_histograma(nome_arquivo_entrada):
     largura, altura, valor_maximo, dados_imagem = ler_arquivo_ppm(nome_arquivo_entrada)
     histograma = [0] * (valor_maximo+1) #256 valores
     for pixel in dados_imagem:
        valor_pixel = pixel
        histograma[valor_pixel]+=1
     #for valor_pixel, qtde in enumerate(histograma):
       # print("Pixel:", valor_pixel, "         Qtde:", qtde)
     return histograma


def limiarizacao (nome_arquivo_entrada, nome_arquivo_saida, limiar):
    largura, altura, valor_maximo, dados_imagem = ler_arquivo_ppm(nome_arquivo_entrada)
    dados_limiar = []
    for pixel in dados_imagem:
        if (pixel>=limiar):
            dados_limiar.append(valor_maximo)
        else:
            dados_limiar.append(0)
    salvar_arquivo_ppm(nome_arquivo_saida, largura, altura, valor_maximo, dados_limiar)

def equalizar_hist (histograma, nome_arquivo_entrada, nome_arquivo_saida):
    largura, altura, valor_maximo, dados_imagem = ler_arquivo_ppm(nome_arquivo_entrada)
    probabilidades = [0]*(valor_maximo+1)
    
    for valor_pixel, qtde in enumerate(histograma):
        probabilidades[valor_pixel] = round(qtde/(largura*altura), 3)

    prob_acumulada = [0] * (valor_maximo+1)
    contador = 0

    for valor_pixel, prob in enumerate(probabilidades):
        contador+=prob
        prob_acumulada[valor_pixel]=round(contador,3)

    listanormalizada = [0]*(valor_maximo+1)

    for valor_pixel, prob in enumerate(prob_acumulada):
        listanormalizada[valor_pixel] = round(prob*valor_maximo)

    hist_equalizado = [0]*(valor_maximo+1)
    for valor_pixel, qtde in enumerate(histograma):
        novo_valor_pixel = listanormalizada[valor_pixel]
        hist_equalizado[novo_valor_pixel] += qtde

    pixels_equalizados = [listanormalizada[pixel] for pixel in dados_imagem] 
    salvar_arquivo_ppm(nome_arquivo_saida, largura, altura, valor_maximo, pixels_equalizados)#salva a imagem equalizada
    return hist_equalizado #retorna o histograma equalizado

# Exemplo de uso
nome_arquivo_entrada = 'Figuras/lago_escuro.pgm'
nome_arquivo_saida_negativo = 'Figuras/lago_escuro_negativo.pgm'
nome_arquivo_saida_limiar = 'Figuras/lago_escuro_limiar.pgm'
nome_arquivo_saida_equal = 'Figuras/lago_escuro_equal.pgm'
histograma = calcular_histograma(nome_arquivo_entrada)
equalizar_hist(histograma, nome_arquivo_entrada, nome_arquivo_saida_equal)

#Escolher Limiar
#limiarizacao(nome_arquivo_entrada, nome_arquivo_saida_limiar, 20)
#Aplicar Negativo
#aplicar_negativo(nome_arquivo_entrada, nome_arquivo_saida_negativo)
# Lê a imagem do arquivo de entrada
#largura, altura, valor_maximo, dados_imagem = ler_arquivo_ppm(nome_arquivo_entrada)

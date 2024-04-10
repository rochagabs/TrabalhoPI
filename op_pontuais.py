def ler_arquivo_ppm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        tipo_arquivo = arquivo.readline().strip()
        if tipo_arquivo != "P1":
            raise ValueError("O arquivo não é do tipo PGM P1")

        # Lê as dimensões da imagem (largura e altura)
        largura, altura = map(int, arquivo.readline().split())

        # Lê os dados de intensidade pixel por pixel
        dados_intensidade = []
        for linha in arquivo:
            # Ignora linhas em branco ou comentários
            if linha.strip() and not linha.startswith('#'):
                dados_intensidade.extend(map(int, linha.split()))

    return largura, altura, dados_intensidade


#print(f"Largura: {largura}")
#print(f"Altura: {altura}")
#print(f"Valor Máximo de Intensidade: {valor_maximo}")
#print(f"Dados de Intensidade: {dados_intensidade}")

def salvar_arquivo_ppm(nome_arquivo, largura, altura, dados_imagem):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write('P1\n')
        arquivo.write(f"{largura} {altura}\n")
        
        # Escreve os dados da imagem
        for i in range(0, len(dados_imagem), largura):
            linha = " ".join(map(str, dados_imagem[i:i+largura]))
            arquivo.write(f"{linha}\n")




# Exemplo de uso
#nome_arquivo_entrada = 'Figuras/lago_escuro.pgm'

# Lê a imagem do arquivo de entrada
#largura, altura, valor_maximo, dados_imagem = ler_arquivo_ppm(nome_arquivo_entrada)

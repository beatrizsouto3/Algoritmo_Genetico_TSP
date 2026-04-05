import math

# Esse arquivo é onde leremos os nossos arquivos tsp
# Eles possuem provas testes de caminhos para o problema do cacheiro viajante

# Essa função carrega o arquivo que for passado por parâmetro
def carregar_instancia(caminho_arquivo):
    # Vamos abrir o arquivo e ler as linhas desse arquivo
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()

    informacao_arquivo = {}
    dados_iniciam_em = 0

    # Vamos armazenar os valores dessas linhas destrinchadas em um dicionário
    # Acessamos linha por linha para pegar os dados do arquivo
    # O enumerate faz contagem das linhas, eu separo essas linhas em chave e valor
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        if ':' in linha:
            chave, valor = linha.split(':', 1)
            informacao_arquivo[chave.strip()] = valor.strip()
        if 'NODE_COORD_SECTION' in linha or 'EDGE_WEIGHT_SECTION' in linha:
            dados_iniciam_em = i + 1
            break
    
    # Após guardar os dados do arquivo em um dicionário, 
    # vamos acessar suas chaves e pegar valores isoladamente
    num_cidades = int(informacao_arquivo.get('DIMENSION', 0))
    caminho_peso = informacao_arquivo.get('EDGE_WEIGHT_TYPE', '')
    formato_peso = informacao_arquivo.get('EDGE_WEIGHT_FORMAT', '')


    print(f"Carregando {informacao_arquivo['NAME']} - Formato: {formato_peso}")
    # Aqui faremos a verificação, como a matriz já vem pré-calculada, 
    # não precisamos aplicar fórmulas para acessar suas distâncias
    if caminho_peso == 'EUC_2D':    
        return _processar_euclidiana(linhas[dados_iniciam_em:], num_cidades)
    
    return _mapear_matriz(linhas[dados_iniciam_em:], num_cidades, formato_peso)

# Essa função vai mapear em uma matriz entendível pelo python, as matrizes dos arquivos tsp
def _mapear_matriz(linhas, num_cidades, formato):
    
    valores_matriz = []
    for linha in linhas:
        if 'EOF' in linha or 'DISPLAY_DATA_SECTION' in linha: break
        # Pega o bruto da matriz e transforma em uma lista de inteiros
        # Adicionei uma segurança para blindar contra qualquer caracter que possa estar 
        # presente no arquivo
        pedacos = linha.split()
        for x in pedacos:
            x = x.strip()
            if x.isdigit() or (x.startswith('-') and x[1:].isdigit()):
                valores_matriz.append(int(x))

    matriz = [[0] * num_cidades for _ in range(num_cidades)]
    index = 0

    # Preenche a matriz de acordo com cada formato específico
    # O formato LOWER_DIAG_ROW preenche a parte inferior da matriz, 
    # incluindo a diagonal, e depois espelha os valores para a parte superior.
    if formato == 'LOWER_DIAG_ROW':
        for i in range(num_cidades):
            for j in range(i + 1):
                matriz[i][j] = valores_matriz[index]
                matriz[j][i] = valores_matriz[index]
                index += 1
    # O formato UPPER_ROW preenche a parte superior da matriz, 
    # sem incluir a diagonal, e depois espelha os valores para a parte inferior.
    elif formato == 'UPPER_ROW':
        for i in range(num_cidades):
            for j in range(i + 1, num_cidades):
                matriz[i][j] = valores_matriz[index]
                matriz[j][i] = valores_matriz[index]
                index += 1
    # O formato FULL_MATRIX preenche a matriz completa, linha por linha, 
    # sem necessidade de espelhamento.
    elif formato == 'FULL_MATRIX':
        for i in range(num_cidades):
            for j in range(num_cidades):
                matriz[i][j] = valores_matriz[index]
                index += 1

    return matriz


def _processar_euclidiana(linhas, num_cidades):
    coordenadas = []
    for i in range(num_cidades):
        partes = linhas[i].split()
        x = float(partes[1])
        y = float(partes[2])
        # Pega as coordenadas do arquivo e armazena em uma lista de tuplas
        coordenadas.append((x, y))
    
    # Inicializa a matriz com zeros
    matriz_distancias = [[0] * num_cidades for _ in range(num_cidades)]
    
    for i in range(num_cidades):
        for j in range(i + 1, num_cidades):
            if i != j:
                # Formula da distância euclidiana: 
                dx = coordenadas[i][0] - coordenadas[j][0]
                dy = coordenadas[i][1] - coordenadas[j][1]
                dist = math.sqrt(dx**2 + dy**2)
                # A soma pelo 0.5 arredonda para o inteiro mais próximo 
                matriz_distancias[i][j] = int(dist + 0.5)
                matriz_distancias[j][i] = int(dist + 0.5)
    
    return matriz_distancias
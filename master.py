import random
import csv
import datetime #pra pegar a data e hora atual e colocar no nome do arquivo csv
import os #gerenciamento dos arquivos e criar pasta (lógica do histórico csv)
from loader import carregar_instancia
from modelotsp import ModeloTsp
from algoritmoGenetico import AlgoritmoGenetico

#função retornando apenas a população
def definir_tamanho_populacao(num_cidades: int) -> int:
    if num_cidades <= 60:
        return 100
    if num_cidades <= 110:
        return 120
    return 160

if __name__ == "__main__":
    
    #todas as intâncias para execução final
    arquivos_teste = {
        'instances/gr17.tsp': 2085,
        'instances/gr21.tsp': 2707,
        'instances/gr24.tsp': 1272,
        'instances/fri26.tsp': 937,
        'instances/dantzig42.tsp': 699,
        'instances/swiss42.tsp': 1273,
        'instances/gr48.tsp': 5046,
        'instances/hk48.tsp': 11461,
        'instances/eil51.tsp': 426,
        'instances/berlin52.tsp': 7542,
        'instances/brazil58.tsp': 25395,
        'instances/st70.tsp': 675,
        'instances/eil76.tsp': 538,
        'instances/pr76.tsp': 108159,
        'instances/rat99.tsp': 1211,
        'instances/kroA100.tsp': 21282,
        'instances/rd100.tsp': 7910,
        'instances/eil101.tsp': 629,
        'instances/lin105.tsp': 14379,
        'instances/pr107.tsp': 44303,
        'instances/gr120.tsp': 6942,
        'instances/pr124.tsp': 59030,
        'instances/bier127.tsp': 118282,
        'instances/ch130.tsp': 6110,
        'instances/pr136.tsp': 96772,
        'instances/pr144.tsp': 58537,
        'instances/ch150.tsp': 6528,
        'instances/kroA150.tsp': 26524,
        'instances/kroB150.tsp': 26130,
        'instances/pr152.tsp': 73682
    }

    #grade de parâmetros solicitada para o experimento
    taxas_cruzamento = [0.95]
    taxas_mutacao = [0.3]
    NUM_EXECUCOES = 30

    #critérios de parada fixos
    MAX_GERACOES = 1000
    LIMITE_ESTAGNACAO = 150

    #aqui ele cria uma pasta para organizar os históricos .csv
    pasta_historico = 'historico_resultados'
    if not os.path.exists(pasta_historico):
        os.makedirs(pasta_historico)

    agora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") #pega o momento exato que o codigo rodou
    #monta o nome do arquivo e o caminho da pasta que ele vai ficar
    nome_arquivo = f'experimentos_{agora}.csv'
    caminho_arquivo_csv = os.path.join(pasta_historico, nome_arquivo)

    print(f"Resultado sera salvo no histórico em: {caminho_arquivo_csv}")


    # Como precisar plotar alguns os resultados obtidos, estarei salvando os resultado em um csv
    # Após receber os resultados no arquivo, vou ler e plotar gráficos com os resultados dos experimentos
    with open(caminho_arquivo_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        campo_nomes = ['instancia', 'cruzamento', 'mutacao', 'execucao', 'fitness', 'limite_otimo', 'erro_relativo_percentual']
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campo_nomes, delimiter=';')
        escritor_csv.writeheader()

        for arquivo, distancia_otima in arquivos_teste.items():
            print(f"\n--- Rodando: {arquivo} ---")
            
            try:
                matriz = carregar_instancia(arquivo)
            except Exception as e:
                print(f"Erro ao ler arquivo: {e}")
                continue
                
            modelo = ModeloTsp(matriz)

            tam_populacao = definir_tamanho_populacao(modelo.quantidade_cidades())
            
            # criei uma lista para varias os parâmetros de cruzamento e mutação
            # para testar o impacto desses parâmetros no resultado final
            for taxa_cru in taxas_cruzamento:
                for taxa_mut in taxas_mutacao:
                    print(f"Taxa de Cruzamento: {taxa_cru}, Taxa de Mutação: {taxa_mut}")
                    #parâmetros padrão do algoritmo genético
                    erro_30_execucoes = []

                    for execucao in range(1, NUM_EXECUCOES + 1):
                        #cumprindo requisitos de sementes aleatórias controladas
                        random.seed(execucao)

                        ag = AlgoritmoGenetico(
                            modelo=modelo, 
                            tam_populacao=tam_populacao,
                            taxa_sub=0.8,
                            taxa_cru=taxa_cru,           
                            taxa_mut=taxa_mut,          
                            max_geracoes=MAX_GERACOES,
                            limite_estagnacao=LIMITE_ESTAGNACAO
                        )
                
                        melhor_rota = ag.run()
                        #apliquei a formula de erro relativo percentual recomendada pelo artigo tsp95
                        erro = ((melhor_rota.fitness - distancia_otima) / distancia_otima) * 100
                        erro_30_execucoes.append(erro)

                        escritor_csv.writerow({
                            'instancia': arquivo,
                            'cruzamento': taxa_cru,
                            'mutacao': taxa_mut,
                            'execucao': execucao,
                            'fitness': melhor_rota.fitness,
                            'limite_otimo': distancia_otima,
                            'erro_relativo_percentual': round(erro, 4)
                        })

                    erro_medio = sum(erro_30_execucoes) / len(erro_30_execucoes)
                    print(f"\n\nErro médio em {NUM_EXECUCOES} execuções: {erro_medio:.2f}%")

    print(f"\n--- Experimento salvo no csv ---\n")
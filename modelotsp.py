import random
from solucao import Solucao

class ModeloTsp:
    def __init__(self, matriz_distancias: list[list[int]]):
        self.matriz_distancias = matriz_distancias
        self.num_cidades = len(matriz_distancias)

    def quantidade_cidades(self) -> int:
        return self.num_cidades
    
    def fitness(self, solucao: Solucao) -> int:
        distancia_total = 0
        # Aqui na fitness, calculamos a distância da cidade atual para a próxima cidade
        # O objetivo do uso dessa função aqui nesse problema é minimizar a distância total percorrida
        # O fitness basicamente seria a distância total do caminho
        for i in range(self.num_cidades - 1):
            cidade_atual = solucao.caminho[i]
            cidade_proxima = solucao.caminho[i + 1]
            distancia_total += self.matriz_distancias[cidade_atual][cidade_proxima]

        cidade_final = solucao.caminho[-1]
        cidade_origem = solucao.caminho[0]
        distancia_total += self.matriz_distancias[cidade_final][cidade_origem]

        return distancia_total
    
    # Aplicando Crossover no cruzamento pois no problema do caixeiro viajante não podemos repetir a passagem em uma cidade
    def cruzamento(self, p1:Solucao, p2:Solucao) -> tuple[Solucao, Solucao]:
        qtd_cidades:int = self.quantidade_cidades()
        filho1 = Solucao(qtd_cidades)
        filho2 = Solucao(qtd_cidades)
        
        # Sorteia 2 pontos de corte diferente
        corte1, corte2 = sorted(random.sample(range(qtd_cidades), 2))

        # Função de que aplica a lógica do crossover para gerar um filho
        def gerar_filho(pai_base, pai_ordem, filho):
            # Preenchemos o filho com valores -1 para reconhecer os não preenchidos
            filho.caminho = [-1] * qtd_cidades
            
            # Copiamos a parte entre os cortes do pai_base para o filho
            # Vai desde a posição corte1 até a posição corte2, incluindo ambas e esse intervalo
            filho.caminho[corte1:corte2] = pai_base.caminho[corte1:corte2]

            # Aqui eu pego o subconjunto de cidades que já estão no filho (entre os cortes) e crio um dicionário para separar as cidades herdadas do pai
            cidades_no_filho = set(filho.caminho[corte1:corte2])
            # Separo as posições vazias (-1) do filho com as cidades do pai 2, verificando quais não estão presentes no filho
            cidades_faltando = [cidade for cidade in pai_ordem.caminho if cidade not in cidades_no_filho]

            # Por fim preencho as posições vazias do filho com as cidades faltantes
            idx_faltando = 0
            for i in range(qtd_cidades):
                if filho.caminho[i] == -1:
                    filho.caminho[i] = cidades_faltando[idx_faltando]
                    idx_faltando += 1

            return filho

        filho1 = gerar_filho(p1, p2, filho1)
        filho2 = gerar_filho(p2, p1, filho2)

        return filho1, filho2
    
    def mutacao(self, taxa:float, solucao: Solucao) -> None:
        # Mutação por indivíduo: cada solução tem uma única chance de sofrer um swap.
        # faz a verificação se a quantidade de cidades é menor que 2, pois nesse caso não tem como fazer o swap

        if random.random() < taxa:
            i, j = random.sample(range(self.quantidade_cidades()), 2)
            solucao.caminho[i], solucao.caminho[j] = solucao.caminho[j], solucao.caminho[i]

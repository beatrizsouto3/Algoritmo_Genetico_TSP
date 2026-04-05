import random
from modelotsp import ModeloTsp
from solucao import Solucao

class AlgoritmoGenetico:
    def __init__(self, modelo:ModeloTsp, tam_populacao:int, taxa_sub:float,
                taxa_cru:float, taxa_mut:float, max_geracoes:int, limite_estagnacao:int
                ):
        self.populacao:list[Solucao] = []
        self.modelo = modelo
        self.taxa_sub = taxa_sub
        self.taxa_cru = taxa_cru
        self.taxa_mut = taxa_mut
        self.tam_populacao = tam_populacao
        self.max_geracoes = max_geracoes
        self.limite_estagnacao = limite_estagnacao

    # Na preparação da população, eu gero soluções aleatórias e calculo o fitness de cada uma delas, armazenando na população inicial
    def preparaPopulacao(self, tam_populacao:int) -> list[Solucao]:
        n = self.modelo.quantidade_cidades()
        for _ in range(tam_populacao):
            solucao = Solucao(n)
            solucao.randomize()
            solucao.fitness = self.modelo.fitness(solucao)
            self.populacao.append(solucao)
        return self.populacao
    
    # Usa o método de seleção por torneio, onde selecionamos 3 soluções aleatórias da população e escolhemos a melhor entre elas.
    def selecao(self) -> list[Solucao]:
        torneio = random.sample(self.populacao, 3)
        melhor = min(torneio, key= lambda s: s.fitness)
        return [melhor]
    
    # O objetivo o substituir os piores fitness da população pelos melhores da nova população
    def substituicao(self, nova_populacao:list[Solucao]) -> None:
        # Mantém uma parte da população atual (elitismo) e substitui o restante com os melhores filhos.
        qtd_substituir = int(self.tam_populacao * self.taxa_sub)
        qtd_substituir = max(1, min(self.tam_populacao, qtd_substituir))
        qtd_manter = self.tam_populacao - qtd_substituir

        atual_ordenada = sorted(self.populacao, key=lambda s: s.fitness)
        nova_ordenada = sorted(nova_populacao, key=lambda s: s.fitness)

        #self.populacao = atual_ordenada[:qtd_manter] + nova_ordenada[:qtd_substituir]

        populacao_combinada = atual_ordenada[:qtd_manter] + nova_ordenada[:qtd_substituir]

        self.populacao = sorted(populacao_combinada, key=lambda s: s.fitness)

    def cruzamento(self, p1:Solucao, p2:Solucao) -> tuple[Solucao, Solucao]:
        return self.modelo.cruzamento(p1, p2)
    
    #def mutacao(self, solucao:Solucao) -> None:
        #self.modelo.mutacao(solucao)
        
    #ajustei aqui por conta de um erro
    def mutacao(self, solucao:Solucao) -> None:
        self.modelo.mutacao(self.taxa_mut, solucao)

    def run(self) -> Solucao:
        # gera as rotas aleatórias da primeira
        self.preparaPopulacao(self.tam_populacao)

        #guarda o melhor global pra testar a estagnação
        melhor_global = min(self.populacao, key=lambda s: s.fitness)
        geracoes_sem_melhora = 0

        #loop principal das gerações
        for geracao in range(self.max_geracoes):
            nova_populacao = []

            #vai criando filho ate encher a capacidade da população
            while len(nova_populacao) < self.tam_populacao:
                
                #pega dois pais por torneio
                pai1 = self.selecao()[0]
                pai2 = self.selecao()[0]

                #tenta cruzar baseado na taxa
                if random.random() < self.taxa_cru:
                    filho1, filho2 = self.cruzamento(pai1, pai2)
                else:
                    #caso não cruze, os filhos são clones exatos dos pais
                    filho1 = pai1.clonar()
                    filho2 = pai2.clonar()

                #tenta mutar o filhos (taxa ja esta controlada dentro do modelo)
                self.mutacao(filho1)
                self.mutacao(filho2)

                #calcula a distância da rota desses novos filhos
                filho1.fitness = self.modelo.fitness(filho1)
                filho2.fitness = self.modelo.fitness(filho2)

                nova_populacao.extend([filho1, filho2])

            #junção da população antiga com a nova e corta os piores (principio do Elitismo)
            self.substituicao(nova_populacao)

            #melhor_atual = min(self.populacao, key=lambda s: s.fitness)
            
            #o melhor individuo esta obrigatoriamente na primeira posição
            melhor_atual = self.populacao[0]
            
            #caso ache uma rota mais curta, atualiza o recorde
            if melhor_atual.fitness < melhor_global.fitness:
                melhor_global = melhor_atual.clonar()
                geracoes_sem_melhora = 0
            else:
                geracoes_sem_melhora += 1

            #se ficar x gerações sem achar uma rota menor, para o loop
            if geracoes_sem_melhora >= self.limite_estagnacao:
                print(f"-> Parou na geração {geracao} por estagnação.")
                break

        return melhor_global

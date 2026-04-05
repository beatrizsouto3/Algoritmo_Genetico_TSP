import random

class Solucao:
    def __init__(self, num_cidades:int):
        self.fitness: float = float('inf')
        self.caminho: list[int] = list(range(num_cidades))

    def randomize(self):
        random.shuffle(self.caminho)
    
    def clonar(self):
        #substituimos o copy.deepcopy() por essa clonagem manual
        nova_solucao = Solucao(len(self.caminho))
        nova_solucao.caminho = self.caminho[:] #copia a lista instantaniamente
        nova_solucao.fitness = self.fitness 

        return nova_solucao
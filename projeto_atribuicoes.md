[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/MwqD5syC)
# [TADS][IC] Projeto TSP + AG

Projeto da disciplina de Inteligência Computacional do curso de Análise e Desenvolvimento de Sistemas da UFRN aplicando algoritmos genéticos para o problema do caixeiro viajante (TSP).

## Descrição

Deve-se desenvolver e analisar algoritmos genéticos para o problema do caixeiro viajante utilizando benchmarks. Como objetivos específicos, deve-se:
- Carregar as instâncias dos problemas indicadas na seção dados;
- Implementar um algoritmo genético que funcione em todos os problemas;
- Determinar quais parâmetros e operadores são mais adequados para os problemas;
- Determinar o comportamento médio do algoritmo em termos de qualidade da solução e variabilidade entre execuções.

Espera-se que, ao final do trabalho, os alunos sejam capazes de modelar algoritmos genéticos e analisar de modo empírico o comportamento e a escolha dos parâmetros.

## Dados

Deve-se utilizar as instâncias abaixo, isto é, o algoritmo desenvolvido deve ser executado para todas as instâncias, encontrando a melhor solução possível para cada uma. A tabela abaixo apresenta as instâncias, em que:

- Nome: nome do arquivo que deve ser carregado e processado;
- #Cidades: quantidade de cidades na instância;
- Tipo: tipo de representação da distância entre os nós, que pode ser no formato de matriz ou no formato de coordenadas para cada nó;
- Limite: melhor solução conhecida para a instância.

| Nome       |# Cidades| Tipo   | Limite  |
|------------|--------:|--------|-------:|
| gr17       | 17      | MATRIX | 2085   |
| gr21       | 21      | MATRIX | 2707   |
| gr24       | 24      | MATRIX | 1272   |
| fri26      | 26      | MATRIX | 937    |
| dantzig42  | 42      | MATRIX | 699    |
| swiss42    | 42      | MATRIX | 1273   |
| gr48       | 48      | MATRIX | 5046   |
| hk48       | 48      | MATRIX | 11461  |
| eil51      | 51      | EUC2D  | 426    |
| berlin52   | 52      | EUC2D  | 7542   |
| brazil58   | 58      | MATRIX | 25395  |
| st70       | 70      | EUC2D  | 675    |
| eil76      | 76      | EUC2D  | 538    |
| pr76       | 76      | EUC2D  | 108159 |
| rat99      | 99      | EUC2D  | 1211   |
| kroA100    | 100     | EUC2D  | 21282  |
| rd100      | 100     | EUC2D  | 7910   |
| eil101     | 101     | EUC2D  | 629    |
| lin105     | 105     | EUC2D  | 14379  |
| pr107      | 107     | EUC2D  | 44303  |
| gr120      | 120     | MATRIX | 6942   |
| pr124      | 124     | EUC2D  | 59030  |
| bier127    | 127     | EUC2D  | 118282 |
| ch130      | 130     | EUC2D  | 6110   |
| pr136      | 136     | EUC2D  | 96772  |
| pr144      | 144     | EUC2D  | 58537  |
| ch150      | 150     | EUC2D  | 6528   |
| kroA150    | 150     | EUC2D  | 26524  |
| kroB150    | 150     | EUC2D  | 26130  |
| pr152      | 152     | EUC2D  | 73682  |

## Função de Fitness

A função de fitness deve ser determinada conforme o artigo em anexo:

REINELT, Gerhard. TSPLIB 95. Heidelberg: Universität Heidelberg, Institut für Angewandte Mathematik, 1995. Technical Report.

É importante que a verificação da função seja efetuada, conforme a seção 2.7 do artigo, utilizando as soluções ótimas conhecidas das instâncias para validação.

## Metodologia

Sugere-se os seguintes passos:

1. Desenvolva um módulo para carregar as instâncias;
2. Desenvolva um módulo para representar as soluções e avaliar a função de fitness;
3. Verifique a função de fitness com as soluções canônicas das instâncias;
4. Desenvolva um algoritmo genético, escolhendo e justificando o tamanho da população, o critério de parada, os operadores de seleção, mutação, cruzamento e substituição;
5. Determine os valores dos parâmetros mais adequados para o algoritmo desenvolvido;
    5.1 Os parâmetros devem ser avaliados em um subconjunto de 5 instâncias, escolhidas e justificadas pelo aluno;
    5.2 Cada combinação de parâmetros deve ser avaliada 30 vezes;
6. Aplique o algoritmo genético em todas as instâncias, reportando o erro relativo percentual.
    6.1 O algoritmo deve ser executado 30 vezes para cada instância.


Para o item 1, o algoritmo deve funcionar para instâncias MATRIX e EUC2D.

Para o item 4, os operadores devem preservar a validade da permutação do TSP. Além disso, o algoritmo deve sempre retornar uma rota válida contendo todas as cidades exatamente uma vez.

Para o item 5, devem ser analisadas ao menos as taxas de mutação e cruzamento. Outros parâmetros podem ser analisados opcionalmente. Cada parâmetro deve ser avaliado com ao menos 3 valores diferentes e as interações entre os parâmetros devem ser consideradas. Por exemplo, se forem variadas as taxas de mutação e cruzamento, então 9 configurações devem ser avaliadas.

Para o item 5.1, o critério de parada deve ser mantido fixo durante o ajuste de parâmetros. As 5 instâncias escolhidas devem ter diferentes tamanhos de problema.

Para o item 6, considere o valor limite na tabela acima como o valor ótimo para determinar o erro relativo percentual, conforme a expressão abaixo, considerando o fitness como o custo da rota:

```math
 erro = \frac{fitness - limite}{limite} \cdot 100
```

As execuções devem utilizar sementes aleatórias controladas para permitir a reprodutibilidade dos experimentos.

A solução deve ser desenvolvida na linguagem Python, sem bibliotecas adicionais além das nativas da linguagem. Para o objetivo da geração de gráficos, é livre o uso de bibliotecas e outros softwares.

## Entrega

A entrega será realizada via github classroom, assim, é importante que sejam feitos commits regulares no repositório, com comentários descrevendo o que foi feito. Devem ser entregues os seguintes itens:

1. Implementação de ao menos três módulos: carregamento dos dados, modelagem do problema e algoritmo genético;
2. Arquivo em markdown descrevendo os seguintes itens:
    - O algoritmo genético, seus parâmetros, operadores e critério de parada, com justificativas para as escolhas;
    - Escolha dos parâmetros, explicando a metodologia e apresentando os resultados por meio de gráficos;
        - Gráfico de box-plot das 30 execuções em cada configuração dos parâmetros.
    - Resultados da execução de 30 vezes para cada instância:
        - Tabela de resultados das instâncias:
            - Colunas de valor mínimo, máximo e médio encontrados;
            - Colunas de valor mínimo, máximo e médio do erro relativo percentual;
            - Coluna para o desvio padrão do erro relativo percentual.
        - Gráfico de colunas do valor médio do erro relativo percentual em cada instância.

## Avaliação

A avaliação considerará os itens solicitados na seção de entrega, no entanto, a atribuição da nota é condicionada à comprovação da autoria por meio de perguntas durante a apresentação, em que poderão ser solicitadas explicações, justificativas e modificações no código apresentado.

Desse modo, haverá apresentação oral obrigatória no dia 6 de abril.

## Prazo

O trabalho deve ser finalizado até o final do dia 4 de abril. Após essa data, vocês não terão permissão de escrita no github.

Não serão aceitas submissões por outros meios.

O prazo não será prorrogado.
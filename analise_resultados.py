import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import datetime


#usamos o 'glob' pra listar todos os arquivos .csv dentro da pasta de histórico.
arquivos_csv = glob.glob('historico_resultados/*.csv')

#se a lista estiver vazia, o programa para e avisa pra evitar erros
if not arquivos_csv:
    print("Erro: Nenhum arquivo CSV encontrado na pasta 'historico_resultados'")
    exit()

#comando 'max' com 'getctime' ver qual o último arquivo criado
caminho_csv = max(arquivos_csv, key=os.path.getctime)
print(f"Lendo os dados do arquivo: {caminho_csv}")

#o pandas lê o arquivo .csv e tranforma em tabela 'df' (dataframe)
df = pd.read_csv(caminho_csv, sep=';')

#criação da pasta 'graficos' pra organizar as imagens (se a pasta não existir)
if not os.path.exists('graficos'):
    os.makedirs('graficos')

#aplicação de um tema visual padronizado biblioteca Seaborn
sns.set_theme(style="whitegrid")

#pega a data e hora pra colocar no nome as imagens
agora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#gráfico 1 - referente ao bloxplot
#o boxplot serve pra mostrar se o erro variou muito nas 30 execuções
plt.figure(figsize=(18, 10))

#plotagem do boxplot
ax = sns.boxplot(data=df, x='instancia', y='erro_relativo_percentual', hue='instancia', palette='Set2', legend=False, linewidth=1.5)

#títulos e ajuste nos textos
plt.title('Dispersão do Erro Relativo (30 Execuções por Instância)', fontsize=18, pad=30, fontweight='bold')
plt.ylabel('Erro Relativo (%)', fontsize=14)
plt.xlabel('Instâncias (Mapas)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10) #inclina o nome dos mapas
plt.tight_layout()      #ajusta as bordas pra não cortar na foto
plt.subplots_adjust(top=0.90, bottom=0.25) #da espaço extra no fundo pros nomes

nome_grafico1 = f'graficos/01_boxplot_error_{agora}.png'
plt.savefig(nome_grafico1, dpi=300)
print(f"Gráfico 1 salvo: {nome_grafico1}")


#gráfico 2 - esse gráfico mostra a média de erro pra cada mapa
plt.figure(figsize=(18, 10))

#calcula a média dos erros por mapa
media_erros = df.groupby('instancia')['erro_relativo_percentual'].mean().reset_index()

#plotagem das barras
ax = sns.barplot(data=media_erros, x='instancia', y='erro_relativo_percentual', hue='instancia', palette='viridis', legend=False)


plt.title('Média do Erro Relativo por Instância', fontsize=18, pad=30, fontweight='bold')
plt.ylabel('Média de Erro (%)', fontsize=14)
plt.xlabel('Instâncias (Mapas)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)

#aqui ele coloca o número da porcentagem em cima de cada barra
for index, row in media_erros.iterrows():
    if row.erro_relativo_percentual > 0.1:
        ax.text(index, row.erro_relativo_percentual + (media_erros['erro_relativo_percentual'].max() * 0.01), 
                f'{row.erro_relativo_percentual:.1f}%', 
                color='black', ha="center", va="bottom", fontsize=9, fontweight='bold')

plt.tight_layout()
plt.subplots_adjust(top=0.90, bottom=0.25)
#salva a imagem com a data e hora no nome do arquivo
nome_grafico2 = f'graficos/02_media_erros_{agora}.png'
plt.savefig(nome_grafico2, dpi=300)
print(f"Gráfico 2 de barras salvo: {nome_grafico2}")

#gráfico 3 - tabela de resutlados
#a biblioteca pandas agrupa por instância e calcula o min, médio, max e dsvio padrão
tabela_resultados = df.groupby('instancia').agg(
    valor_minimo=('fitness', 'min'),
    valor_medio=('fitness', 'mean'),
    valor_maximo=('fitness', 'max'),
    erro_minimo=('erro_relativo_percentual', 'min'),
    erro_medio=('erro_relativo_percentual', 'mean'),
    erro_maximo=('erro_relativo_percentual', 'max'),
    erro_desvio_padrao=('erro_relativo_percentual', 'std')
).reset_index()

#arredonda apenas as colunas que possuem núemros
colunas_numericas = tabela_resultados.select_dtypes(include=['number']).columns
tabela_resultados[colunas_numericas] = tabela_resultados[colunas_numericas].round(2)

#salva a tabela
nome_tabela = f'graficos/03_tabela_resultados_{agora}.csv'
tabela_resultados.to_csv(nome_tabela, sep=';', index=False)
print(f"Tabela Salva: {nome_tabela}")


print("Imagens e tabela salvas na pasta 'graficos'.")
plt.show() #exibição dos gráficos
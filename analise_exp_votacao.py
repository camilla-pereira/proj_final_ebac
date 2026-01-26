import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Ler a base de dados de 2022
vota2022 = pd.read_csv('dados tratados/votos2022.csv')
print(vota2022.columns)

vota2018 = pd.read_csv('dados tratados/votos2018.csv')

#Análise Exploratória I: Votos totais
Votos22PorMunPorDep = vota2022.groupby(['Nome_deputado_padronizado','Situação totalização']).agg({'Votos nominais': 'sum'})
print("Soma de Votos por Município em cada Candidato: \n", Votos22PorMunPorDep.head(20))
print("\n \n \n")

#Análise Exploratória II: 5 Municípios que mais votaram em cada candidato
#Inpute na variável a seguir o nome do candidato escolhido:

candidato = 'MATHEUS PEREIRA GOMES'
top5_municipios = (
    vota2022[vota2022["Nome_deputado_padronizado"] == candidato]
    .sort_values("Votos nominais", ascending=False, ignore_index=True)
    .head(20)
)
top5_municipios.drop_duplicates(subset=['Município'], inplace=True)

print("Municípios que concentram votos em:", candidato, "\n \n", top5_municipios.head(30))
print("\n \n \n")


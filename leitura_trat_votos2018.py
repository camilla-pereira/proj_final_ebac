import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Importando CSV
v2018v1 = pd.read_csv('dados/votacao_candidato2018.csv',dtype=str, encoding='latin1', sep=';')
print(v2018v1.head())
count_row = v2018v1.shape[0]
print(count_row)

#Deletando linhas com valores em branco
v2018v1.dropna(inplace=True)
print(count_row)

#Alterando o formato de votos nominais pra poder somar votos depois
v2018v1["Votos nominais"] = v2018v1["Votos nominais"].astype(int)
print(v2018v1.shape[0])

#Conforme a lista de deputados que enviaram emendas, temos uma lista de quais foram eleitos ou suplentes em 2018/2022
nomeseleitos2018 = pd.read_csv('dados tratados/nomes_padronizados_votos_emendas.csv', dtype=str, encoding='utf-8', sep=',')
enviaram_emendas18 = pd.DataFrame(nomeseleitos2018)
print(enviaram_emendas18.columns)

#Filtrados por eleitos ou suplentes em 2018
deps_eleitos_2018 = enviaram_emendas18[['CANDIDATO_2018','NOME PADRONIZADO']]
print(deps_eleitos_2018.head())

eleitos_2018_nomes = list(deps_eleitos_2018['CANDIDATO_2018'])
print(eleitos_2018_nomes)

votos_eleitos_2018 = v2018v1[v2018v1['Nome candidato'].isin(eleitos_2018_nomes)]
print(votos_eleitos_2018.head())
#VotosEleitos.to_csv("dados tratados/votos2022.csv")

#Agora, temos os dados de votação dos deputados que de fato legislaram
#Vamos retirar as colunas desnecessárias
votacao2018 = votos_eleitos_2018.drop(columns=['Cor/raça', 'Estado civil', 'Faixa etária', 'Gênero', 'Grau de instrução', 'Ocupação', 'UF', 'Zona', 'Número candidato', 'Turno', 'Votos válidos', 'Data de carga', 'Cargo', 'Região'])
print(votacao2018.columns)

#Vamos padronizar os nomes conforme a planilha NOME PADRONIZADO que fizemos no sheets:
dictnomes2018 = dict(zip(enviaram_emendas18['CANDIDATO_2018'],enviaram_emendas18['NOME PADRONIZADO']))
votacao2018['Nome_candidato_padronizado'] = votacao2018['Nome candidato'].map(dictnomes2018)
print(dictnomes2018)

votacao2018.to_csv("dados tratados/votos2018.csv", index=False)
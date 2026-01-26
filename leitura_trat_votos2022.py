import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Importando CSV
v2022v1 = pd.read_csv('dados/votacao_candidato2022.csv',dtype=str, encoding='latin1', sep=';')
#print(v2022v1.head())
count_row = v2022v1.shape[0]
#print(count_row)

#Deletando linhas com valores em branco
v2022v1.dropna(inplace=True)
#print(count_row)

#Confirmando que não sobrou nada em branco
#print(v2022v1.isnull().sum())

#Alterando o formato de votos nominais pra poder somar votos depois
v2022v1["Votos nominais"] = v2022v1["Votos nominais"].astype(int)
#print(v2022v1.shape[0])

#Conforme a lista de deputados que enviaram emendas, temos uma lista de quais foram eleitos ou suplentes em 2018/2022
nomeseleitos = pd.read_csv('dados tratados/nomes_padronizados_votos_emendas.csv', dtype=str, encoding='utf-8', sep=',')
EnviaramEmendas = pd.DataFrame(nomeseleitos)
#print(EnviaramEmendas.columns)

#Filtrados por eleitos ou suplentes em 2022
DepsEleitos2022 = EnviaramEmendas[['CANDIDATO_2022','NOME PADRONIZADO']]
#print(DepsEleitos2022.head())

Eleitos22Nomes = list(DepsEleitos2022['CANDIDATO_2022'])
#print(Eleitos22Nomes)

VotosEleitos = v2022v1[v2022v1['Nome candidato'].isin(Eleitos22Nomes)]
print(VotosEleitos.head())
VotosEleitos.to_csv("dados tratados/votos2022.csv")

#Agora, temos os dados de votação dos deputados que de fato legislaram
#Vamos retirar as colunas desnecessárias
print(VotosEleitos.columns)

votacao2022 = VotosEleitos.drop(columns=['Cor/raça', 'Estado civil', 'Faixa etária', 'Gênero', 'Grau de instrução', 'Ocupação', 'UF', 'Zona', 'Número candidato', 'Turno', 'Votos válidos', 'Data de carga', 'Cargo', 'Região'])
print(votacao2022.columns)

#Vamos padronizar os nomes conforme a planilha NOME PADRONIZADO que fizemos no sheets:
dictnomes = dict(zip(DepsEleitos2022['CANDIDATO_2022'],DepsEleitos2022['NOME PADRONIZADO']))
votacao2022['Nome_deputado_padronizado'] = votacao2022['Nome candidato'].map(dictnomes)

#Vamos padronizar os MUNICIPIOS conforme a planilha Municipio corrigido que fizemos no sheets:
municipioslista2022 = pd.read_csv('dados tratados/listamunicipioscorrigidosvotos2022.csv')
df_municipioslista22 = pd.DataFrame(municipioslista2022)

municipiosdictnomes = dict(zip(df_municipioslista22['Município original 2022'],df_municipioslista22['Municipio_corrigido']))
votacao2022['MUNICIPIO PADRONIZADO'] = votacao2022['Município'].map(municipiosdictnomes)

print(votacao2022.head(7))
print(votacao2022['MUNICIPIO PADRONIZADO'].value_counts())
votacao2022.to_csv("dados tratados/votos2022.csv", index=False)
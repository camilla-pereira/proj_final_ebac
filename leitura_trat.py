import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#limpando linhas em branco de votacao2022
v2022v1 = pd.read_csv('dados/votacao_candidato2022-cortarlinhasvazias.csv')
v2022v1.head()
count_row = v2022v1.shape[0]
#print(count_row)

#Limpa
v2022v1.dropna(inplace=True)
count_row = v2022v1.shape[0]
#print(count_row)

#Salva novo CSV
v2022v1.to_csv('dados/votacao_candidato2022-v2.csv')
v2022v2 = pd.read_csv('dados tratados/votacao_candidato2022-v2.csv')
count_row = v2022v2.shape[0]
#print(count_row)

#Limpa 2018 de não eleitos e linhas em branco
v2018v1 = pd.read_csv('dados/votacao_candidato2018-cortarNeleitoselinhasvazias.csv')
count_row = v2018v1.shape[0]
#print(count_row)

v2018v2 = v2018v1[v2018v1['Situação totalização'] != 'Não Eleito']
count_row = v2018v2.shape[0]
#rint(count_row)

v2018v2.isnull().sum()
v2018v2.to_csv('dados/votacao_candidato2018-v2.csv')

#Verificar Emendas
dfEP = pd.read_csv('dados/EmendasParlamentares2022-2025 - EmendasParlamentares2022-2025 - EmendasParlamentares2022-2025 - EmendasParlamentares2022-2025.csv.csv', sep=',', dtype=str)
count_row = dfEP.shape[0]
dfEP.isnull().sum()

#Tratamento da coluna MUNICÍPIOS em Emendas
#Encontra linhas com Municipio vazio
#e cria a coluna Municipio corrigido, com os valores nao vazios da original
munivazio = dfEP["Municipio"].fillna("").str.strip() == ""
dfEP["Municipio_corrigido"] = dfEP["Municipio"]

# Slice onde Municipio está vazio
dfEP.loc[munivazio, "Municipio_corrigido"] = (
    dfEP["NomeProjeto"].str.split("de", n=1).str[1]
)

#Encontrando quem ainda está em branco:
projemdef = dfEP["NomeProjeto"].str.contains("Em Definicao", na=False)
dfEP.loc[projemdef, "Municipio_corrigido"] = "RS"
dfEP["Municipio_corrigido"] = dfEP["Municipio_corrigido"].str.lstrip()
dfEP.to_csv("dados tratados/Emendas_tratado.csv")
import pandas as pd

#Verificar Emendas
dfEP = pd.read_csv(
    'dados/EmendasParlamentares2022-2025.csv',
    sep=',', dtype=str)
count_row = dfEP.shape[0]
dfEP.isnull().sum()

#Tratamento da coluna MUNICÍPIOS em Emendas
#Encontra linhas com Municipio vazio
#e cria a coluna Municipio corrigido, com os valores não vazios da original
municipiovazio = dfEP["Municipio"].fillna("").str.strip() == ""
dfEP["Municipio_corrigido"] = dfEP["Municipio"]

# Slice onde Municipio está vazio mas o nome está na coluna NomeProjeto
dfEP.loc[municipiovazio, "Municipio_corrigido"] = (
    dfEP["NomeProjeto"].str.split("de", n=1).str[1]
)

#Encontrando quem continua em branco:
projemdef = dfEP["NomeProjeto"].str.contains("Em Definicao", na=False)
dfEP.loc[projemdef, "Municipio_corrigido"] = "RS"
dfEP["Municipio_corrigido"] = dfEP["Municipio_corrigido"].str.lstrip()
dfEP.to_csv("dados tratados/Emendas_tratado.csv")

# Vamos padronizar os nomes dos deputados conforme estão nas outras tabelas
# Procurando valores únicos na coluna Deputado
print(dfEP["Deputado"].unique())
print(dfEP["Deputado"].nunique())

#Encontrei dois valores que estão escritos de duas formas, vamos arrumar:
dfEP.loc[dfEP['Deputado'] == "Neri, o Carteiro", 'Deputado'] = 'Neri o Carteiro'
print(dfEP["Deputado"].nunique())

dfEP.loc[dfEP['Deputado'] == "Professor Issur Koch", 'Deputado'] = 'Issur Koch'
print(dfEP["Deputado"].nunique())

#Vamos padronizar os nomes conforme a planilha NOME PADRONIZADO que fizemos no sheets:
from leitura_trat_votos2022 import nomeseleitos
print(nomeseleitos.head())

#Criando o dicionário
emendas_dictnomes = dict(zip(nomeseleitos['DEP'],nomeseleitos['NOME PADRONIZADO']))
dfEP['Nome_deputado_padronizado'] = dfEP['Deputado'].map(emendas_dictnomes)
print(dfEP.head())

#Eliminando colunas desnecessárias
dfEP = dfEP.drop(columns=['CodUo', 'CodProjeto', 'CodSubtitulo', 'SubtituloResumido', 'Municipio'])
print(dfEP.columns)

dfEP.to_csv('dados tratados/Emendas_tratado.csv', index=False)

#Somar todas as emendas que um deputado mandou para uma cidade específica
dfEP_agrupado = dfEP.groupby(['Nome_deputado_padronizado', 'Municipio_corrigido']).agg({
    'Valor': 'sum'
}).reset_index()

print(dfEP_agrupado.head())
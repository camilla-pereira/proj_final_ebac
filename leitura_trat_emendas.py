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

#Deixando valores no mesmo formato pra soma ficar certinha:
dfEP['Valor'] = pd.to_numeric(dfEP['Valor'], errors='coerce')
dfEP['Valor'] = dfEP['Valor'].fillna(0)

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

#deixando os municípios em caps e com o mesmo nome de coluna das tabelas de voto
dfEP['MUNICIPIO PADRONIZADO'] = dfEP['Municipio_corrigido'].str.upper()
print(dfEP.head())

#Convertendo Ano para Numérico para usar como filtro no looker e separando de Ano de Eleição
dfEP['Ano_de_envio'] = pd.to_numeric(dfEP['Ano'], errors='coerce')
print(dfEP.head())
dfEP.describe()

#Somar todas as emendas que um deputado mandou para uma cidade específica
dfEP_agrupado = dfEP.groupby(['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'Ano_de_envio']).agg({
    'Valor': 'sum'
}).reset_index()

print(dfEP_agrupado.dtypes)

#Organizando ciclos de mandato, para comparar nas datas adequadas:
def definir_ciclo(Ano_de_envio):
    if 2019 <= Ano_de_envio <= 2022:
        return 2018 #Eleito em 2018
    elif 2023 <= Ano_de_envio <= 2026:
        return 2022 #Eleito em 2022
    return Ano_de_envio

dfEP_agrupado['ciclo_eleitoral'] = dfEP_agrupado['Ano_de_envio'].apply(definir_ciclo)
df_EP_merge = dfEP_agrupado.groupby(['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral', 'Ano_de_envio']).agg({'Valor': 'sum'}).reset_index()
print(df_EP_merge.head())
print(df_EP_merge['ciclo_eleitoral'].value_counts())
print(df_EP_merge.columns)
print(df_EP_merge.dtypes)
print(dfEP_agrupado.head())

#Deu certo, agora só tenho dois ciclos eleitorais (o ano de eleição). Bora pro merge!
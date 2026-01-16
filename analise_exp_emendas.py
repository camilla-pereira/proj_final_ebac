import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Ler a base de dados e reduzir CSV apenas para colunas essenciais
EmendasDF = pd.read_csv('dados tratados/Emendas_tratado.csv')

#Análise Exploratória I: Distribuição com soma
EmendasPorAnoeDep = EmendasDF.groupby(['Ano','Partido','Nome_deputado_padronizado','Orgao'])['Valor'].sum()
print("Distribuição de Emendas por Ano e por Deputado: \n", EmendasPorAnoeDep.head(3))
print("\n \n \n")

# #Análise Exploratória II: Soma por Grupo
ValorEmendasPorMunicipioPorAno = EmendasDF.groupby(['Municipio_corrigido', 'Ano'])['Valor'].sum()
print("Distribuição de Emendas por Município, Ano e Valor: \n", ValorEmendasPorMunicipioPorAno.head(3))
print("\n \n \n")

#Análise Exploratória III: Distribuição com agregação
EmendasPorSec = EmendasDF.groupby(["Orgao", "NomeProjeto", "Ano"]).agg({"Valor": "sum"})
print("Distribuição de Emendas por Secretaria ou Órgão Estadual: \n", EmendasPorSec.head(3))
print("\n \n \n")

#Análise Exploratória IV: Ranking e Identificação de Outliers
Top10CidadesMais = (
     EmendasDF.groupby(["Municipio_corrigido"])['Valor']
     .sum()
     .reset_index()
     .rename(columns={"Valor": "Soma_Valores"})
 )
Top10CidadesMais.sort_values("Soma_Valores", ascending=False, inplace=True)
print("Os 10 Municípios que receberam mais recursos, de 2022 a 2025: \n", Top10CidadesMais.head(10))

MunicipioRecebeuMais = Top10CidadesMais.iloc[0,0]
MunicipioSomaValores = Top10CidadesMais.iloc[0,1]
InvestimentoTotal = Top10CidadesMais[["Soma_Valores"]].sum()

print(f"O município que recebeu mais recursos foi {MunicipioRecebeuMais}, com R${MunicipioSomaValores/1000000:,.2f} milhões.")
print("\n \n \n")

#Análise Exploratória V: Comparação entre variáveis (as cidades que recebem mais valores são as mais populosas?)

Top10CidadesMaisPop = {'Município':['Porto Alegre','Caxias do Sul','Canoas','Pelotas', 'Santa Maria', 'Gravataí', 'Novo Hamburgo', 'Viamão', 'São Leopoldo', 'Passo Fundo'],
                        'População': [1332570, 463338, 347657, 325689, 271633, 265074, 227732, 224116, 217410, 206224]}

Top10CidadesMaisPop = pd.DataFrame(Top10CidadesMaisPop)
print("Top 10 cidades com maiores populações, de acordo com o Censo 2022:\n", Top10CidadesMaisPop)
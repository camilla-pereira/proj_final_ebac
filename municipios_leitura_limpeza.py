from leitura_trat_votos2018 import votacao2018
import unicodedata
import pandas as pd

#Limpando a coluna municípios para que ela possa ser chave de busca no dashboard
def remover_acentos(texto):
    if not isinstance(texto, str):
        return texto
    nfkd = unicodedata.normalize('NFKD', texto)
    # Filtra o que não é acento
    return "".join([c for c in nfkd if not unicodedata.category(c).startswith('M')])

votacao2018['Município'] = votacao2018['Município'].apply(remover_acentos).str.strip()
lista_municipios2018 = pd.DataFrame(votacao2018['Município'].unique(), columns=['municipio_original'])
lista_municipios2018 = lista_municipios2018.sort_values(by='municipio_original')
lista_municipios2018.to_csv('dados tratados/listamunicipios2018.csv', index=False)

votacao2018.to_csv("dados tratados/votos2018.csv", index=False)

#Agora vamos incluir o código do município, de acordo com o código estadual da secretaria da fazenda do RS, que é o que já está na tabela emendas
dadosipm = pd.read_csv('dados/dados-aim-ipm.csv', encoding='latin', sep=';')
#print(dadosipm.head())

dfdadosipm = pd.DataFrame(dadosipm)
#print(dfdadosipm.head())

slicecodmun = dfdadosipm[['Cod_Mun', 'Município']]
#print(slicecodmun.head())
#print(len(slicecodmun))
dfslicecodmun = pd.DataFrame(slicecodmun)
dfslicecodmun.drop_duplicates(inplace=True)
#print(len(dfslicecodmun))
#print(dfslicecodmun.head())

dfslicecodmun.set_index('Cod_Mun', inplace=True)
dfslicecodmun.sort_values(by=['Município'], ascending=True, inplace=True)
#print(dfslicecodmun.head())

dfslicecodmun.to_csv("dados tratados/municipioscodsefaz.csv", index=True)

#Agora temos uma lista de municípios com os códigos da sefaz
#Vamos uniformizar

dictcodmun = dict(zip(lista_municipios2018['municipio_original'], dfslicecodmun['Município']))
lista_municipios = pd.DataFrame(votacao2018['Município'].unique(), columns=['municipio_original'])
lista_municipios = lista_municipios.sort_values(by='municipio_original')
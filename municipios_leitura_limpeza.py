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

#Extraindo a lista de municípios
votacao2018['Município'] = votacao2018['Município'].apply(remover_acentos).str.strip()
lista_municipios2018 = pd.DataFrame(votacao2018['Município'].unique(), columns=['municipio_original'])
lista_municipios2018 = lista_municipios2018.sort_values(by='municipio_original')
lista_municipios2018.to_csv('dados tratados/listamunicipios2018.csv', index=False)

votacao2018.to_csv("dados tratados/votos2018.csv", index=False)
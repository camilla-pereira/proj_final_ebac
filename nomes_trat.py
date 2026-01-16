# import pandas as pd
# import re
# from unidecode import unidecode
#
# #importando a lista de nomes únicos eleitos e nomes únicos de deputados que enviaram emendas
#
# from leitura_trat_votos import NomesUniqEleitos
# from leitura_trat_emendas import ListaNomesDeps
#
# #Definindo função para tratar nomes
# def nome_pad(nome):
#     #tudo maiúsculo
#     nome = nome.upper()
#
#     #tira acento
#     nome = unidecode(nome)
#     #tira espaço extra
#     nome = nome.strip()
#
#     return nome
#
# ListaVotosPad = [nome_pad(n) for n in NomesUniqEleitos]
# ListaNomesDepsPad = [nome_pad(n) for n in ListaNomesDeps]
#
# #print(ListaVotosPad)
# #print(ListaNomesDepsPad)
#
# #Unificar listas
# todas = ListaVotosPad + ListaNomesDepsPad
#
# #Remover Repetidos
# nomesunicos = sorted(list(todas))
# #print(len(nomesunicos))
#
# #Gerando código único
# DFdepara = pd.DataFrame(sorted(list(nomesunicos)), columns=["Nome padronizado"])
# DFdepara["codigo"] = range(1, len(DFdepara) + 1)
# DFdepara["nome correto"] = ""
#
# print(DFdepara.head())
# DFdepara.to_csv('dados tratados/nomestratados.csv', index=False, encoding='utf-8-sig')
#
# #aqui ta errado
# # df_map = pd.read_csv('dados tratados/nomestratados.csv')
# mapa = dict(zip(df_map["Nome padronizado"], df_map[""]))
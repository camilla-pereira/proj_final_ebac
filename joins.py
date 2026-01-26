import pandas as pd
import analise_exp_votacao as AEV
import leitura_trat_emendas as LTE

#Vamos dar um join nas duas tabelas de votos para fazer uma análise mais robusta no looker:
print(AEV.vota2018.dtypes)
print(AEV.vota2022.dtypes)

votos2018a2022 = pd.concat([AEV.vota2018, AEV.vota2022], ignore_index=True)
votos2018a2022.rename(columns={'Ano de eleição': 'ciclo_eleitoral'}, inplace=True)
print(votos2018a2022['MUNICIPIO PADRONIZADO'].value_counts())
print(votos2018a2022['ciclo_eleitoral'].value_counts())
print(votos2018a2022.columns)

#Limpando DFs para eliminar erros de soma em Valor
votos_limpos = votos2018a2022.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral']
).agg({
    'Votos nominais': 'sum'
}).reset_index()

emendas_limpas = LTE.dfEP_agrupado.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral']
).agg({
    'Valor': 'sum'
}).reset_index()

votos2018a2022.to_csv('dados tratados/votos2018a2022.csv')

df_master = pd.merge(
    votos_limpos,
    emendas_limpas,
    on=['Nome_deputado_padronizado','MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
    how='left'
).fillna(0)

# Colocando 0 em quem não teve emenda para não dar erro no Looker
#df_master['Valor'] = df_master['Valor'].fillna(0)
#df_master['Ano_de_envio'] = df_master['Ano_de_envio'].fillna(0)

#print(df_master.columns)
#print(df_master.head())

print(f"Soma Votos Original: {votos2018a2022['Votos nominais'].sum()}")
print(f"Soma Votos Após Merge: {df_master['Votos nominais'].sum()}")

print(f"Soma Emendas Original: {LTE.df_EP_merge['Valor'].sum()}")
print(f"Soma Emendas Após Merge: {df_master['Valor'].sum()}")

#df_master.to_csv('dados tratados/votos1822eemendascciclo.csv')
#print(df_master.head())
#print(df_master.dtypes)

# Troubleshooting porque o numero de valores ta altíssimo:
#print("Total de Emendas no Python:", df_master['Valor'].sum())
votos_set = set(votos_limpos['Nome_deputado_padronizado'].unique())
emendas_set = set(emendas_limpas['Nome_deputado_padronizado'].unique())

faltantes = emendas_set - votos_set
print(f"Deputados das emendas não encontrados nos votos: {len(faltantes)}")
print(list(faltantes)[:10])

# Emendas sem match
emendas_nao_pareadas = emendas_limpas[
    ~emendas_limpas.set_index(['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral']).index.isin(
        votos_limpos.set_index(['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral']).index
    )
]

print(f"Total de emendas 'perdidas': {emendas_nao_pareadas['Valor'].sum()}")
print("Exemplo de cidades/deputados que sumiram:")
print(emendas_nao_pareadas[['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'Valor']])
print(len(emendas_nao_pareadas[['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'Valor']]))

#Buscando se o problema é o Nome
emendas_sem_match_nomesdeps = emendas_nao_pareadas['Nome_deputado_padronizado'].drop_duplicates()
print(emendas_sem_match_nomesdeps)
print(len(emendas_sem_match_nomesdeps))

# Verificando se o erro é por ano de eleição
print("Emendas sem match por Ciclo Eleitoral:")
print(emendas_nao_pareadas['ciclo_eleitoral'].value_counts())

import numpy as np

# Criando a coluna de diagnóstico
condicoes = [
    (df_master['Votos nominais'] > 0) & (df_master['Valor'] > 0),
    (df_master['Votos nominais'] > 0) & (df_master['Valor'] == 0),
    (df_master['Votos nominais'] == 0) & (df_master['Valor'] > 0)
]

escolhas = ['Match Completo', 'Apenas Votos (Sem Emenda)', 'Apenas Emendas (Sem Voto)']

df_master['Status_Analise'] = np.select(condicoes, escolhas, default='Outros')

# Verificando se os 26 milhões estão agora na categoria 'Apenas Emendas'
print(df_master.groupby('Status_Analise')['Valor'].sum())

# O parâmetro dropna=False impede que o Pandas delete emendas "sem dono" ou "sem cidade"
emendas_limpas = LTE.dfEP_agrupado.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
    dropna=False
).agg({'Valor': 'sum'}).reset_index()

print(f"Soma após groupby (com dropna=False): {emendas_limpas['Valor'].sum()}")

# Isso vai te mostrar exatamente as linhas que o dropna estava jogando fora
linhas_fantasmagóricas = emendas_limpas[
    emendas_limpas['Nome_deputado_padronizado'].isna() |
    emendas_limpas['MUNICIPIO PADRONIZADO'].isna()
]

print(f"Valor das emendas 'sem dono' ou 'sem cidade': {linhas_fantasmagóricas['Valor'].sum()}")
print(linhas_fantasmagóricas.head())

#####
#ts para saber qual groupby comeu o dinheiro
soma_inicial = LTE.dfEP_agrupado['Valor'].sum()
print(f"1. Soma Inicial (Bruta): {soma_inicial:,.2f}")

# Se os 26 milhões sumirem aqui, o culpado é esse groupby
df_teste_padrao = LTE.dfEP_agrupado.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral']
).agg({'Valor': 'sum'}).reset_index()
soma_padrao = df_teste_padrao['Valor'].sum()
print(f"2. Soma Groupby Padrão:  {soma_padrao:,.2f}")

df_teste_seguro = LTE.dfEP_agrupado.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
    dropna=False
).agg({'Valor': 'sum'}).reset_index()

soma_segura = df_teste_seguro['Valor'].sum()
print(f"3. Soma Groupby Seguro:  {soma_segura:,.2f}")

# Verifica nulos em TODAS as colunas que você usa no groupby
print("Contagem de nulos por coluna:")
print(LTE.dfEP_agrupado[['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral']].isna().sum())


###

LTE.dfEP_agrupado['Nome_deputado_padronizado'] = LTE.dfEP_agrupado['Nome_deputado_padronizado'].astype(str).str.strip()
LTE.dfEP_agrupado['MUNICIPIO PADRONIZADO'] = LTE.dfEP_agrupado['MUNICIPIO PADRONIZADO'].astype(str).str.strip()
LTE.dfEP_agrupado['ciclo_eleitoral'] = LTE.dfEP_agrupado['ciclo_eleitoral'].astype(int)

# Usamos o dropna=False porque ele provou ser a única forma de manter sua soma íntegra
emendas_finais = LTE.dfEP_agrupado.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
    dropna=False
)['Valor'].sum().reset_index()

# 3. Verificação de Ouro
print(f"Soma Final para o Looker: {emendas_finais['Valor'].sum():,.2f}")
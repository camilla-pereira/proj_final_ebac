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

#Limpando DFs para eliminar erros de soma em Valor e Votos
votos_limpos = votos2018a2022.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
).agg({'Votos nominais': 'sum'}).reset_index()
votos2018a2022.to_csv('dados tratados/votos2018a2022.csv')

emendas_limpas = LTE.dfEP_agrupado.groupby(
    ['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral', 'Ano_de_envio'], dropna=False
).agg({'Valor':'sum'}).reset_index()

df_master = pd.merge(
    votos_limpos,
    emendas_limpas,
    on=['Nome_deputado_padronizado','MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
    how='outer')

print(df_master.columns)

# Colocando 0 em quem não teve emenda para não dar erro no Looker
df_master['Valor'] = df_master['Valor'].fillna(0)
df_master['Votos nominais'] = df_master['Votos nominais'].fillna(0)

# Como eu quero ver as emendas ano a ano, o Gemini me orientou a incluir essa parte, que calcula os votos só uma vez:
df_master = df_master.sort_values(['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral', 'Ano_de_envio'])
df_master['Ano_de_envio'] = df_master['Ano_de_envio'].fillna(0).astype(int)

# O subset define o que identifica um "voto único": a combinação de Quem, Onde e Quando (Ciclo)
mascara_duplicados = df_master.duplicated(
    subset=['Nome_deputado_padronizado', 'MUNICIPIO PADRONIZADO', 'ciclo_eleitoral'],
    keep='first' # Mantém o valor apenas na primeira linha encontrada
)

# Zerando os votos nas linhas excedentes | Onde mascara_duplicados for True, o Voto vira 0
df_master.loc[mascara_duplicados, 'Votos nominais'] = 0

# Números finais
print(f"Soma Final de Emendas: {df_master['Valor'].sum():,.2f}")
print(f"Soma Final de Votos:   {df_master['Votos nominais'].sum():,.0f}")


print(df_master.columns)
#print(df_master.head())

df_master.to_csv('dados tratados/basecompletaparalooker.csv', index=False, encoding='utf-8-sig')
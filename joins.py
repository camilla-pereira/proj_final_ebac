import pandas as pd
import analise_exp_votacao as AEV
import leitura_trat_emendas as LTE

#Vamos dar um join nas duas tabelas de votos para fazer uma análise mais robusta no looker:
print(AEV.vota2018.dtypes)
print(AEV.vota2022.dtypes)

votos2018a2022 = pd.concat([AEV.vota2018, AEV.vota2022], ignore_index=True)
print(votos2018a2022['MUNICIPIO PADRONIZADO'].value_counts())

print(votos2018a2022.columns)

votos2018a2022.to_csv('dados tratados/votos2018a2022.csv')

df_master = pd.merge(
    votos2018a2022,
    LTE.dfEP_agrupado,
    on=['Nome_deputado_padronizado','MUNICIPIO PADRONIZADO'],
    how='left'
)

# Colocando 0 em quem não teve emenda para não dar erro no Looker
df_master['Valor'] = df_master['Valor'].fillna(0)

#print(df_master.columns)
#print(df_master.head())

df_master.to_csv('dados tratados/votos1822eemendas.csv')
print(df_master.head())
import pandas as pd

from leitura_trat_votos2018 import votos_eleitos_2018
from leitura_trat_votos2022 import votacao2022

#Concat entre votos de 2018 e 2022
votostotais = pd.read_csv("dados tratados/votos2018a2022.csv")
print(votostotais.head())



#Join entre Emendas e Votos
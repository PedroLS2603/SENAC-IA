from cidade import Cidade
from deslocamento import Deslocamento
import pandas as pd

DOMINIO_GENE = []
DESLOCAMENTOS = []

# Configura as variáveis globais de domínio
def configurar_dominio():
  itens = pd.read_csv("itens.csv").fillna(0)
  deslocamentos = pd.read_csv("deslocamentos.csv")

  for index, row in itens.iterrows():
    DOMINIO_GENE.append(Cidade(nome=row["Cidade"], peso=row["Peso"], valor=row["Valor"], tempo_roubo=row["Tempo_Roubo"], item=row["Item"]))

  for index, row in deslocamentos.iterrows():
    origem = [cidade for cidade in DOMINIO_GENE if row["Origem"] == cidade.nome][0]
    destino = [cidade for cidade in DOMINIO_GENE if row["Destino"] == cidade.nome][0]
    valor = row["Valor"]
    tempo = row["Tempo"]
    DESLOCAMENTOS.append(Deslocamento(origem=origem, destino=destino, tempo=tempo, valor=valor))

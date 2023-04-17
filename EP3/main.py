from agp import AlgoritmoGeneticoPopulacao
from individuo import Individuo
from populacao import Populacao
from data import configurar_dominio


configurar_dominio()

algoritmo = AlgoritmoGeneticoPopulacao(populacao=Populacao())

final = algoritmo.rodar()

print(final)
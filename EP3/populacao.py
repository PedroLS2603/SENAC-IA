from individuo import Individuo
from data import DOMINIO_GENE
from math import floor
from copy import deepcopy
import numpy as np

class Populacao:
  def __init__(self, tamanho = 10):
    self.tamanho = tamanho
    self.populacao = [Individuo() for i in range(tamanho)]
    self.fitness = []

  def fitness_pop(self, individuo):    
    return individuo.fitness()

  def mutacao(self):
    mutacoes = []
    for individuo in self.populacao:
      mutacoes.append(individuo.mutacao())

    return mutacoes

  def crossover(self):
    nova_populacao = []
    rotas_novos_individuos = []

    copy_populacao = deepcopy(self.populacao)

    metade = floor(len(self.populacao)/2)

    populacao_esquerda = copy_populacao[:metade]
    populacao_direita = copy_populacao[metade:]

    for c in range(metade):
      individuo_esquerda = populacao_esquerda[c].imagem
      individuo_direita = populacao_direita[c].imagem

      corte = floor(0.7 * len(individuo_direita))  

      setenta_esquerda = individuo_esquerda[:corte]
      setenta_direita = individuo_direita[:corte]

      trinta_esquerda = individuo_esquerda[corte:]
      trinta_direita = individuo_direita[:corte]

      novo_individuo_1 = setenta_esquerda + trinta_direita
      novo_individuo_2 = setenta_direita + trinta_esquerda

      rotas_novos_individuos.append(novo_individuo_1)
      rotas_novos_individuos.append(novo_individuo_2)

    for rota in rotas_novos_individuos:
      nova_populacao.append(Individuo(imagem=rota))

    return nova_populacao


  def selecionar(self, populacao1, populacao2):
    self.populacao = self.populacao + populacao1 + populacao2
    nova_lista = sorted(self.populacao, key=self.fitness_pop, reverse=True)
    self.populacao = nova_lista[0:10]

  def gerar_populacao(self):
    self.populacao = []

    for i in range(self.tamanho):
      self.populacao.append(Individuo())

  def top_fitness(self):
    return self.fitness_pop(self.populacao[0])
  
  def top_individuo(self):
    return self.populacao[0]
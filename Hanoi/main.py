import numpy as np
import pandas as pd
import math as m
from no import No

class Hanoi():
    estado_inicial =[]
    estado_final = []
    raiz = None

    def __init__(self, numTorres, numDiscos):
        for i in range(numTorres):
            self.estado_inicial.append([])
            self.estado_inicial.append([])

        torre_ordenada = list(range(numDiscos)).sort(reverse=True)

        self.estado_inicial[0] = torre_ordenada
        self.estado_final[-1] = torre_ordenada

    def iniciar(self):
        self.raiz = No(estado=self.estado_inicial, custo=1, heuristica = self.heuristica_inicial())

    def heuristica(self):
        pass

    def acao(self, origem, destino, no: No):
        estado_atual = list(np.copy(no.estado))

        disco = estado_atual[origem].pop()
        estado_atual[destino].append(disco)

        return No(estado=estado_atual, no_pai=no, custo=1, heuristica=self.heuristica())
         

    def gerar_sucessores(self, no: No):
        estado = no.estado
        sucessores = [] 

        expansoes = [torre for torre in estado]
        
        for origem in expansoes:
            for destino in expansoes:
                if expansoes.index(destino) != expansoes.index(origem):
                   sucessor = self.acao(origem, destino, no)
                   if self.valida_estado(sucessor):
                    sucessores.append(sucessor)     

        return sucessores

    def valida_estado(self, no: No):
        for torre in no.estado:
            if torre != torre.sort(reverse=True):
                return False
        
        return True
            

    def custo(self, no: No = None):
        return 1   
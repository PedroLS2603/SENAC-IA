import numpy as np
import pandas as pd
import math as m
from no import No

class Hanoi():
    estado_inicial =[]
    estado_final = []
    raiz = None
    bla = 10

    def __init__(self, numTorres, numDiscos):
        for i in range(numTorres):
            self.estado_inicial.append([])
            self.estado_final.append([])

        torre_ordenada = list(range(numDiscos))
        torre_ordenada.sort(reverse=True)
        torre_ordenada = [x + 1 for x in torre_ordenada]
        
        self.estado_inicial[0] = torre_ordenada
        self.estado_final[-1] = torre_ordenada

        for i in range(len(self.estado_inicial)):
            self.estado_inicial[i] = tuple(self.estado_inicial[i])
            self.estado_final[i] = tuple(self.estado_final[i])

        
    def iniciar(self):
        self.raiz = No(estado=self.estado_inicial, custo=1, heuristica = self.heuristica())
        return self.raiz

    def heuristica(self, no:No = None):
        if no == None:
            return 0 
        return -len(no.estado[-1])

    def acao(self, origem, destino, no: No):
        estado_atual = list()

        for torre in no.estado:
            estado_atual.append(list(torre))
        
        disco = estado_atual[origem].pop()
        estado_atual[destino].append(disco)


        return No(estado=self.list_to_tuple(estado_atual), no_pai=no, custo=1, heuristica=self.heuristica())
         

    def list_to_tuple(self, lista):
        aux = list()
        for item in lista:
            aux.append(tuple(item))

        return aux

    def gerar_sucessores(self, no: No):
        estado = no.estado
        sucessores = [] 

        expansoes = [list(torre) for torre in estado]
        
        for origem in range(len(expansoes)):
            for destino in range(len(expansoes)):
                if destino != origem and len(expansoes[origem]) > 0:
                   sucessor = self.acao(origem, destino, no)
                   if self.valida_estado(sucessor):
                    sucessores.append(sucessor)
                    print(f"{expansoes[origem]}({origem}) -> {expansoes[destino]}({destino})")


        return sucessores

    def valida_estado(self, no: No):
        for torre in no.estado:
            torre = list(torre)
            aux = list.copy(torre)
            aux.sort(reverse=True)
            if torre != aux:
                return False
        
        return True
            

    def custo(self, no: No, destino: No):
        return 1   

    def testar_objetivo(self, no: No):
        return no.estado == self.estado_final
    
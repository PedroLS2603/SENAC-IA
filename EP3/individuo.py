from data import DOMINIO_GENE, DESLOCAMENTOS
import random
from copy import deepcopy
import numpy as np

class Individuo:
    def __init__(self, imagem = None):

        self.imagem = []
        self.deslocamentos = []

        #Gerando uma rota aleatória caso não seja instanciado no indivíduo
        if imagem == None:
            self.imagem = self.rand()
            rota = self.rota()
        else:
            escondidos = DOMINIO_GENE[-1]
            imagem = list(set(imagem))
            imagem.append(escondidos)
            self.imagem = imagem
        rota = self.rota()            

        #Gerando array de deslocamentos
        for i in range(len(rota)):
            if i == len(rota) - 1:
                break
            origem = rota[i]
            destino = rota[i+1]

            if origem.nome == destino.nome:
                continue
            self.deslocamentos.append([deslocamento for deslocamento in DESLOCAMENTOS if ((deslocamento.origem.nome == origem.nome and deslocamento.destino.nome == destino.nome) or (deslocamento.origem.nome == destino.nome and deslocamento.destino.nome == origem.nome))][0])
    def mutacao(self):
        copy_imagem = deepcopy(self.imagem)
        while True:
            substituido = random.choice(copy_imagem)
            substituto = random.choice(copy_imagem)

            if substituido.nome == substituto.nome:
                continue

            i_substituido = copy_imagem.index(substituido)
            i_substituto = copy_imagem.index(substituto)

            copy_imagem[i_substituido] = substituto
            copy_imagem[i_substituto] = substituido

            print(copy_imagem)
            if self.valida_mutacao(copy_imagem):
                return Individuo(copy_imagem)

    def valida_mutacao(self, imagem = None):
        if imagem == None:
            imagem = self.imagem

        count_escondidos = len([cidade for cidade in imagem if cidade.nome == "Escondidos"])
        return imagem[0].nome == "Escondidos" and imagem[1].nome != "Escondidos" and count_escondidos > 1
    
    def fitness(self):
        peso = self.peso_total()
        tempo_gasto = self.tempo_total()
        montante = self.custo_total()
        
        if tempo_gasto > 72 or peso > 20 or not self.valida_mutacao():
            return -(montante + ((tempo_gasto*0.6) + (peso*0.4)))

        
        return montante + ((tempo_gasto*0.6) + (peso*0.4))

    def rota(self, imagem = None):
        if imagem == None:
            imagem = self.rand()
        imagem = self.imagem
        idx_escondidos = imagem[1:].index([cidade for cidade in imagem[1:] if cidade.nome == "Escondidos"][0]) + 1

        return imagem[:idx_escondidos] 

    def fora_de_rota(self, imagem = None):
        if imagem == None:
            imagem = deepcopy(self.imagem)

        idx_escondidos = imagem[1:].index([cidade for cidade in imagem[1:] if cidade.nome == "Escondidos"][0]) + 1

        return imagem[idx_escondidos:] 


    def custo_total(self):
        montante_rota = np.array([cidade.valor for cidade in self.rota()]).sum()
        custo_viagem = np.array([deslocamento.custo for deslocamento in self.deslocamentos]).sum()
        
        return montante_rota - custo_viagem

    def peso_total(self):
        peso = np.array([cidade.peso for cidade in self.rota()]).sum()

        return peso

    def tempo_total(self):
        tempo_rota = np.array([cidade.tempo_roubo for cidade in self.rota()] ).sum()
        custo_viagem = np.array([deslocamento.tempo for deslocamento in self.deslocamentos]).sum()

        return tempo_rota + custo_viagem

    def rand(self):
        #Gerando segunda ocorrência de Escondidos para gerar a rota completa
        escondidos = [cidade for cidade in DOMINIO_GENE if cidade.nome == "Escondidos"][0]
        copy_dominio = deepcopy(DOMINIO_GENE)      
        while True:
            amostra = random.sample(copy_dominio, len(copy_dominio))
            amostra.insert(0, escondidos)

            if amostra[1].nome != "Escondidos":
                return amostra
            
    def __repr__(self):
        rota = self.rota()

        return '->'.join([cidade.nome for cidade in rota])
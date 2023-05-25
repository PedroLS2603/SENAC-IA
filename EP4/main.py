import skfuzzy as fz
from skfuzzy import control as ctr
import numpy as np
import json

banco = json.load(open("./palavras.json"))

banco["positivas"] = [p.lower() for p in banco["positivas"]]
banco["negativas"] = [p.lower() for p in banco["negativas"]]
banco["intensificadores"] = [p.lower() for p in banco["intensificadores"]]
banco["negacoes"] = [p.lower() for p in banco["negacoes"]]
banco["frases"] = [p.lower() for p in banco["frases"]]

frases = banco["frases"]


# Definindo as métricas
class Fuzzy:

    def __init__(self, banco):
        self.freqPP = ctr.Antecedent(np.arange(0, 2, 1), "FP")
        self.freqPN = ctr.Antecedent(np.arange(0, 2, 1), "FN")
        self.freqI = ctr.Antecedent(np.arange(0, 2, 1), "I")
        self.freqNeg = ctr.Antecedent(np.arange(0, 2, 1), "N")

        self.banco_palavras = banco
        

        # Configurando pertencimento
        self.freqPP.automf(names=["ausente", "presente"])
        self.freqPN.automf(names=["ausente", "presente"])
        self.freqI.automf(names=["ausente", "presente"])
        self.freqNeg.automf(names=["ausente", "presente"])

        # Configurando função de pertencimento triangular
        self.sentimento = ctr.Consequent(np.arange(0, 11, 1), "sentimento")
        self.sentimento["muito_negativo"] = fz.trimf(self.sentimento.universe, [0, 0, 3])
        self.sentimento["negativo"] = fz.trimf(self.sentimento.universe, [1, 3, 5])
        self.sentimento["neutro"] = fz.trimf(self.sentimento.universe, [3, 5, 7])
        self.sentimento["positivo"] = fz.trimf(self.sentimento.universe, [5, 7, 9])
        self.sentimento["muito_positivo"] = fz.trimf(self.sentimento.universe, [7, 10, 10])

        # Definir regras

        regras = []

        # Cenários positivos
        regras.append(ctr.Rule(self.freqPP["presente"] & self.freqPN["ausente"], self.sentimento["positivo"]))
        regras.append(ctr.Rule(self.freqPP["presente"] & self.freqI["presente"], self.sentimento["muito_positivo"]))
        regras.append(ctr.Rule(self.freqPN["presente"] & self.freqNeg["presente"], self.sentimento["positivo"]))


        # Cenários neutros
        regras.append(ctr.Rule(self.freqPN["ausente"] & self.freqPP["ausente"], self.sentimento["neutro"]))
        regras.append(ctr.Rule(self.freqPN["presente"] & self.freqPP["presente"], self.sentimento["neutro"]))

        # Cenários negativos

        regras.append(ctr.Rule(self.freqPN["presente"] & self.freqPP["ausente"], self.sentimento["negativo"]))
        regras.append(ctr.Rule(self.freqPP["presente"] & self.freqNeg["presente"], self.sentimento["negativo"]))
        regras.append(ctr.Rule(self.freqPN["presente"] & self.freqI["presente"], self.sentimento["muito_negativo"]))

        self.ctrlSys = ctr.ControlSystem(regras)
        self.simulador = ctr.ControlSystemSimulation(self.ctrlSys)
    
    # Obtendo frequência das métricas
    def carregar_frase(self, frase):
        p_frase = frase.split(" ")
        self.frase = frase
        self.simulador.input["FP"] = 1 if len([p for p in p_frase if p in self.banco_palavras["positivas"]]) > 0 else 0
        self.simulador.input["FN"] = 1 if len([p for p in p_frase if p in self.banco_palavras["negativas"]]) > 0 else 0
        self.simulador.input["I"] = 1 if len([p for p in p_frase if p in self.banco_palavras["intensificadores"]]) > 0 else 0
        self.simulador.input["N"] = 1 if len([p for p in p_frase if p in self.banco_palavras["negacoes"]]) > 0 else 0

    
    # Obtendo grau de verdade
    def analisar(self):
        self.simulador.compute()
        self.grau_sentimento = self.simulador.output["sentimento"]
    
    # Classificando resultado
    def classificar(self):
        if self.grau_sentimento < 2.3:
            msg = "Muito Negativo"
        elif self.grau_sentimento > 2.3 and self.grau_sentimento < 3.5:
            msg = "Negativo"
        elif self.grau_sentimento > 3.5 and self.grau_sentimento < 5.1:
            msg = "Neutro"
        elif self.grau_sentimento > 5.1 and self.grau_sentimento < 7.5:
            msg = "Positivo"
        else:
            msg = "Muito Positivo"
        
        return msg

for frase in frases:
    fuzzy = Fuzzy(banco)
    fuzzy.carregar_frase(frase)
    fuzzy.analisar()
    print(f"{frase} -> {fuzzy.classificar()}")

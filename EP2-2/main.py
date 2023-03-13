import satisfacao_restricoes
import restricoes as r
import numpy as np
import time


variaveis = []
dominios = {}

analises = {
  "AN01": ["UV", "CG"],
  "AN02": ["CL", "EI"],
  "AN03": ["MC", "BA"],
  "AN04": ["EM"],
  "AN05": ["AM", "EI"],
  "AN06": ["CL", "UV"],
  "AN07": ["UV", "MC"],
  "AN08": ["CG"],
  "AN09": ["EI", "BA"],
  "AN10": ["EM", "CG"]
}

equipamentos_lab = set()


for analise, equipamentos in analises.items():
  for equipamento in equipamentos:
    variaveis.append(analise + equipamento)
    equipamentos_lab.add(equipamento)

for variavel in variaveis:
  dominios[variavel] = np.array([1, 2, 3, 4, 5, 6, 7, 8])

problema = satisfacao_restricoes.SatisfacaoRestricoes(variaveis=np.array(variaveis), dominios=dominios)


print("Configurando restrições...")
for analise in analises.keys():
  problema.adicionar_restricao(r.RestricaoAnaliseEmMaquinasSimultaneas(variaveis, analise))

for equipamento in equipamentos_lab:
  problema.adicionar_restricao(r.RestricaoUsoSimultaneoMaquina(variaveis, equipamento))

print("Restrições configuradas!")

print("Procurando solução...")
inicio = time.time()
resposta = problema.busca_backtracking()
fim = time.time()
print("Busca finalizada!")


if resposta is None:
  print("Nenhuma resposta encontrada")
else:
  turnos_utilizados = set(resposta.values())
  for turno in turnos_utilizados:
    print(f"Turno {turno}: {[analise for analise in resposta.keys() if resposta[analise] == turno]}")



print(f"{(fim - inicio):.4f}s em execução.") 
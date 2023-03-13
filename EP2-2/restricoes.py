from satisfacao_restricoes import Restricao


class RestricaoUsoSimultaneoMaquina(Restricao):

  def __init__(self, variaveis, maquina):
    super().__init__(variaveis)
    self.maquina = maquina

  def esta_satisfeita(self, atribuicao):
    for chave, valor in atribuicao.items():
      if chave[4:6] != self.maquina:
        continue

      equipamentos_em_uso = [x for x in atribuicao.keys() if(valor == atribuicao[x] and x[4:6] == self.maquina)]
      if len(equipamentos_em_uso) > 1:
        return False

    return True


class RestricaoAnaliseEmMaquinasSimultaneas(Restricao):
  def __init__(self, variaveis, analise): 
    super().__init__(variaveis)
    self.analise = analise

  def esta_satisfeita(self, atribuicao):
    for chave, valor in atribuicao.items():
      if chave[0:4] != self.analise:
        continue

      equipamentos_analise_no_turno = [x for x in atribuicao.keys() if(valor == atribuicao[x] and x[0:4] == self.analise)]
      if len(equipamentos_analise_no_turno) > 1:
        return False

    return True
  
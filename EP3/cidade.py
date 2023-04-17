class Cidade:
  def __init__(self, nome, peso=0, valor=0, tempo_roubo=0, item=None):
    self.peso = peso
    self.nome = nome
    self.valor = valor
    self.item = item
    self.tempo_roubo = tempo_roubo
    self.sigla = ''.join([palavra[0] for palavra in nome.split()])
  
  def __repr__(self):
    return f"{self.nome}"

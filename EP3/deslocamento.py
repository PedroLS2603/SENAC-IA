class Deslocamento:
    def __init__(self, origem, destino, tempo, valor):
        self.origem = origem
        self.destino = destino
        self.tempo = tempo
        self.custo = valor

    def __repr__(self) -> str:
      return f"{self.origem.nome} -> {self.destino.nome}"
    
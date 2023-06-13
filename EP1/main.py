from hanoi import Hanoi
from algoritmos import a_estrela, bfs, dfs, dijkstra


problema = Hanoi(3,5)
result_a_estrela = a_estrela.a_estrela(problema)
result_djikstra = dijkstra.dijkstra(problema)
print(f"A* -> {result_a_estrela}")
print(f"Djikstra -> {result_djikstra}")



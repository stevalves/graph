# Vanessa

import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

# carregar dataset
try:
    with open("dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("ERRO: O arquivo 'dataset.json' não foi encontrado.")
    exit()

# construir conjuntos de pessoas e gêneros
pessoas = set()
generos = set()

for item in data:
    pessoas.add(item["from"])
    generos.add(item["to"])

pessoas = sorted(list(pessoas))  # linhas da matriz
generos = sorted(list(generos))  # colunas da matriz

n_pessoas = len(pessoas)
n_generos = len(generos)

print(f"\n{'='*80}")
print(f" MATRIZ DE INCIDÊNCIA: {n_pessoas} Pessoas × {n_generos} Gêneros")
print(f"{'='*80}\n")

# construir matriz de incidência
# mapeamento: pessoa -> índice de linha
pessoa_idx = {p: i for i, p in enumerate(pessoas)}
# mapeamento: gênero -> índice de coluna
genero_idx = {g: i for i, g in enumerate(generos)}

# matriz de incidência: M[i, j] = peso da aresta (pessoa_i -> genero_j)
M = np.zeros((n_pessoas, n_generos), dtype=int)

for item in data:
    i = pessoa_idx[item["from"]]
    j = genero_idx[item["to"]]
    w = int(item.get("weight", 1))
    M[i, j] += w

print("Pessoas (linhas):", pessoas)
print("Gêneros (colunas):", generos)
print("\nMatriz de Incidência (M):\n", M)

# criar grafo de incidência (pessoas conectadas por gêneros em comum)
G = nx.Graph()

# adicionar nós de pessoas
for p in pessoas:
    G.add_node(p, type="pessoa")

# conectar pessoas que compartilham gêneros
# peso da aresta = número de gêneros em comum
for i in range(n_pessoas):
    for j in range(i + 1, n_pessoas):
        # calcular gêneros em comum
        generos_em_comum = 0
        for k in range(n_generos):
            if M[i, k] > 0 and M[j, k] > 0:
                generos_em_comum += min(M[i, k], M[j, k])
        
        # adicionar aresta se compartilham pelo menos um gênero
        if generos_em_comum > 0:
            G.add_edge(pessoas[i], pessoas[j], weight=generos_em_comum)

# visualizar grafo de incidência
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))

# Matriz de Incidência
ax1.imshow(M, cmap="YlGnBu", aspect="auto")
ax1.set_title("Matriz de Incidência (Pessoas × Gêneros)", fontsize=16, fontweight="bold")
ax1.set_xticks(np.arange(n_generos))
ax1.set_yticks(np.arange(n_pessoas))
ax1.set_xticklabels(generos, rotation=90, fontsize=10)
ax1.set_yticklabels(pessoas, fontsize=10)
ax1.set_xlabel("Gêneros", fontsize=12, fontweight="bold")
ax1.set_ylabel("Pessoas", fontsize=12, fontweight="bold")

# Anotar valores na matriz
for i in range(n_pessoas):
    for j in range(n_generos):
        text_color = "white" if M[i, j] > 0 else "gray"
        ax1.text(j, i, str(M[i, j]), ha="center", va="center",
                 color=text_color, fontsize=8, fontweight="bold")

# Grafo de Incidência
# layout spring para melhor visualização
pos = nx.spring_layout(G, k=1.5, iterations=300, seed=42)

# detectar comunidades para colorir
from networkx.algorithms import community
coms = list(community.greedy_modularity_communities(G))
node_to_community = {n: idx for idx, c in enumerate(coms) for n in c}
node_colors = [node_to_community[n] for n in G.nodes()]

# desenhar nós
nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.Set3,
                       node_size=1400, edgecolors="black",
                       linewidths=1.5, ax=ax2)

# desenhar arestas com largura proporcional ao peso
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, width=[w*0.5 for w in weights], alpha=0.6, ax=ax2)

# desenhar labels
nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax2)

# desenhar pesos das arestas
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax2)

ax2.set_title("Grafo de Incidência (Pessoas conectadas por gêneros em comum)", 
              fontsize=16, fontweight="bold")
ax2.axis("off")

plt.tight_layout()
plt.savefig("incidencia_grafo.png", dpi=200, bbox_inches="tight")
print("\n✓ Gráficos salvos em 'incidencia_grafo.png'")
plt.show()

# métricas topológicas 
print(f"\n{'='*80}")
print(" métricas topológicas do grafo de incidência")
print(f"{'='*80}\n")

# Vértices (V)
vertices = list(G.nodes())
num_vertices = G.number_of_nodes()
print(f"Vértices (V): {vertices}")
print(f"\nNúmero de Vértices (|V|): **{num_vertices}**")

# Arestas (E)
arestas = list(G.edges(data=True))
num_arestas = G.number_of_edges()
print(f"\nArestas (E): {arestas[:5]} ... (Mostrando as 5 primeiras)")
print(f"\nNúmero de Arestas (|E|): **{num_arestas}**")

# grau dos vértices
graus = dict(G.degree())
print(f"\nGraus dos Vértices (degree):")
for p in pessoas:
    print(f"  {p}: {graus[p]}")

# grau médio
grau_medio = np.mean(list(graus.values()))
print(f"\nGrau Médio (mean(degree)): **{grau_medio:.4f}**")

# pesos das arestas
pesos = nx.get_edge_attributes(G, "weight")
peso_total = sum(pesos.values())
peso_medio = np.mean(list(pesos.values()))
print(f"\nPeso Total das Arestas: **{peso_total}**")
print(f"Peso Médio das Arestas (força média de conexão): **{peso_medio:.4f}**")

# densidade da rede
densidade = nx.density(G)
print(f"\nDensidade da Rede (density): **{densidade:.4f}**")

print(f"\n{'='*80}\n")

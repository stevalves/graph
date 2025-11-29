# Rodrigo

import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community

def fix_collisions(pos, min_distance=0.35, max_passes=10):
    pos = {n: [xy[0], xy[1]] for n, xy in pos.items()}
    nodes = list(pos.keys())

    for _pass in range(max_passes):
        moved = False
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1, n2 = nodes[i], nodes[j]
                x1, y1 = pos[n1]
                x2, y2 = pos[n2]

                dx = x2 - x1
                dy = y2 - y1
                dist = (dx**2 + dy**2) ** 0.5

                if dist == 0:
                    dx, dy = 0.01, 0.01
                    dist = (dx**2 + dy**2) ** 0.5

                if dist < min_distance:
                    overlap = (min_distance - dist) / 2
                    nx_shift = (dx / dist) * overlap
                    ny_shift = (dy / dist) * overlap

                    pos[n1][0] -= nx_shift
                    pos[n1][1] -= ny_shift
                    pos[n2][0] += nx_shift
                    pos[n2][1] += ny_shift
                    moved = True

        if not moved:
            break

    return {n: (p[0], p[1]) for n, p in pos.items()}

try:
    with open("dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("ERRO: O arquivo 'dataset.json' não foi encontrado. Certifique-se de que ele está no mesmo diretório.")
    exit()

person_genres = {}

for item in data:
    pessoa = item["from"]
    genero = item["to"]
    w = int(item.get("weight", 1)) 

    if pessoa not in person_genres:
        person_genres[pessoa] = {}

    person_genres[pessoa][genero] = person_genres[pessoa].get(genero, 0) + w

DG = nx.DiGraph()

for item in data:
    src = item["from"]
    dst = item["to"]
    w = int(item.get("weight", 1))
    DG.add_edge(src, dst, weight=w)

people = list(person_genres.keys())
n = len(people)
sim_matrix = np.zeros((n, n), dtype=int)

for i in range(n):
    for j in range(n):
        if i == j: continue
        g1 = person_genres[people[i]]
        g2 = person_genres[people[j]]
        common = set(g1.keys()) & set(g2.keys())
        weight = sum(min(g1[g], g2[g]) for g in common) 
        sim_matrix[i, j] = weight

G = nx.Graph()
for p in people:
    G.add_node(p, type="pessoa")

for i in range(n):
    for j in range(i + 1, n):
        if sim_matrix[i, j] > 0:
            G.add_edge(people[i], people[j], weight=int(sim_matrix[i, j]))

DGS = nx.DiGraph()
for p in people:
    DGS.add_node(p, type="pessoa")

for i in range(n):
    for j in range(n):
        weight = int(sim_matrix[i, j])
        if weight > 0:
            DGS.add_edge(people[i], people[j], weight=weight)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(38, 12)) 

ax1.imshow(sim_matrix, cmap="Blues")
ax1.set_title("Matriz de Similaridade", fontsize=16)
ax1.set_xticks(np.arange(n))
ax1.set_yticks(np.arange(n))
ax1.set_xticklabels(people, rotation=90, fontsize=8)
ax1.set_yticklabels(people, fontsize=8)
for i in range(n):
    for j in range(n):
        ax1.text(j, i, str(sim_matrix[i, j]),
                 ha="center", va="center", color="black", fontsize=7)
plt.colorbar(ax1.images[0], ax=ax1)

pos_sim = nx.spring_layout(G, k=1.8, iterations=300, seed=42)
pos_sim = fix_collisions(pos_sim, min_distance=0.45, max_passes=15)
coms = list(community.greedy_modularity_communities(G))
node_to_community = {n: idx for idx, c in enumerate(coms) for n in c}
node_colors_sim = [node_to_community[n] for n in G.nodes()]

nx.draw_networkx_nodes(
    G, pos_sim, node_size=1400, node_color=node_colors_sim,
    cmap=plt.cm.Set3, edgecolors="black", linewidths=1.2, ax=ax2
)
nx.draw_networkx_edges(G, pos_sim, width=2, alpha=0.6, ax=ax2)
label_pos_sim = {n: (x, y - 0.06) for n, (x, y) in pos_sim.items()}
nx.draw_networkx_labels(G, label_pos_sim, font_size=10, font_weight="bold", ax=ax2)
nx.draw_networkx_edge_labels(
    G, pos_sim, edge_labels=nx.get_edge_attributes(G, "weight"),
    font_size=8, ax=ax2
)
ax2.set_title("Grafo de Similaridade (Não Direcionado)", fontsize=16)
ax2.axis("off")

pos_sim_dir = nx.spring_layout(DGS, k=1.3, iterations=300, seed=12)
pos_sim_dir = fix_collisions(pos_sim_dir, min_distance=0.45, max_passes=15)
int_sim_labels = {e: int(w) for e, w in nx.get_edge_attributes(DGS, "weight").items()}

nx.draw_networkx_nodes(
    DGS, pos_sim_dir, node_size=1400,
    node_color="#ffb3ba", edgecolors="black",
    linewidths=1.2, ax=ax3
)
nx.draw_networkx_edges(
    DGS, pos_sim_dir, width=2,
    arrows=True, arrowsize=22,
    connectionstyle="arc3,rad=0.15",
    ax=ax3
)
nx.draw_networkx_labels(DGS, pos_sim_dir, font_size=10, font_weight="bold", ax=ax3)
nx.draw_networkx_edge_labels(
    DGS, pos_sim_dir, edge_labels=int_sim_labels,
    font_size=8, ax=ax3
)
ax3.set_title("Grafo de Similaridade Direcional Ponderado", fontsize=16)
ax3.axis("off")


plt.tight_layout()
plt.show()

print("\n=========================================================================")
print(" MÉTRICAS TOPOLÓGICAS")
print("=========================================================================\n")

# V(grafo_sim) -> G.nodes()
vertices = G.nodes()
print(f"Vértices (V): {list(vertices)}")

# length(V(grafo_sim)) -> G.number_of_nodes()
num_vertices = G.number_of_nodes()
print(f"Número de Vértices (length(V)): **{num_vertices}**")

# E(grafo_sim) -> G.edges(data=True)
arestas = G.edges(data=True)
# Imprime apenas as 5 primeiras para evitar poluir a saída
print(f"Arestas (E): {list(arestas)[:5]} ... (Mostrando as 5 primeiras)") 

# ecount(grafo_sim) -> G.number_of_edges()
num_arestas = G.number_of_edges()
print(f"Número de Arestas (ecount): **{num_arestas}**")

# degree(grafo_sim) -> G.degree()
graus_dict = dict(G.degree())
print(f"Graus de Vértice (degree): {graus_dict}")

# mean(degree(grafo_sim)) -> Média dos graus
graus_list = list(dict(G.degree()).values())
grau_medio = np.mean(graus_list)
print(f"Grau Médio (mean(degree)): **{grau_medio:.4f}**")

# E(grafo_sim)$weight -> nx.get_edge_attributes(G, 'weight')
pesos_arestas_dict = nx.get_edge_attributes(G, 'weight')
print(f"Pesos das Arestas (E$weight): {pesos_arestas_dict}")

# mean(E(grafo_sim)$weight) -> Média dos pesos (Força de Conectividade Média)
pesos_list = list(pesos_arestas_dict.values())
if pesos_list:
    forca_media = np.mean(pesos_list)
    print(f"Força de Conectividade Média (mean(E$weight)): **{forca_media:.4f}**")
else:
    print("Força de Conectividade Média: **0** (Grafo sem arestas)")

# edge_density(grafo_sim, loops = FALSE) -> nx.density(G)
densidade_rede = nx.density(G)
print(f"Densidade da Rede (edge_density): **{densidade_rede:.4f}**")
# Guilherme

import pandas as pd
import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt

ARQUIVO_DATASET = 'dataset.json'

print("1. Carregando dados e construindo a Matriz de Incidência (Pessoa x Gênero)...")

try:
    df_raw = pd.read_json(ARQUIVO_DATASET)
    
    matriz_incidencia_df = df_raw.pivot_table(
        index='from', 
        columns='to', 
        values='weight', 
        fill_value=0
    )
    
    matriz_incidencia = matriz_incidencia_df.values
    nomes_pessoas = matriz_incidencia_df.index.tolist()
    nomes_generos = matriz_incidencia_df.columns.tolist()

    if matriz_incidencia.shape[0] < 10 or matriz_incidencia.shape[1] < 4:
         print(f"AVISO: O dataset tem {matriz_incidencia.shape[0]} pessoas e {matriz_incidencia.shape[1]} gêneros. O requisito é 10/4.")

except FileNotFoundError:
    print(f"ERRO: Arquivo '{ARQUIVO_DATASET}' não encontrado.")
    exit()
except Exception as e:
    print(f"ERRO ao processar o JSON: {e}")
    exit()
    
print(f"Matriz de Incidência (M) carregada: {matriz_incidencia.shape} (Pessoas x Gêneros)")

# --- 2. CALCULAR MATRIZ DE COOCORRÊNCIA (C = M^T * M) ---
print("\n2. Calculando a Matriz de Coocorrência (C) entre GÊNEROS...")

matriz_coocorrencia = np.dot(matriz_incidencia.T, matriz_incidencia)

df_coocorrencia = pd.DataFrame(
    matriz_coocorrencia, 
    index=nomes_generos, 
    columns=nomes_generos
)

print("\n--- Matriz de Coocorrência de Gêneros (Contagem de Pessoas Compartilhadas) ---")
print(df_coocorrencia)

# --- 3. CRIAR O GRAFO DE COOCORRÊNCIA (Nós = Gêneros) ---
print("\n3. Criando o Grafo de Coocorrência...")

G_coocorrencia = nx.Graph()
G_coocorrencia.add_nodes_from(nomes_generos)

num_generos = len(nomes_generos)
for i in range(num_generos):
    for j in range(i + 1, num_generos): 
        peso = matriz_coocorrencia[i, j]
        
        if peso > 0:
            genero_i = nomes_generos[i]
            genero_j = nomes_generos[j]
            G_coocorrencia.add_edge(genero_i, genero_j, weight=peso)

print(f"Grafo de Coocorrência criado com {G_coocorrencia.number_of_nodes()} nós (Gêneros) e {G_coocorrencia.number_of_edges()} arestas.")

# --- 4. CALCULAR MÉTRICAS TOPOLÓGICAS ---
print("\n4. Calculando Métricas Topológicas para o Grafo de Coocorrência (Gêneros)...")

densidade = nx.density(G_coocorrencia)
coeficiente_aglomeracao = nx.average_clustering(G_coocorrencia, weight='weight')
try:
    diametro = nx.diameter(G_coocorrencia)
except nx.NetworkXError:
    diametro = "Não Conexo"

grau = dict(G_coocorrencia.degree())
grau_ponderado = dict(G_coocorrencia.degree(weight='weight'))
centralidade_intermediacao = nx.betweenness_centrality(G_coocorrencia, weight='weight')
centralidade_autovetor = nx.eigenvector_centrality(G_coocorrencia, weight='weight', max_iter=1000)

metrics_df = pd.DataFrame({
    'Grau (Degree)': grau,
    'Grau Ponderado (Strength)': grau_ponderado,
    'Intermediação (Betweenness)': centralidade_intermediacao,
    'Autovetor (Eigenvector)': centralidade_autovetor
}).T 

print("\n  - Métricas Globais:")
print(f"    Densidade do Grafo: {densidade:.4f}")
print(f"    Coeficiente de Aglomeração Médio (Ponderado): {coeficiente_aglomeracao:.4f}")
print(f"    Diâmetro do Grafo: {diametro}")

print("\n  - Métricas Locais por Gênero (Top 5 por Grau Ponderado):")
print(metrics_df.round(4).T.sort_values('Grau Ponderado (Strength)', ascending=False).head())

print("\n--- FIM DO PROCESSO ---")

# --- 5. VISUALIZAÇÃO (HEATMAP E GRAFO) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# PLOTAGEM DA MATRIZ (HEATMAP)
im = ax1.imshow(matriz_coocorrencia, cmap="Blues")
ax1.set_title("Matriz de Coocorrência entre Gêneros (Heatmap)", fontsize=14)

n = len(nomes_generos)
ax1.set_xticks(np.arange(n))
ax1.set_yticks(np.arange(n))
ax1.set_xticklabels(nomes_generos, rotation=90, fontsize=9)
ax1.set_yticklabels(nomes_generos, fontsize=9)

for i in range(n):
    for j in range(n):
        ax1.text(j, i, str(matriz_coocorrencia[i, j]),
                 ha="center", va="center", color="black", fontsize=8)

plt.colorbar(im, ax=ax1, label='Contagem de Pessoas Compartilhando o Par de Gêneros')

# PLOTAGEM DO GRAFO
pos = nx.spring_layout(G_coocorrencia, k=0.5, iterations=50, seed=42) 
node_size = [v * 100 for v in grau_ponderado.values()] 
edge_widths = [d['weight'] * 0.4 for (u, v, d) in G_coocorrencia.edges(data=True)]

nx.draw_networkx_nodes(G_coocorrencia, pos, node_size=node_size, node_color='lightblue', edgecolors='black', ax=ax2)
nx.draw_networkx_edges(G_coocorrencia, pos, width=edge_widths, alpha=0.7, edge_color='gray', ax=ax2)
nx.draw_networkx_labels(G_coocorrencia, pos, font_size=10, font_weight='bold', ax=ax2)

edge_labels = nx.get_edge_attributes(G_coocorrencia, 'weight')
nx.draw_networkx_edge_labels(G_coocorrencia, pos, edge_labels=edge_labels, font_size=8, ax=ax2)

ax2.set_title("Grafo de Coocorrência entre Gêneros (Peso = Compartilhamento)", fontsize=14)
ax2.axis('off')

plt.tight_layout()
plt.show()
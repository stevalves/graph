import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Guilherme
def gerar_coocorrencia(data, pessoas, generos):
    # Obtém quantidade de pessoas e gêneros do dataset
    quantidade_pessoas = len(pessoas)
    quantidade_generos = len(generos)

    # Cria mapeamento nome -> índice para acesso rápido à matriz
    indice_por_pessoa = {pessoa: indice for indice, pessoa in enumerate(pessoas)}
    indice_por_genero = {genero: indice for indice, genero in enumerate(generos)}

    # Inicializa matriz de incidência (pessoas × gêneros)
    matriz_incidencia = np.zeros((quantidade_pessoas, quantidade_generos), dtype=int)

    # Preenche matriz com pesos das relações pessoa-gênero
    for relacao in data:
        nome_pessoa = relacao["from"]
        nome_genero = relacao["to"]
        peso_relacao = int(relacao.get("weight", 1))

        indice_pessoa = indice_por_pessoa[nome_pessoa]
        indice_genero = indice_por_genero[nome_genero]

        # Incrementa célula com peso da relação
        matriz_incidencia[indice_pessoa, indice_genero] += peso_relacao

    # Calcula matriz de coocorrência: quantas pessoas compartilham cada par de gêneros
    matriz_coocorrencia = matriz_incidencia.T @ matriz_incidencia  
    # Remove diagonal principal (gênero com ele mesmo)
    np.fill_diagonal(matriz_coocorrencia, 0)

    # Cria grafo onde nós são gêneros e arestas são coocorrências
    grafo_coocorrencia = nx.Graph()

    # Adiciona cada gênero como nó do grafo
    for nome_genero in generos:
        grafo_coocorrencia.add_node(nome_genero, tipo="genero")

    # Conecta gêneros que aparecem juntos com peso de coocorrência
    quantidade_generos = len(generos)
    for indice_genero_origem, genero_origem in enumerate(generos):
        for indice_genero_destino in range(indice_genero_origem + 1, quantidade_generos):
            genero_destino = generos[indice_genero_destino]
            peso_coocorrencia = int(matriz_coocorrencia[indice_genero_origem, indice_genero_destino])

            # Adiciona aresta apenas se houver coocorrência
            if peso_coocorrencia > 0:
                grafo_coocorrencia.add_edge(
                    genero_origem,
                    genero_destino,
                    weight=peso_coocorrencia
                )

    # Desenha matriz de coocorrência em um eixo matplotlib
    def _desenhar_matriz(ax):
        ax.set_title("Matriz de Coocorrência entre Gêneros")
        # Cria heatmap com colormap azul
        mapa = ax.imshow(matriz_coocorrencia, cmap="Blues", aspect="auto")
        ax.set_xticks(np.arange(quantidade_generos))
        ax.set_yticks(np.arange(quantidade_generos))
        ax.set_xticklabels(generos, rotation=90)
        ax.set_yticklabels(generos)
        ax.set_xlabel("Gênero destino")
        ax.set_ylabel("Gênero origem")

        # Adiciona valores numéricos nas células da matriz
        for indice_genero_origem in range(quantidade_generos):
            for indice_genero_destino in range(quantidade_generos):
                valor_celula = matriz_coocorrencia[indice_genero_origem, indice_genero_destino]
                ax.text(
                    indice_genero_destino,
                    indice_genero_origem,
                    str(int(valor_celula)),
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                )

        return mapa 

    # Desenha grafo de coocorrência em um eixo matplotlib
    def _desenhar_grafo(ax):
        # Tamanho dos nós proporcional ao grau ponderado (força)
        graus_ponderados = dict(grafo_coocorrencia.degree(weight="weight"))
        tamanhos_nos = [graus_ponderados.get(genero, 0) * 200 for genero in grafo_coocorrencia.nodes()]

        # Largura das arestas proporcional ao peso de coocorrência
        larguras_arestas = [
            dados_aresta["weight"] * 0.4
            for (_, _, dados_aresta) in grafo_coocorrencia.edges(data=True)
        ]

        # Calcula posição dos nós usando algoritmo spring layout
        posicao_nos = nx.spring_layout(grafo_coocorrencia, k=0.7, iterations=100, seed=42)

        # Desenha nós com tamanho e cores variáveis
        nx.draw_networkx_nodes(
            grafo_coocorrencia,
            posicao_nos,
            node_size=tamanhos_nos,
            node_color="lightblue",
            edgecolors="black",
            ax=ax,
        )

        # Desenha arestas com largura proporcional ao peso
        nx.draw_networkx_edges(
            grafo_coocorrencia,
            posicao_nos,
            width=larguras_arestas,
            alpha=0.7,
            edge_color="gray",
            ax=ax,
        )

        # Adiciona rótulos aos nós
        nx.draw_networkx_labels(
            grafo_coocorrencia,
            posicao_nos,
            font_size=10,
            font_weight="bold",
            ax=ax,
        )

        # Adiciona pesos das arestas como rótulos
        rotulos_arestas = nx.get_edge_attributes(grafo_coocorrencia, "weight")
        nx.draw_networkx_edge_labels(
            grafo_coocorrencia,
            posicao_nos,
            edge_labels=rotulos_arestas,
            font_size=8,
            ax=ax,
        )

        ax.set_title("Grafo de Coocorrência entre Gêneros\n(Peso = pessoas que compartilham o par)")
        ax.axis("off")

    # Exibe apenas a matriz de coocorrência
    def gerar_matriz():
        figura, eixo_matriz = plt.subplots(1, 1, figsize=(10, 8))
        mapa = _desenhar_matriz(eixo_matriz)
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)

        plt.tight_layout()
        plt.show()

    # Exibe apenas o grafo de coocorrência
    def gerar_grafo():
        _, eixo_grafo = plt.subplots(1, 1, figsize=(10, 8))
        _desenhar_grafo(eixo_grafo)
        plt.tight_layout()
        plt.show()

    # Exibe matriz e grafo lado a lado
    def gerar_matriz_e_grafo():
        figura, (eixo_matriz, eixo_grafo) = plt.subplots(1, 2, figsize=(20, 8))

        mapa = _desenhar_matriz(eixo_matriz)
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)

        _desenhar_grafo(eixo_grafo)

        plt.tight_layout()
        plt.show()

    # Calcula e exibe métricas topológicas do grafo
    def calcular_metricas(caminho_arquivo="metricas_coocorrencia.txt"):
        linhas_relatorio = []

        linhas_relatorio.append("MÉTRICAS TOPOLOGICAS - GRAFO DE COOCORRÊNCIA (GÊNEROS) \n")

        # Extrai vértices e conta número total
        vertices = list(grafo_coocorrencia.nodes())
        quantidade_vertices = grafo_coocorrencia.number_of_nodes()
        # Extrai arestas com dados e conta número total
        arestas = list(grafo_coocorrencia.edges(data=True))
        quantidade_arestas = grafo_coocorrencia.number_of_edges()

        linhas_relatorio.append("Vértices (gêneros):")
        linhas_relatorio.append(str(vertices))
        linhas_relatorio.append(f"\nNúmero de vértices (|V|): {quantidade_vertices}\n")

        linhas_relatorio.append("Algumas arestas (primeiras 5):")
        linhas_relatorio.append(str(arestas[:5]))
        linhas_relatorio.append(f"Número de arestas (|E|): {quantidade_arestas}\n")

        # Obtém grau simples e ponderado de cada gênero
        graus = dict(grafo_coocorrencia.degree())
        graus_ponderados = dict(grafo_coocorrencia.degree(weight="weight"))

        linhas_relatorio.append("Grau (degree) por gênero:")
        for genero, grau in graus.items():
            linhas_relatorio.append(f"  {genero}: {grau}")

        linhas_relatorio.append("\nGrau ponderado (strength) por gênero:")
        for genero, grau_p in graus_ponderados.items():
            linhas_relatorio.append(f"  {genero}: {grau_p}")

        # Calcula média dos graus
        grau_medio = float(np.mean(list(graus.values()))) if graus else 0.0
        grau_ponderado_medio = float(np.mean(list(graus_ponderados.values()))) if graus_ponderados else 0.0

        linhas_relatorio.append(f"\nGrau médio: {grau_medio:.4f}")
        linhas_relatorio.append(f"Grau ponderado médio: {grau_ponderado_medio:.4f}\n")

        # Calcula centralidades usando pesos das arestas
        centralidade_intermediacao = nx.betweenness_centrality(grafo_coocorrencia, weight="weight")
        centralidade_autovetor = nx.eigenvector_centrality(grafo_coocorrencia, weight="weight", max_iter=1000)

        linhas_relatorio.append("Centralidade de intermediação (betweenness):")
        for genero, valor in centralidade_intermediacao.items():
            linhas_relatorio.append(f"  {genero}: {valor:.4f}")

        linhas_relatorio.append("\nCentralidade de autovetor (eigenvector):")
        for genero, valor in centralidade_autovetor.items():
            linhas_relatorio.append(f"  {genero}: {valor:.4f}")

        # Calcula métricas globais do grafo
        densidade = nx.density(grafo_coocorrencia)
        coeficiente_aglomeracao = nx.average_clustering(grafo_coocorrencia, weight="weight")

        # Tenta calcular diâmetro (falha se grafo não é conexo)
        try:
            diametro = nx.diameter(grafo_coocorrencia)
        except nx.NetworkXError:
            diametro = "Não conexo"

        linhas_relatorio.append("\nMétricas globais:")
        linhas_relatorio.append(f"  Densidade do grafo: {densidade:.4f}")
        linhas_relatorio.append(f"  Coeficiente de aglomeração médio (ponderado): {coeficiente_aglomeracao:.4f}")
        linhas_relatorio.append(f"  Diâmetro do grafo: {diametro}")

        # Grava métricas em arquivo
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas_relatorio))

    # Retorna tupla de funções para o menu chamar
    return gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas

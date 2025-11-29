import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Rodrigo
def gerar_similaridade(data, pessoas, generos):
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

    # Calcula matriz de similaridade: quantos gêneros pessoas compartilham
    matriz_similaridade = matriz_incidencia @ matriz_incidencia.T
    # Remove diagonal principal (pessoa com ela mesma)
    np.fill_diagonal(matriz_similaridade, 0)

    # Cria grafo onde nós são pessoas e arestas são similaridades
    grafo_similaridade = nx.Graph()

    # Adiciona cada pessoa como nó do grafo
    for nome_pessoa in pessoas:
        grafo_similaridade.add_node(nome_pessoa, tipo="pessoa")

    # Conecta pessoas que compartilham gêneros com peso de similaridade
    quantidade_pessoas = len(pessoas)
    for indice_pessoa_origem, pessoa_origem in enumerate(pessoas):
        for indice_pessoa_destino in range(indice_pessoa_origem + 1, quantidade_pessoas):
            pessoa_destino = pessoas[indice_pessoa_destino]
            peso_similaridade = int(matriz_similaridade[indice_pessoa_origem, indice_pessoa_destino])

            # Adiciona aresta apenas se houver similaridade
            if peso_similaridade > 0:
                grafo_similaridade.add_edge(
                    pessoa_origem,
                    pessoa_destino,
                    weight=peso_similaridade
                )

    # Desenha matriz de similaridade em um eixo matplotlib
    def _desenhar_matriz(ax):
        ax.set_title("Matriz de Similaridade entre Pessoas")
        # Cria heatmap com colormap verde
        mapa = ax.imshow(matriz_similaridade, cmap="Greens", aspect="auto")
        ax.set_xticks(np.arange(quantidade_pessoas))
        ax.set_yticks(np.arange(quantidade_pessoas))
        ax.set_xticklabels(pessoas, rotation=90)
        ax.set_yticklabels(pessoas)
        ax.set_xlabel("Pessoa destino")
        ax.set_ylabel("Pessoa origem")

        # Adiciona valores numéricos nas células da matriz
        for indice_pessoa_origem in range(quantidade_pessoas):
            for indice_pessoa_destino in range(quantidade_pessoas):
                valor_celula = matriz_similaridade[indice_pessoa_origem, indice_pessoa_destino]
                ax.text(
                    indice_pessoa_destino,
                    indice_pessoa_origem,
                    str(int(valor_celula)),
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                )

        return mapa

    # Desenha grafo de similaridade em um eixo matplotlib
    def _desenhar_grafo(ax):
        # Tamanho dos nós proporcional ao grau ponderado (força)
        graus_ponderados = dict(grafo_similaridade.degree(weight="weight"))
        tamanhos_nos = [graus_ponderados.get(pessoa, 0) * 200 for pessoa in grafo_similaridade.nodes()]

        # Largura das arestas proporcional ao peso de similaridade
        larguras_arestas = [
            dados_aresta["weight"] * 0.4
            for (_, _, dados_aresta) in grafo_similaridade.edges(data=True)
        ]

        # Calcula posição dos nós usando algoritmo spring layout
        posicao_nos = nx.spring_layout(grafo_similaridade, k=0.7, iterations=100, seed=42)

        # Desenha nós com tamanho e cores variáveis
        nx.draw_networkx_nodes(
            grafo_similaridade,
            posicao_nos,
            node_size=tamanhos_nos,
            node_color="lightgreen",
            edgecolors="black",
            ax=ax,
        )

        # Desenha arestas com largura proporcional ao peso
        nx.draw_networkx_edges(
            grafo_similaridade,
            posicao_nos,
            width=larguras_arestas,
            alpha=0.7,
            edge_color="gray",
            ax=ax,
        )

        # Adiciona rótulos aos nós
        nx.draw_networkx_labels(
            grafo_similaridade,
            posicao_nos,
            font_size=10,
            font_weight="bold",
            ax=ax,
        )

        # Adiciona pesos das arestas como rótulos
        rotulos_arestas = nx.get_edge_attributes(grafo_similaridade, "weight")
        nx.draw_networkx_edge_labels(
            grafo_similaridade,
            posicao_nos,
            edge_labels=rotulos_arestas,
            font_size=8,
            ax=ax,
        )

        ax.set_title("Grafo de Similaridade entre Pessoas\n(Peso = gêneros que compartilham)")
        ax.axis("off")

    # Exibe apenas a matriz de similaridade
    def gerar_matriz():
        figura, eixo_matriz = plt.subplots(1, 1, figsize=(10, 8))
        mapa = _desenhar_matriz(eixo_matriz)
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)

        plt.tight_layout()
        plt.show()

    # Exibe apenas o grafo de similaridade
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
    def calcular_metricas(caminho_arquivo="metricas_similaridade.txt"):
        linhas_relatorio = []

        linhas_relatorio.append("MÉTRICAS TOPOLOGICAS - GRAFO DE SIMILARIDADE (PESSOAS) \n")

        # Extrai vértices e conta número total
        vertices = list(grafo_similaridade.nodes())
        quantidade_vertices = grafo_similaridade.number_of_nodes()
        # Extrai arestas com dados e conta número total
        arestas = list(grafo_similaridade.edges(data=True))
        quantidade_arestas = grafo_similaridade.number_of_edges()

        linhas_relatorio.append("Vértices (pessoas):")
        linhas_relatorio.append(str(vertices))
        linhas_relatorio.append(f"\nNúmero de vértices (|V|): {quantidade_vertices}\n")

        linhas_relatorio.append("Algumas arestas (primeiras 5):")
        linhas_relatorio.append(str(arestas[:5]))
        linhas_relatorio.append(f"Número de arestas (|E|): {quantidade_arestas}\n")

        # Obtém grau simples e ponderado de cada pessoa
        graus = dict(grafo_similaridade.degree())
        graus_ponderados = dict(grafo_similaridade.degree(weight="weight"))

        linhas_relatorio.append("Grau (degree) por pessoa:")
        for pessoa, grau in graus.items():
            linhas_relatorio.append(f"  {pessoa}: {grau}")

        linhas_relatorio.append("\nGrau ponderado (strength) por pessoa:")
        for pessoa, grau_p in graus_ponderados.items():
            linhas_relatorio.append(f"  {pessoa}: {grau_p}")

        # Calcula média dos graus
        grau_medio = float(np.mean(list(graus.values()))) if graus else 0.0
        grau_ponderado_medio = float(np.mean(list(graus_ponderados.values()))) if graus_ponderados else 0.0

        linhas_relatorio.append(f"\nGrau médio: {grau_medio:.4f}")
        linhas_relatorio.append(f"Grau ponderado médio: {grau_ponderado_medio:.4f}\n")

        # Calcula centralidades usando pesos das arestas
        centralidade_intermediacao = nx.betweenness_centrality(grafo_similaridade, weight="weight")
        centralidade_autovetor = nx.eigenvector_centrality(grafo_similaridade, weight="weight", max_iter=1000)

        linhas_relatorio.append("Centralidade de intermediação (betweenness):")
        for pessoa, valor in centralidade_intermediacao.items():
            linhas_relatorio.append(f"  {pessoa}: {valor:.4f}")

        linhas_relatorio.append("\nCentralidade de autovetor (eigenvector):")
        for pessoa, valor in centralidade_autovetor.items():
            linhas_relatorio.append(f"  {pessoa}: {valor:.4f}")

        # Calcula métricas globais do grafo
        densidade = nx.density(grafo_similaridade)
        coeficiente_aglomeracao = nx.average_clustering(grafo_similaridade, weight="weight")

        # Tenta calcular diâmetro (falha se grafo não é conexo)
        try:
            diametro = nx.diameter(grafo_similaridade)
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

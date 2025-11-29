import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Vanessa
def gerar_incidencia(data, pessoas, generos):
    # Obtém quantidade de pessoas e gêneros do dataset
    quantidade_pessoas = len(pessoas)
    quantidade_generos = len(generos)

    # Cria mapeamento nome -> índice para rápido acesso à matriz
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

    # Cria grafo bipartido com nós de pessoas e gêneros
    grafo_incidencia = nx.Graph()

    # Adiciona nós de pessoas com atributo de tipo
    for nome_pessoa in pessoas:
        grafo_incidencia.add_node(
            nome_pessoa,
            tipo="pessoa",
            bipartite=0
        )

    # Adiciona nós de gêneros com atributo de tipo
    for nome_genero in generos:
        grafo_incidencia.add_node(
            nome_genero,
            tipo="genero",
            bipartite=1
        )

    # Conecta pessoas a gêneros com peso baseado na matriz
    for indice_pessoa, nome_pessoa in enumerate(pessoas):
        for indice_genero, nome_genero in enumerate(generos):
            peso_conexao = matriz_incidencia[indice_pessoa, indice_genero]
            # Adiciona aresta apenas se houver peso positivo
            if peso_conexao > 0:
                grafo_incidencia.add_edge(
                    nome_pessoa,
                    nome_genero,
                    weight=int(peso_conexao)
                )

    # Desenha matriz de incidência em um eixo matplotlib
    def _desenhar_matriz(ax):
        ax.set_title("Matriz de Incidência (Pessoas e Gêneros)")
        # Cria heatmap com colormap amarelo-verde-azul
        mapa = ax.imshow(matriz_incidencia, cmap="YlGnBu", aspect="auto")
        ax.set_xticks(np.arange(quantidade_generos))
        ax.set_yticks(np.arange(quantidade_pessoas))
        ax.set_xticklabels(generos, rotation=45, ha="right")
        ax.set_yticklabels(pessoas)
        ax.set_xlabel("Gêneros")
        ax.set_ylabel("Pessoas")

        # Adiciona valores numéricos nas células da matriz
        for indice_pessoa in range(quantidade_pessoas):
            for indice_genero in range(quantidade_generos):
                valor_celula = matriz_incidencia[indice_pessoa, indice_genero]
                cor_texto = "white" if valor_celula > 0 else "gray"
                ax.text(
                    indice_genero,
                    indice_pessoa,
                    str(valor_celula),
                    ha="center",
                    va="center",
                    color=cor_texto,
                    fontsize=8,
                    fontweight="bold",
                )

        return mapa

    # Desenha grafo de incidência em um eixo matplotlib
    def _desenhar_grafo(ax):
        # Calcula posição dos nós usando algoritmo spring layout
        posicao_nos = nx.spring_layout(grafo_incidencia, seed=42)

        # Extrai pesos das arestas para ajustar largura das linhas
        pesos_arestas = [
            dados_aresta["weight"]
            for (_, _, dados_aresta) in grafo_incidencia.edges(data=True)
        ]

        # Desenha grafo com nós azuis e arestas cinzas
        nx.draw(
            grafo_incidencia,
            posicao_nos,
            with_labels=True,
            node_size=1000,
            node_color="#AED6F1",
            edge_color="#34495E",
            width=[peso for peso in pesos_arestas],
            font_size=9,
            ax=ax,
        )

        ax.set_title("Grafo de Incidência (Pessoas e Gêneros)")
        ax.axis("off")

    # Exibe apenas a matriz de incidência
    def gerar_matriz():
        figura, eixo_matriz = plt.subplots(1, 1, figsize=(10, 8))
        mapa = _desenhar_matriz(eixo_matriz)
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)

        plt.tight_layout()
        plt.show()

    # Exibe apenas o grafo de incidência
    def gerar_grafo():
        _, eixo_grafo = plt.subplots(1, 1, figsize=(10, 8))
        _desenhar_grafo(eixo_grafo)

        plt.tight_layout()
        plt.show()

    # Exibe matriz e grafo lado a lado
    def gerar_matriz_e_grafo():
        figura, (eixo_matriz, eixo_grafo) = plt.subplots(1, 2, figsize=(18, 8))

        mapa = _desenhar_matriz(eixo_matriz)
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)

        _desenhar_grafo(eixo_grafo)

        plt.tight_layout()
        plt.show()

    # Calcula e exibe métricas topológicas do grafo
    def calcular_metricas(caminho_arquivo="metricas_incidencia.txt"):
        linhas_relatorio = []

        linhas_relatorio.append("MÉTRICAS TOPOLOGICAS - GRAFO DE INCIDÊNCIA (PESSOAS E GÊNEROS) \n")

        # Extrai vértices e conta número total
        vertices = list(grafo_incidencia.nodes())
        quantidade_vertices = grafo_incidencia.number_of_nodes()
        # Extrai arestas com dados e conta número total
        arestas = list(grafo_incidencia.edges(data=True))
        quantidade_arestas = grafo_incidencia.number_of_edges()

        linhas_relatorio.append("Vértices (nós):")
        linhas_relatorio.append(str(vertices))
        linhas_relatorio.append(f"\nNúmero de vértices (|V|): {quantidade_vertices}\n")

        linhas_relatorio.append("Algumas arestas (primeiras 5):")
        linhas_relatorio.append(str(arestas[:5]))
        linhas_relatorio.append(f"Número de arestas (|E|): {quantidade_arestas}\n")

        # Obtém grau de cada vértice (número de conexões)
        graus_vertices = dict(grafo_incidencia.degree())
        linhas_relatorio.append("Graus dos vértices (degree):")
        for nome_vertice, grau_vertice in graus_vertices.items():
            linhas_relatorio.append(f"  {nome_vertice}: {grau_vertice}")
        # Calcula média dos graus
        grau_medio = float(np.mean(list(graus_vertices.values()))) if graus_vertices else 0.0
        linhas_relatorio.append(f"\nGrau médio: {grau_medio:.4f}\n")

        # Extrai pesos de todas as arestas
        pesos_dict = nx.get_edge_attributes(grafo_incidencia, "weight")
        pesos_valores = list(pesos_dict.values())
        # Calcula soma e média dos pesos
        peso_total = sum(pesos_valores) if pesos_valores else 0
        peso_medio = float(np.mean(pesos_valores)) if pesos_valores else 0.0

        linhas_relatorio.append("Pesos das arestas (weight):")
        linhas_relatorio.append(str(pesos_dict))
        linhas_relatorio.append(f"Peso total das arestas: {peso_total}")
        linhas_relatorio.append(f"Peso médio das arestas: {peso_medio:.4f}\n")

        # Calcula densidade (proporção de arestas existentes)
        densidade = nx.density(grafo_incidencia)
        linhas_relatorio.append(f"Densidade da rede: {densidade:.4f}")

        # Grava métricas em arquivo
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas_relatorio))

    # Retorna tupla de funções para o menu chamar
    return gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas

import numpy as np  # Importa NumPy para operações com matrizes
import networkx as nx  # Importa NetworkX para trabalhar com grafos
import matplotlib.pyplot as plt  # Importa Matplotlib para criar gráficos

# Vanessa - Responsável pelo módulo de incidência
def gerar_incidencia(data, pessoas, generos):  # Define função principal que recebe dados, lista de pessoas e lista de gêneros
    # Obtém quantidade de pessoas e gêneros do dataset
    quantidade_pessoas = len(pessoas)  # Conta quantas pessoas existem
    quantidade_generos = len(generos)  # Conta quantos gêneros existem

    # Cria mapeamento nome -> índice para rápido acesso à matriz
    indice_por_pessoa = {pessoa: indice for indice, pessoa in enumerate(pessoas)}  # Dicionário que mapeia nome da pessoa para seu índice numérico
    indice_por_genero = {genero: indice for indice, genero in enumerate(generos)}  # Dicionário que mapeia nome do gênero para seu índice numérico

    # Inicializa matriz de incidência (pessoas × gêneros)
    matriz_incidencia = np.zeros((quantidade_pessoas, quantidade_generos), dtype=int)  # Cria matriz zerada com linhas=pessoas e colunas=gêneros

    # Preenche matriz com pesos das relações pessoa-gênero
    for relacao in data:  # Loop que percorre cada relação no dataset
        nome_pessoa = relacao["from"]  # Pega o nome da pessoa desta relação
        nome_genero = relacao["to"]  # Pega o nome do gênero desta relação
        peso_relacao = int(relacao.get("weight", 1))  # Pega o peso da relação (ou 1 se não existir)

        indice_pessoa = indice_por_pessoa[nome_pessoa]  # Busca o índice da linha correspondente a esta pessoa
        indice_genero = indice_por_genero[nome_genero]  # Busca o índice da coluna correspondente a este gênero

        # Incrementa célula com peso da relação
        matriz_incidencia[indice_pessoa, indice_genero] += peso_relacao  # Adiciona o peso na célula [pessoa, gênero]

    # Cria grafo bipartido com nós de pessoas e gêneros
    grafo_incidencia = nx.Graph()  # Cria um grafo vazio não-direcionado

    # Adiciona nós de pessoas com atributo de tipo
    for nome_pessoa in pessoas:  # Loop que percorre cada pessoa
        grafo_incidencia.add_node(  # Adiciona um nó (vértice) ao grafo
            nome_pessoa,  # Nome do nó
            tipo="pessoa",  # Atributo indicando que é uma pessoa
            bipartite=0  # Atributo indicando grupo 0 do grafo bipartido
        )

    # Adiciona nós de gêneros com atributo de tipo
    for nome_genero in generos:  # Loop que percorre cada gênero
        grafo_incidencia.add_node(  # Adiciona um nó (vértice) ao grafo
            nome_genero,  # Nome do nó
            tipo="genero",  # Atributo indicando que é um gênero
            bipartite=1  # Atributo indicando grupo 1 do grafo bipartido
        )

    # Conecta pessoas a gêneros com peso baseado na matriz
    for indice_pessoa, nome_pessoa in enumerate(pessoas):  # Loop que percorre pessoas com seus índices
        for indice_genero, nome_genero in enumerate(generos):  # Loop aninhado que percorre gêneros com seus índices
            peso_conexao = matriz_incidencia[indice_pessoa, indice_genero]  # Pega o valor da matriz nesta posição
            # Adiciona aresta apenas se houver peso positivo
            if peso_conexao > 0:  # Se houver relação entre pessoa e gênero
                grafo_incidencia.add_edge(  # Adiciona aresta (conexão) ao grafo
                    nome_pessoa,  # Nó de origem (pessoa)
                    nome_genero,  # Nó de destino (gênero)
                    weight=int(peso_conexao)  # Peso da aresta
                )

    # Desenha matriz de incidência em um eixo matplotlib
    def _desenhar_matriz(ax):  # Define função interna para desenhar matriz
        ax.set_title("Matriz de Incidência (Pessoas e Gêneros)")  # Define título do gráfico
        # Cria heatmap com colormap amarelo-verde-azul
        mapa = ax.imshow(matriz_incidencia, cmap="YlGnBu", aspect="auto")  # Cria mapa de calor da matriz
        ax.set_xticks(np.arange(quantidade_generos))  # Define posições das marcações no eixo X
        ax.set_yticks(np.arange(quantidade_pessoas))  # Define posições das marcações no eixo Y
        ax.set_xticklabels(generos, rotation=45, ha="right")  # Define rótulos do eixo X (gêneros) rotacionados 45°
        ax.set_yticklabels(pessoas)  # Define rótulos do eixo Y (pessoas)
        ax.set_xlabel("Gêneros")  # Define texto do eixo X
        ax.set_ylabel("Pessoas")  # Define texto do eixo Y

        # Adiciona valores numéricos nas células da matriz
        for indice_pessoa in range(quantidade_pessoas):  # Loop que percorre cada linha (pessoa)
            for indice_genero in range(quantidade_generos):  # Loop aninhado que percorre cada coluna (gênero)
                valor_celula = matriz_incidencia[indice_pessoa, indice_genero]  # Pega valor da célula atual
                cor_texto = "white" if valor_celula > 0 else "gray"  # Define cor do texto: branco se tem valor, cinza se zero
                ax.text(  # Adiciona texto no gráfico
                    indice_genero,  # Posição X (coluna)
                    indice_pessoa,  # Posição Y (linha)
                    str(valor_celula),  # Texto a exibir (valor convertido para string)
                    ha="center",  # Alinhamento horizontal centralizado
                    va="center",  # Alinhamento vertical centralizado
                    color=cor_texto,  # Cor do texto
                    fontsize=8,  # Tamanho da fonte
                    fontweight="bold",  # Texto em negrito
                )

        return mapa  # Retorna objeto do mapa para criar barra de cores

    # Desenha grafo de incidência em um eixo matplotlib
    def _desenhar_grafo(ax):  # Define função interna para desenhar grafo
        # Calcula posição dos nós usando algoritmo spring layout
        posicao_nos = nx.spring_layout(grafo_incidencia, seed=42)  # Calcula posições dos nós usando algoritmo de molas

        # Extrai pesos das arestas para ajustar largura das linhas
        pesos_arestas = [  # Cria lista com pesos das arestas
            dados_aresta["weight"]  # Pega o campo weight de cada aresta
            for (_, _, dados_aresta) in grafo_incidencia.edges(data=True)  # Loop que percorre arestas com dados
        ]

        # Desenha grafo com nós azuis e arestas cinzas
        nx.draw(  # Função que desenha o grafo completo
            grafo_incidencia,  # Grafo a ser desenhado
            posicao_nos,  # Dicionário com posições dos nós
            with_labels=True,  # Mostra nomes dos nós
            node_size=1000,  # Tamanho dos círculos dos nós
            node_color="#AED6F1",  # Cor dos nós (azul claro)
            edge_color="#34495E",  # Cor das arestas (cinza escuro)
            width=[peso for peso in pesos_arestas],  # Largura de cada aresta baseada em seu peso
            font_size=9,  # Tamanho da fonte dos rótulos
            ax=ax,  # Eixo onde desenhar
        )

        ax.set_title("Grafo de Incidência (Pessoas e Gêneros)")  # Define título do gráfico
        ax.axis("off")  # Desliga exibição dos eixos

    # Exibe apenas a matriz de incidência
    def gerar_matriz():  # Define função pública para mostrar só a matriz
        figura, eixo_matriz = plt.subplots(1, 1, figsize=(10, 8))  # Cria figura com 1 subplot de 10x8 polegadas
        mapa = _desenhar_matriz(eixo_matriz)  # Chama função para desenhar matriz
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)  # Adiciona barra de cores lateral

        plt.tight_layout()  # Ajusta espaçamento automático
        plt.show()  # Abre janela mostrando o gráfico

    # Exibe apenas o grafo de incidência
    def gerar_grafo():  # Define função pública para mostrar só o grafo
        _, eixo_grafo = plt.subplots(1, 1, figsize=(10, 8))  # Cria figura com 1 subplot de 10x8 polegadas
        _desenhar_grafo(eixo_grafo)  # Chama função para desenhar grafo

        plt.tight_layout()  # Ajusta espaçamento automático
        plt.show()  # Abre janela mostrando o gráfico

    # Exibe matriz e grafo lado a lado
    def gerar_matriz_e_grafo():  # Define função pública para mostrar matriz E grafo
        figura, (eixo_matriz, eixo_grafo) = plt.subplots(1, 2, figsize=(18, 8))  # Cria figura com 2 subplots lado a lado

        mapa = _desenhar_matriz(eixo_matriz)  # Desenha matriz no primeiro eixo
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)  # Adiciona barra de cores na matriz

        _desenhar_grafo(eixo_grafo)  # Desenha grafo no segundo eixo

        plt.tight_layout()  # Ajusta espaçamento automático
        plt.show()  # Abre janela mostrando ambos os gráficos

    # Calcula e exibe métricas topológicas do grafo
    def calcular_metricas(caminho_arquivo="metricas_incidencia.txt"):  # Define função pública para calcular métricas
        linhas_relatorio = []  # Cria lista vazia para acumular linhas do relatório

        linhas_relatorio.append("MÉTRICAS TOPOLOGICAS - GRAFO DE INCIDÊNCIA (PESSOAS E GÊNEROS) \n")  # Adiciona cabeçalho

        # Extrai vértices e conta número total
        vertices = list(grafo_incidencia.nodes())  # Pega lista de todos os nós do grafo
        quantidade_vertices = grafo_incidencia.number_of_nodes()  # Conta quantos nós existem
        # Extrai arestas com dados e conta número total
        arestas = list(grafo_incidencia.edges(data=True))  # Pega lista de todas as arestas com seus dados
        quantidade_arestas = grafo_incidencia.number_of_edges()  # Conta quantas arestas existem

        linhas_relatorio.append("Vértices (nós):")  # Adiciona título da seção
        linhas_relatorio.append(str(vertices))  # Adiciona lista de vértices convertida para string
        linhas_relatorio.append(f"\nNúmero de vértices (|V|): {quantidade_vertices}\n")  # Adiciona contagem de vértices

        linhas_relatorio.append("Algumas arestas (primeiras 5):")  # Adiciona título da seção
        linhas_relatorio.append(str(arestas[:5]))  # Adiciona primeiras 5 arestas convertidas para string
        linhas_relatorio.append(f"Número de arestas (|E|): {quantidade_arestas}\n")  # Adiciona contagem de arestas

        # Obtém grau de cada vértice (número de conexões)
        graus_vertices = dict(grafo_incidencia.degree())  # Cria dicionário com grau de cada vértice
        linhas_relatorio.append("Graus dos vértices (degree):")  # Adiciona título da seção
        for nome_vertice, grau_vertice in graus_vertices.items():  # Loop que percorre cada vértice e seu grau
            linhas_relatorio.append(f"  {nome_vertice}: {grau_vertice}")  # Adiciona linha com nome e grau
        # Calcula média dos graus
        grau_medio = float(np.mean(list(graus_vertices.values()))) if graus_vertices else 0.0  # Calcula média aritmética dos graus
        linhas_relatorio.append(f"\nGrau médio: {grau_medio:.4f}\n")  # Adiciona grau médio formatado com 4 casas decimais

        # Extrai pesos de todas as arestas
        pesos_dict = nx.get_edge_attributes(grafo_incidencia, "weight")  # Pega dicionário com pesos de todas as arestas
        pesos_valores = list(pesos_dict.values())  # Converte valores do dicionário para lista
        # Calcula soma e média dos pesos
        peso_total = sum(pesos_valores) if pesos_valores else 0  # Soma todos os pesos
        peso_medio = float(np.mean(pesos_valores)) if pesos_valores else 0.0  # Calcula média dos pesos

        linhas_relatorio.append("Pesos das arestas (weight):")  # Adiciona título da seção
        linhas_relatorio.append(str(pesos_dict))  # Adiciona dicionário de pesos convertido para string
        linhas_relatorio.append(f"Peso total das arestas: {peso_total}")  # Adiciona peso total
        linhas_relatorio.append(f"Peso médio das arestas: {peso_medio:.4f}\n")  # Adiciona peso médio formatado

        # Calcula densidade (proporção de arestas existentes)
        densidade = nx.density(grafo_incidencia)  # Calcula densidade do grafo (0 a 1)
        linhas_relatorio.append(f"Densidade da rede: {densidade:.4f}")  # Adiciona densidade formatada

        # Grava métricas em arquivo
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:  # Abre arquivo para escrita com codificação UTF-8
            arquivo.write("\n".join(linhas_relatorio))  # Junta todas as linhas com quebra e escreve no arquivo

    # Retorna tupla de funções para o menu chamar
    return gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas  # Retorna as 4 funções públicas

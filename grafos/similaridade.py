import numpy as np  # Importa NumPy para operações com matrizes
import networkx as nx  # Importa NetworkX para trabalhar com grafos
import matplotlib.pyplot as plt  # Importa Matplotlib para criar gráficos

# Rodrigo - Responsável pelo módulo de similaridade
def gerar_similaridade(data, pessoas, generos):  # Define função principal que recebe dados, lista de pessoas e lista de gêneros
    # Obtém quantidade de pessoas e gêneros do dataset
    quantidade_pessoas = len(pessoas)  # Conta quantas pessoas existem
    quantidade_generos = len(generos)  # Conta quantos gêneros existem

    # Cria mapeamento nome -> índice para acesso rápido à matriz
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

    # Calcula matriz de similaridade: quantos gêneros pessoas compartilham
    matriz_similaridade = matriz_incidencia @ matriz_incidencia.T  # Multiplica matriz pela sua transposta (M @ M^T)
    # Remove diagonal principal (pessoa com ela mesma)
    np.fill_diagonal(matriz_similaridade, 0)  # Zera a diagonal para remover auto-conexões

    # Cria grafo onde nós são pessoas e arestas são similaridades
    grafo_similaridade = nx.Graph()  # Cria um grafo vazio não-direcionado

    # Adiciona cada pessoa como nó do grafo
    for nome_pessoa in pessoas:  # Loop que percorre cada pessoa
        grafo_similaridade.add_node(nome_pessoa, tipo="pessoa")  # Adiciona nó com atributo tipo="pessoa"

    # Conecta pessoas que compartilham gêneros com peso de similaridade
    quantidade_pessoas = len(pessoas)  # Conta quantas pessoas existem
    for indice_pessoa_origem, pessoa_origem in enumerate(pessoas):  # Loop que percorre pessoas com seus índices
        for indice_pessoa_destino in range(indice_pessoa_origem + 1, quantidade_pessoas):  # Loop aninhado que percorre pessoas seguintes (evita duplicar arestas)
            pessoa_destino = pessoas[indice_pessoa_destino]  # Pega a pessoa de destino pela posição
            peso_similaridade = int(matriz_similaridade[indice_pessoa_origem, indice_pessoa_destino])  # Pega o valor da matriz nesta posição

            # Adiciona aresta apenas se houver similaridade
            if peso_similaridade > 0:  # Se houver gêneros compartilhados entre essas duas pessoas
                grafo_similaridade.add_edge(  # Adiciona aresta (conexão) ao grafo
                    pessoa_origem,  # Nó de origem
                    pessoa_destino,  # Nó de destino
                    weight=peso_similaridade  # Peso da aresta (quantos gêneros compartilham)
                )

    # Desenha matriz de similaridade em um eixo matplotlib
    def _desenhar_matriz(ax):  # Define função interna para desenhar matriz
        ax.set_title("Matriz de Similaridade entre Pessoas")  # Define título do gráfico
        # Cria heatmap com colormap verde
        mapa = ax.imshow(matriz_similaridade, cmap="Greens", aspect="auto")  # Cria mapa de calor da matriz
        ax.set_xticks(np.arange(quantidade_pessoas))  # Define posições das marcações no eixo X
        ax.set_yticks(np.arange(quantidade_pessoas))  # Define posições das marcações no eixo Y
        ax.set_xticklabels(pessoas, rotation=90)  # Define rótulos do eixo X (pessoas) rotacionados 90°
        ax.set_yticklabels(pessoas)  # Define rótulos do eixo Y (pessoas)
        ax.set_xlabel("Pessoa destino")  # Define texto do eixo X
        ax.set_ylabel("Pessoa origem")  # Define texto do eixo Y

        # Adiciona valores numéricos nas células da matriz
        for indice_pessoa_origem in range(quantidade_pessoas):  # Loop que percorre cada linha (pessoa de origem)
            for indice_pessoa_destino in range(quantidade_pessoas):  # Loop aninhado que percorre cada coluna (pessoa de destino)
                valor_celula = matriz_similaridade[indice_pessoa_origem, indice_pessoa_destino]  # Pega valor da célula atual
                ax.text(  # Adiciona texto no gráfico
                    indice_pessoa_destino,  # Posição X (coluna)
                    indice_pessoa_origem,  # Posição Y (linha)
                    str(int(valor_celula)),  # Texto a exibir (valor convertido para string)
                    ha="center",  # Alinhamento horizontal centralizado
                    va="center",  # Alinhamento vertical centralizado
                    color="black",  # Cor do texto
                    fontsize=8,  # Tamanho da fonte
                )

        return mapa  # Retorna objeto do mapa para criar barra de cores

    # Desenha grafo de similaridade em um eixo matplotlib
    def _desenhar_grafo(ax):  # Define função interna para desenhar grafo
        # Tamanho dos nós proporcional ao grau ponderado (força)
        graus_ponderados = dict(grafo_similaridade.degree(weight="weight"))  # Cria dicionário com grau ponderado de cada nó
        tamanhos_nos = [graus_ponderados.get(pessoa, 0) * 200 for pessoa in grafo_similaridade.nodes()]  # Cria lista com tamanho proporcional ao grau de cada nó

        # Largura das arestas proporcional ao peso de similaridade
        larguras_arestas = [  # Cria lista com larguras das arestas
            dados_aresta["weight"] * 0.4  # Multiplica peso por fator de escala 0.4
            for (_, _, dados_aresta) in grafo_similaridade.edges(data=True)  # Loop que percorre arestas com dados
        ]

        # Calcula posição dos nós usando algoritmo spring layout
        posicao_nos = nx.spring_layout(grafo_similaridade, k=0.7, iterations=100, seed=42)  # Calcula posições dos nós usando algoritmo de molas

        # Desenha nós com tamanho e cores variáveis
        nx.draw_networkx_nodes(  # Função que desenha os nós do grafo
            grafo_similaridade,  # Grafo a ser desenhado
            posicao_nos,  # Dicionário com posições dos nós
            node_size=tamanhos_nos,  # Lista com tamanhos dos nós
            node_color="lightgreen",  # Cor dos nós (verde claro)
            edgecolors="black",  # Cor da borda dos nós
            ax=ax,  # Eixo onde desenhar
        )

        # Desenha arestas com largura proporcional ao peso
        nx.draw_networkx_edges(  # Função que desenha as arestas do grafo
            grafo_similaridade,  # Grafo a ser desenhado
            posicao_nos,  # Dicionário com posições dos nós
            width=larguras_arestas,  # Lista com larguras das arestas
            alpha=0.7,  # Transparência das arestas
            edge_color="gray",  # Cor das arestas
            ax=ax,  # Eixo onde desenhar
        )

        # Adiciona rótulos aos nós
        nx.draw_networkx_labels(  # Função que adiciona nomes dos nós
            grafo_similaridade,  # Grafo a ser desenhado
            posicao_nos,  # Dicionário com posições dos nós
            font_size=10,  # Tamanho da fonte dos rótulos
            font_weight="bold",  # Texto em negrito
            ax=ax,  # Eixo onde desenhar
        )

        # Adiciona pesos das arestas como rótulos
        rotulos_arestas = nx.get_edge_attributes(grafo_similaridade, "weight")  # Pega dicionário com pesos de todas as arestas
        nx.draw_networkx_edge_labels(  # Função que adiciona rótulos nas arestas
            grafo_similaridade,  # Grafo a ser desenhado
            posicao_nos,  # Dicionário com posições dos nós
            edge_labels=rotulos_arestas,  # Dicionário com rótulos das arestas
            font_size=8,  # Tamanho da fonte dos rótulos
            ax=ax,  # Eixo onde desenhar
        )

        ax.set_title("Grafo de Similaridade entre Pessoas\n(Peso = gêneros que compartilham)")  # Define título do gráfico
        ax.axis("off")  # Desliga exibição dos eixos

    # Exibe apenas a matriz de similaridade
    def gerar_matriz():  # Define função pública para mostrar só a matriz
        figura, eixo_matriz = plt.subplots(1, 1, figsize=(10, 8))  # Cria figura com 1 subplot de 10x8 polegadas
        mapa = _desenhar_matriz(eixo_matriz)  # Chama função para desenhar matriz
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)  # Adiciona barra de cores lateral

        plt.tight_layout()  # Ajusta espaçamento automático
        plt.show()  # Abre janela mostrando o gráfico

    # Exibe apenas o grafo de similaridade
    def gerar_grafo():  # Define função pública para mostrar só o grafo
        _, eixo_grafo = plt.subplots(1, 1, figsize=(10, 8))  # Cria figura com 1 subplot de 10x8 polegadas
        _desenhar_grafo(eixo_grafo)  # Chama função para desenhar grafo

        plt.tight_layout()  # Ajusta espaçamento automático
        plt.show()  # Abre janela mostrando o gráfico

    # Exibe matriz e grafo lado a lado
    def gerar_matriz_e_grafo():  # Define função pública para mostrar matriz E grafo
        figura, (eixo_matriz, eixo_grafo) = plt.subplots(1, 2, figsize=(20, 8))  # Cria figura com 2 subplots lado a lado

        mapa = _desenhar_matriz(eixo_matriz)  # Desenha matriz no primeiro eixo
        figura.colorbar(mapa, ax=eixo_matriz, fraction=0.046, pad=0.04)  # Adiciona barra de cores na matriz

        _desenhar_grafo(eixo_grafo)  # Desenha grafo no segundo eixo

        plt.tight_layout()  # Ajusta espaçamento automático
        plt.show()  # Abre janela mostrando ambos os gráficos

    # Calcula e exibe métricas topológicas do grafo
    def calcular_metricas(caminho_arquivo="metricas_similaridade.txt"):  # Define função pública para calcular métricas
        linhas_relatorio = []  # Cria lista vazia para acumular linhas do relatório

        linhas_relatorio.append("MÉTRICAS TOPOLOGICAS - GRAFO DE SIMILARIDADE (PESSOAS) \n")  # Adiciona cabeçalho

        # Extrai vértices e conta número total
        vertices = list(grafo_similaridade.nodes())  # Pega lista de todos os nós do grafo
        quantidade_vertices = grafo_similaridade.number_of_nodes()  # Conta quantos nós existem
        # Extrai arestas com dados e conta número total
        arestas = list(grafo_similaridade.edges(data=True))  # Pega lista de todas as arestas com seus dados
        quantidade_arestas = grafo_similaridade.number_of_edges()  # Conta quantas arestas existem

        linhas_relatorio.append("Vértices (pessoas):")  # Adiciona título da seção
        linhas_relatorio.append(str(vertices))  # Adiciona lista de vértices convertida para string
        linhas_relatorio.append(f"\nNúmero de vértices (|V|): {quantidade_vertices}\n")  # Adiciona contagem de vértices

        linhas_relatorio.append("Algumas arestas (primeiras 5):")  # Adiciona título da seção
        linhas_relatorio.append(str(arestas[:5]))  # Adiciona primeiras 5 arestas convertidas para string
        linhas_relatorio.append(f"Número de arestas (|E|): {quantidade_arestas}\n")  # Adiciona contagem de arestas

        # Obtém grau simples e ponderado de cada pessoa
        graus = dict(grafo_similaridade.degree())  # Cria dicionário com grau simples de cada vértice
        graus_ponderados = dict(grafo_similaridade.degree(weight="weight"))  # Cria dicionário com grau ponderado de cada vértice

        linhas_relatorio.append("Grau (degree) por pessoa:")  # Adiciona título da seção
        for pessoa, grau in graus.items():  # Loop que percorre cada pessoa e seu grau
            linhas_relatorio.append(f"  {pessoa}: {grau}")  # Adiciona linha com nome e grau

        linhas_relatorio.append("\nGrau ponderado (strength) por pessoa:")  # Adiciona título da seção
        for pessoa, grau_p in graus_ponderados.items():  # Loop que percorre cada pessoa e seu grau ponderado
            linhas_relatorio.append(f"  {pessoa}: {grau_p}")  # Adiciona linha com nome e grau ponderado

        # Calcula média dos graus
        grau_medio = float(np.mean(list(graus.values()))) if graus else 0.0  # Calcula média aritmética dos graus simples
        grau_ponderado_medio = float(np.mean(list(graus_ponderados.values()))) if graus_ponderados else 0.0  # Calcula média aritmética dos graus ponderados

        linhas_relatorio.append(f"\nGrau médio: {grau_medio:.4f}")  # Adiciona grau médio formatado com 4 casas decimais
        linhas_relatorio.append(f"Grau ponderado médio: {grau_ponderado_medio:.4f}\n")  # Adiciona grau ponderado médio formatado

        # Calcula centralidades usando pesos das arestas
        centralidade_intermediacao = nx.betweenness_centrality(grafo_similaridade, weight="weight")  # Calcula centralidade de intermediação (betweenness) ponderada
        centralidade_autovetor = nx.eigenvector_centrality(grafo_similaridade, weight="weight", max_iter=1000)  # Calcula centralidade de autovetor (eigenvector) ponderada

        linhas_relatorio.append("Centralidade de intermediação (betweenness):")  # Adiciona título da seção
        for pessoa, valor in centralidade_intermediacao.items():  # Loop que percorre cada pessoa e sua centralidade
            linhas_relatorio.append(f"  {pessoa}: {valor:.4f}")  # Adiciona linha com nome e valor formatado

        linhas_relatorio.append("\nCentralidade de autovetor (eigenvector):")  # Adiciona título da seção
        for pessoa, valor in centralidade_autovetor.items():  # Loop que percorre cada pessoa e sua centralidade
            linhas_relatorio.append(f"  {pessoa}: {valor:.4f}")  # Adiciona linha com nome e valor formatado

        # Calcula métricas globais do grafo
        densidade = nx.density(grafo_similaridade)  # Calcula densidade do grafo (0 a 1)
        coeficiente_aglomeracao = nx.average_clustering(grafo_similaridade, weight="weight")  # Calcula coeficiente de aglomeração médio ponderado

        # Tenta calcular diâmetro (falha se grafo não é conexo)
        try:  # Tenta executar bloco de código
            diametro = nx.diameter(grafo_similaridade)  # Calcula diâmetro do grafo (maior distância entre dois nós)
        except nx.NetworkXError:  # Se houver erro (grafo não conexo)
            diametro = "Não conexo"  # Define mensagem indicando que grafo não é conexo

        linhas_relatorio.append("\nMétricas globais:")  # Adiciona título da seção
        linhas_relatorio.append(f"  Densidade do grafo: {densidade:.4f}")  # Adiciona densidade formatada
        linhas_relatorio.append(f"  Coeficiente de aglomeração médio (ponderado): {coeficiente_aglomeracao:.4f}")  # Adiciona coeficiente formatado
        linhas_relatorio.append(f"  Diâmetro do grafo: {diametro}")  # Adiciona diâmetro

        # Grava métricas em arquivo
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:  # Abre arquivo para escrita com codificação UTF-8
            arquivo.write("\n".join(linhas_relatorio))  # Junta todas as linhas com quebra e escreve no arquivo

    # Retorna tupla de funções para o menu chamar
    return gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas  # Retorna as 4 funções públicas

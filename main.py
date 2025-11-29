from helpers.load_dataset import load_dataset
from helpers.easy_log import easy_log
from grafos.incidencia import gerar_incidencia
from grafos.coocorrencia import gerar_coocorrencia
from grafos.similaridade import gerar_similaridade

def menu_principal():
    easy_log("SUCCESS", "ANÁLISE DE MATRIZES E GRAFOS - CATEGORIAS DE ANIME")
    easy_log("INFO", f"Menu principal aberto.")
    easy_log("OPTION", "Escolha uma das opções abaixo:\n")
    easy_log("CASE", "  1 - Analisar Incidência")
    easy_log("CASE", "  2 - Analisar Coocorrência")
    easy_log("CASE", "  3 - Analisar Similaridade")
    easy_log("CASE", "  4 - Executar todas as análises")
    easy_log("CASE", "  0 - Sair\n")

def menu_interno(tipo):
    easy_log("SUCCESS", f"[{tipo}] Deseja visualizar a matriz, grafo ou as métricas topológicas?\n")
    easy_log("INFO", f"Menu interno [{tipo}] aberto.")
    easy_log("OPTION", "Escolha uma das opções abaixo:")
    easy_log("CASE", "  1 - Matriz")
    easy_log("CASE", "  2 - Grafo")
    easy_log("CASE", "  3 - Matriz e Grafo")
    easy_log("CASE", "  4 - Métricas Topológicas")
    easy_log("CASE", "  5 - Todas as opções acima")
    easy_log("CASE", "  0 - Voltar ao menu principal\n")


def main():
    easy_log("INFO", "Iniciando aplicação de análise de matrizes e grafos...")
    
    try:
        easy_log("INFO", "Carregando dataset...")
        data, pessoas, generos = load_dataset()
        easy_log("SUCCESS", f"Dataset carregado com sucesso: {len(data)} interações, {len(pessoas)} pessoas, {len(generos)} gêneros\n")
    except Exception as e:
        easy_log("ERROR", f"Erro ao carregar dataset: {e}")
        return

    while True:
        menu_principal()
        opcao = input("Digite a opção desejada (0-4): ").strip()

        if opcao == "1":
            easy_log("INFO", "Abrindo menu de Incidência...")
            gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas = gerar_incidencia(data, pessoas, generos)
            while True:
                menu_interno("INCIDÊNCIA")

                sub_opcao = input("Digite a opção desejada (0-4): ").strip()

                if sub_opcao == "1":
                    gerar_matriz()
                elif sub_opcao == "2":
                    gerar_grafo()
                elif sub_opcao == "3":
                    gerar_matriz_e_grafo()
                elif sub_opcao == "4":
                    calcular_metricas()
                elif sub_opcao == "5":
                    gerar_matriz()
                    gerar_grafo()
                    gerar_matriz_e_grafo()
                    calcular_metricas()
                elif sub_opcao == "0":
                    break
                else:
                    easy_log("WARNING", "Opção inválida! Digite uma opção entre 0 e 4.")
                
                input("\nPressione ENTER para continuar...")

        elif opcao == "2":
            easy_log("INFO", "Abrindo menu de Coocorrência...")
            gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas = gerar_coocorrencia(data, pessoas, generos)
            while True:
                menu_interno("COOCORRÊNCIA")

                sub_opcao = input("Digite a opção desejada (0-4): ").strip()

                if sub_opcao == "1":
                    gerar_matriz()
                elif sub_opcao == "2":
                    gerar_grafo()
                elif sub_opcao == "3":
                    gerar_matriz_e_grafo()
                elif sub_opcao == "4":
                    calcular_metricas()
                elif sub_opcao == "5":
                    gerar_matriz()
                    gerar_grafo()
                    gerar_matriz_e_grafo()
                    calcular_metricas()
                elif sub_opcao == "0":
                    break
                else:
                    easy_log("WARNING", "Opção inválida! Digite uma opção entre 0 e 4.")
                
                input("\nPressione ENTER para continuar...")

        elif opcao == "3":
            easy_log("INFO", "Abrindo menu de Similaridade...")
            gerar_matriz, gerar_grafo, gerar_matriz_e_grafo, calcular_metricas = gerar_similaridade(data, pessoas, generos)
            while True:
                menu_interno("SIMILARIDADE")
                sub_opcao = input("Digite a opção desejada (0-4): ").strip()

                if sub_opcao == "1":
                    gerar_matriz()
                elif sub_opcao == "2":
                    gerar_grafo()
                elif sub_opcao == "3":
                    gerar_matriz_e_grafo()
                elif sub_opcao == "4":
                    calcular_metricas()
                elif sub_opcao == "5":
                    gerar_matriz()
                    gerar_grafo()
                    gerar_matriz_e_grafo()
                    calcular_metricas()
                elif sub_opcao == "0":
                    break
                else:
                    easy_log("WARNING", "Opção inválida! Digite uma opção entre 0 e 4.")
                
                input("\nPressione ENTER para continuar...")

        elif opcao == "4":
            easy_log("INFO", "Executando todas as análises...")
            
            try:
                easy_log("INFO", "Executando análise de Incidência...")
                gerar_incidencia(data, pessoas, generos)
                easy_log("SUCCESS", "Incidência concluída!")
                
                easy_log("INFO", "Executando análise de Coocorrência...")
                gerar_coocorrencia(data, pessoas, generos)
                easy_log("SUCCESS", "Coocorrência concluída!")
                
                easy_log("INFO", "Executando análise de Similaridade...")
                gerar_similaridade(data, pessoas, generos)
                easy_log("SUCCESS", "Similaridade concluída!")
                
                easy_log("SUCCESS", "Todas as análises foram concluídas com sucesso!")
            except Exception as e:
                easy_log("ERROR", f"Erro ao executar análises: {e}")

        elif opcao == "0":
            easy_log("INFO", "Encerrando programa...")
            break

        else:
            easy_log("WARNING", "Opção inválida! Digite uma opção entre 0 e 4.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
import json  # Importa biblioteca para trabalhar com arquivos JSON
from .easy_log import easy_log  # Importa função de log do módulo easy_log

def load_dataset():  # Define função para carregar o dataset do arquivo JSON

    data = {}  # Inicializa variável que armazenará os dados do JSON
    pessoas = set()  # Cria conjunto vazio para armazenar pessoas únicas (set remove duplicatas automaticamente)
    generos = set()  # Cria conjunto vazio para armazenar gêneros únicos (set remove duplicatas automaticamente)

    try:  # Tenta executar bloco de código que pode gerar erro
        with open("dataset.json", "r", encoding="utf-8") as json_file:  # Abre arquivo JSON para leitura com codificação UTF-8
            data = json.load(json_file)  # Carrega conteúdo do arquivo JSON e converte para estrutura Python
            easy_log("SUCCESS", "Arquivo 'dataset.json' carregado com sucesso.")  # Exibe mensagem de sucesso
    except FileNotFoundError:  # Se arquivo não for encontrado
        easy_log("ERROR", "O arquivo 'dataset.json' não foi encontrado.")  # Exibe mensagem de erro
        exit()  # Encerra execução do programa

    for item in data:  # Loop que percorre cada item (relação) no dataset
        pessoas.add(item["from"])  # Adiciona pessoa ao conjunto (campo "from")
        generos.add(item["to"])  # Adiciona gênero ao conjunto (campo "to")

    easy_log("INFO", f"Carregados: {len(data)} interações, {len(pessoas)} pessoas únicas, {len(generos)} gêneros únicos.")  # Exibe estatísticas do dataset carregado
    return (data, sorted(list(pessoas)), sorted(list(generos)))  # Retorna tupla com: dados brutos, lista ordenada de pessoas, lista ordenada de gêneros

    

    
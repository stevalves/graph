import json
from .easy_log import easy_log

def load_dataset():

    data = {}
    pessoas = set()
    generos = set()

    try:
        with open("dataset.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            easy_log("SUCCESS", "Arquivo 'dataset.json' carregado com sucesso.")
    except FileNotFoundError:
        easy_log("ERROR", "O arquivo 'dataset.json' não foi encontrado.")
        exit()

    for item in data:
        pessoas.add(item["from"])
        generos.add(item["to"])

    easy_log("INFO", f"Carregados: {len(data)} interações, {len(pessoas)} pessoas únicas, {len(generos)} gêneros únicos.")
    return (data, sorted(list(pessoas)), sorted(list(generos)))

    

    
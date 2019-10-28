import os
import json
from datetime import datetime


def get_content(year):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + f"/../database/{year}.json"
    with open(file_path) as json_file:
        return json.load(json_file)


def grade_chave(chave):
    return f"grade_{chave}"


def grade_chaves(content):
    chaves = content['grade'].keys()
    return [grade_chave(i) for i in chaves]


def get_grade_opcoes(content):
    try:
        chaves = content['grade'].keys()

        opcoes = []
        for chave in chaves:
            label = content['grade'][chave]['label']
            chave = grade_chave(chave)
            opcoes.append([(label, chave)])

        return opcoes
    except FileNotFoundError:
        return []


now = datetime.now()
current_year = now.year
content = get_content(current_year)

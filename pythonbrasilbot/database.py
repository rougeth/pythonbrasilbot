import os
import json


def get_content(year):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + f"/../database/{year}.json"
    with open(file_path) as json_file:
        return json.load(json_file)


def get_grade_opcoes(year):
    content = get_content(year)
    return content['grade'].keys()

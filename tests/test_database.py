import pytest
from pythonbrasilbot.database import (get_content,
                                      get_grade_opcoes,
                                      grade_chave,
                                      grade_chaves)


def test_get_content_raise_filenotfound():
    with pytest.raises(FileNotFoundError):
        get_content(2000)


def test_get_content():
    assert type(get_content(2019)) == dict


def test_grade_chave():
    chave = grade_chave('teste')
    assert chave == 'grade_teste'


def test_grade_chaves():
    content = get_content(2019)
    chaves_list = grade_chaves(content)

    chaves = content['grade'].keys()
    chaves = [grade_chave(i) for i in chaves]

    assert iter(chaves_list)
    assert len(chaves) == len(chaves_list)
    assert chaves_list == chaves


def test_get_grade_opcoes():
    content = get_content(2019)
    opcoes = get_grade_opcoes(content)
    assert isinstance(opcoes, list)

import pytest
from pythonbrasilbot.database import get_content, get_grade_opcoes


def test_get_content_raise_filenotfound():
    with pytest.raises(FileNotFoundError):
        get_content(2000)


def test_get_content():
    assert type(get_content(2019)) == dict


def test_get_grade_opcoes():
    opcoes = get_grade_opcoes(2019)
    assert iter(opcoes)

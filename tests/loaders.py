import pytest

from sexpr import load, Grammar


def test_load_from_object_raises_TypeError():
    with pytest.raises(TypeError):
        load(object())


def test_load_from_string():
    src = '''
        rules:
            exp:
                - exp1
                - exp2
            exp1:
                [ false ]
            exp2:
                [ true ]
    '''

    grammar = load(src)

    assert type(grammar) is Grammar
    assert grammar.root == 'exp'
    assert grammar.yaml == {
        'exp': ['exp1', 'exp2'],
        'exp1': [False],
        'exp2': [True]
    }


def test_load_from_dict():
    src = {
        'rules': {
            'exp': ['exp1', 'exp2'],
            'exp1': [False],
            'exp2': [True]
        }
    }

    grammar = load(src)

    assert type(grammar) is Grammar
    assert grammar.root == 'exp'
    assert set(grammar.rules.keys()) == {'exp', 'exp1', 'exp2'}


def test_load_from_file():
    assert load('tests/predicate.yml').root == 'predicate'


def test_load_with_overridden_root():
    src = '''
        root:
            exp1
        rules:
            exp:
                - exp1
                - exp2
            exp1:
                [ false ]
            expr2:
                [ true ]
    '''

    assert load(src).root == 'exp1'

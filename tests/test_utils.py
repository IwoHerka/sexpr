import pytest

from sexpr import *


def test_inject():
    obj1 = object()
    obj2 = object()
    sexpr = ['tag', obj1]

    injected = inject(sexpr, lambda x: [x, obj2])

    assert injected[0] == 'tag'
    assert injected[1][0] == obj1
    assert injected[1][1] == obj2
    assert not injected.grammar

    grammar = load('''
        rules:
            exp:
                - exp1
            exp1:
                [ false ]
    ''')
    sexpr = Sexpr(sexpr, grammar)
    injected = inject(sexpr, lambda x: x)

    assert injected.grammar == grammar


def test_find_descendant():
    descendant = ['table_name', 'suppliers']

    sexp = [
        'select',
        ['set_quantifier', "all"],
        ['from_clause',
            ['table_as',
                descendant,
                ['range_var_name', "s1"]
            ]
        ],
        ['where_clause',
            ['tautology', True]
        ]
    ]

    assert descendant == find_descendant(sexp, 'table_name')
    assert descendant == find_descendant(Sexpr(sexp), 'table_name')

    with pytest.raises(ValueError):
        assert not find_descendant([], 'whatever')
    with pytest.raises(ValueError):
        assert not find_descendant(object(), 'whatever')
    with pytest.raises(ValueError):
        assert not find_descendant(None, 'whatever')
    with pytest.raises(ValueError):
        assert not find_descendant(sexpr, None)


def test_find_and_replace():
    sexp = [
        'select',
        ['set_quantifier', "all"],
        ['from_clause',
            ['table_as',
                ['table_name', 'suppliers'],
                ['range_var_name', "s1"]
            ]
        ],
        ['where_clause',
            ['tautology', True]
        ]
    ]

    find = lambda s: isinstance(s, list) and s[0] == 'table_name'
    replace = lambda s: ['_table_name', s[1]]

    modified = find_and_replace(sexp, find, replace)

    assert modified[2][1][1] == ['_table_name', 'suppliers']


def test_find_child():
    sexp = [
        'select',
        ['set_quantifier', "all"],
        ['from_clause',
            ['table_as',
                ['table_name', 'suppliers'],
                ['range_var_name', "s1"]
            ]
        ],
        ['where_clause',
            ['tautology', True]
        ]
    ]

    assert find_child(sexp, 'set_quantifier')
    assert find_child(sexp, 'where_clause') == [
        'where_clause', ['tautology', True]
    ]
    assert not find_child(sexp, 'range_var_name')

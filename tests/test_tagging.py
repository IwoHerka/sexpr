from sexpr import Grammar, Sexpr, load, register


def setup_function():
    Grammar.registered_tags = {}


grammar = load('''
    root:
        exp1
    rules:
        exp:
            - exp1
            - exp2
        exp1:
            [ false ]
        exp2:
            [ exp3 ]
        exp3:
            [ exp4 ]
        exp4:
            [ True, False ]
''')


class Exp1(Sexpr):
    pass


class Exp2(Sexpr):
    pass


class Exp3(Sexpr):
    pass


class Exp4(Sexpr):
    pass


tags = dict(exp1=Exp1, exp2=Exp2, exp3=Exp3, exp4=Exp4)


def test_tagging():
    Grammar.register(**tags)

    node = grammar.sexpr(['exp1', True])
    assert type(node) is Exp1

    node = grammar.sexpr(['exp2', False])
    assert type(node) is Exp2

    node = grammar.sexpr(['exp2', ['exp3', ['exp4', False]]])
    assert type(node) is Exp2
    assert node.tag == 'exp2'
    assert type(node[1]) is Exp3
    assert type(node[1][1]) is Exp4
    assert node[1][1][1] is False


def test_register_from_module():
    Grammar.register(**tags)
    via_class = Grammar.registered_tags
    Grammar.registered_tags = {}
    register(**tags)
    via_module = Grammar.registered_tags

    assert via_class == via_module

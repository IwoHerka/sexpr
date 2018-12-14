from sexpr import extend, inject, load, Sexpr

grammar = load('tests/predicate.yml')


def test_inplace():
    sexp = grammar.sexpr(['tautology', True])
    sexp.inject(lambda e: not e)
    sexp.extend(lambda e: ['not', e])

    assert sexp.tag == 'not'
    assert sexp.body == [['tautology', False]]
    assert sexp.sexpr == ['not', ['tautology', False]]

    q = sexp
    p = sexp.copy()

    sexp = Sexpr(['not', ['or', p, q]], grammar)
    sexp.inject(lambda exp: (['not', exp[1]], ['not', exp[2]]))
    sexp.extend(lambda exp: ['and', *exp[1:]])

    assert sexp.tag, 'and'
    assert sexp.body == [['not', p], ['not', q]]
    assert sexp.sexpr == ['and', ['not', p], ['not', q]]

import os
import unittest

from sexpr import extend, inject, load, Sexpr

cd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
grammar = load(os.path.join(cd, 'predicate.yml'))


class ManipulationTestCase(unittest.TestCase):
    def test_pure(self):
        sexp = ['tautology', True]
        sexp = inject(sexp, lambda e: not e)
        sexp = extend(sexp, lambda e: ['not', e])
        self.assertEqual(sexp, ['not', ['tautology', False]])

        sexp = inject(['and', ['lit', True], ['lit', False]], lambda left, right: ['or', left, right])
        self.assertEqual(sexp, ['and', ['or', ['lit', True], ['lit', False]]])

    def test_inplace(self):
        sexp = grammar.sexpr(['tautology', True])
        sexp.inject(lambda e: not e)
        sexp.extend(lambda e: ['not', e])

        self.assertEqual(sexp.tag, 'not')
        self.assertEqual(sexp.body, [['tautology', False]])
        self.assertEqual(sexp.sexpr, ['not', ['tautology', False]])

        q = sexp
        p = sexp.copy()

        sexp = Sexpr(['not', ['or', p, q]], grammar)
        sexp.inject(lambda exp: (['not', exp[1]], ['not', exp[2]]))
        sexp.extend(lambda exp: ['and', *exp[1:]])

        self.assertEqual(sexp.tag, 'and')
        self.assertEqual(sexp.body, [['not', p], ['not', q]])
        self.assertEqual(sexp.sexpr, ['and', ['not', p], ['not', q]])

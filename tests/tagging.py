import os
import sexpr
import unittest

from sexpr.grammar import Grammar
from sexpr.sexpr import Sexpr


grammar = sexpr.load('''
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


Grammar.register('exp1', Exp1)
Grammar.register('exp2', Exp2)
Grammar.register('exp3', Exp3)
sexpr.register('exp4', Exp4)


class TaggingTest(unittest.TestCase):
    def test_tagging(self):
        node = grammar.sexpr(['exp1', True])
        self.assertEqual(type(node), Exp1)

        node = grammar.sexpr(['exp2', False])
        self.assertEqual(type(node), Exp2)

        node = grammar.sexpr(['exp2', ['exp3', ['exp4', False]]])
        self.assertEqual(type(node), Exp2)
        self.assertEqual(node.tag, 'exp2')
        self.assertEqual(type(node[1]), Exp3)
        self.assertEqual(type(node[1][1]), Exp4)
        self.assertEqual(node[1][1][1], False)

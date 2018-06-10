import unittest

import sexpr

grammar = sexpr.load('''
    rules:
        expr:
            - expr1
            - expr2
        expr1:
            - [ literal1 ]
        expr2:
            - [ literal2 ]
        literal1:
            [ true, false ]
        literal2:
            - true
            - false
''')


class OtherTest(unittest.TestCase):
    '''Test alternative representations.'''
    def test_literal1(self):
        s = ['expr1', True]
        self.assertTrue(grammar.matches(s))

    def test_literal2(self):
        s = ['expr2', True]
        self.assertTrue(grammar.matches(s))

import unittest

import sexpr


grammar = sexpr.load('''
    rules:
        expr:
            - exactly_one
            - exactly_two
            - one_or_more
            - zero_or_more
            - optional
            - literal
        one_or_more:
            - [ expr+ ]
        zero_or_more:
            - [ expr* ]
        exactly_two:
            - [ expr, expr ]
        exactly_one:
            - [ expr ]
        optional:
            - [ 'expr?' ]
        literal:
            - [ lit ]
        lit:
            - true
            - false
''')


def expr():
    # TODO: Randomize?
    return ['literal', True]


class RepetitionModifiersTest(unittest.TestCase):
    def test_exactly_one(self):
        e = ['exactly_one']
        self.assertFalse(grammar.matches(e))

        e = ['exactly_one', expr()]
        self.assertTrue(grammar.matches(e))

        e = ['exactly_one', expr(), expr()]
        self.assertFalse(grammar.matches(e))

    def test_exactly_two(self):
        e = ['exactly_two']
        self.assertFalse(grammar.matches(e))

        e = ['exactly_two', expr()]
        self.assertFalse(grammar.matches(e))

        e = ['exactly_two', expr(), expr()]
        self.assertTrue(grammar.matches(e))

        e = ['exactly_two', expr(), expr(), expr()]
        self.assertFalse(grammar.matches(e))

    def test_zero_or_more(self):
        e = ['zero_or_more']
        self.assertTrue(grammar.matches(e))

        e = ['zero_or_more', expr()]
        self.assertTrue(grammar.matches(e))

        e = ['zero_or_more', expr(), expr()]
        self.assertTrue(grammar.matches(e))

    def test_one_or_more(self):
        e = ['one_or_more']
        self.assertFalse(grammar.matches(e))

        e = ['one_or_more', expr()]
        self.assertTrue(grammar.matches(e))

        e = ['one_or_more', expr(), expr()]
        self.assertTrue(grammar.matches(e))

    def test_optional(self):
        e = ['optional']
        self.assertTrue(grammar.matches(e))

        e = ['optional', expr()]
        self.assertTrue(grammar.matches(e))

        e = ['optional', expr(), expr()]
        self.assertFalse(grammar.matches(e))

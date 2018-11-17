import unittest

import sexpr


grammar = sexpr.load('tests/predicate.yml')


class CompositionTest(unittest.TestCase):
    def test_cannot_match_terminal(self):
        e = ['name', 'foo']
        self.assertFalse(grammar.matches(e))

    def test_can_match_nonterminal(self):
        e = ['identifier', 'foo']
        self.assertTrue(grammar.matches(e))

    def test_cannot_match_nonexistent_symbol(self):
        e = ['foo', 'bar']
        self.assertFalse(grammar.matches(e))

    def test_matches_valid_regexpr(self):
        e = ['identifier', 'foo']
        self.assertTrue(grammar.matches(e))

    def test_cannot_match_invalid_regexpr(self):
        e = ['identifier', '&^51*=']
        self.assertFalse(grammar.matches(e))

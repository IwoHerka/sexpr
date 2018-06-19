import unittest
from collections import OrderedDict
from random import choice, randint

from sexpr.grammar import Grammar
from sexpr.types import *
from sexpr.yaml import Regexpr

from ..utils import random_list


# Terminals and corresponding valid values.
terminals = [
    (True,             Terminal(True, Terminal.VALUE)),
    ('string',         Terminal(Regexpr('[a-z]+'), Terminal.REGEXPR)),
    (777,              Terminal('int', Terminal.TYPE, True)),
    (dict(a=1),        Terminal('dict', Terminal.TYPE, True)),
    (OrderedDict(a=1), Terminal('dict', Terminal.TYPE, False))
]

# Values quaranteed to be invalid (w.r.t to `terminals`).
invals = [False, 'STRING', 333.3, [1, 2], (1, 2)]

NR_ROUNDS = 10


class MatchingUnitTest(unittest.TestCase):
    def test_alternative(self):
        for _ in range(NR_ROUNDS):
            vals = []
            terms = []

            for _ in range(randint(2, 5)):
                terminal = choice(terminals)
                vals.append(terminal[0])
                terms.append(terminal[1])

            node = Alternative(terms)

            for val in vals:
                # Test valid value matches.
                self.assertTrue(node.matches(val))
                # Test valid value is popped.
                self.assertEqual(node.eat([val]), [])
                # Test invalid value mismatches.
                self.assertFalse(node.matches(choice(invals)))
                # Test attempt at popping invalid value fails.
                self.assertEqual(node.eat([choice(invals)]), None)
                # Test valid prefix is popped off.
                self.assertEqual(len(node.eat([val, choice(invals)])), 1)

    def test_non_terminal(self):
        for _ in range(NR_ROUNDS):
            valid_terms = [choice(terminals) for _ in range(randint(2, 5))]
            valid, terms = [list(t) for t in zip(*valid_terms)]
            node = NonTerminal('name', Sequence(terms))
            valid.insert(0, 'name')

            # Test valid matches.
            self.assertTrue(node.matches(valid))
            # Test invalid doesn't match.
            self.assertFalse(node.matches(choice(invals)))
            # Test valid is popped off.
            self.assertEqual(node.eat([valid]), [])
            # Test invalid cannot be popped off.
            self.assertEqual(node.eat(valid), None)

    def test_reference(self):
        for _ in range(NR_ROUNDS):
            grammar = Grammar({}, dict(root='name'))
            valid, term = choice(terminals)
            grammar.rules['name'] = term
            node = Reference('name', grammar)

            # Test valid matches.
            self.assertTrue(node.matches(valid))
            # Test invalid doesn't match.
            self.assertFalse(node.matches(choice(invals)))
            # Test valid is popped off.
            self.assertEqual(node.eat([valid]), [])
            # Test invalid cannot be popped off
            # (watch out for true-negatives).
            self.assertTrue(node.eat(valid) in [None, 'tring'])

    def test_multiple(self):
        for _ in range(randint(2, 5)):
            val, term = choice(terminals)
            node = Multiple(term, 0, 1)
            valid = [val]

            for seed in range(10):
                invalid = random_list(seed=seed)
                self.assertTrue(node.matches(valid))
                self.assertTrue(len(node.eat(invalid)) in [len(invalid), len(invalid) - 1])
                self.assertTrue(node.matches(invalid))

            val, term = choice(terminals)
            node = Multiple(term, 1, None)
            valid = [val]

            for seed in range(10):
                invalid = random_list(seed=seed)
                mismatched = valid + invalid
                self.assertTrue(node.matches(valid))
                self.assertEqual(node.eat(invalid), None)
                self.assertFalse(node.matches(invalid))
                self.assertEqual(len(node.eat(mismatched)), len(invalid))

    def test_sequence(self):
        for seed in range(NR_ROUNDS):
            valid_terms = [choice(terminals) for _ in range(randint(2, 5))]
            valid, terms = [list(t) for t in zip(*valid_terms)]
            node = Sequence(terms)
            invalid = random_list(seed=seed)

            # Test valid matches.
            self.assertTrue(node.matches(valid))
            # Test valid is popped off.
            self.assertEqual(node.eat(valid), [])

            if invalid != valid:
                mismatching = valid + invalid
                # Test invalid doesn't match.
                self.assertFalse(node.matches(invalid))
                # Test valid cannot be popped off.
                self.assertEqual(node.eat(invalid), None)
                # Test mismatched is partially popped off.
                self.assertEqual(len(node.eat(mismatching)), len(invalid))

    def test_terminal(self):
        pass

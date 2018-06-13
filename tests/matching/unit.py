import unittest

from sexpr.types import *
from ..utils import random_list


class MatchingUnitTest(unittest.TestCase):
    def test_sequence(self):
        valid_terms = [
            (True,  Terminal(True, Terminal.VALUE)),
            (False, Terminal(False, Terminal.VALUE))
        ]

        valid, terms = [list(t) for t in zip(*valid_terms)]
        seq = Sequence(terms)
        self.assertTrue(seq.matches(valid))

        for seed in range(20):
            invalid = random_list(seed=seed)

            if invalid != valid:
                mismatching = valid + invalid
                self.assertFalse(seq.matches(invalid))
                self.assertEqual(seq.eat(invalid), None)
                self.assertEqual(len(seq.eat(mismatching)), len(invalid))
                self.assertFalse(seq.matches(invalid))

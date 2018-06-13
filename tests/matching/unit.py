import unittest

from sexpr.types import *
from ..utils import random_list


class MatchingUnitTest(unittest.TestCase):
    def test_sequence(self):
        invalid = [
            [],
            (),
            ((),),
            ((),()),
            [[]],
            [[], []],
            [True, True],
            [False, False],
            [False, True, False],
            [False, True],
            [object()],
            (object(),),
            [object(), object()]
        ]

        mismatching = [
            [True, False, False],
            [True, False, object()]
        ]

        true = Terminal(True, Terminal.VALUE)
        false = Terminal(False, Terminal.VALUE)
        seq = Sequence([true, false])

        self.assertTrue(seq.matches([True, False]))

        for e in invalid:
            if isinstance(e, list):
                self.assertFalse(seq.matches(e))
            else:
                with self.assertRaises(TypeError):
                    seq.matches(e)
            self.assertEqual(seq.eat(e), None)

        for e in mismatching:
            self.assertEqual(len(seq.eat(e)), 1)
            self.assertFalse(seq.matches(e))

        for i in range(10):
            li = random_list(seed=i)
            print(li)
            if li != [True, False]:
                self.assertFalse(seq.matches(e))

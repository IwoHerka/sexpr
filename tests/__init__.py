import os
import sexpr
import unittest
import yaml

from sexpr.utils import merge_options


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

bool_yml = os.path.join(__location__, 'bool.yml')


class Test(unittest.TestCase):
    def test_load_from_object(self):
        with self.assertRaises(TypeError):
            sexpr.load(object())

    # def test_load_from_string(self):
    #     sexpr.load('string')
    #     self.assertEqual(True, True)

    def test_load_from_file(self):
        grammar = sexpr.load(bool_yml)

        print(grammar.rules['bool_expr'])

        self.assertEqual(True, True)

    # def test_load_from_dict(self):
    #     sexpr.load(dict(key='val'))
    #     self.assertEqual(True, True)

    # def test_merging_options(self):
    #     first = dict(a=1, b=2)
    #     second = dict(b=3, c=4)
    #     third = merge_options(first, second)
    #     self.assertEqual(third['a'], 1)
    #     self.assertEqual(third['b'], 3)
    #     self.assertEqual(third['c'], 4)


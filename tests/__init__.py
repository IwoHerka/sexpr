import os
import sexpr
import unittest

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

    # def test_load_from_dict(self):
    #     sexpr.load(dict(rules='val'))
    #     self.assertEqual(True, True)

    def test_merging_options(self):
        first = dict(a=1, b=2)
        second = dict(b=3, c=4)
        third = merge_options(first, second)
        self.assertEqual(third['a'], 1)
        self.assertEqual(third['b'], 3)
        self.assertEqual(third['c'], 4)

    def test_load_from_file(self):
        grammar = sexpr.load(bool_yml)
        for v in grammar.rules.values():
            print(v)
        print('...................................................')

    def test_1(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_lit', True]
        self.assertEqual(grammar.matches(s), True)

    def test_2(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_lit', False]
        self.assertEqual(grammar.matches(s), True)

    def test_3(self):
        grammar = sexpr.load(bool_yml)
        s = ['var_ref', "x"]
        self.assertEqual(grammar.matches(s), True)

    def test_4(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_not', ['bool_lit', False]]
        self.assertEqual(grammar.matches(s), True)

    def test_5(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_not', ['var_ref', "y"]]
        self.assertEqual(grammar.matches(s), True)

    def test_6(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_not', ['bool_not', ['bool_lit', True]]]
        self.assertEqual(grammar.matches(s), True)

    def test_7(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_and', ['bool_lit', True], ['bool_lit', False]]
        self.assertEqual(grammar.matches(s), True)

    def test_8(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_or', ['bool_lit', True], ['bool_lit', False]]
        self.assertEqual(grammar.matches(s), True)

    def test_9(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_and', ['bool_not', ['var_ref', "x"]], ['bool_lit', True]]
        self.assertEqual(grammar.matches(s), True)

    def test_10(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_or', ['bool_and', ['bool_not', ['var_ref', "x"]],
                                     ['bool_lit', True]],
                        ['bool_lit', False]]
        self.assertEqual(grammar.matches(s), True)

    def test_11(self):
        grammar = sexpr.load(bool_yml)
        s = ['til_loob', False]
        self.assertEqual(grammar.matches(s), False)

    def test_12(self):
        grammar = sexpr.load(bool_yml)
        s = ['bool_lit', ['bool_lit', True]]
        self.assertEqual(grammar.matches(s), False)

    def test_13(self):
        grammar = sexpr.load(bool_yml)
        s = ['literal', True]
        self.assertEqual(grammar.matches(s), False)

    def test_14(self):
        grammar = sexpr.load(bool_yml)
        s = ['var_name', "foo"]
        self.assertEqual(grammar.matches(s), False)

    def test_15(self):
        grammar = sexpr.load(bool_yml)
        s = ['var_type', "::object"]
        self.assertEqual(grammar.matches(s), False)

    def test_16(self):
        grammar = sexpr.load(bool_yml)
        s = ['type_ref', "::object"]
        self.assertEqual(grammar.matches(s), True)

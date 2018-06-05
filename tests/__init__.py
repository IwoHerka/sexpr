import os
import sexpr
import unittest
import yaml


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

bool_yml = os.path.join(__location__, 'bool.yml')


class Test(unittest.TestCase):
    def test_load_from_object(self):
        with self.assertRaises(TypeError):
            sexpr.load(object())

    def test_load_from_string(self):
        sexpr.load('string')
        self.assertEqual(True, True)

    def test_load_from_file(self):
        sexpr.load(bool_yml)
        self.assertEqual(True, True)

    def test_load_from_dict(self):
        sexpr.load(dict(key='val'))
        self.assertEqual(True, True)

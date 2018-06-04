import unittest
import sexpr

class Test(unittest.TestCase):
    def test_load_from_object(self):
        with self.assertRaises(TypeError):
            sexpr.load(object())

    def test_load_from_string(self):
        sexpr.load('string')
        self.assertEqual(True, True)

    def test_load_from_file(self):
        sexpr.load('./tests.py')
        self.assertEqual(True, True)

    def test_load_from_dict(self):
        sexpr.load(dict(key='val'))
        self.assertEqual(True, True)

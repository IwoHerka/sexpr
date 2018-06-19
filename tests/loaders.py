import os
import sexpr
import unittest

from sexpr.grammar import Grammar


cd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_path = os.path.join(cd, 'bool.yml')


grammar = sexpr.load('''
    root:
        exp1
    rules:
        exp:
            - exp1
            - exp2
        exp1:
            [ false ]
        expr2:
            [ false ]
''')

class LoadersTest(unittest.TestCase):
    def test_load_from_object(self):
        with self.assertRaises(TypeError):
            sexpr.load(object())

    def test_load_from_string(self):
        raw = '''
            rules:
                exp:
                    - exp1
                    - exp2
                exp1:
                    [ false ]
                expr2:
                    [ true ]
        '''

        grammar = sexpr.load(raw)
        self.assertTrue(isinstance(grammar, Grammar))
        self.assertEqual(grammar.root, 'exp')

        # Test options override default root.
        grammar = sexpr.load(raw, dict(root='exp1'))
        self.assertTrue(isinstance(grammar, Grammar))
        self.assertEqual(grammar.root, 'exp1')

    def test_load_from_dict(self):
        source = {
            'rules': {
                'exp': ['exp1', 'exp2'],
                'exp1': [False],
                'exp2': [True]
            }
        }
        grammar = sexpr.load(source)
        self.assertTrue(isinstance(grammar, Grammar))

        source['root'] = 'exp1'
        # Test options override default root.
        grammar = sexpr.load(source)
        self.assertEqual(grammar.root, 'exp1')

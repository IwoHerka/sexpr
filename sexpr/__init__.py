__version__ = '0.1.7'

from .loaders import load, load_file, load_string, load_dict
from .sexpr import Sexpr, inject, extend
from .print import pprint
from .grammar import Grammar


def register(*args):
    if args and isinstance(args[0], tuple):
        for arg in args:
            Grammar.register(*arg)
    else:
        Grammar.register(*args)

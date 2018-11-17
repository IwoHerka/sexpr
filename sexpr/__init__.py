__version__ = '0.2.0'

from .loaders import load, load_file, load_string, load_dict
from .utils import *
from .sexpr import Sexpr
from .print import pprint
from .grammar import Grammar


def register(*args, **kwargs):
    if args:
        Grammar.register(args)
    else:
        Grammar.register(**kwargs)

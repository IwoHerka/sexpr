__version__ = '0.1.6'

from .loaders import load, load_file, load_string, load_dict
from .sexpr import Sexpr, inject, extend
from .print import pprint
from .grammar import Grammar


def register(tag, tag_class):
    Grammar.register(tag, tag_class)

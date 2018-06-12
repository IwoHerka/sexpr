__version__ = '0.0.1'

from copy import deepcopy
from .loaders import load, load_file, load_string, load_dict
from .sexpr import Sexpr


def inject(sexpr, func):
    copy = deepcopy(sexpr)
    copy.inject(func)
    return copy


def extend(sexpr, func):
    copy = deepcopy(sexpr)
    copy.extend(func)
    return copy

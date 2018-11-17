from __future__ import print_function

from typing import Union

from .sexpr import Sexpr


def pformat(sexp: Union[list, Sexpr], indent: int=None) -> str:
    is_sexp = lambda s: isinstance(s, (list, Sexpr))
    is_long_sexp = lambda s: is_sexp(s) and len(s) > 2

    indent = indent or 0
    off = ' ' * 4 * indent

    def tostr(exp):
        if isinstance(exp, str):
            return "'{}'".format(exp)
        return str(exp)

    if is_long_sexp(sexp) or (is_sexp(sexp) and is_long_sexp(sexp[1])):
        fmt = off + "['%s',\n" % sexp[0]

        for exp in sexp[1:]:
           fmt += '%s,\n' % pformat(exp, indent + 1)

        return fmt[:-2] + '\n' + off + ']'
    else:
        return off + tostr(sexp)


def pprint(sexp):
    print(pformat(sexp))

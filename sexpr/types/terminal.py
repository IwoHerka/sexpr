from types import *
from ..matcher import Matcher


class Terminal(Matcher):
    def __init__(self, value):
        self.value = value

    def pop(self, sexp):
        if sexp and isinstance(sexp, list):
            return sexp[1:] if self.matches(sexp[0]) else None

    def __repr__(self):
        return '(terminal %s)' % self.value


class ValueTerminal(Terminal):
    def matches(self, sexp):
        return self.value == sexp


class RegexpTerminal(Terminal):
    def matches(self, sexp):
        if isinstance(sexp, (str, bytes)):
            return self.value.matches(sexp)
        return False


class TypeTerminal(Terminal):
    def __init__(self, value, strict):
        self.value = value
        self.strict = strict
        self.type_cls = eval(self.value)

    def matches(self, sexp):
        if self.strict:
            return type(sexp) is self.type_cls
        return isinstance(sexp, self.type_cls)

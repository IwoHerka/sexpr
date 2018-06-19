from ..matcher import Matcher


class Terminal(Matcher):
    def __init__(self, value):
        self.value = value

    def pop(self, sexpr):
        try:
            return sexpr[1:] if sexpr and self.matches(sexpr[0]) else None
        except:
            pass

    def __repr__(self):
        return '(terminal %s)' % self.value


class ValueTerminal(Terminal):
    def matches(self, sexp):
        return self.value == sexp


class TypeTerminal(Terminal):
    def __init__(self, value, strict):
        self.value = value
        self.strict = strict

        if self.value == 'function':
            from types import FunctionType
            self.type_cls = FunctionType
        else:
            self.type_cls = eval(self.value)

    def matches(self, sexp):
        if self.strict:
            return type(sexp) is self.type_cls
        return isinstance(sexp, self.type_cls)


class RegexpTerminal(Terminal):
    def matches(self, sexp):
        if isinstance(sexp, (str, bytes)):
            return self.value.matches(sexp)
        return False

from ..matcher import Matcher


class Terminal(Matcher):
    REGEXPR = 'regexpr'
    TYPE    = 'type'
    VALUE   = 'value'

    def __init__(self, value, ttype, strict = None):
        self.value = value
        self.type = ttype
        if self.type == self.TYPE:
            if self.value == 'function':
                from types import FunctionType
                self.type_cls = FunctionType
            else:
                self.type_cls = eval(self.value)
            self.strict = strict

    def matches(self, sexpr):
        if isinstance(sexpr, str) and self.type == self.REGEXPR:
            return self.value.matches(sexpr)
        elif self.type == self.TYPE:
            if self.strict:
                return type(sexpr) is self.type_cls
            return isinstance(sexpr, self.type_cls)

        return self.value == sexpr

    def pop(self, sexpr):
        try:
            return sexpr[1:] if sexpr and self.matches(sexpr[0]) else None
        except:
            pass

    def __repr__(self):
        return '(terminal %s)' % self.value

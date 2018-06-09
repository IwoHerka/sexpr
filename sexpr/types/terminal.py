from ..matcher import Matcher


class Terminal(Matcher):
    REGEXPR = 'regexpr'
    TYPE    = 'type'
    VALUE   = 'value'

    def __init__(self, value, ttype):
        self.value = value
        self.type = ttype
        if self.type == self.TYPE:
            self.type_cls = eval(self.value)

    def matches(self, sexpr):
        if self.type == self.REGEXPR:
            return self.value.matches(sexpr)
        elif self.type == self.TYPE:
            return isinstance(sexpr, self.type_cls)

        return self.value == sexpr

    def eat(self, sexpr):
        return sexpr[1:] if self.matches(sexpr[0]) else None

    def __repr__(self):
        return '(terminal %s)' % self.value

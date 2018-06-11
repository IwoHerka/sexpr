from ..matcher import Matcher


class NonTerminal(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def matches(self, sexpr):
        if sexpr and self.name == sexpr[0]:
            return self.body.matches(sexpr[1:])

    def eat(self, sexpr):
        return sexpr[1:] if sexpr and self.matches(sexpr[0]) else None

    def __repr__(self):
        return '(non-terminal %s)' % self.body

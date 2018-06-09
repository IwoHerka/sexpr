from ..matcher import Matcher


class Rule(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def matches(self, sexpr):
        return self.body.matches(sexpr)

    def eat(self, sexpr):
        return self.body.eat(sexpr)

    def __repr__(self):
        return '(rule %s, %s)' % (self.name, self.body)

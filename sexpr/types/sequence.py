from ..matcher import Matcher


class Sequence(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexpr):
        rest = self.eat(sexpr)
        return rest != None and len(rest) == 0

    def eat(self, sexpr):
        rest = sexpr
        for t in self.terms:
            rest = t.eat(rest)
        return rest

    def __repr__(self):
        return '(seq %s)' % self.terms

from ..matcher import Matcher


class Sequence(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexpr):
        if isinstance(sexpr, list):
            eaten = self.eat(sexpr)
            assert isinstance(eaten, (type(None), list))
            return eaten != None and len(eaten) == 0

    def eat(self, sexpr):
        rest = sexpr
        for t in self.terms:
            rest = t.eat(rest)
            assert isinstance(rest, (type(None), list))
        return rest

    def __repr__(self):
        return '(seq %s)' % self.terms

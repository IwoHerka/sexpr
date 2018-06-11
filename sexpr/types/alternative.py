from ..matcher import Matcher


class Alternative(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexpr):
        return any(t.matches(sexpr) for t in self.terms)

    def eat(self, sexpr):
        for t in self.terms:
            rest = t.eat(sexpr)
            if rest != None:
                return rest

    def __repr__(self):
        return '(alt %s)' % self.terms

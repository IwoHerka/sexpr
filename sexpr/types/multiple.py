from ..matcher import Matcher


class Multiple(Matcher):
    def __init__(self, term, lower, higher = None):
        self.term = term
        self.lower = lower
        self.higher = higher

    def matches(self, sexpr):
        if isinstance(sexpr, list):
            rest = self.eat(sexpr)
            if rest != None:
                return len(rest) == 0

    def eat(self, sexpr):
        i, last = 0, sexpr
        while sexpr and (not self.higher or i < self.higher):
            res = self.term.eat(sexpr)
            if res != None:
                last = res
                i += 1
            sexpr = res
        return last if i >= self.lower else None

    def __repr__(self):
        return '(many %s, %s)' % (self.term, self.lower)

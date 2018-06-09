from ..matcher import Matcher


class Multiple(Matcher):
    def __init__(self, term, lower):
        self.term = term
        self.lower = 1
        self.higher = None

    def matches(self, sexpr):
        if isinstance(sexpr, list):
            eaten = self.eat(sexpr)
            if eaten != None:
                return len(eaten) == 0

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

from ..matcher import Matcher


class Multiple(Matcher):
    def __init__(self, term, lower, higher = None):
        self.term = term
        self.lower = lower
        self.higher = higher

    def matches(self, sexpr):
        if not self.lower:
            return True

        if isinstance(sexpr, list):
            rest = self.pop(sexpr)
            if rest != None:
                return len(rest) == 0
        return False

    def pop(self, sexpr):
        i, last = 0, sexpr
        while sexpr and (not self.higher or i < self.higher):
            res = self.term.pop(sexpr)
            if res != None:
                last = res
                i += 1
            sexpr = res
        return last if i >= self.lower else None

    def __repr__(self):
        return '(multiple %s, %s)' % (self.term, self.lower)

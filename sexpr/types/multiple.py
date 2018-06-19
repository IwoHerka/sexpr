from ..matcher import Matcher


class Multiple(Matcher):
    def __init__(self, term, lower, higher = None):
        self.term = term
        self.lower = lower
        self.higher = higher

    def matches(self, sexp):
        if not self.lower:
            return True

        if isinstance(sexp, list):
            if self.pop(sexp) == []:
                return True

        return False

    def pop(self, sexp):
        i, last = 0, sexp
        while sexp and (not self.higher or i < self.higher):
            res = self.term.pop(sexp)
            if res != None:
                last = res
                i += 1
            sexp = res
        return last if i >= self.lower else None

    def __repr__(self):
        return '(multiple %s, %s)' % (self.term, self.lower)

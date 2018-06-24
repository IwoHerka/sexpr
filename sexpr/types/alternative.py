from ..matcher import Matcher


class Alternative(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexp):
        return any(t.matches(sexp) for t in self.terms)

    def pop(self, sexp):
        for t in self.terms:
            rest = t.pop(sexp)
            if rest != None:
                return rest

    def __repr__(self):
        return '(alt %s)' % self.terms

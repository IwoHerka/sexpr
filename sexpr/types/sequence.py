from ..matcher import Matcher


class Sequence(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexp):
        return self.pop(sexp) == []

    def pop(self, sexp):
        '''
        Notes: Sequence works a bit different than other nodes.
        This method (like others) expectes a list. However, sequence matches
        against the list, whereas other nodes try to match against elements
        of the list.
        '''
        for t in self.terms:
            sexp = t.pop(sexp)
        return sexp

    def __repr__(self):
        return '(seq %s)' % self.terms

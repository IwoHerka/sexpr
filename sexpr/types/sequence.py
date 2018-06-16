from ..matcher import Matcher


class Sequence(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexpr):
        if not isinstance(sexpr, list):
            raise TypeError('Expected a sequence, got {}.'.format(sexpr))
        rest = self.eat(sexpr)
        return rest != None and len(rest) == 0

    def eat(self, sexpr):
        '''
        Notes: Sequence works a bit different than other nodes.
        This method (like others) expectes a list. However, sequence matches
        against the list, whereas other nodes try to match against elements
        of the list.
        '''
        rest = sexpr
        for t in self.terms:
            rest = t.eat(rest)
        return rest

    def __repr__(self):
        return '(seq %s)' % self.terms

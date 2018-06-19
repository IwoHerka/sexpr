from ..matcher import Matcher


class Reference(Matcher):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    @property
    def rule(self):
        return self.grammar.get(self.name, None)

    def matches(self, sexp):
        return self.rule and self.rule.matches(sexp)

    def pop(self, sexp):
        return self.rule.pop(sexp) if self.rule else None

    def __repr__(self):
        return '(ref %s ...)' % self.name

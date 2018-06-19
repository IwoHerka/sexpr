from ..matcher import Matcher


class Reference(Matcher):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    @property
    def rule(self):
        return self.grammar.get(self.name, None)

    def matches(self, sexpr):
        return self.rule and self.rule.matches(sexpr)

    def pop(self, sexpr):
        return self.rule.pop(sexpr) if self.rule else None

    def __repr__(self):
        return '(ref %s ...)' % self.name

from ..matcher import Matcher


class Reference(Matcher):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    @property
    def rule(self):
        return self.grammar[self.name]

    def matches(self, sexpr):
        return self.rule and self.rule.matches(sexpr)

    def eat(self, sexpr):
        if self.rule:
            return self.rule.eat(sexpr)

    def __repr__(self):
        return '(ref %s ...)' % self.name

from ..matcher import Matcher


class Reference(Matcher):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    @property
    def rule(self):
        return self.grammar[self.name] if self.name in self.grammar else None

    def matches(self, sexpr):
        return self.rule and self.rule.matches(sexpr)

    def eat(self, sexpr):
        return self.rule.eat(sexpr) if self.rule else None

    def __repr__(self):
        return '(ref %s ...)' % self.name

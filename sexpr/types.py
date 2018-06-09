from .yaml import Regexpr
from .matcher import Matcher


class Terminal(Matcher):
    def __init__(self, value):
        self.value = value

    def matches(self, sexpr):
        return self._terminal_matches(sexpr)

    def eat(self, sexpr):
        return sexpr[1:] if self.matches(sexpr.first) else None

    def _terminal_matches(self, sexpr):
        if isinstance(self.value, Regexpr):
            return self.value.matches(sexpr)

        return self.value == sexpr

    def __repr__(self):
        return '<Terminal %s>' % self.value


class Alternative(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def __repr__(self):
        return '(alt %s)' % self.terms


class NonTerminal(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return '(non-terminal %s, %s)' % (self.name, self.body)


class Many(Matcher):
    def __init__(self, term, lower):
        self.term = term
        self.lower = lower

    def __repr__(self):
        return '(many %s, %s)' % (self.term, self.lower)


class Reference(Matcher):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    @property
    def rule(self):
        return self.grammar[self.name]

    def __repr__(self):
        return '(ref %s, %s)' % (self.name, self.rule)


class Rule(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return '(rule %s, %s)' % (self.name, self.body)


class Sequence(Matcher):
    def __init__(self, term):
        self.term = term

    def __repr__(self):
        return '(seq %s)' % self.term

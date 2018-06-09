from .yaml import Regexpr
from .matcher import Matcher


class Terminal(Matcher):
    REGEXPR = 'regexpr'
    TYPE    = 'type'
    VALUE   = 'value'

    def __init__(self, value, ttype):
        self.value = value
        self.type = ttype
        if self.type == self.TYPE:
            self.type_cls = eval(self.value)

    def matches(self, sexpr):
        if self.type == self.REGEXPR:
            return self.value.matches(sexpr)
        elif self.type == self.TYPE:
            return isinstance(sexpr, self.type_cls)

        return self.value == sexpr

    def eat(self, sexpr):
        return sexpr[1:] if self.matches(sexpr[0]) else None

    def __repr__(self):
        return '(terminal %s)' % self.value


class Alternative(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexpr):
        return any(t.matches(sexpr) for t in self.terms)

    def eat(self, sexpr):
        for t in self.terms:
            res = t.eat(sexpr)
            if res != None:
                return res

    def __repr__(self):
        return '(alt %s)' % self.terms


class NonTerminal(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def matches(self, sexpr):
        if isinstance(sexpr, list) and self.name == sexpr[0]:
            return self.body.matches(sexpr[1:])

    def eat(self, sexpr):
        return sexpr[1:] if self.matches(sexpr[0]) else None

    def __repr__(self):
        return '(non-terminal %s, %s)' % (self.name, self.body)


class Many(Matcher):
    def __init__(self, term, lower):
        self.term = term
        self.lower = 1
        self.higher = None

    def matches(self, sexpr):
        if isinstance(sexpr, list):
            eaten = self.eat(sexpr)
            if eaten != None:
                return len(eaten) == 0

    def eat(self, sexpr):
        i, last = 0, sexpr
        while sexpr and (not self.higher or i < self.higher):
            res = self.term.eat(sexpr)
            if res != None:
                last = res
                i += 1
            sexpr = res
        return last if i >= self.lower else None

    def __repr__(self):
        return '(many %s, %s)' % (self.term, self.lower)


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


class Rule(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def matches(self, sexpr):
        return self.body.matches(sexpr)

    def eat(self, sexpr):
        return self.body.eat(sexpr)

    def __repr__(self):
        return '(rule %s, %s)' % (self.name, self.body)


class Sequence(Matcher):
    def __init__(self, terms):
        self.terms = terms

    def matches(self, sexpr):
        if isinstance(sexpr, list):
            eaten = self.eat(sexpr)
            assert isinstance(eaten, (type(None), list))
            return eaten != None and len(eaten) == 0

    def eat(self, sexpr):
        rest = sexpr
        for t in self.terms:
            rest = t.eat(rest)
            assert isinstance(rest, (type(None), list))
        return rest

    def __repr__(self):
        return '(seq %s)' % self.terms

from ..matcher import Matcher


class Rule(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def matches(self, sexp):
        return self.body.matches(sexp)

    def pop(self, sexp):
        return self.body.pop(sexp)

    def __repr__(self):
        return '(rule %s, %s)' % (self.name, self.body)

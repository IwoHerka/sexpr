from copy import deepcopy


def inject(sexpr, func):
    body = func(*sexpr[1:] if sexpr else None)
    body = body if isinstance(body, tuple) else (body, )
    return [sexpr[0], *body]


def extend(sexpr, func):
    return func(sexpr)


class Sexpr(object):
    def __init__(self, sexpr, grammar):
        self.sexpr = sexpr
        self.grammar = grammar

    def __getitem__(self, index):
        return self.sexpr[index]

    @property
    def tag(self):
        return self.sexpr[0] if self.sexpr else None

    @property
    def body(self):
        return self.sexpr[1:] if self.sexpr else None

    def inject(self, func):
        self.sexpr = inject(self.sexpr, func)

    def extend(self, func):
        self.sexpr = extend(self.sexpr, func)

    def copy(self):
        return deepcopy(self.body)

    def __repr__(self):
        return '(sexpr {})'.format(self.sexpr)

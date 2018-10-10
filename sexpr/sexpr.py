from copy import deepcopy


def inject(sexpr, func):
    body = func(*sexpr[1:] if sexpr else None)
    body = body if isinstance(body, tuple) else (body, )
    return [sexpr[0], *body]


def extend(sexpr, func):
    return func(sexpr)


class Sexpr(object):
    def __init__(self, sexpr, grammar=None, **kwargs):
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
        return repr(self.sexpr)

    def __str__(self):
        return pformat(self.sexpr)

    def with_insert(self, index, sexpr):
        self.sexpr.insert(index, sexpr)
        return self

    def with_replace(self, index, sexpr):
        self.sexpr[index] = sexpr
        return self

    def find_child(self, tag):
        for s in self.sexpr:
            if s.tag == tag:
                return s
            else:
                candidate = self.find_child(s)

                if candidate and candidate.tag == tag:
                    return candidate

    def find_and_replace(self, test, replace):
        for i, c in enumerate(self.body):
            if test(c):
                self.sexpr[i + 1] = replace(c)

            elif isinstance(c, Sexpr):
                self.sexpr[i + 1] = c.find_and_replace(test, replace)

        return self


from .print import pformat

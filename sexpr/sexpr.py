class Sexpr(object):
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def __getitem__(self, index):
        return self.sexpr[index]

    @property
    def tag(self):
        return self.sexpr[0] if self.sexpr else None

    @property
    def body(self):
        return self.sexpr[1:] if self.sexpr else None

    def inject(self, func):
        body = func(*self.body)
        body = body if isinstance(body, tuple) else (body, )
        self.sexpr = [self.tag, *body]

    def extend(self, func):
        self.sexpr = func(self.sexpr)

    def __repr__(self):
        return str(self.sexpr)

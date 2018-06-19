from .matcher import Matcher
from .sexpr import Sexpr

_str_format = '''
(grammar
    path:
        {}
    root:
        {}
    rules:
        {}
)'''


class Grammar(Matcher):
    def __init__(self, source, options = None):
        rules = source.get('rules', {})

        self.options = options or {}
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(rules)

        try:
            self.root = self.options.get('root', None)
            self.root = self.root or list(rules.items())[0][0]
        except IndexError:
            raise ValueError('Cannot load root node. Grammar is ill-formed.')

    def sexpr(self, sexpr):
        if isinstance(sexpr, Sexpr):
            return sexpr
        return Sexpr(sexpr, self) if self.matches(sexpr) else None

    def __repr__(self):
        print_rule = lambda r: '{} = {}'.format(r.name, r.body)

        return _str_format.format(
            self.path or '-',
            self.root,
            '\n        '.join(print_rule(r) for r in self.rules.values())
        )

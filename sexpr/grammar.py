from .matcher import Matcher
from .sexpr import Sexpr
from .utils import merge_options

grammar_str_form = \
'''(grammar
    path:
        {}
    root:
        {}
    rules:
        {}
)'''


class Grammar(Matcher):
    default_options = {}

    def __init__(self, source, options = None):
        rules = source.get('rules', {})

        self.options = merge_options(self.default_options, options or {})
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(rules)

        try:
            self.root = self.options.get('root', list(rules.items())[0][0])
        except IndexError:
            raise ValueError('Cannot load root node. Grammar is ill-formed.')

    def sexpr(self, sexpr):
        if isinstance(sexpr, Sexpr):
            return sexpr
        return Sexpr(sexpr, self) if self.matches(sexpr) else None

    def __repr__(self):
        print_rule = lambda r: '{} = {}'.format(r.name, r.body)

        return grammar_str_form.format(
            self.path if self.path else '-',
            self.root,
            '\n        '.join(print_rule(r) for r in self.rules.values())
        )

    def __str__(self):
        return self.__repr__()

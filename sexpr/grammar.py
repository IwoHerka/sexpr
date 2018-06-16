from .matcher import Matcher
from .sexpr import Sexpr
from .utils import merge_options

NoneType = type(None)


class Grammar(Matcher):
    default_options = {}
    default_parser_options = {}

    def __init__(self, source, options = None):
        rules = source.get('rules', {})

        self.options = merge_options(self.default_options, options or {})
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(rules)

        try:
            self.root = self.options.get('root', list(rules.items())[0][0])
        except IndexError:
            self.root = None

    def sexpr(self, sexpr):
        if isinstance(sexpr, Sexpr):
            return sexpr
        return Sexpr(sexpr, self) if self.matches(sexpr) else None

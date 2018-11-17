from typing import Dict

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
    registered_tags: Dict[str, type] = {}

    @classmethod
    def register(cls, *args, **kwargs):
        items = args if args else kwargs.items()

        for tag, tag_class in items:
            cls.registered_tags[tag]  = tag_class

    def __init__(self, source, options = None):
        self.options = options or {}
        self.yaml = source.get('rules', {})
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(self.yaml)

        try:
            self.root = self.options.get('root', None)
            self.root = self.root or list(self.yaml.items())[0][0]
            self.top_tags = self.yaml.get(self.root, [])
        except IndexError:
            raise ValueError('Cannot load root node. Grammar is ill-formed.')


    def sexpr(self, sexpr):
        if isinstance(sexpr, list) and sexpr and sexpr[0] in self.rules:
            sexpr = [sexpr[0]] + [self.sexpr(n) for n in sexpr[1:]]
            return self.tag_node(sexpr)

        return sexpr

    def tag_node(self, sexpr):
        if isinstance(sexpr, Sexpr):
            return sexpr

        elif sexpr and sexpr[0] in self.registered_tags:
            return self.registered_tags[sexpr[0]](sexpr, self)

        return Sexpr(sexpr, self)

    def __repr__(self):
        print_rule = lambda r: '{} = {}'.format(r.name, r.body)

        return _str_format.format(
            self.path or '-',
            self.root,
            '\n        '.join(print_rule(r) for r in self.rules.values())
        )

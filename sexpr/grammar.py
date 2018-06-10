from .matcher import Matcher
from .utils import merge_options

NoneType = type(None)


class Grammar(Matcher):
    default_options = {}
    default_parser_options = {}

    def __init__(self, source, options = None):
        self.options = merge_options(self.default_options, options or {})
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(source.get('rules', {}))
        # TODO: Rewrite this ugliness.
        self.root = self.options.get('root', list(source['rules'].items())[0][0])

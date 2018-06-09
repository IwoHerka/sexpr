from .utils import merge_options
from .matcher import Matcher

NoneType = type(None)


class Grammar(Matcher):
    default_options = {}
    default_parser_options = {}

    def __init__(self, source, options = None):
        self.options = merge_options(self.default_options, options or {})
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(source.get('rules', {}))

    # def parse(self, source, options = None):
    #     options = merge_options(self.default_parser_options, options or {})
    #     return parser.parse(source, options)

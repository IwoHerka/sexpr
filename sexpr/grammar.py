import re

from .utils import merge_options
from .yaml import Regexpr

NoneType = type(None)


class Grammar(object):
    re_many = re.compile('([\?\+\*])$')
    re_reference = re.compile('^[a-z][a-z_]+$')
    re_terminal = re.compile('^::([A-Z][a-z]*.*)$')
    default_options = {}

    def compile_rules(self, rules):
        return {k: self.compile_rule(k, v) for k, v in rules.items()}

    def compile_rule(self, name, body):
        rule = self.compile_body(body)
        if not (isinstance(body, Terminal) or isinstance(body, Alternative)):
            rule = NonTerminal(name, rule)
        return Rule(name, rule)

    def compile_body(self, body, grammar = None):
        grammar = grammar or self
        if isinstance(body, Regexpr):
            return
        elif isinstance(body, bool) or isinstance(body, NoneType):
            return
        elif isinstance(body, list):
            return
        elif isinstance(body, str):
            if self.re_many.match(body):
                pass

    def __init__(self, source, options = None):
        self.options = merge_options(self.default_options, options or {})
        self.path = self.options.get('path', None)
        self.rules = self.compile_rules(source.get('rules', {}))

    def parse(self, source, options = None):
        pass

    def sexpr(self, source):
        pass

    def matches(self, sexpr):
        pass

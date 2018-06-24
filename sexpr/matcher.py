import re

from .yaml import Regexpr

# Mapping from Backus-Naur repetition operator symbols to tuples
# representing bounds.
#
# Keys: symbol (str): BNF repetition operator symbol (?, +, *)
# Values: (int, int/NoneType): Tuple representing min/max bounds.
#         None should be interpreted as infinity.
factor_operator = {
    '?': (0, 1),
    '+': (1, None),
    '*': (0, None)
}

# Mapping from strictness operator symbol to boolean specifying whether
# type checking should be strict.
factor_strictness = {
    '=': True,
    '~': False
}

# Compiled regular expressions objects for symbol matching (see `compile_str`).
re_many      = re.compile('.*[\?\+\*]')
re_reference = re.compile('[a-z][a-z_]+')
re_terminal  = re.compile('[=~]([a-zA-z][a-z]*.*)')


class Matcher(object):
    def __getitem__(self, key):
        return self.rules[key]

    def __contains__(self, key):
        return key in self.rules

    def get(self, key, default = None):
        return self.rules.get(key, default)

    @property
    def root_rule(self):
        return self.rules[self.root]

    def matches(self, sexp):
        return self.root_rule.matches(sexp)

    def compile_rules(self, rules):
        return {k: self.compile_rule(k, v) for k, v in rules.items()}

    def compile_rule(self, name, body):
        rule = self.compile_body(body)

        if not (isinstance(rule, Terminal) or isinstance(rule, Alternative)):
            rule = NonTerminal(name, rule)

        return Rule(name, rule)

    def compile_body(self, body, grammar = None):
        grammar = grammar or self

        if isinstance(body, bool):
            return ValueTerminal(body)

        elif isinstance(body, Regexpr):
            return RegexpTerminal(body)

        elif isinstance(body, list):
            return self.compile_list(body, grammar)

        elif isinstance(body, str):
            return self.compile_str(body, grammar)

        raise TypeError('Unsupported expression: %s of type: %s' % (body, type(body)))

    def compile_list(self, li, grammar):
        if len(li) == 1 and isinstance(li[0], list):
            return Sequence([self.compile_body(b, grammar) for b in li[0]])

        return Alternative([self.compile_body(b, grammar) for b in li])

    def compile_str(self, string, grammar):
        if re_many.match(string):
            bounds = factor_operator[string[-1]]
            return Multiple(self.compile_body(string[0:-1]), *bounds)

        elif re_reference.match(string):
            return Reference(string, grammar)

        elif re_terminal.match(string):
            strict = factor_strictness[string[0]]
            return TypeTerminal(string[1:], strict)


from .types import *

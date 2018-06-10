import re

from .yaml import Regexpr


'''
Mapping from Backus-Naur repetition operator symbols to tuples
representing bounds.

Keys: symbol (str): BNF repetition operator symbol (?, +, *)
Values: (int, int/NoneType): Tuple representing min/max bounds.
        None should be interpreted as infinity.
'''
factor_operator = {
    '?': (0, 1),
    '+': (1, None),
    '*': (0, None)
}

'''
Compiled regular expressions objects for symbol matching.
'''
re_many      = re.compile('.*[\?\+\*]')
re_reference = re.compile('[a-z][a-z_]+')
re_terminal  = re.compile('::([a-zA-z][a-z]*.*)')

NoneType = type(None)


class Matcher(object):
    def __getitem__(self, key):
        return self.rules[key]

    @property
    def root_rule(self):
        return self.rules[self.root]

    def matches(self, sexpr):
        return self.root_rule.matches(sexpr)

    def compile_rules(self, rules):
        return {k: self.compile_rule(k, v) for k, v in rules.items()}

    def compile_rule(self, name, body):
        rule = self.compile_body(body)

        if not isinstance(rule, Terminal) and not isinstance(rule, Alternative):
            rule = NonTerminal(name, rule)

        return Rule(name, rule)

    def compile_body(self, body, grammar = None):
        grammar = grammar or self

        if isinstance(body, (bool, NoneType)):
            return Terminal(body, Terminal.VALUE)

        elif isinstance(body, Regexpr):
            return Terminal(body, Terminal.REGEXPR)

        elif isinstance(body, list):
            if len(body) == 1 and isinstance(body[0], list):
                return Sequence([self.compile_body(b, grammar) for b in body[0]])

            return Alternative([self.compile_body(b, grammar) for b in body])

        elif isinstance(body, str):
            if re_many.match(body):
                bounds = factor_operator[body[-1]]
                return Multiple(self.compile_body(body[0:-1]), *bounds)

            elif re_reference.match(body):
                return Reference(body, grammar)

            elif re_terminal.match(body):
                return Terminal(body[2:], Terminal.TYPE)

        raise TypeError('Unsupported expression: %s of type: %s' % (body, type(body)))


from .types import *

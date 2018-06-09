import re

from .yaml import Regexpr

NoneType = type(None)


class Matcher(object):
    re_many = re.compile('.*[\?\+\*]')
    re_reference = re.compile('[a-z][a-z_]+')
    re_terminal = re.compile('::([a-zA-z][a-z]*.*)')

    def __getitem__(self, key):
        return self.rules[key]

    def root_rule(self):
        return self.rules['root']

    def matches(self, sexpr):
        return self.root_rule().matches(sexpr)

    def compile_rules(self, rules):
        return {k: self.compile_rule(k, v) for k, v in rules.items()}

    def compile_rule(self, name, body):
        rule = self.compile_body(body)

        if not isinstance(rule, Terminal) and not isinstance(rule, Alternative):
            rule = NonTerminal(name, rule)

        return Rule(name, rule)

    def compile_body(self, body, grammar = None):
        print(body, type(body))
        grammar = grammar or self

        if isinstance(body, (bool, NoneType, Regexpr)):
            return Terminal(body)
        elif isinstance(body, list):
            return Alternative([self.compile_body(b, grammar) for b in body])
        elif isinstance(body, str):
            if self.re_many.match(body):
                return Many(self.compile_body('bool_expr'), '+')
            elif self.re_reference.match(body):
                return Reference(body, grammar)
            elif self.re_terminal.match(body):
                found = body[2:]
                return Terminal(found)

        raise TypeError('Unsupported expression: %s' % body)



from .types import Terminal, Alternative, NonTerminal, Reference, Rule, Many

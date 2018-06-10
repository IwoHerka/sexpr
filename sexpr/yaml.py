import re

import yaml


class Regexpr(yaml.YAMLObject):
    yaml_tag = u'!regexpr'

    def __init__(self, pattern):
        self.pattern = pattern
        self.re_pattern = re.compile(pattern)

    def matches(self, string):
        return self.re_pattern.match(string)

    @classmethod
    def from_yaml(cls, loader, node):
        return Regexpr(node.value)

    def __repr__(self):
        return '(regex %s)' % self.pattern

import re
from typing import TYPE_CHECKING, Match, Optional

import yaml

if TYPE_CHECKING:
    from yamlloader.ordereddict.loaders import Loader
    from yaml.nodes import ScalarNode


class Regexpr(yaml.YAMLObject):
    yaml_tag = u'!regexpr'

    @classmethod
    def from_yaml(cls, loader: 'Loader', node: 'ScalarNode') -> 'Regexpr':
        return Regexpr(node.value)

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.re_pattern = re.compile(pattern)

    def __repr__(self):
        return '(regex %s)' % self.pattern

    def matches(self, string: str) -> Optional[Match[str]]:
        return self.re_pattern.match(string)

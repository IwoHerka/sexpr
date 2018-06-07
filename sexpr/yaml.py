import yaml


class Regexpr(yaml.YAMLObject):
    yaml_tag = u'!regexpr'

    def __init__(self, pattern):
        self.pattern = pattern

    @classmethod
    def from_yaml(cls, loader, node):
        return Regexpr(node.value)

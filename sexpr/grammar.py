from . import utils


class Grammar(object):
    default_options = {}

    def __init__(self, rules, options = None):
        self.options = utils.merge_options(self.default_options, options or {})
        self.raw_rules = rules

    def parse(self, source, options = None):
        pass

    def sexpr(self, source):
        pass

    def match(self, sexpr):
        pass


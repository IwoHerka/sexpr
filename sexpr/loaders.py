import os
import yaml
import yamlloader

from .grammar import Grammar
from .yaml import Regexpr


def regexpr_constructor(loader, node):
    return Regexpr(node.value)

yaml.add_constructor(u'!regexpr', regexpr_constructor)


def load(source, options = None):
    if isinstance(source, str):
        if os.path.exists(source):
            return load_file(source, options)
        else:
            return load_string(source, options)

    elif isinstance(source, dict):
        return load_dict(source, options)

    else:
        raise TypeError('Attempted to load grammar from '
                        'invalid source: %s' % type(source))


def load_file(path, options = None):
    with open(path) as f:
        options = options or {}
        options.update({'path': path})
        return load_string(f.read(), options)


def load_string(string, options):
    return load_dict(yaml.load(string, Loader=yamlloader.ordereddict.Loader), options)


def load_dict(dictionary, options):
    # for k, v in dictionary['rules'].items():
    #     print('%s: %s' % (k, v))
    # print('---------------------------')
    return Grammar(dictionary, options)

import os
import yaml

from .grammar import Grammar


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


def load_file(path, options):
    with open(path) as f:
        return load_string(f.read(), options)


def load_string(string, options):
    return load_dict(yaml.safe_load(string), options)


def load_dict(dictionary, options):
    Grammar(dictionary, options)

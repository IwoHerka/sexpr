import os

import yaml
import yamlloader

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


def load_file(path, options = None):
    with open(path) as f:
        options = options or {}
        options.update(dict(path=path))
        return load_string(f.read(), options)


def load_string(string, options = None):
    return load_dict(yaml.load(string, Loader=yamlloader.ordereddict.Loader), options)


def load_dict(dictionary, options = None):
    options = options or {}
    if 'root' in dictionary and not 'root' in options:
        # Move 'root' from source to options.
        options.update(root = dictionary['root'])
    return Grammar(dictionary, options)

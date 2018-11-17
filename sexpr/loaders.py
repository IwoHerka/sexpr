import os
from typing import Any, Dict, Optional

import yaml
import yamlloader

from .grammar import Grammar

MaybeOptions = Optional[Dict[str, Any]]


def load(source: str, options: MaybeOptions=None) -> Grammar:
    if isinstance(source, str):
        if _is_pathname_valid(source):
            return load_file(source, options)
        else:
            return load_string(source, options)

    elif isinstance(source, dict):
        return load_dict(source, options)

    else:
        raise TypeError(
            'Attempted to load grammar from invalid source: %s' % type(source)
        )


def load_file(path: str, options: MaybeOptions=None) -> Grammar:
    with open(path) as f:
        options = options or {}
        options.update(dict(path=path))
        return load_string(f.read(), options)


def load_string(string: str, options: MaybeOptions=None) -> Grammar:
    loaded = yaml.load(string, Loader=yamlloader.ordereddict.Loader)
    return load_dict(loaded, options)


def load_dict(dictionary: dict, options: MaybeOptions=None) -> Grammar:
    options = options or {}

    if 'root' in dictionary and not 'root' in options:
        # Move 'root' from source to options.
        options.update(root = dictionary['root'])

    return Grammar(dictionary, options)


def _is_pathname_valid(pathname: str) -> bool:
    try:
        os.stat(pathname)
    except os.error:
        return False

    return True

import os


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

def load_file(source, options):
    pass

def load_string(source, options):
    pass

def load_dict(source, options):
    pass

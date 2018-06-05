def merge_options(first, second):
    '''
    Merge two dictionaries by overriding values from the first one with
    values from the second one. Python 2.* compatible.
    '''
    third = first.copy()
    third.update(second)
    return third

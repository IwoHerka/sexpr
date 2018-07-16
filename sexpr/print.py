from __future__ import print_function


def pformat(sexp, indent = None):
    indent = indent or 0
    off = ' ' * 4 * indent

    if sexp and (isinstance(sexp, list) and
            (len(sexp) > 2 or isinstance(sexp[1], list))):
        fmt = off + "['%s'\n" % sexp[0]

        for exp in sexp[1:]:
           fmt += '%s,\n' % pformat(exp, indent + 1)

        return fmt[:-2] + '\n' + off + ']'
    else:
        return off + str(sexp)


def pprint(sexp):
    print(pformat(sexp))

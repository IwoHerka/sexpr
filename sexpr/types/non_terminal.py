from ..matcher import Matcher


class NonTerminal(Matcher):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def matches(self, sexpr):
        '''
        Body of a non-terminal is always a :class:`Sequence`. For an s-expr
        to match, it must be of the form::

            ['name'] + [sexpr-0, ..., sexpr-n]

        where the first list contains a name of the non-terminal,
        and the second one matches its body sequence.
        '''
        if isinstance(sexpr, list) and self.name == sexpr[0]:
            return self.body.matches(sexpr[1:])
        return False

    def pop(self, sexpr):
        '''
        Assuming *s-expr* of the form::

            [sexpr-0, ..., sexpr-n]

        For an *sexpr-0* to be popped by a non-terminal, it must match
        that of required by :meth:`~NonTerminal.matches`. If it doesn't,
        None is returned.
        '''
        return sexpr[1:] if sexpr and self.matches(sexpr[0]) else None

    def __repr__(self):
        return '(non-terminal %s)' % self.body

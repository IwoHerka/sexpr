Utilities
=========

:class:`~sexpr.sexpr.Sexpr` is a utility wrapper class for s-expressions.
It provides some convienience properties, such as *tag*, *body* and
in-place versions of *inject* and *extend*.
``Sexpr`` subclasses list.

.. code-block:: python

    sexp = grammar.sexpr(['and', ['literal', True], ['literal', False]])
    # or Sexpr(<expression>, grammar)

    sexpr.tag
    # = 'and'

    sexpr.body
    # = ['literal', True], ['literal', False']

    sexp.inject(lambda exp: ['not', exp])
    # = ['not', ['and', ['literal', True], ['literal', False]]]

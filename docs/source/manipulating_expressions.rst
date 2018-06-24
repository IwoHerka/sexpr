Manipulating S-expressions
==========================

Transformation of s-expression is implemented with `inject` and `extend` functions.

`inject` is used to inject (or replace) children in an expression. It expects
a function which is called with children of the expression in the first
argument and returns new s-expression with the expression's tag and body
returned from the function:

.. code-block:: python

    sexp = ['and', ['lit', True], ['lit', False]]

    apply_or = lambda left, right: ['or', left, right]

    inject(sexp, apply_or)
    # = ['and', ['or', ['lit', True], ['lit', False]]]

Similarly, `extend` is used to extend the expression (or replace its tag):

.. code-block:: python

    extend(['lit', True], lambda exp: ['not', not exp])
    # = ['not', ['lit', False]]]

    # `Sexpr` implements sequence type. Therefore, to replace expression's tag it's enough:

    extend(['lit', True], lambda exp: ['literal', exp[1:])
    # = ['literal', True]

If an expression has multiple children, argument function must expect
and return multiple arguments. In case of anonymous lambda, this means
than it must return a tuple:

.. code-block:: python

    inject(exp, lambda first, second: (not first, not second))

Otherwise, Python's interpreter would take the second return value as an
argument to `inject`.

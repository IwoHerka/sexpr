Defining Grammar
================

Grammar in **sexpr** is defined in YAML, data serialisation language.
If you're looking for a quick primer, check out: `Learn YAML in Y minutes
<https://learnxinyminutes.com/docs/yaml/>`_.
Don't worry though, you don't need to know it to you define a grammar.
Syntax is very simple. Before we dive into concretes,
however, we must agree on some basic lingo.

Basic notions
-------------

Notation used in **sexpr** it very similar to `ENBF
<https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form>`_.
Every grammar is defined in terms or *rules*. Rules can be
*terminal* or *non-terminal*. Simply put, non-terminal rules
are all rules that correspond to concrete nodes in the end s-expression,
whereas terminal rules always define substitution.

Therefore, in an expression `(add 1 2)` of the grammar::

    rules:
        op:
            - add
        add:
            - [ val ]
        val:
            [ 1, 2 ]

`add` is a non-terminal and `val` is a terminal rule. Please note that, by that
definition, root rule `op` is also a terminal rule. Moreover, as a consequence
of this definition, names of terminal rules defined in YAML are the only
ones to appear in the end s-expression.

Finally, in the above example, literals *1* and *2* are called *terminal symbols*.
They are the bottom of the hierarchy and cannot be substitued for anything
else.

Grammar in YAML
---------------

With that out of the way, writing actual grammar is pretty straightforward.
Each grammar must start with a **root rule**. Root rule is a top-level rule
definining what *every* valid s-expression in the grammar must be.
For example, in the grammar of predicates, root rule would simply be "predicate"::

    rules:
        predicate:
            - tautology
            - contradiction
            - bool_or
            - bool_and
            - bool_not

Typically, like in this example, root rule is an alternative
(:class:`~sexpr.types.Alternative`). It says
that every predicate is a tautology or a contradiction or an alternation or
a conjunction or a negative.

Next in line are non-terminal rules. In YAML, they always have the form::

    <name>:
        - [ <expr><modifier>?[, <expr><modifier>?]* ]

For example::

    one_or_more:
        - [ expr+ ]      # e.g. ['tag', 1, 2, 3]
    zero_or_more:
        - [ expr* ]      # e.g. ['tag'] or ['tag', 1, 2, 3, 4]
    exactly_two:
        - [ expr, expr ] # e.g. ['tag', 1, 2]
    exactly_one:
        - [ expr ]       # e.g. ['tag', 1]
    optional:
        - [ 'expr?' ]    # e.g. ['tag'] or ['tag', 1]

In the example above, '?', '+' and '*' are so-called repetition modifiers.
Because of restrictions of YAML syntax, optional terms must be wrapped
in quotation marks.

Terminal Rules
---------------

In **sexpr**, terminal rules can be object literals (e.g. ``7`` or ``[1, 2, 3]``),
regular expressions (compiled using standard ``re`` module) or Python's
types:

.. code-block:: python

    lucky_number:
        777
    varname:
        !regexpr '[a-zA-Z_]+' # Parsed using Python's re module.
    sequence:
        '~list' # Any descendant of list.
    dictionary:
        '=dict' # Strict check. This will match dict() but not OrderedDict().

When terminal rules are object literals, values in s-expression are compared
with Python's ``==`` operator. In case of regular expressions (which are
are prefix with ``!regexpr`` directive), terminal
values must be strings or ``bytes`` and match defined pattern. Finally,
in case of types, values are matches using ``isinstance`` and ``type()``
bultins (for "~" and "=" modifiers respectively). Type modifiers are
required.

Verifing S-expressions
======================

Validation of s-expressions could not be simpler. You just pass the expression
and receive a boolean in return:

.. code-block:: python

    grammar = sexpr.load('sql.yml')

    exp = ['select',
              ['set_quantifier', "all"],
              ['from_clause',
                  ['table_as',
                      ['table_name', 'suppliers'],
                      ['range_var_name', "s1"]
                  ]
              ],
              ['where_clause',
                  ['tautology', true]
              ]
          ]

    grammar.matches(exp)
    # = True

    grammar.matches(['+', 1, 2])
    # = False (oops, wrong grammar)

For simplicity and convienience, s-expressions are constructed with lists.
Everything other than a list is assumed to be a terminal. You can, however,
use a subclass of the list.

.. warning::

    As a consequence of using lists as containers for s-expressions,
    **terminal** lists (if they are allowed by your grammar)
    with the same grammar as expressions they are embedded
    in can easily produce false results. As rare as such situation is,
    in order to avoid it altogheter it's best to convert such lists to tuples
    (or wrap them with a terminal).

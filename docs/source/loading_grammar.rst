Loading Grammar
===============

Having defined a grammar, loading it is a breeze. You have three options:

Loading from YAML
-----------------

.. code-block:: python

    import sexpr
    grammar = sexpr.load('./predicate.yml')

Loading from a string
---------------------

.. code-block:: python

    import sexpr

    yml = '''
        rules:
            expr:
                - first
                - second
            first:
                - [ True ]
            second:
                - [ False ]
    '''

    grammar = sexpr.load(yml)

Loading from a dictionary
-------------------------

.. code-block:: python

    import sexpr

    dictionary = {
        'root': 'expr',
        'rules': {
            'expr': ['first', 'second'],
            'first': [[True]],
            'second': [[False]]
        }
    }

    grammar = sexpr.load(dictionary)

Each grammar must have a *root* rule. Normally, it is the first rule in your YAML.
When loading from a dictionary you must specify the name yourself. There are a
couple of options. You can either use `OrderedDict`, add ``"root"`` key to
your dictionary or provide it in the options like so:

.. code-block:: python

    sexpr.load(dictionary, options = {'root': 'expr'})

And there you go. You can quickly preview your grammar by printing it:

.. code-block:: python

    (grammar
        path:
            -
        root:
            expr
        rules:
            first = (non-terminal (seq [(terminal True)]))
            expr = (alt [(ref first ...), (ref second ...)])
            second = (non-terminal (seq [(terminal False)]))
    )

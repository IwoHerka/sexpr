<img align="right" height="400" src="https://raw.githubusercontent.com/IwoHerka/sexpr/master/lisp_theory_and_practice.jpg">

## S-expression toolkit for Python

[![Build Status](https://travis-ci.org/IwoHerka/sexpr.svg?branch=master)](https://travis-ci.org/IwoHerka/sexpr)
[![Coverage Status](https://coveralls.io/repos/github/IwoHerka/sexpr/badge.svg?branch=master)](https://coveralls.io/github/IwoHerka/sexpr?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/dc96c6c6dc5141c4ba956bedb35c120f)](https://www.codacy.com/app/IwoHerka/sexpr?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=IwoHerka/sexpr&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/bd380c4f4a9848a87a20/maintainability)](https://codeclimate.com/github/IwoHerka/sexpr/maintainability)

**sexpr** is small and compact toolkit for working with s-expressions in Python.

If want a quick summary of the features have a look at the README and when ready
check out full <a href="http://sexpr.readthedocs.io/en/latest/">documentation</a>.
Additionally, as an example usage, take a look at
<a href="https://github.com/IwoHerka/auk">auk</a> - micro-package for
compiling s-expression into predicate functions.

<br/>

In short, **sexpr** is:

#### 1. Meta-syntax notation for grammar definition in YAML, similar to EBNF:

```yaml
rules:
    predicate:
        - bool_not
        - bool_and
        - bool_or
        - bool_lit
    bool_not:
        - [ predicate ]
    bool_and:
        - [ predicate, predicate ]
    bool_or:
        - [ predicate+ ]
    bool_lit:
        - [ truth_value ]
    truth_value:
        - true
        - false
```

Supported notation allows to:

  1. Describe repetition of terms with repetition modifers: `?` (optional), `+` (one or more) and `*` (zero or more).
  2. Define allowable terminal values in terms of literals, regular expressions and Python's types:

```yaml
lucky_number:
    777
varname:
    !regexpr '[a-zA-Z_]+' # Parsed using Python's re module.
sequence:
    '~list' # Any descendant of list.
dictionary:
    '=dict' # Strict check. This will match dict() but not OrderedDict().
```

You can load grammar from YAML, string or dict:

```python
grammar = sexpr.load('''
    rules:
        root_rule:
            - some_rule
            - other_rule
        some_rule:
            [ false ]
        other_rule:
            [ false ]
''')

# Every grammar must have a root node.
# You can point to the root explicitly with 'root' key.
# Otherwise, root is taken as the first rule in the definition.

grammar.root_node
# (rule root_rule, (alt [(ref some_rule ...), (ref other_rule ...)]))
```


#### 2. Validation of s-expressions against defined grammar:

```python
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

```

#### 3. Minimal (but sufficient) manipulation framework

Transformation is implemented with `inject` and `extend` functions:

`inject` is used to inject (or replace) children in an expression. It expects
a function which is called with children of the expression in the first
argument and returns new s-expression with the expression's tag and body
returned from the function:

```python
sexp = ['and', ['lit', True], ['lit', False]]

apply_or = lambda left, right: ['or', left, right]

inject(sexp, apply_or)
# = ['and', ['or', ['lit', True], ['lit', False]]]
```

Similarly, `extend` is used to extend the expression (or replace its tag):

```python
extend(['lit', True], lambda exp: ['not', not exp])
# = ['not', ['lit', False]]]

# `Sexpr` implements sequence type. Therefore, to replace expression's tag it's enough:

extend(['lit', True], lambda exp: ['literal', exp[1:])
# = ['literal', True]
```

If an expression has multiple children, argument function must expect
and return multiple arguments. In case of anonymous lambda, this means
than it must return a tuple:

```python
inject(exp, lambda first, second: (not first, not second))
```

Otherwise, Python's interpreter would take the second return value as an
argument to `inject`.

#### 4. Utility classes

Expressions can be wrapped with `Sexpr` helper:

```python
sexp = grammar.sexpr(['and', ['literal', True], ['literal', False]])
# or Sexpr(<expression>, grammar)

sexpr.tag
# = 'and'

sexpr.body
# = ['literal', True], ['literal', False']
```

In-place variants or `inject` and `extend` are provided as methods:

```python
sexp.inject(lambda exp: ['not', exp])
```

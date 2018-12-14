from typing import TYPE_CHECKING, Callable, Optional

from copy import deepcopy
from typing import Any


class Sexpr:
    def __init__(self, sexpr: list, grammar: 'Grammar'=None, **kwargs: Any):
        self.sexpr = sexpr
        self.grammar = grammar

    def __getitem__(self, index):
        return self.sexpr[index]

    def __setitem__(self, index, item):
        self.sexpr[index] = item

    def __repr__(self):
        return repr(self.sexpr)

    def __str__(self):
        return pformat(self.sexpr)

    def __len__(self):
        return len(self.sexpr)

    def __eq__(self, other):
        if isinstance(other, list):
            return self.sexpr == other

        return self.sexpr == other.sexpr

    @property
    def tag(self):
        return self.sexpr[0] if self.sexpr else None

    @property
    def body(self):
        return self.sexpr[1:] if self.sexpr else None

    def copy(self):
        return deepcopy(self.body)

    def inject(self, func):
        self.sexpr = inject(self.sexpr, func)

    def extend(self, func):
        self.sexpr = extend(func, self.sexpr)

    def with_insert(self, index, sexpr):
        self.sexpr.insert(index, sexpr)
        return self

    def with_replace(self, index, sexpr):
        self.sexpr[index] = sexpr
        return self

    def find_descendant(self, tag: str) -> Optional['Sexpr']:
        return find_descendant(self, tag)

    def find_and_replace(self,
                         test_fn: Callable[['Sexpr'], bool],
                         replace_fn: Callable[['Sexpr'], 'Sexpr']) -> 'Sexpr':

        return find_and_replace(self, test_fn, replace_fn)

    def find_child(self, *tags: str) -> Optional['Sexpr']:
        return find_child(self, *tags)


from .print import pformat
from .utils import *

if TYPE_CHECKING:
    from .grammar import Grammar

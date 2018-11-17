from typing import TYPE_CHECKING, Callable, Optional

from copy import deepcopy
from typing import Any, Union


class Sexpr:
    def __init__(self, sexpr: list, grammar: 'Grammar'=None, **k: Any) -> None:
        self.sexpr = sexpr
        self.grammar = grammar

    def __getitem__(self, item: Union[int, slice]) -> Any:
        return self.sexpr[item]

    def __setitem__(self, index: int, item: Any) -> None:
        self.sexpr[index] = item

    def __repr__(self) -> str:
        return repr(self.sexpr)

    def __str__(self) -> str:
        return pformat(self.sexpr)

    def __len__(self) -> int:
        return len(self.sexpr)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, list):
            return self.sexpr == other
        elif isinstance(other, Sexpr):
            return self.sexpr == other.sexpr
        else:
            return super().__eq__(other)

    @property
    def tag(self) -> str:
        return self.sexpr[0] if self.sexpr else None

    @property
    def body(self) -> Optional[list]:
        return self.sexpr[1:] if self.sexpr else None

    def copy(self) -> 'Sexpr':
        return Sexpr(deepcopy(self.sexpr), self.grammar)

    def inject(self, fn: Callable[[list], list]) -> None:
        self.sexpr = utils.inject(self.sexpr, fn)

    def extend(self, fn: Callable[[list], list]) -> None:
        self.sexpr = utils.extend(self.sexpr, fn)

    def with_insert(self, index: int, sexpr: Union[list, 'Sexpr']) -> 'Sexpr':
        self.sexpr.insert(index, sexpr)
        return self

    def with_replace(self, index: int, sexpr: Union[list, 'Sexpr']) -> 'Sexpr':
        self.sexpr[index] = sexpr
        return self

    def find_descendant(self, tag: str) -> Optional['Sexpr']:
        return utils.find_descendant(self, tag)

    def find_and_replace(self,
                         test_fn: Callable[['Sexpr'], bool],
                         replace_fn: Callable[['Sexpr'], 'Sexpr']) -> 'Sexpr':

        return utils.find_and_replace(self, test_fn, replace_fn)

    def find_child(self, *tags: str) -> Optional['Sexpr']:
        return utils.find_child(self, *tags)


from .print import pformat
from . import utils

if TYPE_CHECKING:
    from .grammar import Grammar

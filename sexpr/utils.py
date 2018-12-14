"""
    utils
    ~~~~~

    Collection of utility functions used for manipulation,
    transformation and traversal of s-expressions.
"""
from typing import *

from .sexpr import Sexpr


def inject(sexpr: Sexpr, fn: Callable[[Sexpr], Sexpr]) -> Sexpr:
    assert _is_valid_sexpr(sexpr)

    body = fn(*sexpr[1:] if sexpr else None)
    body = body if isinstance(body, tuple) else (body, )
    return Sexpr([sexpr[0], *body], getattr(sexpr, 'grammar', None))


def extend(sexpr: Sexpr, fn: Callable[[Sexpr], Sexpr]) -> Sexpr:
    assert _is_valid_sexpr(sexpr)

    return Sexpr(fn(sexpr), getattr(sexpr, 'grammar', None))


def find_descendant(sexpr: Sexpr, tag: str) -> Optional[Sexpr]:
    assert _is_valid_sexpr(sexpr)

    for child in sexpr[1:]:
        if issexpr(child):
            if child[0] == tag:
                return child
            else:
                desc = find_descendant(child, tag)

                if desc and desc[0] == tag:
                    return desc

    return None


def find_and_replace(sexpr: Sexpr,
                     test_fn: Callable[[Sexpr], bool],
                     replace_fn: Callable[[Sexpr], Sexpr]) -> Sexpr:
    assert _is_valid_sexpr(sexpr)

    for i, child in enumerate(sexpr[1:]):
        if test_fn(child):
            sexpr[i + 1] = replace_fn(child) # type: ignore

        elif issexpr(child):
            sexpr[i + 1] = find_and_replace(child, test_fn, replace_fn) # type: ignore

    return sexpr


def find_child(sexpr: Sexpr, *tags: str) -> Optional[Sexpr]:
    """Search for a tag among direct children of the s-expression."""
    assert _is_valid_sexpr(sexpr)

    for child in sexpr[1:]:
        if issexpr(child) and child[0] in tags:
            return child

    return None


def issexpr(sexpr: Any) -> bool:
    if (
        isinstance(sexpr, Sexpr)
        # Accept lists with string head.
        or (sexpr and isinstance(sexpr, list) and type(sexpr[0]) is str)
    ):
        return True

    return False


def _is_valid_sexpr(sexpr: Sexpr) -> bool:
    """
    Wrapper for `issexpr` which throws an exception if sexpr is not valid.
    """
    if not issexpr(sexpr):
        raise ValueError('{} is not a valid s-expression'.format(sexpr))

    return True

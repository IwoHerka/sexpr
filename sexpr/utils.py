from typing import Any, Callable, Optional, Dict

from .sexpr import Sexpr


def inject(sexpr: Sexpr, fn: Callable[[list], list]) -> Sexpr:
    _assert_valid_sexpr(sexpr)

    result = fn(*sexpr[1:] if sexpr else [])
    body = result if isinstance(result, tuple) else (result, )
    return Sexpr([sexpr[0], *body], getattr(sexpr, 'grammar', None))


def extend(sexpr: Sexpr, fn: Callable[[list], list]) -> Sexpr:
    _assert_valid_sexpr(sexpr)

    return Sexpr(fn(sexpr.sexpr), getattr(sexpr, 'grammar', None))


def find_descendant(sexpr: Sexpr, tag: str) -> Optional[Sexpr]:
    _assert_valid_sexpr(sexpr)

    for child in sexpr[1:]:
        if _is_sexpr(child):
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
    _assert_valid_sexpr(sexpr)

    for i, child in enumerate(sexpr[1:]):
        if test_fn(child):
            sexpr[i + 1] = replace_fn(child) # type: ignore

        elif _is_sexpr(child):
            sexpr[i + 1] = find_and_replace(child, test_fn, replace_fn) # type: ignore

    return sexpr


def find_child(sexpr: Sexpr, *tags: str) -> Optional[Sexpr]:
    """Search for a tag among direct children of the s-expression."""
    _assert_valid_sexpr(sexpr)

    for child in sexpr[1:]:
        if _is_sexpr(child) and child[0] in tags:
            return child

    return None


def _is_sexpr(sexpr: Any) -> bool:
    if isinstance(sexpr, Sexpr) or (
            sexpr and isinstance(sexpr, list) and type(sexpr[0]) is str):
        return True

    return False


def _assert_valid_sexpr(sexpr: Sexpr) -> None:
    if not _is_sexpr(sexpr):
        raise ValueError('{} is not a valid s-expression'.format(sexpr))

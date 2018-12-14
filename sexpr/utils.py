"""
    utils
    ~~~~~

    Collection of utility functions used for manipulation,
    transformation and traversal of s-expressions.
"""
from .sexpr import Sexpr
from .typing import *


def gettag(sexpr: SexprLike) -> Optional[str]:
    """
    Return tag string from the sexpr if present.
    Does not check s-expression's validity.
    """
    return sexpr[0] if sexpr else None


def getbody(sexpr: SexprLike) -> Optional[list]:
    """
    Return tag string from the sexpr if present.
    Does not check s-expression's validity.
    """
    return sexpr[1:] if sexpr else None


def inject(sexpr: SexprLike, fn: SexprFn) -> SexprLike:
    assert _is_valid_sexpr(sexpr)

    body = fn(*getbody(sexpr))
    body = body if isinstance(body, tuple) else (body, )
    return Sexpr([gettag(sexpr), *body], getattr(sexpr, 'grammar', None))


def extend(fn: SexprFn, sexpr: SexprLike) -> SexprLike:
    """
    Transform `sexpr` by applying of `fn` on it. `fn` must accept and
    return s-expression. Example:

        >>> extend(['lit', True], lambda exp: ['not', [exp[0], not exp[1]]])
        >>> ['not', ['lit', False]]]
    """
    assert _is_valid_sexpr(sexpr)

    # TODO: This is ugly, fix this
    return Sexpr(fn(sexpr), getattr(sexpr, 'grammar', None))


def find_descendant(sexpr: SexprLike, tag: str) -> Optional[SexprLike]:
    """
    Traverse s-expression tree in DPS order trying to find a child
    with specified tag. If any, first match is returned.
    """
    assert _is_valid_sexpr(sexpr)

    for child in getbody(sexpr):
        if issexpr(child):
            if gettag(child) == tag:
                return child
            else:
                desc = find_descendant(child, tag)

                if desc and gettag(desc) == tag:
                    return desc

    return None


def find_and_replace(sexpr: SexprLike,
                     test_fn: Callable[[SexprLike], bool],
                     replace_fn: SexprFn) -> SexprLike:
    assert _is_valid_sexpr(sexpr)

    for i, child in enumerate(getbody(sexpr)):
        if test_fn(child):
            sexpr[i + 1] = replace_fn(child) # type: ignore

        elif issexpr(child):
            sexpr[i + 1] = find_and_replace(child, test_fn, replace_fn) # type: ignore

    return sexpr


def find_child(sexpr: SexprLike, *tags: str) -> Optional[SexprLike]:
    """
    Search for an s-expression with matching tag among _direct_
    children of the argument s-expression.
    """
    assert _is_valid_sexpr(sexpr)

    for child in getbody(sexpr):
        if issexpr(child) and gettag(child) in tags:
            return child

    return None


def issexpr(sexpr: Any) -> bool:
    """
    Check if sexpr is valid s-expression (`SexprLike`), which
    is an instance of `Sexpr` or a list with string head.
    """
    return (
        isinstance(sexpr, Sexpr)
        or (sexpr and isinstance(sexpr, list) and type(gettag(sexpr)) is str)
    )


def _is_valid_sexpr(sexpr: SexprLike) -> bool:
    """
    Wrapper for `issexpr` which throws an exception if sexpr is not valid.
    Meant to be used in `assert` statements.
    """
    if not issexpr(sexpr):
        raise ValueError('{} is not a valid s-expression'.format(sexpr))

    return True

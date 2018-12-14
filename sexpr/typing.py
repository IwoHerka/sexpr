from typing import *

from .sexpr import Sexpr

# Could use some of those dependent types here...
SexprLike = Union[Sexpr, list]

SexprFn = Callable[[SexprLike], SexprLike]

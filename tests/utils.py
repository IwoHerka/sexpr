import random
from random import choice, randint
from string import digits

# Default constructors for the ``random_list``.
default_constructors = (
    object,
    dict,
    lambda: bool(randint(0, 1)),
    lambda: randint(1, 1000),
    lambda: ''.join(choice(digits) for _ in range(randint(1, 10)))
)


def random_list(max_len = 10, seed = None, constructors = None):
    '''
    Generate list of random objects. Typically something looking like::

        [(269, '6'), [{}, 990, 347, <object object at 0x7f51b230b130>, {},
        [{}, '91921063', 302, '0047953', {}, ()], True], '70262', True]

    Args:
        max_len (int): Maximal length of generated list. Actual length is
            randomly selected from the range (1, max_length).

        constructors (List[Union[function, class]]): List of constructors
            (callables to be precise) used to construct elements of the list.
            Constructors are selected randomly. Additionally, there is a chance
            (2/3 for each element) that an element of the list is another
            random list or tuple.

            If no constructors are specified, default ones are used.

    Notes:
        ``depth`` serves as an "annealing factor". That is, because the
        function may call itself (to create inner lits/tuples), we need to
        ensure that the recursion is not infinite. ``depth`` is subtracted
        from randomly generated length of the list/tuple, so that it's
        shorter on each call.
    '''
    constructors = constructors or default_constructors

    if seed:
        random.seed(seed)

    def gen_list(depth):
        return [
            choice(choices)(depth + 1)
            for _ in range(max(randint(1, max_len) - depth, 0))
        ]

    choices = (
        gen_list,
        lambda     _: choice(constructors)(),
        lambda depth: tuple(gen_list(depth))
    )

    return gen_list(0)


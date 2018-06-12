from random import randint, choice
from string import digits


constructors = [
    object,
    dict,
    lambda: bool(randint(0, 1)),
    lambda: randint(1, 1000),
    lambda: ''.join(choice(digits) for _ in range(randint(1, 10)))
]


def fake_list(off = None):
    '''Creates a list populated with random objects.'''
    off = off or 0
    off += 1
    li = []

    for _ in range(max(randint(1, 10) - off, 0)):
        i = randint(0, 7)

        if i <= 4:
            li.append(constructors[i]())
        elif i == 5:
            li.append(fake_list(off))
        elif i == 6:
            li.append(tuple(fake_list(off)))

    return li

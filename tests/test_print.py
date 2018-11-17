from sexpr import Sexpr
from sexpr.print import pformat


def test_pformat():
    exp = ['select_exp',
        ['set_quantifier', 'all'],
        ['select_list',
            ['select_item', ['column_name', 'sid']],
            ['select_item', ['column_name', 'status']],
        ],
        ['inner_join',
            ['from_clause', ['table_name', 'suppliers']],
            ['from_clause', ['table_name', 'parts']],
            ['eq',
                ['select_item', ['column_name', 'city']],
                ['select_item', ['column_name', 'city']]
            ]
        ]
    ]

    assert pformat(exp) == '''\
['select_exp',
    ['set_quantifier', 'all'],
    ['select_list',
        ['select_item', ['column_name', 'sid']],
        ['select_item', ['column_name', 'status']]
    ],
    ['inner_join',
        ['from_clause', ['table_name', 'suppliers']],
        ['from_clause', ['table_name', 'parts']],
        ['eq',
            ['select_item', ['column_name', 'city']],
            ['select_item', ['column_name', 'city']]
        ]
    ]
]'''

    exp = Sexpr(['tag', 1])
    assert pformat(exp) == "['tag', 1]"

    exp = ['eq',
        ['select_item', ['column_name', 'city']],
        ['select_item', ['column_name', 'city']]
    ]

    assert pformat(exp) == '''\
['eq',
    ['select_item', ['column_name', 'city']],
    ['select_item', ['column_name', 'city']]
]'''

    obj0 = object()
    obj1 = object()
    exp = ['eq',
        ['select_item', obj0],
        ['select_item', obj1]
    ]
    repr0 = repr(obj0)
    repr1 = repr(obj1)

    assert pformat(exp) == '''\
['eq',
    ['select_item', {}],
    ['select_item', {}]
]'''.format(repr0, repr1)

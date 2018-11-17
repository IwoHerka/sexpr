from sexpr import pprint, Sexpr


def test_pretty_print():
    exp = Sexpr(['select_exp',
        ['set_quantifier', 'all'],
        ['select_list',
            ['select_item', ['column_name', 'sid']],
            ['select_item', ['column_name', 'status']],
            ['select_item', ['column_name', 'name']],
            ['select_item', ['column_name', 'city']],
            ['select_item', ['column_name', 'pid']],
            ['select_item', ['column_name', 'pname']],
            ['select_item', ['column_name', 'color']],
            ['select_item', ['column_name', 'weight']]
        ],
        ['inner_join',
            ['from_clause', ['table_name', 'suppliers']],
            ['from_clause', ['table_name', 'parts']],
            ['eq',
                ['select_item', ['column_name', 'city']],
                ['select_item', ['column_name', 'city']]
            ]
        ]
    ])

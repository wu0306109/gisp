from gisp import gisp


def test_nothing() -> None:
    assert True


def test_transform() -> None:
    sequences = [
        [(0, {'a', }), (86400, {'a', 'b', 'c', }), (259200, {'a', 'c', })],
        [(0, {'a', 'd', }), (259200, {'c', })],
        [(0, {'a', 'e', 'f', }), (172800, {'a', 'b', })],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a', ]), (86400, ['a', 'b', 'c', ]), (259200, ['a', 'c', ])],
        [(0, ['a', 'd', ]), (259200, ['c', ])],
        [(0, ['a', 'e', 'f', ]), (172800, ['a', 'b', ])],
    ]
    assert left == right

    sequences = [
        [
            (0, {'a', }),
            (2, {'a', 'c', }),
            (7, {'a', 'b', }),
            (20, {'c', 'f', }),
        ],
        [
            (0, {'a', 'd', }),
            (14, {'c', }),
            (26, {'c', }),
        ],
        [
            (0, {'a', 'e', 'f', }),
            (6, {'a', 'b', 'd', }),
            (19, {'b', 'c', }),
        ],
    ]
    left = gisp.transform(sequences)
    right = [
        [
            (0, ['a', ]),
            (2, ['a', 'c', ]),
            (7, ['a', 'b', ]),
            (20, ['c', 'f', ]),
        ],
        [
            (0, ['a', 'd', ]),
            (14, ['c', ]),
            (26, ['c', ]),
        ],
        [
            (0, ['a', 'e', 'f', ]),
            (6, ['a', 'b', 'd', ]),
            (19, ['b', 'c', ]),
        ],
    ]
    assert left == right


def test_transform_item_is_sorted() -> None:
    # TODO: check if items are sorted
    pass


def test_transform_sequence_is_sorted() -> None:
    # TODO: check if sequence is sorted by occurence time
    pass


def test_transform_items_in_same_time_are_merged() -> None:
    # TODO: check items in the are merged
    pass

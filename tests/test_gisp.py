from pandas.testing import assert_frame_equal
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
    assert_frame_equal(left, right, check_dtype=False)

    left = [
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
    right = gisp.transform(sequences)
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
    assert_frame_equal(left, right, check_dtype=False)
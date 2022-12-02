from math import inf, log2

from gisp import gisp
from gisp.gisp import Pattern, mine, mine_subpatterns

# TODO: sort extpectd values in advance for easy testing

# TODO: use Pattern(), mine(), ... instead of gisp.Pattern(), gisp.mine(), ...


def test_transform() -> None:
    sequences = [
        [(0, {'a'}), (86400, {'a', 'b', 'c'}), (259200, {'a', 'c'})],
        [(0, {'a', 'd'}), (259200, {'c'})],
        [(0, {'a', 'e', 'f'}), (172800, {'a', 'b'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (86400, ['a', 'b', 'c']), (259200, ['a', 'c'])],
        [(0, ['a', 'd']), (259200, ['c'])],
        [(0, ['a', 'e', 'f']), (172800, ['a', 'b'])],
    ]
    assert left == right

    sequences = [
        [(0, {'a'}), (2, {'a', 'c'}), (7, {'a', 'b'}), (20, {'c', 'f'})],
        [(0, {'a', 'd'}), (14, {'c'}), (26, {'c'})],
        [(0, {'a', 'e', 'f'}), (6, {'a', 'b', 'd'}), (19, {'b', 'c'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    assert left == right


def test_transform_item_is_sorted() -> None:
    sequences = [
        [(0, {'a'}), (86400, {'b', 'a', 'c'}), (259200, {'c', 'a'})],
        [(0, {'a', 'd'}), (259200, {'c'})],
        [(0, {'e', 'f', 'a'}), (172800, {'a', 'b'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (86400, ['a', 'b', 'c']), (259200, ['a', 'c'])],
        [(0, ['a', 'd']), (259200, ['c'])],
        [(0, ['a', 'e', 'f']), (172800, ['a', 'b'])],
    ]
    assert left == right

    sequences = [
        [(0, {'a'}), (2, {'a', 'c'}), (7, {'a', 'b'}), (20, {'c', 'f'})],
        [(0, {'a', 'd'}), (14, {'c'}), (26, {'c'})],
        [(0, {'e', 'a', 'f'}), (6, {'b', 'd', 'a'}), (19, {'c', 'b'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    assert left == right


def test_transform_sequence_is_sorted() -> None:
    sequences = [
        [(86400, {'b', 'a', 'c'}), (259200, {'c', 'a'}), (0, {'a'})],
        [(0, {'a', 'd'}), (259200, {'c'})],
        [(0, {'e', 'f', 'a'}), (172800, {'a', 'b'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (86400, ['a', 'b', 'c']), (259200, ['a', 'c'])],
        [(0, ['a', 'd']), (259200, ['c'])],
        [(0, ['a', 'e', 'f']), (172800, ['a', 'b'])],
    ]
    assert left == right

    sequences = [
        [(0, {'a'}), (7, {'a', 'b'}), (2, {'a', 'c'}), (20, {'c', 'f'})],
        [(14, {'c'}), (26, {'c'}), (0, {'a', 'd'})],
        [(19, {'c', 'b'}), (6, {'b', 'a', 'd'}), (0, {'e', 'a', 'f'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    assert left == right


def test_transform_items_in_same_time_are_merged() -> None:
    sequences = [
        [
            (86400, {'b', 'a'}),
            (86400, {'c'}),
            (259200, {'c', 'a'}),
            (0, {'a'}),
        ],
        [(0, {'d'}), (0, {'a'}), (259200, {'c'})],
        [(0, {'e'}), (172800, {'b'}), (172800, {'a'}), (0, {'f', 'a'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (86400, ['a', 'b', 'c']), (259200, ['a', 'c'])],
        [(0, ['a', 'd']), (259200, ['c'])],
        [(0, ['a', 'e', 'f']), (172800, ['a', 'b'])],
    ]
    assert left == right

    sequences = [
        [
            (0, {'a'}),
            (7, {'a', 'b'}),
            (2, {'c'}),
            (2, {'a'}),
            (20, {'c', 'f'}),
        ],
        [(0, 'a'), (14, {'c'}), (26, {'c'}), (0, {'d'})],
        [(0, {'a', 'f'}), (19, {'c', 'b'}), (6, {'b', 'a', 'd'}), (0, {'e'})],
    ]
    left = gisp.transform(sequences)
    right = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    assert left == right


def test_mine_subpatterns() -> None:
    projected_db = [
        [
            [(0, []), (86400, ['a', 'b', 'c']), (259200, ['a', 'c'])],
            [(0, ['b', 'c']), (172800, ['a', 'c'])],
            [(0, ['c'])],
        ],
        [
            [(0, ['d']), (259200, ['c'])],
        ],
        [
            [(0, ['e', 'f']), (172800, ['a', 'b'])],
            [(0, ['b'])],
        ],
    ]
    left = gisp.mine_subpatterns(
        projected_db,
        itemize=lambda t: t // 86400,
        min_support=2,
        min_interval=0,
        max_interval=172800,
        min_whole_interval=0,
        max_whole_interval=inf,
    )
    right = [
        gisp.Pattern([(0, 'b')], 2),
        gisp.Pattern([(2, 'a')], 2),
    ]
    assert sorted(left) == sorted(right)


def test_mine() -> None:
    sequences = [
        [(0, ['a']), (86400, ['a', 'b', 'c']), (259200, ['a', 'c'])],
        [(0, ['a', 'd']), (259200, ['c'])],
        [(0, ['a', 'e', 'f']), (172800, ['a', 'b'])],
    ]
    left = gisp.mine(
        sequences,
        itemize=lambda t: t // 86400,
        min_support=2,
        max_interval=172800,
    )
    right = [
        gisp.Pattern([(0, 'a')], 3),
        gisp.Pattern([(0, 'a'), (0, 'b')], 2),
        gisp.Pattern([(0, 'a'), (2, 'a')], 2),
        gisp.Pattern([(0, 'b')], 2),
        gisp.Pattern([(0, 'c')], 2),
    ]
    assert sorted(left) == sorted(right)


def test_mine_subpatterns_with_multi_level_projection() -> None:
    projected_db = [
        [
            [(0, ['b']), (13, ['c', 'f'])],
        ],
        [
            [(0, ['b', 'c']), (13, ['b', 'c'])],
        ],
    ]
    left = mine_subpatterns(
        projected_db,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
        min_interval=0,
        max_interval=inf,
        min_whole_interval=0,
        max_whole_interval=inf,
    )
    right = [
        Pattern([(0, 'b')], 2),
        Pattern([(3, 'c')], 2),
        Pattern([(0, 'b'), (3, 'c')], 2),
    ]
    assert sorted(left) == sorted(right)

    projected_db = [
        [
            [(0, []), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
            [(0, ['c']), (5, ['a', 'b']), (18, ['c', 'f'])],
            [(0, ['b']), (13, ['c', 'f'])],
        ],
        [
            [(0, ['d']), (14, ['c']), (26, ['c'])],
        ],
        [
            [(0, ['e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
            [(0, ['b', 'd']), (13, ['b', 'c'])],
        ],
    ]
    left = mine_subpatterns(
        projected_db,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
        min_interval=0,
        max_interval=inf,
        min_whole_interval=0,
        max_whole_interval=inf,
    )
    right = [
        Pattern(sequence=[(0, 'b')], support=2),
        Pattern(sequence=[(0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'd')], support=2),
        Pattern(sequence=[(0, 'd'), (3, 'c')], support=2),
        Pattern(sequence=[(2, 'a')], support=2),
        Pattern(sequence=[(2, 'a'), (0, 'b')], support=2),  #
        Pattern(sequence=[(2, 'a'), (0, 'b'), (3, 'c')], support=2),  #
        Pattern(sequence=[(2, 'a'), (3, 'c')], support=2),  #
        Pattern(sequence=[(2, 'b')], support=2),
        Pattern(sequence=[(2, 'b'), (3, 'c')], support=2),  #
        Pattern(sequence=[(3, 'b')], support=2),
        Pattern(sequence=[(3, 'c')], support=3),
        Pattern(sequence=[(4, 'c')], support=3)
    ]
    assert sorted(left) == right


def test_mine_with_multi_level_projection() -> None:
    sequences = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    left = mine(
        sequences,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
    )
    right = [
        Pattern(sequence=[(0, 'a')], support=3),
        Pattern(sequence=[(0, 'a'), (0, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'd')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'd'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (0, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'c')], support=3),
        Pattern(sequence=[(0, 'a'), (4, 'c')], support=3),
        Pattern(sequence=[(0, 'b')], support=2),
        Pattern(sequence=[(0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'c')], support=3),
        Pattern(sequence=[(0, 'd')], support=2),
        Pattern(sequence=[(0, 'd'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'f')], support=2),
    ]
    assert sorted(left) == right


def test_mine_with_min_interval() -> None:
    sequences = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    left = mine(
        sequences,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
        min_interval=6,
    )
    right = [
        Pattern(sequence=[(0, 'a')], support=3),
        Pattern(sequence=[(0, 'a'), (3, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'c')], support=3),
        Pattern(sequence=[(0, 'a'), (4, 'c')], support=3),
        Pattern(sequence=[(0, 'b')], support=2),
        Pattern(sequence=[(0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'c')], support=3),
        Pattern(sequence=[(0, 'd')], support=2),
        Pattern(sequence=[(0, 'd'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'f')], support=2),
    ]
    assert sorted(left) == right


def test_mine_with_max_interval() -> None:
    sequences = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    left = mine(
        sequences,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
        max_interval=13,
    )
    right = [
        Pattern(sequence=[(0, 'a')], support=3),
        Pattern(sequence=[(0, 'a'), (0, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'd')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (0, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'b')], support=2),
        Pattern(sequence=[(0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'c')], support=3),
        Pattern(sequence=[(0, 'd')], support=2),
        Pattern(sequence=[(0, 'f')], support=2),
    ]
    assert sorted(left) == right


def test_mine_with_min_whole_interval() -> None:
    sequences = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    left = mine(
        sequences,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
        min_whole_interval=6,
    )
    right = [
        Pattern(sequence=[(0, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'd'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'c')], support=3),
        Pattern(sequence=[(0, 'a'), (4, 'c')], support=3),
        Pattern(sequence=[(0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'd'), (3, 'c')], support=2),
    ]
    assert sorted(left) == right


def test_mine_with_max_whole_interval() -> None:
    sequences = [
        [(0, ['a']), (2, ['a', 'c']), (7, ['a', 'b']), (20, ['c', 'f'])],
        [(0, ['a', 'd']), (14, ['c']), (26, ['c'])],
        [(0, ['a', 'e', 'f']), (6, ['a', 'b', 'd']), (19, ['b', 'c'])],
    ]
    left = mine(
        sequences,
        itemize=lambda t: int(log2(t + 1)),
        min_support=2,
        max_whole_interval=13,
    )
    right = [
        Pattern(sequence=[(0, 'a')], support=3),
        Pattern(sequence=[(0, 'a'), (0, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'a'), (0, 'd')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'a'), (0, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (2, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'b')], support=2),
        Pattern(sequence=[(0, 'a'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'b')], support=2),
        Pattern(sequence=[(0, 'b'), (3, 'c')], support=2),
        Pattern(sequence=[(0, 'c')], support=3),
        Pattern(sequence=[(0, 'd')], support=2),
        Pattern(sequence=[(0, 'f')], support=2),
    ]
    assert sorted(left) == right

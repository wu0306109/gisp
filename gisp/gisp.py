from typing import Callable, Iterable, List, NamedTuple, Tuple


class Pattern(NamedTuple):

    sequence: List[Tuple[int, str]]
    support: int  # number of the pattern occurrence


def transform(
    sequences: List[Tuple[int, Iterable[str]]]
) -> List[Tuple[int, List[str]]]:
    # items is sorted
    # sequence is sorted by occurence time
    pass


def mine_subpatterns() -> List[Pattern]:
    pass


def mine(
    sequences: List[Tuple[int, List[str]]], itemize: Callable[[int], int],
    min_support: int, min_interval: int = None, max_interval: int = None,
    min_whole_interval: int = None, max_whole_interval: int = None,
) -> List[Pattern]:
    """Mine frequent interval-extended sequences.

    Args:
        sequences: Interval-extended sequences, 
            where each sequence is a list of (interval, items).
        itemize: Converting function from interval to pseudo counts.
        min_support: Minimal number of occurrence for resulting patterns.
        min_interval: Minimum interval between any two adjacent items.
        max_interval: Maximum interval between any two adjacent items.
        min_whole_interval: Minimum interval between 
            the head and the tail of the sequence.
        max_whole_interval: Maximum interval between
            the head and the tail of the sequence.

    Returns:
        List of Pattern(sequence, support), 
        where sequence is a list of (itemized_interval, item),
        and support is the number of the pattern occurrence.
    """
    pass

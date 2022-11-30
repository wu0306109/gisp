from collections import defaultdict
from typing import Callable, Iterable, List, NamedTuple, Tuple

Sequence = List[Tuple[int, List[str]]]


class Pattern(NamedTuple):

    sequence: List[Tuple[int, str]]  # frequent interval-extended sequence
    support: int  # number of the pattern occurrence


def transform(sequences: Sequence) -> List[Tuple[int, List[str]]]:
    result_sequences = []
    for sequence in sequences:
        # XXX: use dictionary to merge items,
        # when allowing time (interval) in float type may cause problem
        items_mapper = defaultdict(list)  # {time -> items}
        for time, items in sequence:
            items_mapper[time].extend(items)

        result_sequence = []
        for time, items in sorted(items_mapper.items(), key=lambda x: x[0]):
            result_sequence.append((time, sorted(items)))

        result_sequences.append(result_sequence)

    return result_sequences


def mine_subpatterns(
        projected_db: List[List[Sequence]], itemize: Callable[[int], int],
        min_support: int, min_interval: int, max_interval: int,
        min_whole_interval: int, max_whole_interval: int) -> List[Pattern]:
    pass


def mine(
    sequences: List[Sequence], itemize: Callable[[int], int],
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

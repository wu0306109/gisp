from collections import defaultdict
from typing import Callable, Iterable, List, NamedTuple, Tuple


class Pattern(NamedTuple):

    sequence: List[Tuple[int, str]]
    support: int  # number of the pattern occurrence


def transform(
    sequences: List[Tuple[int, Iterable[str]]]
) -> List[Tuple[int, List[str]]]:
    # TODO: items should be sorted
    # TODO: sequence should be sorted by occurence time
    # TODO: merge items in the same time (interval)

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

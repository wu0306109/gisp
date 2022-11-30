from collections import Counter, defaultdict
from typing import Callable, List, NamedTuple, Tuple

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
    # TODO: implement fucntions in class to avoid passing so many arguments

    # Count number of (itemize(interval), item) pairs in projected database
    counter = Counter()
    for postfixes in projected_db:
        # for each postfixes of a corresponding sequence,
        # get all unique (itemize(interval), item) pairs fitting the constraints
        unique_pairs = set()
        for postfix in postfixes:
            origin = postfix[0][0]  # origin interval of the postfix
            for whole_interval, items in postfix:
                interval = whole_interval - origin
                if (whole_interval > max_whole_interval
                        or interval > max_interval):
                    # because sequence is sorted, no need to continue
                    break
                elif (whole_interval < min_whole_interval
                      or interval < min_interval):
                    # skip if not fitting the constraints
                    continue

                unique_pairs.update(
                    (itemize(whole_interval-origin), item) for item in items)

        counter.update(unique_pairs)

    patterns = []
    for (interval, item), count in counter.items():
        if count < min_support:
            continue

        patterns.append(
            Pattern(sequence=[(interval, item), ], support=count))

        # generate child progected database by
        # the (itemize(interval), item) pair
        child_db = []
        for postfixes in projected_db:
            child_postfixes = []
            for postfix in postfixes:
                origin = postfix[0][0]  # origin interval of the postfix
                for i, (whole_interval, items) in enumerate(postfix):
                    item_interval = whole_interval-origin
                    if item_interval > max_whole_interval:
                        # skip redundant calculation to the next postfix
                        # when interval exceed the max whole interval
                        break
                    elif not (item in items and item_interval == interval):
                        # skip to the next item if not match
                        continue

                    # generate child postfix
                    items = items[items.index(item)+1:]
                    child_postfix = [(whole_interval, items), *postfix[i+1:]]
                    if items or len(child_postfix) > 1:
                        child_postfixes.append(child_postfix)

            if child_postfixes:
                child_db.append(child_postfixes)

        if not child_db or len(child_db) < min_support:
            continue

        # recursively mine child projected database
        subpatterns = mine_subpatterns(
            child_db, itemize=itemize, min_support=min_support,
            min_interval=min_interval, max_interval=max_interval,
            min_whole_interval=min_whole_interval,
            max_whole_interval=max_whole_interval)

        for pattern in subpatterns:
            pattern.sequence.insert(0, (interval, item))
        patterns.extend(subpatterns)

    return patterns


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

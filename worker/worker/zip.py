import itertools
from typing import List, Tuple


class ExhaustedError(Exception):
    def __init__(self, index):
        """The index is the 0-based index of the exhausted iterable."""
        self.index = index


def raising_iter(i: int) -> None:
    """Return an iterator that raises an ExhaustedError."""
    raise ExhaustedError(i)
    yield


def terminate_iter(i: int, iterable: List[str]) -> itertools.chain:
    """Return an iterator that raises an ExhaustedError at the end."""
    return itertools.chain(iterable, raising_iter(i))


def zip_equal(*iterables: Tuple[str]) -> None:
    iterators = [terminate_iter(*args) for args in enumerate(iterables)]
    try:
        yield from zip(*iterators)
    except ExhaustedError as exc:
        index = exc.index
        if index > 0:
            raise RuntimeError(f'iterable {index} exhausted first') from None
        # Check that all other iterators are also exhausted.
        for i, iterator in enumerate(iterators[1:], start=1):
            try:
                next(iterator)
            except ExhaustedError:
                pass
            else:
                raise RuntimeError(f'iterable {i} is longer') from None

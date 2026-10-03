"""Top-down merge sort."""

from collections.abc import Sequence


def merge_sort(items: Sequence[int]) -> list[int]:
    """Return a new list with the items in ascending order; the input is not changed."""
    out = list(items)
    if len(out) > 1:
        _sort(out, [0] * len(out), 0, len(out))
    return out


def _sort(a: list[int], buf: list[int], lo: int, hi: int) -> None:
    """Sort a[lo:hi] in place, using buf as scratch space."""
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    _sort(a, buf, lo, mid)
    _sort(a, buf, mid, hi)
    if a[mid - 1] <= a[mid]:  # halves already in order
        return
    buf[lo:hi] = a[lo:hi]
    i, j = lo, mid
    for k in range(lo, hi):
        if j >= hi or (i < mid and buf[i] <= buf[j]):
            a[k] = buf[i]
            i += 1
        else:
            a[k] = buf[j]
            j += 1

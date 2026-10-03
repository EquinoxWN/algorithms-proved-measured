"""Binary search in its lower-bound form."""

from collections.abc import Sequence


def lower_bound(items: Sequence[int], target: int) -> int:
    """Return the first index whose value is >= target, or len(items) if none."""
    lo, hi = 0, len(items)
    # Invariant: every value before lo is < target, every value from hi on is >= target.
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

"""Levenshtein edit distance by dynamic programming."""


def edit_distance(a: str, b: str) -> int:
    """Minimum inserts, deletes and substitutions that turn a into b."""
    if len(a) < len(b):
        a, b = b, a  # keep the row as short as possible
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]

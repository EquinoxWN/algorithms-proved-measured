"""Knuth-Morris-Pratt substring search."""


def find_all(text: str, pattern: str) -> list[int]:
    """Every start index where pattern occurs in text, overlaps included."""
    if not pattern:
        return list(range(len(text) + 1))
    border = _prefix_function(pattern)
    out: list[int] = []
    k = 0
    for i, ch in enumerate(text):
        while k and ch != pattern[k]:
            k = border[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            out.append(i - k + 1)
            k = border[k - 1]
    return out


def _prefix_function(p: str) -> list[int]:
    """Length of the longest proper border of every prefix of p."""
    pi = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = pi[k - 1]
        if p[i] == p[k]:
            k += 1
        pi[i] = k
    return pi

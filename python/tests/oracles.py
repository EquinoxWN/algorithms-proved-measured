"""Brute-force oracles: obviously correct, deliberately slow, used only on small inputs."""

from collections.abc import Sequence


def lower_bound(items: Sequence[int], target: int) -> int:
    """Linear scan for the first value >= target."""
    return next((i for i, x in enumerate(items) if x >= target), len(items))


def sort(items: Sequence[int]) -> list[int]:
    """Selection sort."""
    out = list(items)
    for i in range(len(out)):
        m = min(range(i, len(out)), key=out.__getitem__)
        out[i], out[m] = out[m], out[i]
    return out


def shortest_paths(n: int, edges: Sequence[Sequence[int]], source: int) -> list[int]:
    """Bellman-Ford: relax every edge n - 1 times."""
    inf = float("inf")
    dist = [inf] * n
    dist[source] = 0
    for _ in range(max(n - 1, 0)):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return [int(d) if d != inf else -1 for d in dist]


def edit_distance(a: str, b: str) -> int:
    """Plain recursion over the three edit choices (exponential time)."""
    if not a or not b:
        return len(a) + len(b)
    if a[0] == b[0]:
        return edit_distance(a[1:], b[1:])
    return 1 + min(edit_distance(a[1:], b), edit_distance(a, b[1:]), edit_distance(a[1:], b[1:]))


def find_all(text: str, pattern: str) -> list[int]:
    """Compare the pattern at every position."""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i : i + m] == pattern]

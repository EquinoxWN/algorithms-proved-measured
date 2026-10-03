"""Dijkstra's single-source shortest paths on a directed graph."""

from collections.abc import Sequence
from heapq import heappop, heappush


def dijkstra(n: int, edges: Sequence[Sequence[int]], source: int) -> list[int]:
    """Shortest distance from source to every vertex; -1 marks unreachable vertices."""
    if not 0 <= source < n:
        raise ValueError("source out of range")
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge endpoint out of range")
        if w < 0:
            raise ValueError("negative edge weight")
        adj[u].append((v, w))
    dist = [-1] * n
    heap = [(0, source)]
    while heap:
        d, u = heappop(heap)
        if dist[u] != -1:  # already settled with a shorter distance
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] == -1:
                heappush(heap, (d + w, v))
    return dist

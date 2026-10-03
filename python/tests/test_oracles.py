"""Random inputs: every implementation must agree with its brute-force oracle."""

import random

import oracles
import pytest

from algorithms_proved_measured import dijkstra, edit_distance, find_all, lower_bound, merge_sort

CASES = 500  # random cases per algorithm


def test_lower_bound_matches_linear_scan():
    rng = random.Random(1)
    for _ in range(CASES):
        items = sorted(rng.randint(-30, 30) for _ in range(rng.randint(0, 40)))
        target = rng.randint(-35, 35)
        assert lower_bound(items, target) == oracles.lower_bound(items, target), (items, target)


def test_merge_sort_matches_selection_sort_and_keeps_input():
    rng = random.Random(2)
    for _ in range(CASES):
        items = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
        before = list(items)
        assert merge_sort(items) == oracles.sort(items), items
        assert items == before


def test_dijkstra_matches_bellman_ford():
    rng = random.Random(3)
    for _ in range(CASES):
        n = rng.randint(1, 15)
        edges = [
            [rng.randrange(n), rng.randrange(n), rng.randint(0, 30)]
            for _ in range(rng.randint(0, 4 * n))
        ]
        source = rng.randrange(n)
        assert dijkstra(n, edges, source) == oracles.shortest_paths(n, edges, source), (
            n,
            edges,
            source,
        )


def test_edit_distance_matches_recursion():
    rng = random.Random(4)
    for _ in range(CASES):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
        b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
        assert edit_distance(a, b) == oracles.edit_distance(a, b), (a, b)


def test_find_all_matches_naive_search():
    rng = random.Random(5)
    for _ in range(CASES):
        text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 50)))
        pattern = "".join(rng.choice("ab") for _ in range(rng.randint(0, 5)))
        assert find_all(text, pattern) == oracles.find_all(text, pattern), (text, pattern)


@pytest.mark.parametrize(
    ("edges", "source", "message"),
    [
        ([], 3, "source out of range"),
        ([[0, 5, 1]], 0, "endpoint out of range"),
        ([[0, 1, -1]], 0, "negative"),
    ],
)
def test_dijkstra_rejects_bad_input(edges, source, message):
    with pytest.raises(ValueError, match=message):
        dijkstra(2, edges, source)

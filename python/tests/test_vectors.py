"""Run every shared vector in spec/vectors against the Python implementations."""

import json
from pathlib import Path

import pytest

from algorithms_proved_measured import dijkstra, edit_distance, find_all, lower_bound, merge_sort

VECTORS = Path(__file__).resolve().parents[2] / "spec" / "vectors"

CALLS = {
    "lower_bound": lambda i: lower_bound(i["items"], i["target"]),
    "merge_sort": lambda i: merge_sort(i["items"]),
    "dijkstra": lambda i: dijkstra(i["n"], i["edges"], i["source"]),
    "edit_distance": lambda i: edit_distance(i["a"], i["b"]),
    "find_all": lambda i: find_all(i["text"], i["pattern"]),
}


def _cases():
    """Yield (algorithm, case) for every vector file."""
    for name in sorted(CALLS):
        doc = json.loads((VECTORS / f"{name}.json").read_text(encoding="utf-8"))
        for case in doc["cases"]:
            yield pytest.param(name, case, id=f"{name}: {case['name']}")


@pytest.mark.parametrize(("algorithm", "case"), list(_cases()))
def test_vector(algorithm, case):
    assert CALLS[algorithm](case["input"]) == case["expect"]


def test_every_algorithm_has_vectors():
    assert {p.stem for p in VECTORS.glob("*.json")} == set(CALLS)

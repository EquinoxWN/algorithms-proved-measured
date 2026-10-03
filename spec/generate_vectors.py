"""Generate the shared test vectors from the brute-force oracles.

Usage:
    python spec/generate_vectors.py           # rewrite spec/vectors/*.json
    python spec/generate_vectors.py --check   # fail if the committed files are stale
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "python" / "tests"))

import oracles  # noqa: E402

SEED = 20261004
OUT = HERE / "vectors"


def lower_bound_cases(rng: random.Random) -> list[dict]:
    """Edge cases plus random sorted arrays with duplicates."""
    inputs = [
        ([], 5),
        ([1], 0),
        ([1], 1),
        ([1], 2),
        ([2, 2, 2, 2], 2),
        ([1, 3, 3, 5, 7], 4),
        ([1, 3, 3, 5, 7], 8),
        ([-5, -1, 0, 0, 9], -3),
    ]
    for _ in range(12):
        items = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 30)))
        inputs.append((items, rng.randint(-25, 25)))
    return [
        {
            "name": f"case {i}",
            "input": {"items": a, "target": t},
            "expect": oracles.lower_bound(a, t),
        }
        for i, (a, t) in enumerate(inputs)
    ]


def merge_sort_cases(rng: random.Random) -> list[dict]:
    """Empty, sorted, reversed, duplicates and random arrays."""
    inputs = [[], [7], [2, 1], list(range(10)), list(range(10, 0, -1)), [3, 3, 3], [0, -1, 5, -1]]
    inputs += [[rng.randint(-50, 50) for _ in range(rng.randint(0, 40))] for _ in range(13)]
    return [
        {"name": f"case {i}", "input": {"items": a}, "expect": oracles.sort(a)}
        for i, a in enumerate(inputs)
    ]


def dijkstra_cases(rng: random.Random) -> list[dict]:
    """Single vertex, unreachable parts, parallel edges, zero weights and random graphs."""
    inputs = [
        (1, [], 0),
        (3, [], 1),
        (3, [[0, 1, 5], [0, 1, 2], [1, 2, 0]], 0),
        (4, [[0, 1, 1], [1, 2, 1], [0, 2, 5], [2, 0, 1]], 0),
        (5, [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1], [2, 3, 5]], 0),
    ]
    for _ in range(15):
        n = rng.randint(1, 12)
        edges = [
            [rng.randrange(n), rng.randrange(n), rng.randint(0, 20)]
            for _ in range(rng.randint(0, 3 * n))
        ]
        inputs.append((n, edges, rng.randrange(n)))
    return [
        {
            "name": f"case {i}",
            "input": {"n": n, "edges": e, "source": s},
            "expect": oracles.shortest_paths(n, e, s),
        }
        for i, (n, e, s) in enumerate(inputs)
    ]


def edit_distance_cases(rng: random.Random) -> list[dict]:
    """Empty strings, equal strings, classic examples and random short strings."""
    inputs = [
        ("", ""),
        ("", "abc"),
        ("abc", ""),
        ("same", "same"),
        ("kitten", "sitting"),
        ("flaw", "lawn"),
    ]
    for _ in range(14):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
        b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
        inputs.append((a, b))
    return [
        {"name": f"case {i}", "input": {"a": a, "b": b}, "expect": oracles.edit_distance(a, b)}
        for i, (a, b) in enumerate(inputs)
    ]


def find_all_cases(rng: random.Random) -> list[dict]:
    """Empty pattern, overlaps, no match, pattern longer than text and random text."""
    inputs = [
        ("abc", ""),
        ("", "a"),
        ("aaaa", "aa"),
        ("abababab", "abab"),
        ("abc", "abcd"),
        ("hello world", "o"),
        ("aabaabaaab", "aab"),
    ]
    for _ in range(13):
        text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 40)))
        pattern = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
        inputs.append((text, pattern))
    return [
        {"name": f"case {i}", "input": {"text": t, "pattern": p}, "expect": oracles.find_all(t, p)}
        for i, (t, p) in enumerate(inputs)
    ]


BUILDERS = {
    "lower_bound": lower_bound_cases,
    "merge_sort": merge_sort_cases,
    "dijkstra": dijkstra_cases,
    "edit_distance": edit_distance_cases,
    "find_all": find_all_cases,
}


def build() -> dict[str, str]:
    """Return {file name: JSON text} for every algorithm."""
    rng = random.Random(SEED)
    return {
        f"{name}.json": json.dumps({"algorithm": name, "cases": make(rng)}, indent=1) + "\n"
        for name, make in BUILDERS.items()
    }


def main() -> int:
    """Write the vectors, or with --check compare them to the committed files."""
    files = build()
    if "--check" in sys.argv:
        stale = [
            n
            for n, text in files.items()
            if not (OUT / n).exists() or (OUT / n).read_text() != text
        ]
        for name in stale:
            print(f"stale: spec/vectors/{name} (run python spec/generate_vectors.py)")
        return 1 if stale else 0
    OUT.mkdir(exist_ok=True)
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    cases = sum(len(json.loads(t)["cases"]) for t in files.values())
    print(f"wrote {len(files)} files, {cases} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())

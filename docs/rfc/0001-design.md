# RFC 0001: algorithms-proved-measured design

- **Status:** Accepted (M1 implemented)
- **Author:** EquinoxWN
- **Created:** 2026

## Problem

"It passed the sample input" is the most common way a wrong algorithm ships. Hand-picked examples
miss the edge cases that matter (empty input, duplicates, unreachable vertices, overlapping
matches), and when the same algorithm is written in several languages the copies drift apart.
This project keeps every algorithm honest in three ways: shared test vectors that all languages
must pass, a brute-force oracle that checks hundreds of random small inputs, and (from M2) a
written correctness argument plus a measured growth rate.

## Goals

- Each algorithm exists in Java, Python and JavaScript behind the same signature.
- Shared JSON vectors, generated from brute-force oracles, are replayed in every language.
- Every language also compares its implementation with its own brute-force oracle on 500 seeded
  random inputs per algorithm.
- Later: a correctness argument and fitted complexity per algorithm (M2), and write-ups where
  theory and measurement disagree plus a pattern index (M3).

## Non-goals

- A complete algorithms library; each algorithm earns its place by teaching a technique.
- Unicode-aware string algorithms. Strings are compared by code unit, and vectors use ASCII so
  Java, JavaScript (UTF-16) and Python (code points) agree.
- Running as a hosted production service.

## Proposed design

![architecture](../architecture.png)

```
python/tests/oracles.py ──► spec/generate_vectors.py ──► spec/vectors/*.json
                                                            ├─► java   VectorsTest  + OracleTest (Oracles.java)
                                                            ├─► python test_vectors + test_oracles (oracles.py)
                                                            └─► js     vectors.test + oracle.test (oracles.js)
```

### Algorithms in M1 (one per technique family)

| Algorithm | Signature (Python / Java / JS) | Technique | Oracle |
|---|---|---|---|
| Lower-bound binary search | `lower_bound(items, target)` | Loop invariant on a half-open range | Linear scan |
| Merge sort | `merge_sort(items)` returns a new list | Divide and conquer | Selection sort |
| Dijkstra | `dijkstra(n, edges, source)`, `-1` = unreachable | Greedy with a priority queue | Bellman-Ford |
| Edit distance | `edit_distance(a, b)` | Dynamic programming, two rows | Plain exponential recursion |
| KMP search | `find_all(text, pattern)`, overlaps included | Prefix function (failure links) | Compare at every position |

Language naming conventions are kept (`lowerBound` in Java and JS). Invalid graph input (source or
endpoint out of range, negative weight) raises `ValueError`, `IllegalArgumentException` or
`RangeError`; an empty pattern matches at every index `0..len(text)`, the same rule as Python's
`str.find`.

## Alternatives considered

| Option | Why not (yet) |
|---|---|
| Hand-written examples per language | The usual approach, and the reason edge cases slip through; no shared truth across languages. |
| Shared vectors only, no per-language oracles | 100 fixed cases are not enough to catch rare bugs; random oracle comparison adds 2,500 checks per language at almost no cost (ADR 0002). |
| Property-based testing libraries from day one (Hypothesis, jqwik, fast-check) | Better shrinking, but three different libraries and seeds. Seeded loops are identical in spirit across languages; libraries join in M2 for invariants. |
| Compare against the standard library (`sorted`, `Arrays.sort`) as the oracle | Fine for sorting, but there is no standard Dijkstra or KMP. Brute force works for every algorithm and is obviously correct. |
| Generate expected results with one implementation | A bug in that implementation would become the "truth" for all three. |

## Measurement plan

- M1: 100 shared vector cases and 7,500 random oracle comparisons (500 per algorithm, per
  language), all passing.
- M2: each implementation runs on inputs from 10^2 to 10^6; a log-log fit of time against size
  must match the claimed complexity (slope about 1 for O(n), about 1.0-1.1 for O(n log n)).
- M3: cases where theory and measurement disagree (quicksort on sorted input, hash collisions).

## Milestones

- **M1 (done):** five algorithms in three languages, vector generator with `--check`, three
  vector runners and three oracle test suites.
- **M2:** correctness arguments, growth-rate harness and charts, more algorithms (heap sort,
  radix sort, MST, SCC, Z-function, knapsack).
- **M3:** theory-versus-measurement write-ups and the pattern index.

## Risks and open questions

- Integer limits differ (Java `int` and `long`, JS doubles, Python big ints). Inputs stay small
  enough that distances fit in a JS double exactly; M2 must keep large benchmark inputs in range.
- Oracles can share a misunderstanding with the implementation (for example, what an empty
  pattern means). The rule is written down here and covered by an explicit vector.
- Seeded random tests find bugs only for the sizes they generate. M2 adds property tests with
  shrinking for invariants.

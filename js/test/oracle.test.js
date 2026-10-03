import assert from "node:assert/strict";
import { test } from "node:test";
import { dijkstra, editDistance, findAll, lowerBound, mergeSort } from "../src/index.js";
import * as oracles from "./oracles.js";

const CASES = 500; // random cases per algorithm

/** Small seeded generator (mulberry32) so failures are reproducible. */
function rng(seed) {
  let s = seed >>> 0;
  const next = () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const int = (lo, hi) => lo + Math.floor(next() * (hi - lo + 1));
  const str = (alphabet, n) => Array.from({ length: n }, () => alphabet[int(0, alphabet.length - 1)]).join("");
  return { int, str };
}

test("lowerBound matches a linear scan", () => {
  const r = rng(1);
  for (let c = 0; c < CASES; c++) {
    const items = Array.from({ length: r.int(0, 40) }, () => r.int(-30, 30)).sort((x, y) => x - y);
    const target = r.int(-35, 35);
    assert.equal(lowerBound(items, target), oracles.lowerBound(items, target), JSON.stringify([items, target]));
  }
});

test("mergeSort matches selection sort and keeps its input", () => {
  const r = rng(2);
  for (let c = 0; c < CASES; c++) {
    const items = Array.from({ length: r.int(0, 60) }, () => r.int(-100, 100));
    const before = [...items];
    assert.deepEqual(mergeSort(items), oracles.sort(items), JSON.stringify(items));
    assert.deepEqual(items, before);
  }
});

test("dijkstra matches Bellman-Ford", () => {
  const r = rng(3);
  for (let c = 0; c < CASES; c++) {
    const n = r.int(1, 15);
    const edges = Array.from({ length: r.int(0, 4 * n) }, () => [r.int(0, n - 1), r.int(0, n - 1), r.int(0, 30)]);
    const source = r.int(0, n - 1);
    assert.deepEqual(dijkstra(n, edges, source), oracles.shortestPaths(n, edges, source), JSON.stringify([n, edges, source]));
  }
});

test("editDistance matches plain recursion", () => {
  const r = rng(4);
  for (let c = 0; c < CASES; c++) {
    const a = r.str("abc", r.int(0, 6));
    const b = r.str("abc", r.int(0, 6));
    assert.equal(editDistance(a, b), oracles.editDistance(a, b), `${a} / ${b}`);
  }
});

test("findAll matches naive search", () => {
  const r = rng(5);
  for (let c = 0; c < CASES; c++) {
    const text = r.str("ab", r.int(0, 50));
    const pattern = r.str("ab", r.int(0, 5));
    assert.deepEqual(findAll(text, pattern), oracles.findAll(text, pattern), `${text} / ${pattern}`);
  }
});

test("dijkstra rejects bad input", () => {
  assert.throws(() => dijkstra(2, [], 3), /source out of range/);
  assert.throws(() => dijkstra(2, [[0, 5, 1]], 0), /endpoint out of range/);
  assert.throws(() => dijkstra(2, [[0, 1, -1]], 0), /negative/);
});

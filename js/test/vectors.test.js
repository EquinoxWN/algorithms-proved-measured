import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { test } from "node:test";
import { dijkstra, editDistance, findAll, lowerBound, mergeSort } from "../src/index.js";

const VECTORS = new URL("../../spec/vectors/", import.meta.url);

const CALLS = {
  lower_bound: (i) => lowerBound(i.items, i.target),
  merge_sort: (i) => mergeSort(i.items),
  dijkstra: (i) => dijkstra(i.n, i.edges, i.source),
  edit_distance: (i) => editDistance(i.a, i.b),
  find_all: (i) => findAll(i.text, i.pattern),
};

for (const [name, call] of Object.entries(CALLS)) {
  const doc = JSON.parse(readFileSync(new URL(`${name}.json`, VECTORS), "utf8"));
  for (const c of doc.cases) {
    test(`${name}: ${c.name}`, () => assert.deepEqual(call(c.input), c.expect));
  }
}

test("every algorithm has vectors", () => {
  const files = readdirSync(VECTORS).filter((f) => f.endsWith(".json")).map((f) => f.slice(0, -5));
  assert.deepEqual(files.sort(), Object.keys(CALLS).sort());
});

// Brute-force oracles: obviously correct, deliberately slow, used only on small inputs.

/** Linear scan for the first value >= target. */
export function lowerBound(items, target) {
  const i = items.findIndex((x) => x >= target);
  return i === -1 ? items.length : i;
}

/** Selection sort. */
export function sort(items) {
  const out = [...items];
  for (let i = 0; i < out.length; i++) {
    let m = i;
    for (let j = i + 1; j < out.length; j++) if (out[j] < out[m]) m = j;
    [out[i], out[m]] = [out[m], out[i]];
  }
  return out;
}

/** Bellman-Ford: relax every edge n - 1 times. */
export function shortestPaths(n, edges, source) {
  const dist = new Array(n).fill(Infinity);
  dist[source] = 0;
  for (let round = 0; round < n - 1; round++) {
    for (const [u, v, w] of edges) if (dist[u] + w < dist[v]) dist[v] = dist[u] + w;
  }
  return dist.map((d) => (d === Infinity ? -1 : d));
}

/** Plain recursion over the three edit choices (exponential time). */
export function editDistance(a, b) {
  if (a.length === 0 || b.length === 0) return a.length + b.length;
  if (a[0] === b[0]) return editDistance(a.slice(1), b.slice(1));
  return 1 + Math.min(editDistance(a.slice(1), b), editDistance(a, b.slice(1)), editDistance(a.slice(1), b.slice(1)));
}

/** Compare the pattern at every position. */
export function findAll(text, pattern) {
  const out = [];
  for (let i = 0; i + pattern.length <= text.length; i++) if (text.startsWith(pattern, i)) out.push(i);
  return out;
}

/** First index whose value is >= target, or items.length if none. */
export function lowerBound(items, target) {
  let lo = 0;
  let hi = items.length;
  // Invariant: every value before lo is < target, every value from hi on is >= target.
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (items[mid] < target) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}

/** New array with the items in ascending order; the input is not changed. */
export function mergeSort(items) {
  const out = [...items];
  if (out.length > 1) sortRange(out, new Array(out.length), 0, out.length);
  return out;
}

/** Sorts a[lo, hi) in place, using buf as scratch space. */
function sortRange(a, buf, lo, hi) {
  if (hi - lo < 2) return;
  const mid = (lo + hi) >>> 1;
  sortRange(a, buf, lo, mid);
  sortRange(a, buf, mid, hi);
  if (a[mid - 1] <= a[mid]) return; // halves already in order
  for (let k = lo; k < hi; k++) buf[k] = a[k];
  let i = lo;
  let j = mid;
  for (let k = lo; k < hi; k++) {
    if (j >= hi || (i < mid && buf[i] <= buf[j])) a[k] = buf[i++];
    else a[k] = buf[j++];
  }
}

/** Shortest distance from source to every vertex; -1 marks unreachable vertices. */
export function dijkstra(n, edges, source) {
  if (!(source >= 0 && source < n)) throw new RangeError("source out of range");
  const adj = Array.from({ length: n }, () => []);
  for (const [u, v, w] of edges) {
    if (!(u >= 0 && u < n && v >= 0 && v < n)) throw new RangeError("edge endpoint out of range");
    if (w < 0) throw new RangeError("negative edge weight");
    adj[u].push([v, w]);
  }
  const dist = new Array(n).fill(-1);
  const heap = new MinHeap();
  heap.push([0, source]);
  while (heap.size > 0) {
    const [d, u] = heap.pop();
    if (dist[u] !== -1) continue; // already settled with a shorter distance
    dist[u] = d;
    for (const [v, w] of adj[u]) if (dist[v] === -1) heap.push([d + w, v]);
  }
  return dist;
}

/** Binary min-heap of [priority, value] pairs. */
class MinHeap {
  #a = [];

  get size() {
    return this.#a.length;
  }

  /** Adds an entry. */
  push(entry) {
    const a = this.#a;
    a.push(entry);
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (a[p][0] <= a[i][0]) break;
      [a[p], a[i]] = [a[i], a[p]];
      i = p;
    }
  }

  /** Removes and returns the smallest entry. */
  pop() {
    const a = this.#a;
    const top = a[0];
    const last = a.pop();
    if (a.length > 0) {
      a[0] = last;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1;
        const r = l + 1;
        let m = i;
        if (l < a.length && a[l][0] < a[m][0]) m = l;
        if (r < a.length && a[r][0] < a[m][0]) m = r;
        if (m === i) break;
        [a[m], a[i]] = [a[i], a[m]];
        i = m;
      }
    }
    return top;
  }
}

/** Minimum inserts, deletes and substitutions that turn a into b. */
export function editDistance(a, b) {
  if (a.length < b.length) [a, b] = [b, a]; // keep the row as short as possible
  let prev = Array.from({ length: b.length + 1 }, (_, j) => j);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) {
      const sub = prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1);
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, sub);
    }
    prev = cur;
  }
  return prev[b.length];
}

/** Every start index where pattern occurs in text, overlaps included. */
export function findAll(text, pattern) {
  if (pattern.length === 0) return Array.from({ length: text.length + 1 }, (_, i) => i);
  const border = prefixFunction(pattern);
  const out = [];
  let k = 0;
  for (let i = 0; i < text.length; i++) {
    while (k > 0 && text[i] !== pattern[k]) k = border[k - 1];
    if (text[i] === pattern[k]) k++;
    if (k === pattern.length) {
      out.push(i - k + 1);
      k = border[k - 1];
    }
  }
  return out;
}

/** Length of the longest proper border of every prefix of p. */
function prefixFunction(p) {
  const pi = new Array(p.length).fill(0);
  let k = 0;
  for (let i = 1; i < p.length; i++) {
    while (k > 0 && p[i] !== p[k]) k = pi[k - 1];
    if (p[i] === p[k]) k++;
    pi[i] = k;
  }
  return pi;
}

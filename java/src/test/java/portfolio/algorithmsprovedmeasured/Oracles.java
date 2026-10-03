package portfolio.algorithmsprovedmeasured;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Brute-force oracles: obviously correct, deliberately slow, used only on small inputs. */
final class Oracles {
    private Oracles() {}

    /** Linear scan for the first value >= target. */
    static int lowerBound(int[] items, int target) {
        for (int i = 0; i < items.length; i++) {
            if (items[i] >= target) {
                return i;
            }
        }
        return items.length;
    }

    /** Selection sort. */
    static int[] sort(int[] items) {
        int[] out = items.clone();
        for (int i = 0; i < out.length; i++) {
            int m = i;
            for (int j = i + 1; j < out.length; j++) {
                if (out[j] < out[m]) {
                    m = j;
                }
            }
            int t = out[i];
            out[i] = out[m];
            out[m] = t;
        }
        return out;
    }

    /** Bellman-Ford: relax every edge n - 1 times. */
    static long[] shortestPaths(int n, int[][] edges, int source) {
        long inf = Long.MAX_VALUE;
        long[] dist = new long[n];
        Arrays.fill(dist, inf);
        dist[source] = 0;
        for (int round = 0; round < n - 1; round++) {
            for (int[] e : edges) {
                if (dist[e[0]] != inf && dist[e[0]] + e[2] < dist[e[1]]) {
                    dist[e[1]] = dist[e[0]] + e[2];
                }
            }
        }
        for (int i = 0; i < n; i++) {
            if (dist[i] == inf) {
                dist[i] = -1;
            }
        }
        return dist;
    }

    /** Plain recursion over the three edit choices (exponential time). */
    static int editDistance(String a, String b) {
        if (a.isEmpty() || b.isEmpty()) {
            return a.length() + b.length();
        }
        if (a.charAt(0) == b.charAt(0)) {
            return editDistance(a.substring(1), b.substring(1));
        }
        int best = Math.min(editDistance(a.substring(1), b), editDistance(a, b.substring(1)));
        return 1 + Math.min(best, editDistance(a.substring(1), b.substring(1)));
    }

    /** Compare the pattern at every position. */
    static List<Integer> findAll(String text, String pattern) {
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i + pattern.length() <= text.length(); i++) {
            if (text.startsWith(pattern, i)) {
                out.add(i);
            }
        }
        return out;
    }
}

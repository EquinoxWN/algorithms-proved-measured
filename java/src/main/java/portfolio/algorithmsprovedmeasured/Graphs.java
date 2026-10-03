package portfolio.algorithmsprovedmeasured;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

/** Dijkstra's single-source shortest paths on a directed graph. */
public final class Graphs {
    private Graphs() {}

    /** Shortest distance from source to every vertex; -1 marks unreachable vertices. */
    public static long[] dijkstra(int n, int[][] edges, int source) {
        if (source < 0 || source >= n) {
            throw new IllegalArgumentException("source out of range");
        }
        List<List<int[]>> adj = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        for (int[] e : edges) {
            if (e[0] < 0 || e[0] >= n || e[1] < 0 || e[1] >= n) {
                throw new IllegalArgumentException("edge endpoint out of range");
            }
            if (e[2] < 0) {
                throw new IllegalArgumentException("negative edge weight");
            }
            adj.get(e[0]).add(new int[] {e[1], e[2]});
        }
        long[] dist = new long[n];
        Arrays.fill(dist, -1);
        PriorityQueue<long[]> heap = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
        heap.add(new long[] {0, source});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (dist[u] != -1) { // already settled with a shorter distance
                continue;
            }
            dist[u] = top[0];
            for (int[] vw : adj.get(u)) {
                if (dist[vw[0]] == -1) {
                    heap.add(new long[] {top[0] + vw[1], vw[0]});
                }
            }
        }
        return dist;
    }
}

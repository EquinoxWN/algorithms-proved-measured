package portfolio.algorithmsprovedmeasured;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Arrays;
import java.util.Random;
import org.junit.jupiter.api.Test;

/** Random inputs: every implementation must agree with its brute-force oracle. */
class OracleTest {
    private static final int CASES = 500;

    @Test
    void lowerBoundMatchesLinearScan() {
        Random rng = new Random(1);
        for (int c = 0; c < CASES; c++) {
            int[] items = randomInts(rng, rng.nextInt(41), -30, 30);
            Arrays.sort(items);
            int target = rng.nextInt(71) - 35;
            assertEquals(Oracles.lowerBound(items, target), Search.lowerBound(items, target),
                    () -> Arrays.toString(items) + " " + target);
        }
    }

    @Test
    void mergeSortMatchesSelectionSortAndKeepsInput() {
        Random rng = new Random(2);
        for (int c = 0; c < CASES; c++) {
            int[] items = randomInts(rng, rng.nextInt(61), -100, 100);
            int[] before = items.clone();
            assertArrayEquals(Oracles.sort(items), Sorting.mergeSort(items), () -> Arrays.toString(items));
            assertArrayEquals(before, items);
        }
    }

    @Test
    void dijkstraMatchesBellmanFord() {
        Random rng = new Random(3);
        for (int c = 0; c < CASES; c++) {
            int n = 1 + rng.nextInt(15);
            int[][] edges = new int[rng.nextInt(4 * n + 1)][];
            for (int i = 0; i < edges.length; i++) {
                edges[i] = new int[] {rng.nextInt(n), rng.nextInt(n), rng.nextInt(31)};
            }
            int source = rng.nextInt(n);
            assertArrayEquals(Oracles.shortestPaths(n, edges, source), Graphs.dijkstra(n, edges, source),
                    () -> n + " " + Arrays.deepToString(edges) + " " + source);
        }
    }

    @Test
    void editDistanceMatchesRecursion() {
        Random rng = new Random(4);
        for (int c = 0; c < CASES; c++) {
            String a = randomString(rng, "abc", rng.nextInt(7));
            String b = randomString(rng, "abc", rng.nextInt(7));
            assertEquals(Oracles.editDistance(a, b), DynamicProgramming.editDistance(a, b), a + " / " + b);
        }
    }

    @Test
    void findAllMatchesNaiveSearch() {
        Random rng = new Random(5);
        for (int c = 0; c < CASES; c++) {
            String text = randomString(rng, "ab", rng.nextInt(51));
            String pattern = randomString(rng, "ab", rng.nextInt(6));
            assertEquals(Oracles.findAll(text, pattern), Strings.findAll(text, pattern), text + " / " + pattern);
        }
    }

    @Test
    void dijkstraRejectsBadInput() {
        assertThrows(IllegalArgumentException.class, () -> Graphs.dijkstra(2, new int[0][], 3));
        assertThrows(IllegalArgumentException.class, () -> Graphs.dijkstra(2, new int[][] {{0, 5, 1}}, 0));
        assertThrows(IllegalArgumentException.class, () -> Graphs.dijkstra(2, new int[][] {{0, 1, -1}}, 0));
    }

    /** n random ints in [lo, hi]. */
    private static int[] randomInts(Random rng, int n, int lo, int hi) {
        int[] out = new int[n];
        for (int i = 0; i < n; i++) {
            out[i] = lo + rng.nextInt(hi - lo + 1);
        }
        return out;
    }

    /** Random string of length n over the alphabet. */
    private static String randomString(Random rng, String alphabet, int n) {
        StringBuilder sb = new StringBuilder(n);
        for (int i = 0; i < n; i++) {
            sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
        }
        return sb.toString();
    }
}

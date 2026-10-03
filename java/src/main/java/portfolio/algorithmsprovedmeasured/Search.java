package portfolio.algorithmsprovedmeasured;

/** Binary search in its lower-bound form. */
public final class Search {
    private Search() {}

    /** First index whose value is >= target, or items.length if none. */
    public static int lowerBound(int[] items, int target) {
        int lo = 0;
        int hi = items.length;
        // Invariant: every value before lo is < target, every value from hi on is >= target.
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (items[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return lo;
    }
}

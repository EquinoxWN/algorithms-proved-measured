package portfolio.algorithmsprovedmeasured;

/** Top-down merge sort. */
public final class Sorting {
    private Sorting() {}

    /** New array with the items in ascending order; the input is not changed. */
    public static int[] mergeSort(int[] items) {
        int[] out = items.clone();
        if (out.length > 1) {
            sort(out, new int[out.length], 0, out.length);
        }
        return out;
    }

    /** Sorts a[lo, hi) in place, using buf as scratch space. */
    private static void sort(int[] a, int[] buf, int lo, int hi) {
        if (hi - lo < 2) {
            return;
        }
        int mid = (lo + hi) >>> 1;
        sort(a, buf, lo, mid);
        sort(a, buf, mid, hi);
        if (a[mid - 1] <= a[mid]) { // halves already in order
            return;
        }
        System.arraycopy(a, lo, buf, lo, hi - lo);
        int i = lo;
        int j = mid;
        for (int k = lo; k < hi; k++) {
            if (j >= hi || (i < mid && buf[i] <= buf[j])) {
                a[k] = buf[i++];
            } else {
                a[k] = buf[j++];
            }
        }
    }
}

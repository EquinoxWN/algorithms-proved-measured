package portfolio.algorithmsprovedmeasured;

/** Levenshtein edit distance by dynamic programming. */
public final class DynamicProgramming {
    private DynamicProgramming() {}

    /** Minimum inserts, deletes and substitutions that turn a into b. */
    public static int editDistance(String a, String b) {
        if (a.length() < b.length()) { // keep the row as short as possible
            String t = a;
            a = b;
            b = t;
        }
        int[] prev = new int[b.length() + 1];
        for (int j = 0; j <= b.length(); j++) {
            prev[j] = j;
        }
        for (int i = 1; i <= a.length(); i++) {
            int[] cur = new int[b.length() + 1];
            cur[0] = i;
            for (int j = 1; j <= b.length(); j++) {
                int sub = prev[j - 1] + (a.charAt(i - 1) == b.charAt(j - 1) ? 0 : 1);
                cur[j] = Math.min(Math.min(prev[j] + 1, cur[j - 1] + 1), sub);
            }
            prev = cur;
        }
        return prev[b.length()];
    }
}

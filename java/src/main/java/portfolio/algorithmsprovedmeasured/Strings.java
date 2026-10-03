package portfolio.algorithmsprovedmeasured;

import java.util.ArrayList;
import java.util.List;

/** Knuth-Morris-Pratt substring search. */
public final class Strings {
    private Strings() {}

    /** Every start index where pattern occurs in text, overlaps included. */
    public static List<Integer> findAll(String text, String pattern) {
        List<Integer> out = new ArrayList<>();
        if (pattern.isEmpty()) {
            for (int i = 0; i <= text.length(); i++) {
                out.add(i);
            }
            return out;
        }
        int[] border = prefixFunction(pattern);
        int k = 0;
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            while (k > 0 && ch != pattern.charAt(k)) {
                k = border[k - 1];
            }
            if (ch == pattern.charAt(k)) {
                k++;
            }
            if (k == pattern.length()) {
                out.add(i - k + 1);
                k = border[k - 1];
            }
        }
        return out;
    }

    /** Length of the longest proper border of every prefix of p. */
    private static int[] prefixFunction(String p) {
        int[] pi = new int[p.length()];
        int k = 0;
        for (int i = 1; i < p.length(); i++) {
            while (k > 0 && p.charAt(i) != p.charAt(k)) {
                k = pi[k - 1];
            }
            if (p.charAt(i) == p.charAt(k)) {
                k++;
            }
            pi[i] = k;
        }
        return pi;
    }
}

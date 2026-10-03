# ADR 0002: Check every language against its own brute-force oracle, not only shared vectors

- **Status:** Accepted

## Context

Shared vectors make the three languages agree on 100 fixed cases, and those cases are generated
from brute-force oracles so their expected values are trustworthy. But 100 cases cover only the
inputs someone thought of, and a rare bug (an off-by-one that appears only with duplicates at the
end of an array, or a failure link that is wrong for one pattern shape) can pass all of them.

## Decision

Each language ships its own brute-force oracles (linear scan, selection sort, Bellman-Ford, plain
recursion, naive matching) in its test folder and compares the real implementation with them on
500 seeded random inputs per algorithm. Inputs are kept small so the slow oracles stay fast.
Seeds are fixed, so any failure can be reproduced from the message, which prints the input.

## Consequences

- 7,500 extra checks per full run (2,500 per language) for about one second of test time.
- Oracle code is written three times. It is short and deliberately naive, so it is easy to review;
  a mistake in one language's oracle shows up as a disagreement with the shared vectors.
- Random inputs come from different generators in each language, so together they explore more
  of the input space than one shared random set would.
- Small inputs cannot expose problems that appear only at scale (overflow, recursion depth). The
  M2 growth-rate harness covers large inputs.

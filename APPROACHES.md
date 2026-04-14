# Candidate approach families

This repository exists to compare deterministic OMR-reading approaches on one or more PDFs.

The current implementations should be seen as the first three benchmarked candidates in an expanding study.

## Current benchmarked approaches

### Approach 1. Manual calibration baseline

Use fixed coordinates for the answer cells and read darkness directly at those positions.

Characteristics:
- simplest implementation
- highly auditable
- strongest dependency on fixed geometry
- good baseline for comparison

Current result on `sample.pdf`:
- 44/45 exact
- 0 wrong
- 1 `NULL`

### Approach 2. Template registration + intensity reading

Align the page to a canonical layout, then read the answer cells at the expected coordinates.

Characteristics:
- keeps the same transparent scoring as approach 1
- adds geometric normalization before measurement
- intended to be more robust when input geometry drifts slightly

Current result on `sample.pdf`:
- 44/45 exact
- 0 wrong
- 1 `NULL`

### Approach 3. Timing-mark anchored registration

Detect the right-edge timing marks and use them as structural anchors for row positioning before reading answer cells.

Characteristics:
- uses form structure designed for machine reading
- remains deterministic and auditable
- best current fit for row alignment on this sheet family

Current result on `sample.pdf`:
- 45/45 exact
- 0 wrong
- 0 `NULL`

## Additional approach families worth testing later

These are still reasonable candidates for later expansion:

### Approach 4. Hybrid registration

Combine coarse template registration with local timing-mark correction.

Why it matters:
- likely strongest classical CV option if geometry variation grows
- natural next hardening step after approaches 2 and 3

### Approach 5. Contour/component-based OMR

Detect answer areas through thresholding and connected components rather than using predeclared cell centers.

Why it matters:
- more layout-driven than coordinate-driven
- useful as a contrasting family in the benchmark

### Approach 6. Learned filled-vs-empty cell classifier

After registration, classify cropped cells as filled or empty.

Why it matters:
- may help with faint or noisy marks
- more complex and less elegant than current deterministic methods

### Approach 7. Multi-method consensus

Run several approaches and only accept an answer when they agree or when one wins with strong confidence.

Why it matters:
- can trade coverage for trustworthiness
- attractive once there are multiple datasets and known failure modes

## Current recommendation

For the current repository state:
1. keep approach 1 as a reference baseline
2. treat approaches 2 and 3 as real comparative candidates
3. prefer approach 3 as the best observed method on the first dataset
4. evolve the repo around cross-dataset comparison, not around one single winning script

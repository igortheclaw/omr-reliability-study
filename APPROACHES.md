# Candidate approach families

This repository compares deterministic OMR-reading approaches across dataset directories, not one-off PDFs.

## Current benchmarked approaches

### Approach 1. Manual calibration baseline

Use fixed coordinates for the answer cells and read darkness directly at those positions.

Characteristics:
- simplest implementation
- highly auditable
- strongest dependency on fixed geometry
- good baseline for comparison

Current observed result on dataset `sample`:
- 44/45 exact
- 0 wrong
- 1 `NULL`

### Approach 2. Template registration + intensity reading

Align the page to a canonical layout, then read the answer cells at the expected coordinates.

Characteristics:
- keeps the same transparent scoring as approach 1
- adds geometric normalization before measurement
- intended to be more robust when input geometry drifts slightly

Current observed result on dataset `sample`:
- 44/45 exact
- 0 wrong
- 1 `NULL`

### Approach 3. Timing-mark anchored registration

Detect the right-edge timing marks and use them as structural anchors for row positioning before reading answer cells.

Characteristics:
- uses form structure designed for machine reading
- remains deterministic and auditable
- best current fit for row alignment on this sheet family

Current observed result on dataset `sample`:
- 45/45 exact
- 0 wrong
- 0 `NULL`

## Additional approach families worth testing later

### Approach 4. Hybrid registration

Combine coarse template registration with local timing-mark correction.

### Approach 5. Contour/component-based OMR

Detect answer areas through thresholding and connected components rather than using predeclared cell centers.

### Approach 6. Learned filled-vs-empty cell classifier

After registration, classify cropped cells as filled or empty.

### Approach 7. Multi-method consensus

Run several approaches and only accept an answer when they agree or when one wins with strong confidence.

## Current recommendation

- keep approach 1 as the reference baseline
- treat approaches 2 and 3 as real comparative candidates
- prefer approach 3 as the best observed method on `sample`
- expand the repo by filling dataset ground truth, not by adding one-off scripts

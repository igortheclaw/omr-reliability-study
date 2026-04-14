# Comparative OMR approaches for this sheet

## Goal

Evaluate multiple deterministic ways to read rows 1-45 from `sample.pdf`, using the same ground truth and comparable metrics.

## Implemented approaches

### 1. Manual calibration baseline

Method:
- keep the original hand-tuned bubble centers for the two visible answer groups
- measure mean darkness inside a circular patch at each A/B/C/D location
- pick the darkest option
- return `NULL` when the top two scores are too close

Why it matters:
- simplest and easiest to audit
- serves as the control for the rest of the study

Observed result:
- **44/45 exact**
- **0 wrong**
- **1 NULL**
- borderline row: **35**

### 2. Fixed-template registration + intensity reading

Method:
- treat the current page layout as a canonical template
- run affine ECC registration on the answer-region crop
- transform the expected bubble coordinates through the estimated warp
- read bubble darkness at the registered positions
- use the same margin rule as approach 1

Why it matters:
- same transparent readout logic as the baseline
- introduces an explicit geometric normalization stage
- useful as the natural next hardening step for small drift

Observed result:
- **44/45 exact**
- **0 wrong**
- **1 NULL**
- same borderline row: **35**

Interpretation:
- on this already well-aligned sample, template registration does not materially change the result
- it still documents the registration-based family honestly and reproducibly

### 3. Timing-mark anchored registration

Method:
- threshold the page and detect the repeated right-edge timing marks as connected components
- sort them vertically and use the visible sequence as the row anchor set
- map each scored row onto its detected timing mark Y coordinate
- keep fixed X coordinates for the A/B/C/D bubbles within each answer group
- read bubble darkness using the same deterministic scorer

Why it matters:
- uses structural features that are actually designed for machine reading
- reduces dependence on hand-entered row Y coordinates
- stays simple and auditable

Observed result:
- **45/45 exact**
- **0 wrong**
- **0 NULL**

Interpretation:
- on the provided page, the timing marks correct the slight Y offset that made row 35 ambiguous for the baseline family
- this is the best observed method in the repo right now

## Shared evaluation policy

All approaches are benchmarked the same way:
- same rendered page
- same ground truth
- same answer vocabulary
- same metrics: exact matches, wrong, NULL, accuracy, accepted precision, accepted coverage

## Recommendation from the current evidence

For this specific sample:
1. keep approach 1 as the clean control baseline
2. keep approach 2 as the registration-family comparator
3. prefer approach 3 as the best observed deterministic method

Important caveat:
- this repo still benchmarks one provided form only
- stronger claims would require perturbation tests or more pages

# Benchmark report

## Baseline tested

Manual calibration plus deterministic cell darkness reading on a fixed 200 DPI render of `sample.pdf`.

## Calibration

Two visible answer groups were calibrated independently:

- Rows 1-25
- Rows 26-45

For each row, the method samples four circular regions centered on the A/B/C/D bubbles and computes darkness as `255 - mean_intensity`.

Decision rule:
- choose the darkest option
- return `NULL` if the margin over the second darkest option is below `10.0`

Parameters:
- render DPI: 200
- sample radius: 11 px
- row spacing: 34 px

## Result against trusted ground truth

- Exact matches: **44 / 45**
- Wrong answers: **0 / 45**
- `NULL`: **1 / 45**
- Accuracy: **97.78%**
- Accepted precision: **100%**
- Accepted coverage: **97.78%**

## Failure analysis

Only one row was rejected:

- Row 35
  - Ground truth: `A`
  - Predicted: `NULL`
  - Best-vs-second margin: `7.28`

This is acceptable under the project preference that `NULL` is better than a wrong answer.

## Current assessment

This baseline already clears the stated success condition.

Strengths:
- simple
- auditable
- deterministic
- no wrong accepted answers on rows 1-45

Weaknesses:
- currently calibrated to one fixed render geometry
- not yet tested against perturbations
- row 35 is borderline and should be inspected in robustness tests

## Recommended next steps

1. Refactor the baseline into a reusable CLI with configurable calibration.
2. Add perturbation tests:
   - different DPI
   - small rotation
   - brightness/contrast changes
   - tiny crop shifts
3. Add optional local registration so calibration survives small image drift.
4. Produce a final recommendation after robustness testing.

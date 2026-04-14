# TASK

## Objective

Determine the most reliable way to read the filled answer boxes in `sample.pdf` for rows **1-45** only.

## Success condition

A method is acceptable if it demonstrates either:
- **>90% exact accuracy**, or
- very high precision with `NULL` for ambiguous rows

## Current status

Phase 1 through Phase 3 have a working first pass.

Implemented baseline:
- manual calibration
- fixed 200 DPI render
- deterministic cell darkness reading
- `NULL` when confidence margin is too small

Current benchmark result:
- **44/45 exact matches**
- **0 wrong answers**
- **1 NULL**
- **97.78% exact accuracy**
- **100% accepted precision**

Known borderline row:
- row 35, currently returned as `NULL`

## Remaining work

### Phase 4 — Robustness tests

Test the current baseline against small perturbations:
- different DPI renders
- tiny rotation
- brightness/contrast changes
- slight crop shifts
- blur/noise

A method that collapses under minor perturbations is not acceptable.

### Phase 5 — Final recommendation

Document:
- whether the current baseline remains above threshold under perturbation
- whether a lightweight registration step is necessary
- remaining failure modes
- whether the method is safe for production use

## Deliverables

Already available:
- `ground_truth.json`
- `omr_baseline.py`
- `out/baseline_overlay.png`
- `out/baseline_results.json`
- `benchmark_report.md`

Still desirable:
- robustness test harness
- final recommendation report
- optional calibration/registration abstraction

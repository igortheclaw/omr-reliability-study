# TASK

## Objective

Determine the most reliable way to read the filled answer boxes in `sample.pdf` for rows **1-45** only.

## Non-goals

- No exam-question parsing
- No database integration
- No reuse of previous project assumptions
- No attempt to read rows 46-100 as valid answers

## Required success condition

A proposed method is only acceptable if it can be demonstrated to reach:
- **>90% accuracy**, or
- very high precision with `NULL` for ambiguous rows

## Phase 1 — Ground truth

A trusted manual answer file for rows 1-45 is already provided.

Available artifact:
- `ground_truth.json`

Optional follow-up artifacts:
- annotated image showing row number and selected option

Possible first helper steps (not implemented yet):
- render `sample.pdf` to PNG at one or more fixed DPI values
- generate an overlay image with rows 1-45 clearly numbered
- create a small review checklist for manual annotation consistency

## Phase 2 — Baseline implementation

Implement at least one deterministic baseline, ideally:
- manual calibration + fixed coordinates, or
- template registration + cell intensity reading

Deliverables:
- extraction script
- debug images
- result JSON with confidence per row

## Phase 3 — Benchmarking

For each method tested, report:
- exact matches / 45
- wrong answers / 45
- `NULL` answers / 45
- precision, recall, and accepted coverage
- rows that fail repeatedly

Deliverables:
- benchmark script
- benchmark report in Markdown

## Phase 4 — Robustness tests

Test the method against small perturbations:
- different DPI renders
- tiny rotation
- brightness/contrast changes
- slight crop shifts
- blur/noise

A method that collapses under minor perturbations is not acceptable.

## Phase 5 — Final recommendation

Document:
- best method
- why it won
- remaining failure modes
- whether it is safe for production use

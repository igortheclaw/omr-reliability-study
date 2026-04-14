# OMR Reliability Study

Small isolated project to evaluate how reliably we can read filled answer boxes from a single OMR-style PDF page.

## Scope

This project is intentionally narrow.

- Only one page family is in scope: `sample.pdf`
- Only rows **1-45** matter
- Valid outputs are `A`, `B`, `C`, `D`, or `NULL`
- `NULL` is preferred over a wrong answer

The sheet contains 100 numbered rows, but rows 46-100 are out of scope.

## Goal

Identify a method that is:
- reproducible
- auditable
- robust
- above 90% reliability on rows 1-45

## Current result

A first deterministic baseline is implemented in `omr_baseline.py`.

Benchmark on the provided `sample.pdf`:
- **44 / 45 exact matches**
- **0 wrong answers**
- **1 `NULL`**
- **97.78% exact accuracy**
- **100% precision on accepted answers**

This already clears the project success threshold.

## Method in use

Current baseline:
- render `sample.pdf` at 200 DPI
- use manual calibration for the two visible answer groups
- sample darkness at the A/B/C/D bubble centers for each row
- pick the darkest option
- emit `NULL` if the best-vs-second-best margin is too small

The current implementation is deterministic and easy to inspect.

## Repository contents

Core inputs:
- `sample.pdf` — target document
- `ground_truth.json` — trusted answers for rows 1-45
- `ground_truth.template.json` — template for manual answer files

Core implementation:
- `omr_baseline.py` — current baseline extractor and benchmark runner

Documentation:
- `TASK.md` — current project status and next steps
- `APPROACHES.md` — candidate method families and recommendation
- `benchmark_report.md` — current benchmark summary

Generated artifacts:
- `out/page-1.png` — 200 DPI render used by the baseline
- `out/baseline_overlay.png` — debug overlay showing sampled cells
- `out/baseline_results.json` — predictions, scores, and metrics

## How to run

From the repo root:

```bash
mkdir -p out
pdftoppm -png -r 200 sample.pdf out/page
python3 omr_baseline.py
```

## Current assessment

The baseline is already good enough to count as a viable solution for the provided sample.

What remains before calling it production-safe:
- robustness testing under small perturbations
- optional lightweight registration so the calibration survives minor geometric drift
- cleanup into a more reusable CLI or module shape

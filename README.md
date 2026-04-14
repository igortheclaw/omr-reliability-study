# OMR Reliability Study

Small deterministic CV study for reading the filled answer bubbles on `sample.pdf`.

## Scope

This repo stays intentionally narrow.

- One page family: `sample.pdf`
- Only rows **1-45** are benchmarked
- Valid outputs are `A`, `B`, `C`, `D`, or `NULL`
- `NULL` is preferable to a wrong answer

The sheet contains 100 numbered rows, but rows 46-100 are out of scope for this study.

## What this repo does now

This is now a **comparative OMR study**, not just a single working baseline.

Implemented approaches:

1. **Approach 1, manual calibration baseline**
   - fixed bubble coordinates
   - direct intensity reading at bubble centers
   - `NULL` on low best-vs-second-best margin
2. **Approach 2, fixed-template registration + intensity reading**
   - affine ECC registration to a canonical layout
   - then the same deterministic bubble readout
3. **Approach 3, timing-mark anchored registration**
   - detect the right-edge timing marks
   - use them as row anchors
   - then read the fixed answer columns

## Observed benchmark on the provided sample

From `python3 benchmark_all.py`:

| Approach | Exact | Wrong | NULL | Accuracy | Accepted precision | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Approach 1, baseline | 44/45 | 0 | 1 | 97.78% | 100.00% | 97.78% |
| Approach 2, template registration | 44/45 | 0 | 1 | 97.78% | 100.00% | 97.78% |
| Approach 3, timing marks | 45/45 | 0 | 0 | 100.00% | 100.00% | 100.00% |

Best observed result on the provided page: **Approach 3**.

## Repository layout

Inputs:
- `sample.pdf`
- `ground_truth.json`
- `ground_truth.template.json`

Implementation:
- `omr_core.py` - shared geometry, scoring, evaluation, and artifact helpers
- `omr_approaches.py` - all implemented approaches
- `omr_baseline.py` - compatibility entrypoint for approach 1 only
- `benchmark_all.py` - common comparative benchmark runner

Documentation:
- `TASK.md`
- `APPROACHES.md`
- `benchmark_report.md`

Generated artifacts in `out/`:
- `page-1.png`
- per-approach overlays and result JSON files
- `benchmark_summary.json`

## How to run

Render the page if needed, then run either the baseline or the full comparison.

```bash
mkdir -p out
pdftoppm -png -r 200 sample.pdf out/page
python3 omr_baseline.py
python3 benchmark_all.py
```

## Notes

- The methods here are deliberately simple, deterministic, and auditable.
- No ML classifier is used.
- The benchmark results are only for the provided `sample.pdf`; they are not a claim of production robustness on unseen forms.

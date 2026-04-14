# TASK

## Objective

Turn this repo from a single working extractor into a small but real comparative OMR study for rows **1-45** of `sample.pdf`.

## Done

Completed work:
- kept the original manual baseline as **approach 1**
- implemented **approach 2**: fixed-template registration + intensity reading
- implemented **approach 3**: timing-mark anchored registration
- added a shared benchmark runner for all approaches
- saved per-approach overlays and JSON outputs under `out/`
- updated the docs to report a comparison instead of only the first success

## Benchmark status

Current observed benchmark on the provided page:

| Approach | Exact | Wrong | NULL | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Approach 1, baseline | 44/45 | 0 | 1 | 97.78% |
| Approach 2, template registration | 44/45 | 0 | 1 | 97.78% |
| Approach 3, timing marks | 45/45 | 0 | 0 | 100.00% |

## Current recommendation

Best observed deterministic method on the provided sample:
- **Approach 3, timing-mark anchored registration**

Reason:
- it preserves the same transparent intensity scoring
- it replaces manually stepped row Y positions with detected structural anchors
- it resolves the baseline's lone ambiguous row on the current sample

## Remaining optional work

Useful next steps if the study is expanded:
- perturbation tests across DPI, rotation, crop shift, blur, and contrast changes
- multiple-page evaluation if more sheets become available
- hybrid registration combining coarse page alignment with timing-mark correction

## Deliverables now present

- `omr_core.py`
- `omr_approaches.py`
- `benchmark_all.py`
- updated `omr_baseline.py`
- updated `README.md`
- updated `APPROACHES.md`
- updated `benchmark_report.md`
- generated benchmark artifacts in `out/`

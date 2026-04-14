# Benchmark report

## Purpose

This report summarizes the current comparative benchmark for the implemented OMR approaches on the first dataset in the study.

Dataset currently evaluated:
- `sample.pdf`
- rows 1-45
- ground truth from `ground_truth.json`

## Command run

```bash
python3 benchmark_all.py
```

## Results

| Approach | Exact matches | Wrong | NULL | Accuracy | Accepted precision | Accepted coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Approach 1, manual calibration baseline | 44 | 0 | 1 | 0.9778 | 1.0000 | 0.9778 |
| Approach 2, template registration + intensity reading | 44 | 0 | 1 | 0.9778 | 1.0000 | 0.9778 |
| Approach 3, timing-mark anchored registration | 45 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |

## Failure details

### Approach 1
- row 35 -> predicted `NULL`, truth `A`

### Approach 2
- row 35 -> predicted `NULL`, truth `A`

### Approach 3
- no failures on rows 1-45 for the provided sample

## Interpretation

- Approach 1 is a solid conservative baseline.
- Approach 2 shows that adding template registration does not improve this already well-aligned sample, but it remains a meaningful comparison point.
- Approach 3 is the strongest observed deterministic method because the timing marks provide a better row anchor than manually stepped row positions.

## Why this matters for the next phase

The next project phase is expected to add more PDFs.

That means the most important value of this repo is now:
- shared benchmark structure
- side-by-side approach comparison
- clear per-dataset reporting

The current results should be read as a benchmark on the **first dataset**, not as a universal claim about future sheets.

## Artifacts

Generated under `out/`:
- `approach_1_baseline_results.json`
- `approach_1_baseline_overlay.png`
- `approach_2_template_registration_results.json`
- `approach_2_template_registration_overlay.png`
- `approach_3_timing_marks_results.json`
- `approach_3_timing_marks_overlay.png`
- `benchmark_summary.json`

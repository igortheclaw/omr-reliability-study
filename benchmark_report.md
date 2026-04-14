# Benchmark report

## Command run

```bash
python3 benchmark_all.py
```

## Results

| Approach | Exact matches | Wrong | NULL | Accuracy | Accepted precision | Accepted coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Approach 1, manual calibration baseline | 44 | 0 | 1 | 0.9778 | 1.0000 | 0.9778 |
| Approach 2, fixed-template registration + intensity reading | 44 | 0 | 1 | 0.9778 | 1.0000 | 0.9778 |
| Approach 3, timing-mark anchored registration | 45 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |

## Failure details

### Approach 1
- row 35 -> predicted `NULL`, truth `A`

### Approach 2
- row 35 -> predicted `NULL`, truth `A`

### Approach 3
- no failures on rows 1-45 for the provided sample

## Interpretation

- The original baseline remains strong and conservative.
- The template-registration variant is honest but neutral on this already aligned page.
- The timing-mark method is the strongest observed deterministic approach in this repo because it fixes the row alignment drift that left row 35 ambiguous in the baseline family.

## Artifacts

Generated under `out/`:
- `approach_1_baseline_results.json`
- `approach_1_baseline_overlay.png`
- `approach_2_template_registration_results.json`
- `approach_2_template_registration_overlay.png`
- `approach_3_timing_marks_results.json`
- `approach_3_timing_marks_overlay.png`
- `benchmark_summary.json`

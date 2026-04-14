# Benchmark report

## Purpose

This report summarizes the currently verified benchmark status after the multi-dataset refactor.

## Command run

```bash
python3 benchmark_all.py --dataset sample
```

## Benchmarkable datasets on 2026-04-14

- `sample` is benchmarkable because its ground truth contains labeled answers.
- `2021_2P_PER_modelo_B_definitiva4`, `2022_3P_PER_modelo_A`, `2023_1P_PER_modelo_B`, `2024_2-SOL_PER_modelo_A`, and `2026_1-SOL_PER_modelo_A` are prepared but not benchmarkable yet because their `ground_truth.json` files are still all `null`.

## Results for `sample`

| Approach | Exact matches | Wrong | NULL | Accuracy | Accepted precision | Accepted coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Approach 1, manual calibration baseline | 44 | 0 | 1 | 0.9778 | 1.0000 | 0.9778 |
| Approach 2, template registration + intensity reading | 44 | 0 | 1 | 0.9778 | 1.0000 | 0.9778 |
| Approach 3, timing-mark anchored registration | 45 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |

## Failure details for `sample`

### Approach 1
- row 35 -> predicted `NULL`, truth `A`

### Approach 2
- row 35 -> predicted `NULL`, truth `A`

### Approach 3
- no failures on the 45 labeled rows

## Artifact locations

Per-dataset artifacts for `sample` are generated under `out/sample/`.
The aggregate run summary is generated at `out/benchmark_summary.json`.

## Interpretation

The implementation is now ready to benchmark multiple datasets honestly.
Additional datasets will start contributing results only after trusted answers are filled into their own `ground_truth.json` files.

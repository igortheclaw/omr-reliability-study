# Benchmark report

## Purpose

This report summarizes the verified benchmark status after the multi-dataset refactor and the later geometry work that produced a general cross-template solution.

## Command run

```bash
python3 benchmark_all.py --all
```

## Benchmarkable datasets

The following datasets are currently benchmarkable because their `ground_truth.json` files contain labeled answers:

- `sample`
- `2021_2P_PER_modelo_B_definitiva4`
- `2022_3P_PER_modelo_A`
- `2023_1P_PER_modelo_B`
- `2024_2-SOL_PER_modelo_A`
- `2026_1-SOL_PER_modelo_A`

## Final verified results

| Dataset | Best approach | Exact matches | Wrong | NULL | Accuracy |
| --- | --- | ---: | ---: | ---: | ---: |
| sample | Approach 3 or 4 | 45 | 0 | 0 | 1.0000 |
| 2021_2P_PER_modelo_B_definitiva4 | Approach 4 | 38 | 0 | 0 | 1.0000 |
| 2022_3P_PER_modelo_A | Approach 4 | 45 | 0 | 0 | 1.0000 |
| 2023_1P_PER_modelo_B | Approach 4 | 45 | 0 | 0 | 1.0000 |
| 2024_2-SOL_PER_modelo_A | Approach 3 or 4 | 45 | 0 | 0 | 1.0000 |
| 2026_1-SOL_PER_modelo_A | Approach 3 or 4 | 45 | 0 | 0 | 1.0000 |

## Geometry lessons captured by the benchmark

### What failed

- Fixed manual calibration did not generalize across template families.
- ECC-style affine registration by itself did not recover enough structure to solve the older variants.
- Strict timing-mark registration from the top of the right edge failed whenever the visible chain was partial, shifted, or fragmented.
- Circle-grid-first alignment was promising but less robust than the printed edge marks.

### What worked

Approach 4 solved the template-family split by using the printed right-edge marks more realistically:

- detect the longest usable chain on the right edge,
- estimate row spacing from the observed chain,
- anchor from the last visible mark,
- extrapolate row positions upward,
- apply a global horizontal shift,
- read the bubbles with a slightly more tolerant sampler.

This preserved perfect performance on the already-good template family and unlocked perfect results on the previously failing family.

## Notes on benchmark execution

- `benchmark_all.py` now reports per-approach failures without aborting the full run.
- Per-dataset artifacts are generated under `out/<dataset_id>/`.
- The aggregate run summary is generated at `out/benchmark_summary.json`.

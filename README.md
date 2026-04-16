# OMR Reliability Study

Comparative study of deterministic OMR-reading approaches across multiple prepared datasets.

## Objective

The repository is organized around one stable question: how the same deterministic OMR approaches behave across different answer-sheet PDFs.

The code now uses dataset directories under `datasets/<dataset_id>/` as the primary input contract.

## Dataset-oriented workflow

Each dataset lives under `datasets/<dataset_id>/` and should contain:
- `dataset.json` with the dataset id and PDF location
- the source PDF for that dataset
- `ground_truth.json` with trusted answers for benchmarked rows
- `README.md` with dataset-specific notes

The benchmark reads:
- the PDF path from `datasets/<dataset_id>/dataset.json`
- the answers from `datasets/<dataset_id>/ground_truth.json`

Generated artifacts are written under:
- `out/<dataset_id>/page-1.png`
- `out/<dataset_id>/approach_*_results.json`
- `out/<dataset_id>/approach_*_overlay.png`
- `out/<dataset_id>/benchmark_summary.json`

The aggregate multi-dataset summary is written to `out/benchmark_summary.json`.

## Implemented approaches

1. Approach 1, manual calibration baseline
2. Approach 2, template registration + intensity reading
3. Approach 3, timing-mark anchored registration
4. Approach 4, right-edge extrapolated hybrid

These remain deterministic and auditable. The comparative structure is unchanged; only the dataset handling was generalized.

## What was learned

The core difficulty was not answer scoring, but geometry.

Across the prepared datasets, the repository now reflects these findings:

- Fixed manual geometry is not reliable across template families.
- Affine template registration alone was not enough because the effective printed anchor structure differs between exam variants.
- The right-edge timing marks are the strongest printed geometric signal shared across templates, but some variants expose a complete chain while others expose only a partial chain.
- Bottom-edge marks are very useful for horizontal sanity checks, but the final robust solution did not need to depend on them.
- The bubble grid itself is detectable, but using it directly as the main geometric anchor was less robust than using printed edge marks.

The successful general strategy is:

- detect the longest usable chain of right-edge timing marks,
- estimate the vertical row spacing from the observed marks,
- anchor from the last visible mark instead of assuming visibility from the top,
- extrapolate the row positions upward,
- apply a global horizontal shift derived from the observed right-edge mark positions,
- then read bubbles with a slightly more forgiving sampler.

This is implemented in Approach 4.

## How to run

Benchmark every discovered dataset with at least one labeled answer:

```bash
python3 benchmark_all.py
```

Benchmark one dataset explicitly:

```bash
python3 benchmark_all.py --dataset sample
```

Explicitly enumerate all prepared datasets and skip unfinished ones with a reason:

```bash
python3 benchmark_all.py --all
```

Legacy wrapper for approach 1 only:

```bash
python3 run_legacy_baseline.py --dataset sample
```

## Current benchmark status

The benchmark now reads ground truth directly from each dataset folder. Current verified results across all benchmarkable datasets are:

| Dataset | Best approach | Exact | Wrong | NULL | Accuracy |
| --- | --- | ---: | ---: | ---: | ---: |
| sample | Approach 3 or 4 | 45/45 | 0 | 0 | 100.00% |
| 2021_2P_PER_modelo_B_definitiva4 | Approach 4 | 38/38 | 0 | 0 | 100.00% |
| 2022_3P_PER_modelo_A | Approach 4 | 45/45 | 0 | 0 | 100.00% |
| 2023_1P_PER_modelo_B | Approach 4 | 45/45 | 0 | 0 | 100.00% |
| 2024_2-SOL_PER_modelo_A | Approach 3 or 4 | 45/45 | 0 | 0 | 100.00% |
| 2026_1-SOL_PER_modelo_A | Approach 3 or 4 | 45/45 | 0 | 0 | 100.00% |

Any dataset with non-null answers in `ground_truth.json` is benchmarked automatically.

## Repository structure

```text
.
├── benchmark_all.py
├── run_legacy_baseline.py
├── omr_core.py
├── omr_approaches.py
├── datasets/
│   └── <dataset_id>/
├── out/
└── README.md
```

## Notes

- `datasets/sample/` is the canonical replacement for the original top-level `sample.pdf` + `ground_truth.json` benchmark case.
- Top-level legacy files are kept only as compatibility history; the main path is dataset-oriented.
- Datasets with empty or partially unfilled ground truth are not used to make benchmark claims beyond their labeled rows.
- `benchmark_all.py` now tolerates per-approach failures and keeps reporting the rest of the benchmark instead of aborting the full run.
- Approach 3 remains valuable for templates with a complete visible right-edge chain.
- Approach 4 is the current general-purpose winner for mixed template families because it can recover geometry from incomplete but still usable right-edge chains.

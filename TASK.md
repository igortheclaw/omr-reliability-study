# TASK

## Objective

Keep this repository focused on a clear purpose:

**compare OMR-reading approaches across one or more PDF sheets using a common benchmark structure.**

The current repo should be treated as the first dataset in that broader study, not as a one-off script for a single page.

## Current status

Implemented approaches:
- Approach 1, manual calibration baseline
- Approach 2, template registration + intensity reading
- Approach 3, timing-mark anchored registration

Shared benchmark runner:
- `benchmark_all.py`

Shared core logic:
- `omr_core.py`
- `omr_approaches.py`

Current benchmarked dataset:
- `sample.pdf`
- rows 1-45
- ground truth in `ground_truth.json`

Additional PDFs already added to the repo for the next phase:
- `datasets/2021_2P_PER_modelo_B_definitiva4.pdf`
- `datasets/2022_3P_PER_modelo_A.pdf`
- `datasets/2023_1P_PER_modelo_B.pdf`
- `datasets/2024_2-SOL_PER_modelo_A.pdf`
- `datasets/2026_1-SOL_PER_modelo_A.pdf`

## Current benchmark

| Approach | Exact | Wrong | NULL | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Approach 1 | 44/45 | 0 | 1 | 97.78% |
| Approach 2 | 44/45 | 0 | 1 | 97.78% |
| Approach 3 | 45/45 | 0 | 0 | 100.00% |

## Immediate cleanup goal

Make the repo structure and naming clearly communicate that:
- the benchmark compares approaches
- the same framework should later support more PDFs
- old one-off baseline entrypoints are secondary, not the main story

## Next phase expectations

When new PDFs are added, the repo should support:
- adding a new dataset without rewriting the approach logic
- running the same approaches against each dataset
- storing per-dataset outputs and benchmark summaries
- comparing approach behavior across datasets, not only within one page

## Good next technical steps

1. Introduce a dataset-oriented layout, for example per-PDF inputs and outputs.
2. Generalize the benchmark runner so it can target a selected dataset or all datasets.
3. Move any legacy naming that over-emphasizes the original baseline into clearer compatibility wrappers or remove it.
4. Keep reports honest: only claim results that were actually run.

## Standard of success

The repo is in good shape when a new PDF can be added as a new benchmark case with minimal glue code, and the main user experience remains:
- define dataset
- run benchmark
- compare approaches

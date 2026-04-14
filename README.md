# OMR Reliability Study

Comparative study of deterministic OMR-reading approaches across multiple prepared datasets.

## Objective

The repository is organized around one stable question: how the same deterministic OMR approaches behave across different answer-sheet PDFs.

The code now uses dataset directories under `datasets/<dataset_id>/` as the primary input contract.

## Dataset-oriented workflow

Each dataset lives under `datasets/<dataset_id>/` and should contain:
- `dataset.json` with the dataset id and PDF location
- `ground_truth.json` with trusted answers for benchmarked rows
- `ground_truth.template.json` as a blank template
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

These remain deterministic and auditable. The comparative structure is unchanged; only the dataset handling was generalized.

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

As of 2026-04-14, only `datasets/sample/ground_truth.json` contains non-null answers, so only `sample` is benchmarkable today.

Current observed results on `sample`:

| Approach | Exact | Wrong | NULL | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Approach 1 | 44/45 | 0 | 1 | 97.78% |
| Approach 2 | 44/45 | 0 | 1 | 97.78% |
| Approach 3 | 45/45 | 0 | 0 | 100.00% |

Other prepared datasets are supported by the code and will be benchmarked automatically once their `ground_truth.json` files contain trusted non-null answers.

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

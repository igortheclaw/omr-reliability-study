# Datasets

Each benchmark case lives in its own directory under `datasets/<dataset_id>/`.

## Required files

Each dataset directory should contain:
- `dataset.json`
- `ground_truth.json`
- `ground_truth.template.json`
- `README.md`

## `dataset.json`

Minimum expected fields:
- `dataset_id`: stable identifier used for CLI selection and output paths
- `pdf_path`: repo-relative path to the source PDF
- `rows_used`: currently `45`
- `allowed_values`: `A`, `B`, `C`, `D`, or `null`
- `status`: human-readable progress note

## Ground truth policy

Fill `ground_truth.json` manually with trusted answers.

Expected values per row:
- `"A"`
- `"B"`
- `"C"`
- `"D"`
- `null`

Benchmark behavior:
- a dataset is benchmarkable only when at least one row has a non-null answer
- if a dataset is only partially filled, only the labeled rows are scored
- datasets with all-null answers are skipped and never used for benchmark claims

## Adding a new dataset

1. Create `datasets/<dataset_id>/`.
2. Add `dataset.json` pointing at the PDF path in the repo.
3. Copy or create `ground_truth.template.json` for rows `1` to `45`.
4. Copy it to `ground_truth.json` and fill trusted answers as they become available.
5. Add a short `README.md` with any sheet-specific notes.
6. Run `python3 benchmark_all.py --dataset <dataset_id>` after ground truth is available.

## Prepared datasets in this repo

- `sample/`
- `2021_2P_PER_modelo_B_definitiva4/`
- `2022_3P_PER_modelo_A/`
- `2023_1P_PER_modelo_B/`
- `2024_2-SOL_PER_modelo_A/`
- `2026_1-SOL_PER_modelo_A/`

`sample/ground_truth.json` is currently the only filled benchmark source as of 2026-04-14.

# Datasets

Each dataset should live in its own subdirectory under `datasets/`.

## Prepared datasets

- `sample/`
- `2021_2P_PER_modelo_B_definitiva4/`
- `2022_3P_PER_modelo_A/`
- `2023_1P_PER_modelo_B/`
- `2024_2-SOL_PER_modelo_A/`
- `2026_1-SOL_PER_modelo_A/`

## Per-dataset structure

Each dataset directory is prepared with:
- `dataset.json` — metadata and status
- `ground_truth.template.json` — empty template for rows 1-45
- `ground_truth.json` — working ground-truth file to fill in
- `README.md` — quick reminder of what belongs there

## What to fill in manually

For each sheet, edit:
- `datasets/<dataset_id>/ground_truth.json`

Expected values:
- `A`
- `B`
- `C`
- `D`
- `null`

## Notes

- `sample/ground_truth.json` is already populated from the original benchmark case.
- The newly added datasets are scaffolded and ready for manual completion.
- The current benchmark code is not yet fully switched over to this per-dataset structure, but the repo is now prepared for that next step.

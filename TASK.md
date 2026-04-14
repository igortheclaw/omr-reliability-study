# TASK

## Objective

Keep the repository focused on one job:

**compare deterministic OMR-reading approaches across one or more PDF datasets using a shared benchmark structure.**

## Current status

Implemented approaches:
- Approach 1, manual calibration baseline
- Approach 2, template registration + intensity reading
- Approach 3, timing-mark anchored registration

Main benchmark runner:
- `benchmark_all.py`

Core shared logic:
- `omr_core.py`
- `omr_approaches.py`

Primary input contract:
- `datasets/<dataset_id>/dataset.json`
- `datasets/<dataset_id>/ground_truth.json`

Primary output contract:
- `out/<dataset_id>/...`
- `out/benchmark_summary.json`

## What is working now

- one dataset can be selected with `--dataset <dataset_id>`
- all prepared datasets can be enumerated in one run
- datasets without labeled ground truth are skipped without creating benchmark claims
- partially labeled datasets are scored only on labeled rows
- the original `sample` benchmark still works through `datasets/sample/`

## Current benchmark status on 2026-04-14

Benchmarkable dataset:
- `sample`

Prepared but not benchmarkable yet:
- `2021_2P_PER_modelo_B_definitiva4`
- `2022_3P_PER_modelo_A`
- `2023_1P_PER_modelo_B`
- `2024_2-SOL_PER_modelo_A`
- `2026_1-SOL_PER_modelo_A`

## Standard of success

The repo is in good shape when adding a new PDF means:
1. create `datasets/<dataset_id>/`
2. point `dataset.json` at the PDF
3. fill `ground_truth.json`
4. run the shared benchmark
5. compare approaches using per-dataset outputs

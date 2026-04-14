# OMR Reliability Study

Comparative study of deterministic OMR-reading approaches for a growing set of PDF answer sheets.

## Project objective

The main goal of this repository is to **compare candidate approaches**, not just to keep a single working extractor.

The repo already contains multiple PDFs and is being prepared to benchmark them with the same approach framework.

## Scope today

Currently benchmarked dataset:
- `sample.pdf`
- rows **1-45** only
- valid outputs: `A`, `B`, `C`, `D`, or `NULL`

Additional PDFs already added for the next phase live under `datasets/`.

`NULL` is preferred over a wrong answer.

## What the repo contains

### Implemented approaches

1. **Approach 1, manual calibration baseline**
   - fixed answer-cell coordinates
   - deterministic darkness scoring
   - `NULL` on low confidence margin

2. **Approach 2, template registration + intensity reading**
   - affine registration to a canonical layout
   - same deterministic readout after alignment

3. **Approach 3, timing-mark anchored registration**
   - detect right-edge timing marks
   - use them to anchor row positions
   - deterministic readout on the fixed answer columns

### Shared benchmarking pieces

- `omr_core.py` — shared rendering, scoring, evaluation, and artifact helpers
- `omr_approaches.py` — all currently implemented approaches
- `benchmark_all.py` — main comparative benchmark entrypoint
- `run_legacy_baseline.py` — compatibility entrypoint for approach 1 only
- `omr_baseline.py` — thin compatibility wrapper kept for legacy usage

### Dataset inputs

Current benchmark case:
- `sample.pdf`
- `ground_truth.json`
- `ground_truth.template.json`

Additional PDFs for future benchmark cases:
- `datasets/2021_2P_PER_modelo_B_definitiva4.pdf`
- `datasets/2022_3P_PER_modelo_A.pdf`
- `datasets/2023_1P_PER_modelo_B.pdf`
- `datasets/2024_2-SOL_PER_modelo_A.pdf`
- `datasets/2026_1-SOL_PER_modelo_A.pdf`

### Reports

- `APPROACHES.md` — candidate-family overview and strategy
- `TASK.md` — current project state and next expansion steps
- `benchmark_report.md` — current benchmark results and interpretation

## Current benchmark on the first dataset

Run with:

```bash
python3 benchmark_all.py
```

Observed results on `sample.pdf`:

| Approach | Exact | Wrong | NULL | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Approach 1 | 44/45 | 0 | 1 | 97.78% |
| Approach 2 | 44/45 | 0 | 1 | 97.78% |
| Approach 3 | 45/45 | 0 | 0 | 100.00% |

Best observed approach on the current dataset: **Approach 3**.

## Repository structure

```text
.
├── sample.pdf
├── ground_truth.json
├── ground_truth.template.json
├── omr_core.py
├── omr_approaches.py
├── benchmark_all.py
├── run_legacy_baseline.py
├── omr_baseline.py
├── datasets/
├── README.md
├── APPROACHES.md
├── TASK.md
├── benchmark_report.md
└── out/
```

Generated artifacts under `out/` include:
- one rendered page image
- one overlay per approach
- one result JSON per approach
- `benchmark_summary.json`

## How to run

Render if needed, then run the benchmark:

```bash
mkdir -p out
pdftoppm -png -r 200 sample.pdf out/page
python3 benchmark_all.py
```

Legacy single-approach run, if needed:

```bash
python3 run_legacy_baseline.py
```

## Direction for the next phase

This repo should grow by **wiring the added PDFs into the shared benchmark and evaluating the same approach families on all of them**.

That means future cleanup and development should bias toward:
- dataset-oriented organization
- reusable benchmark entrypoints
- per-dataset results
- honest cross-approach comparison

## Non-goal

This repo is not trying to become a generic OCR platform or a production grading system yet. Right now it is a focused comparative study of deterministic OMR strategies.

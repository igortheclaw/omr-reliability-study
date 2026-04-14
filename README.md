# OMR Reliability Study

Small isolated project to evaluate ways to recognize filled answer boxes from a single OMR-style PDF page with **>90% reliability**.

## Files

- `sample.pdf` — target document
- `APPROACHES.md` — possible solution paths
- `TASK.md` — proposed experiment plan
- `ground_truth.template.json` — template for trusted manual answers

## Problem

We only care about one page family.

- The sheet has 100 numbered rows
- only rows **1-45** matter
- we need reliable detection of the filled option for each row
- acceptable outputs are `A`, `B`, `C`, `D`, or `NULL`
- `NULL` is preferred over a wrong answer

## Goal

Find an approach that is:
- reproducible
- auditable
- robust
- above 90% reliability on rows 1-45

## Suggested workflow

1. Build trusted ground truth for rows 1-45
2. Implement one baseline reader
3. Benchmark against ground truth
4. Add perturbation tests
5. Compare methods and pick the safest one

## Possible initial helper tasks

These are intentionally only noted, not implemented:
- render `sample.pdf` into one or more PNG images
- generate a visual overlay for rows 1-45
- prepare a simple manual review flow for creating `ground_truth.json`

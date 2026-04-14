# OMR reliability study for a single answer sheet

## Objective

Recognize the filled answer boxes in `sample.pdf` for rows 1-45 with reliability above 90%.

## What we learned so far

The simplest useful approach already works well:
- manual calibration
- fixed render geometry
- deterministic darkness measurement per answer cell
- `NULL` on low-margin cases

Current observed result on the provided sample:
- 44/45 exact matches
- 0 wrong answers
- 1 `NULL`
- 97.78% exact accuracy

So the main question is no longer "can this work?" but "how much geometry hardening is needed to make it robust?"

## Candidate method families

### 1. Manual calibration + deterministic extractor

Use fixed coordinates for the two visible answer groups and measure darkness at the expected bubble centers.

Pros:
- simplest implementation
- highly auditable
- already clears the success threshold on the provided sample

Cons:
- tied to one render geometry unless registration is added

Status:
- **implemented**
- currently the leading approach

### 2. Fixed-template registration + intensity reading

Register the page to a canonical template, then read cells using known coordinates.

Pros:
- natural next step from the current baseline
- keeps the same auditable measurement logic
- likely improves tolerance to small drift

Cons:
- more implementation complexity than pure fixed calibration

Status:
- not yet implemented
- strongest next hardening step

### 3. Timing-mark-based registration

Use the right-side OMR timing marks to infer row alignment and refine cell positions.

Pros:
- uses form structure intended for machine reading
- potentially robust to small geometric variation

Cons:
- requires reliable timing-mark detection
- more work than the current baseline

Status:
- not yet implemented
- good second hardening path if template registration is not enough

### 4. Hybrid registration

Use coarse template registration plus local timing-mark correction.

Pros:
- likely the strongest classical CV option
- good safety upgrade if perturbation tests expose drift sensitivity

Cons:
- more engineering overhead

Status:
- not yet implemented
- probably unnecessary unless robustness tests fail

### 5. Other exploratory methods

These remain lower priority:
- contour/component-based OMR
- blob/circle detection
- learned cell classifier
- vision model reading
- multi-method consensus

They may be useful later, but the current evidence suggests the fixed-coordinate family is the right starting point.

## Recommendation

Recommended order from here:

1. keep the current deterministic extractor as the baseline
2. run perturbation tests
3. add lightweight registration only if perturbations expose instability
4. consider hybrid methods only if registration alone is not enough

I would not lead with ML or vision-model methods here. This problem is narrow, structured, and already yielding to a simpler, more auditable approach.

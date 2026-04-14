# OMR reliability study for a single answer sheet

## Objective

Recognize the **filled answer boxes with >90% reliability** from this single PDF:

- `sample.pdf`
- Source URL: <https://www.juntadeandalucia.es/sites/default/files/inline-files/2025/11/2025_3-SOL_PER_modelo_A.pdf>

## Scope

This project is intentionally narrow.

- Only **one page / one PDF** is in scope.
- Only the **first 45 question numbers** matter.
- The sheet contains **100 numbered rows**, but rows 46-100 must be ignored.
- The right-side **OMR timing/alignment marks** are part of the problem and may help registration.
- This project does **not** depend on or reference any previous exam/question database project.
- We only care about **reading filled boxes reliably**.

## Success criteria

A solution is acceptable only if it can be shown to reach at least one of these:

- **>90% exact accuracy** on the 45 answers, measured against a trusted ground truth
- or **very high precision** with blanks/`unknown` for ambiguous rows, if the accepted rows still meet the reliability target

Preferred outcome:

- `A/B/C/D/NULL` per row 1-45
- with a per-row confidence score
- with reproducible debug artifacts

## Constraints and observations

- This is a printed OMR sheet, not a born-digital form field PDF.
- The page includes alignment/timing marks on the right margin.
- The layout likely supports more rows than the exam actually uses.
- The real task is not generic OCR, but **robust mark detection on a fixed layout**.
- A low-confidence answer is not acceptable as a final output.
- `NULL` is better than a wrong answer.

---

# Possible solution paths

## 1. Fixed-template image registration + cell intensity reading

### Idea
Choose one canonical rendering of the PDF, detect the page boundary, register every test rendering to a fixed template, and read only the 45 x 4 answer cells using known coordinates.

### How it works
- Render PDF to PNG at fixed DPI
- Detect page contour and deskew
- Register image to a template using affine or perspective transform
- Define exact bounding boxes for rows 1-45 and columns A-D
- Measure darkness/fill level in each box
- Select the darkest cell if separation is above threshold, else `NULL`

### Pros
- Most appropriate for a **single known form**
- Highly auditable
- Easy to debug visually
- Alignment marks can improve registration

### Cons
- Needs precise calibration once
- Sensitive to bad registration if not done carefully

### Expected reliability
Very promising. This is probably the strongest baseline.

---

## 2. Registration using the right-side OMR timing marks

### Idea
Use the right-side OMR marks as the primary geometric reference system, instead of relying on full-page contour or generic feature matching.

### How it works
- Detect the vertical sequence of timing marks on the right margin
- Use their spacing and positions to infer scale, skew, and row alignment
- Reconstruct the expected y-position of rows 1-45
- Read answer cells relative to that recovered grid

### Pros
- Uses structure already designed for machine reading
- More robust than generic circle detection
- Good against slight scale/rotation drift

### Cons
- Requires reliable detection of all or most timing marks
- If marks are faint or partially cropped, registration can fail

### Expected reliability
Excellent if the timing marks are clean and stable.

---

## 3. Hybrid approach: template registration + timing-mark correction

### Idea
Combine a coarse page/template alignment with a local correction driven by timing marks.

### How it works
- First align the sheet globally to a template
- Then refine row positions using the right-side marks
- Finally read answer boxes from corrected local coordinates

### Pros
- Likely more robust than either method alone
- Good if scan/render introduces local distortions

### Cons
- More implementation complexity
- Harder to tune initially

### Expected reliability
Potentially the best engineering option.

---

## 4. Classical OMR by connected components / contours

### Idea
Binarize the page, detect the answer boxes or filled regions directly as connected components, then infer which option is marked in each row.

### How it works
- Threshold image
- Find contours/components for boxes and marks
- Cluster into rows and columns
- Determine selected option by fill ratio

### Pros
- No ML required
- Fully local and explainable

### Cons
- Often brittle when print artifacts or line noise exist
- Can mistake borders/labels for marks
- Harder when layout contains many non-answer elements

### Expected reliability
Useful as a baseline, but probably not best alone.

---

## 5. Hough/circle or blob detection for bubble-like marks

### Idea
Detect circular or blob-like marked areas corresponding to candidate answers.

### How it works
- Use HoughCircles, LoG/DoG blob detection, or similar
- Cluster detections into 45 rows and 4 columns
- Infer chosen answer from strongest blob

### Pros
- Works if the marks are circular and high contrast
- Fast to prototype

### Cons
- Often unstable on printed forms
- Easy to over-detect irrelevant geometry
- Poor fit if answer areas are not clean circles

### Expected reliability
Probably not enough as the main method.

---

## 6. Learned image classifier on cropped cells

### Idea
After registration, crop each answer cell and classify it as filled vs empty with a lightweight ML model.

### How it works
- Register sheet to fixed coordinates
- Extract all candidate cells
- Train a small classifier using synthetic augmentations and manually labeled examples
- For each row, select the filled cell or `NULL`

### Pros
- Can outperform hard thresholds on subtle fill patterns
- More tolerant of faint marks and print variation

### Cons
- Needs labeled data or synthetic generation
- Overkill for a single document if classical methods already work
- Still depends on good registration

### Expected reliability
Strong as a refinement layer, not as step one.

---

## 7. Vision-model reading of the full page

### Idea
Use a multimodal model to read the page and return answers 1-45.

### How it works
- Pass rendered page image to a vision model
- Ask it to extract marked option per row
- Optionally use multiple passes and voting

### Pros
- Minimal custom computer vision code
- Fast to test

### Cons
- Hard to guarantee determinism
- Hard to prove >90% reliability without manual verification
- Auditing is weaker than explicit geometry-based methods

### Expected reliability
Good for exploratory support, weak as the final authoritative path.

---

## 8. Multi-method consensus system

### Idea
Run several readers and only accept answers when they agree.

### How it works
- Run two or three methods, for example:
  - fixed-template intensity
  - timing-mark-based registration
  - cropped-cell classifier
- Accept answer only if methods agree or confidence margin is high
- Otherwise output `NULL`

### Pros
- Raises trustworthiness
- Reduces silent failures
- Good for final production mode

### Cons
- More engineering work
- Lower coverage if methods disagree often

### Expected reliability
Very strong if paired with `NULL` for conflicts.

---

## 9. Manual calibration + deterministic extractor

### Idea
Do a one-time manual calibration of exact coordinates for rows 1-45 and columns A-D on this one PDF, then build a deterministic reader around that.

### How it works
- Render the page at fixed DPI
- Manually record the coordinates of all relevant boxes
- Implement direct fill measurement with no automatic layout discovery
- Optionally add a small alignment correction before reading

### Pros
- Extremely simple conceptually
- Perfectly suited to the “single known page family” problem
- Highly auditable

### Cons
- Less generalizable
- Requires careful setup

### Expected reliability
Very high, if the render pipeline is fixed and stable.

---

## 10. PDF-native analysis before raster OMR

### Idea
Inspect the PDF structure first to see whether useful vector/text elements can help locate the answer grid before raster analysis.

### How it works
- Check whether boxes, labels, or guide marks are vector elements
- Use PDF coordinates to bootstrap registration
- Then read marks from rasterized image at those coordinates

### Pros
- Could make alignment easier
- Avoids unnecessary detection work if structure is encoded cleanly

### Cons
- Many scanned/flattened PDFs will not expose useful form structure
- May not help with actual fill detection

### Expected reliability
Worth testing early, but unlikely to solve the whole problem alone.

---

# Recommended evaluation plan

## Phase 1: establish ground truth

A trusted answer key for rows 1-45 is already available in `ground_truth.json`.

Recommended complementary outputs:
- annotated debug image with row numbers and chosen option

This means the project can directly benchmark candidate methods instead of first creating the ground truth.

## Phase 2: implement the best 3 candidate families

Recommended first candidates:
1. **Fixed-template registration + cell intensity**
2. **Timing-mark-based registration**
3. **Hybrid registration + timing-mark correction**

## Phase 3: measure

For each method, report:
- exact matches out of 45
- precision on accepted answers
- recall if `NULL` is allowed
- per-row confidence distribution
- failure modes by row

## Phase 4: harden

Keep only methods that are:
- auditable
- deterministic or near-deterministic
- robust under small perturbations

Suggested perturbation tests:
- render at different DPI values
- slight rotation
- light blur
- brightness/contrast variation
- tiny crop shifts

If a method breaks under these, it is not production-ready.

---

# Recommendation

If the target is **real >90% reliability**, the best order to try is:

1. **Manual calibration + deterministic extractor**
2. **Fixed-template registration + intensity reading**
3. **Timing-mark refinement**
4. **Consensus between 2 and 3**

I would avoid using a vision LLM or raw blob/circle detection as the primary solution. They may help exploration, but they are weaker as the final authoritative reader.

---

# Deliverables this project should eventually produce

- `sample.pdf`
- `ground_truth.json`
- one or more extraction scripts
- one benchmark script
- one report comparing methods
- debug overlays showing detected rows/cells/marks
- final decision on the most reliable approach

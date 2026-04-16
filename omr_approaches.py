from __future__ import annotations

import cv2
import numpy as np

from omr_core import (
    ApproachResult,
    DatasetConfig,
    GROUPS,
    NULL_MARGIN,
    RADIUS,
    evaluate_answers,
    get_dataset,
    load_page,
    render_overlay,
    run_circle_sampler,
    save_result,
)


CANONICAL_LEFT = np.array([[315, 1387], [430, 1387], [315, 2203]], dtype=np.float32)
CANONICAL_RIGHT = np.array([[650, 1374], [762, 1374], [650, 2020]], dtype=np.float32)
CANONICAL_ALL = np.vstack([CANONICAL_LEFT, CANONICAL_RIGHT])
TIMING_MARK_X_MIN = 1575
TIMING_MARK_AREA_MIN = 500
FIRST_VISIBLE_MARK_INDEX = 16
TIMING_MARK_Y_GAP_MAX = 45
TIMING_MARK_TOTAL_MIN = FIRST_VISIBLE_MARK_INDEX + 25
RIGHT_EDGE_HYBRID_X_MIN = 1590
RIGHT_EDGE_HYBRID_AREA_MIN = 500
RIGHT_EDGE_HYBRID_W_MIN = 30
RIGHT_EDGE_HYBRID_H_MIN = 15
RIGHT_EDGE_CANONICAL_X = 1633.0
HYBRID_RADIUS = 13
HYBRID_NULL_MARGIN = 7.0


def _resolve_dataset(dataset: DatasetConfig | None) -> DatasetConfig:
    return dataset or get_dataset()


def approach_1_baseline(dataset: DatasetConfig | None = None):
    dataset = _resolve_dataset(dataset)
    gray, rgb = load_page(dataset)

    def geometry(group, row):
        y = group['y0'] + group['dy'] * (row - group['rows'].start)
        return y, group['xs']

    answers, debug = run_circle_sampler(gray, geometry, null_margin=NULL_MARGIN, radius=RADIUS)
    metrics = evaluate_answers(dataset, answers, debug, extra_metrics={'null_margin': NULL_MARGIN, 'radius': RADIUS})
    result = ApproachResult(
        approach_id='approach_1_baseline',
        name='Approach 1, manual calibration baseline',
        summary='Fixed coordinates from manual calibration, direct darkness readout, NULL on low margin.',
        dataset_id=dataset.dataset_id,
        answers=answers,
        debug=debug,
        metrics=metrics,
    )
    render_overlay(rgb, debug, dataset.out_dir / 'approach_1_baseline_overlay.png')
    save_result(dataset, result)
    return result


def _estimate_template_affine(gray):
    template = gray.copy()
    roi = (220, 1240, 860, 1020)
    x, y, w, h = roi
    moving = gray[y:y + h, x:x + w].astype(np.float32) / 255.0
    fixed = template[y:y + h, x:x + w].astype(np.float32) / 255.0
    warp = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    try:
        _, warp = cv2.findTransformECC(fixed, moving, warp, cv2.MOTION_AFFINE, criteria, None, 5)
    except cv2.error:
        pass
    return warp


def approach_2_template_registration(dataset: DatasetConfig | None = None):
    dataset = _resolve_dataset(dataset)
    gray, rgb = load_page(dataset)
    warp = _estimate_template_affine(gray)

    def geometry(group, row):
        base_y = group['y0'] + group['dy'] * (row - group['rows'].start)
        positions = {label: float(x) for label, x in group['xs'].items()}
        pts = np.array([[[positions['A'], base_y]], [[positions['D'], base_y]]], dtype=np.float32)
        transformed = cv2.transform(pts, warp)
        y = float(transformed[:, 0, 1].mean())
        ax = float(transformed[0, 0, 0])
        dx = float(transformed[1, 0, 0])
        scale = (dx - ax) / (positions['D'] - positions['A']) if positions['D'] != positions['A'] else 1.0
        shifted = {label: ax + (x - positions['A']) * scale for label, x in positions.items()}
        return y, shifted

    answers, debug = run_circle_sampler(gray, geometry, null_margin=NULL_MARGIN, radius=RADIUS)
    metrics = evaluate_answers(
        dataset,
        answers,
        debug,
        extra_metrics={
            'null_margin': NULL_MARGIN,
            'radius': RADIUS,
            'warp_matrix': warp.tolist(),
        },
    )
    result = ApproachResult(
        approach_id='approach_2_template_registration',
        name='Approach 2, fixed-template registration + intensity reading',
        summary='Affine ECC registration to a canonical template, then read the canonical bubble grid.',
        dataset_id=dataset.dataset_id,
        answers=answers,
        debug=debug,
        metrics=metrics,
    )
    render_overlay(rgb, debug, dataset.out_dir / 'approach_2_template_registration_overlay.png')
    save_result(dataset, result)
    return result


def _detect_timing_marks(gray):
    _, th = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    num, _, stats, _ = cv2.connectedComponentsWithStats(th, 8)
    marks = []
    for i in range(1, num):
        x, y, w, h, area = stats[i]
        if x >= TIMING_MARK_X_MIN and area >= TIMING_MARK_AREA_MIN and w >= 35 and h >= 15:
            marks.append({'x': float(x + w / 2), 'y': float(y + h / 2), 'w': int(w), 'h': int(h), 'area': int(area)})
    marks.sort(key=lambda m: m['y'])
    if not marks:
        return marks

    chains = []
    chain = [marks[0]]
    for mark in marks[1:]:
        gap = mark['y'] - chain[-1]['y']
        if gap <= TIMING_MARK_Y_GAP_MAX:
            chain.append(mark)
        else:
            chains.append(chain)
            chain = [mark]
    chains.append(chain)

    best_chain = max(chains, key=len)
    if len(best_chain) >= TIMING_MARK_TOTAL_MIN:
        return best_chain
    return marks


def approach_3_timing_marks(dataset: DatasetConfig | None = None):
    dataset = _resolve_dataset(dataset)
    gray, rgb = load_page(dataset)
    marks = _detect_timing_marks(gray)
    if len(marks) < FIRST_VISIBLE_MARK_INDEX + 25:
        raise SystemExit(f'Expected enough timing marks, found {len(marks)}')

    def geometry(group, row):
        mark_idx = FIRST_VISIBLE_MARK_INDEX + (row - group['rows'].start)
        mark_y = marks[mark_idx]['y']
        return mark_y, group['xs']

    answers, debug = run_circle_sampler(gray, geometry, null_margin=NULL_MARGIN, radius=RADIUS)
    metrics = evaluate_answers(
        dataset,
        answers,
        debug,
        extra_metrics={
            'null_margin': NULL_MARGIN,
            'radius': RADIUS,
            'detected_timing_marks': len(marks),
            'first_visible_mark_index': FIRST_VISIBLE_MARK_INDEX,
            'timing_marks_preview': marks[FIRST_VISIBLE_MARK_INDEX:FIRST_VISIBLE_MARK_INDEX + 5],
        },
    )
    result = ApproachResult(
        approach_id='approach_3_timing_marks',
        name='Approach 3, timing-mark anchored registration',
        summary='Use detected right-edge timing marks to set each row Y position, then read fixed answer columns.',
        dataset_id=dataset.dataset_id,
        answers=answers,
        debug=debug,
        metrics=metrics,
    )
    render_overlay(rgb, debug, dataset.out_dir / 'approach_3_timing_marks_overlay.png')
    save_result(dataset, result)
    return result


def _detect_right_edge_hybrid_chain(gray):
    _, th = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    num, _, stats, centroids = cv2.connectedComponentsWithStats(th, 8)
    marks = []
    for i in range(1, num):
        x, y, w, h, area = stats[i]
        cx, cy = centroids[i]
        if cx > RIGHT_EDGE_HYBRID_X_MIN and area > RIGHT_EDGE_HYBRID_AREA_MIN and w >= RIGHT_EDGE_HYBRID_W_MIN and h >= RIGHT_EDGE_HYBRID_H_MIN:
            marks.append({'x': float(cx), 'y': float(cy), 'w': int(w), 'h': int(h), 'area': int(area)})
    marks.sort(key=lambda m: m['y'])
    if not marks:
        raise SystemExit('No right-edge timing marks detected')

    chains = []
    chain = [marks[0]]
    for mark in marks[1:]:
        if mark['y'] - chain[-1]['y'] <= TIMING_MARK_Y_GAP_MAX:
            chain.append(mark)
        else:
            chains.append(chain)
            chain = [mark]
    chains.append(chain)
    return max(chains, key=len)


def approach_4_right_edge_extrapolated_hybrid(dataset: DatasetConfig | None = None):
    dataset = _resolve_dataset(dataset)
    gray, rgb = load_page(dataset)
    chain = _detect_right_edge_hybrid_chain(gray)
    if len(chain) < 9:
        raise SystemExit(f'Expected at least 9 right-edge marks, found {len(chain)}')

    ys = [m['y'] for m in chain]
    xs = [m['x'] for m in chain]
    dy = float(np.median(np.diff(ys)))
    y_last = float(ys[-1])
    dx = float(np.median(xs) - RIGHT_EDGE_CANONICAL_X)

    def geometry(group, row):
        local_row = row if row <= 25 else row - 25
        y = y_last - (25 - local_row) * dy
        shifted = {label: float(x + dx) for label, x in group['xs'].items()}
        return y, shifted

    answers, debug = run_circle_sampler(gray, geometry, null_margin=HYBRID_NULL_MARGIN, radius=HYBRID_RADIUS)
    metrics = evaluate_answers(
        dataset,
        answers,
        debug,
        extra_metrics={
            'null_margin': HYBRID_NULL_MARGIN,
            'radius': HYBRID_RADIUS,
            'detected_right_edge_marks': len(chain),
            'right_edge_chain_preview': chain[:5],
            'dy': dy,
            'dx': dx,
            'y_last': y_last,
        },
    )
    result = ApproachResult(
        approach_id='approach_4_right_edge_extrapolated_hybrid',
        name='Approach 4, right-edge extrapolated hybrid',
        summary='Use the longest detected right-edge chain, anchor from the last visible mark, extrapolate row Y positions upward, and apply a global horizontal shift before reading bubbles.',
        dataset_id=dataset.dataset_id,
        answers=answers,
        debug=debug,
        metrics=metrics,
    )
    render_overlay(rgb, debug, dataset.out_dir / 'approach_4_right_edge_extrapolated_hybrid_overlay.png')
    save_result(dataset, result)
    return result


APPROACHES = [
    approach_1_baseline,
    approach_2_template_registration,
    approach_3_timing_marks,
    approach_4_right_edge_extrapolated_hybrid,
]

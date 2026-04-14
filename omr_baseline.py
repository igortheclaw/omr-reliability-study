import json
from pathlib import Path
from statistics import mean

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
PNG = ROOT / 'out' / 'page-1.png'
GT = ROOT / 'ground_truth.json'
OUT = ROOT / 'out'

# Initial manual calibration from visual inspection
GROUPS = [
    {
        'rows': range(1, 26),
        'xs': {'A': 315, 'B': 353, 'C': 392, 'D': 430},
        'y0': 1387,
        'dy': 34,
    },
    {
        'rows': range(26, 46),
        'xs': {'A': 650, 'B': 687, 'C': 725, 'D': 762},
        'y0': 1374,
        'dy': 34,
    },
]
RADIUS = 11
NULL_MARGIN = 10.0


def circle_darkness(img, cx, cy, r=RADIUS):
    y, x = np.ogrid[:img.shape[0], :img.shape[1]]
    mask = (x - cx) ** 2 + (y - cy) ** 2 <= r * r
    vals = img[mask]
    return float(255.0 - vals.mean())


def pick(scores):
    items = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    best_label, best = items[0]
    second = items[1][1]
    margin = best - second
    if margin < NULL_MARGIN:
        return None, margin
    return best_label, margin


def main():
    OUT.mkdir(exist_ok=True)
    gray = cv2.imread(str(PNG), cv2.IMREAD_GRAYSCALE)
    rgb = cv2.imread(str(PNG), cv2.IMREAD_COLOR)
    if gray is None:
        raise SystemExit(f'Could not read {PNG}')

    answers = {}
    debug = []

    for group in GROUPS:
        for row in group['rows']:
            y = int(round(group['y0'] + group['dy'] * (row - group['rows'].start)))
            scores = {label: circle_darkness(gray, x, y) for label, x in group['xs'].items()}
            pred, margin = pick(scores)
            answers[str(row)] = pred
            debug.append({'row': row, 'y': y, 'scores': scores, 'pred': pred, 'margin': margin})
            for label, x in group['xs'].items():
                color = (0, 255, 0) if pred == label else (255, 0, 0)
                cv2.circle(rgb, (x, y), RADIUS, color, 1)
            cv2.putText(rgb, f"{row}:{pred or 'NULL'}", (min(group['xs'].values()) - 55, y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

    with open(GT, 'r', encoding='utf-8') as f:
        gt = json.load(f)['answers']

    exact = wrong = nulls = 0
    accepted_correct = 0
    accepted_total = 0
    failures = []
    for row_s, truth in gt.items():
        pred = answers[row_s]
        if pred is None:
            nulls += 1
            failures.append({'row': int(row_s), 'truth': truth, 'pred': None})
        elif pred == truth:
            exact += 1
            accepted_correct += 1
            accepted_total += 1
        else:
            wrong += 1
            accepted_total += 1
            failures.append({'row': int(row_s), 'truth': truth, 'pred': pred})

    metrics = {
        'exact_matches': exact,
        'wrong': wrong,
        'null': nulls,
        'rows': len(gt),
        'accuracy': exact / len(gt),
        'accepted_precision': (accepted_correct / accepted_total) if accepted_total else None,
        'accepted_coverage': accepted_total / len(gt),
        'null_margin': NULL_MARGIN,
        'radius': RADIUS,
        'mean_margin': mean(d['margin'] for d in debug),
        'failures': failures,
    }

    (OUT / 'baseline_results.json').write_text(json.dumps({'answers': answers, 'debug': debug, 'metrics': metrics}, indent=2), encoding='utf-8')
    cv2.imwrite(str(OUT / 'baseline_overlay.png'), rgb)
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Callable

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out'
PNG = OUT / 'page-1.png'
GT = ROOT / 'ground_truth.json'

GROUPS = [
    {
        'name': 'left',
        'rows': range(1, 26),
        'xs': {'A': 315, 'B': 353, 'C': 392, 'D': 430},
        'y0': 1387,
        'dy': 34,
    },
    {
        'name': 'right',
        'rows': range(26, 46),
        'xs': {'A': 650, 'B': 687, 'C': 725, 'D': 762},
        'y0': 1374,
        'dy': 34,
    },
]
RADIUS = 11
NULL_MARGIN = 10.0


@dataclass
class ApproachResult:
    approach_id: str
    name: str
    summary: str
    answers: dict
    debug: list
    metrics: dict

    def to_json(self):
        return {
            'approach_id': self.approach_id,
            'name': self.name,
            'summary': self.summary,
            'answers': self.answers,
            'debug': self.debug,
            'metrics': self.metrics,
        }


def ensure_rendered_page():
    OUT.mkdir(exist_ok=True)
    if PNG.exists():
        return PNG
    cmd = ['pdftoppm', '-png', '-r', '200', str(ROOT / 'sample.pdf'), str(OUT / 'page')]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit('Could not render sample.pdf. Install pdftoppm and rerun.') from exc
    if not PNG.exists():
        raise SystemExit('Could not render sample.pdf. Install pdftoppm and rerun.')
    return PNG


def load_page():
    ensure_rendered_page()
    gray = cv2.imread(str(PNG), cv2.IMREAD_GRAYSCALE)
    rgb = cv2.imread(str(PNG), cv2.IMREAD_COLOR)
    if gray is None or rgb is None:
        raise SystemExit(f'Could not read {PNG}')
    return gray, rgb


def load_ground_truth():
    return json.loads(GT.read_text(encoding='utf-8'))['answers']


def circle_darkness(img, cx, cy, r=RADIUS):
    y, x = np.ogrid[:img.shape[0], :img.shape[1]]
    mask = (x - cx) ** 2 + (y - cy) ** 2 <= r * r
    vals = img[mask]
    return float(255.0 - vals.mean())


def pick(scores, null_margin=NULL_MARGIN):
    items = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    best_label, best = items[0]
    second = items[1][1]
    margin = best - second
    if margin < null_margin:
        return None, margin
    return best_label, margin


def evaluate_answers(answers, debug, extra_metrics=None):
    gt = load_ground_truth()
    exact = wrong = nulls = 0
    accepted_correct = accepted_total = 0
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
        'mean_margin': mean(d['margin'] for d in debug),
        'failures': failures,
    }
    if extra_metrics:
        metrics.update(extra_metrics)
    return metrics


def render_overlay(base_rgb, debug, path):
    rgb = base_rgb.copy()
    for d in debug:
        row = d['row']
        pred = d['pred']
        y = int(round(d['y']))
        for label, x in d['positions'].items():
            color = (0, 255, 0) if pred == label else (255, 0, 0)
            cv2.circle(rgb, (int(round(x)), y), RADIUS, color, 1)
        cv2.putText(
            rgb,
            f"{row}:{pred or 'NULL'}",
            (int(min(d['positions'].values())) - 55, y + 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )
    cv2.imwrite(str(path), rgb)


def run_circle_sampler(
    gray,
    row_geometry: Callable[[dict, int], tuple[float, dict]],
    *,
    null_margin=NULL_MARGIN,
    radius=RADIUS,
):
    answers = {}
    debug = []
    for group in GROUPS:
        for row in group['rows']:
            y, xs = row_geometry(group, row)
            scores = {label: circle_darkness(gray, int(round(x)), int(round(y)), r=radius) for label, x in xs.items()}
            pred, margin = pick(scores, null_margin=null_margin)
            answers[str(row)] = pred
            debug.append({
                'row': row,
                'group': group['name'],
                'y': float(y),
                'positions': {k: float(v) for k, v in xs.items()},
                'scores': scores,
                'pred': pred,
                'margin': float(margin),
            })
    return answers, debug


def save_result(result: ApproachResult):
    OUT.mkdir(exist_ok=True)
    out_json = OUT / f'{result.approach_id}_results.json'
    out_json.write_text(json.dumps(result.to_json(), indent=2), encoding='utf-8')
    return out_json

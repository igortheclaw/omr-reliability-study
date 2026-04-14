import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Callable

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
DATASETS_DIR = ROOT / 'datasets'
OUT = ROOT / 'out'
DEFAULT_DATASET_ID = 'sample'

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


@dataclass(frozen=True)
class DatasetConfig:
    dataset_id: str
    dataset_dir: Path
    pdf_path: Path
    ground_truth_path: Path
    metadata_path: Path
    metadata: dict

    @property
    def out_dir(self) -> Path:
        return OUT / self.dataset_id

    @property
    def rendered_png(self) -> Path:
        return self.out_dir / 'page-1.png'


@dataclass
class ApproachResult:
    approach_id: str
    name: str
    summary: str
    dataset_id: str
    answers: dict
    debug: list
    metrics: dict

    def to_json(self):
        return {
            'approach_id': self.approach_id,
            'name': self.name,
            'summary': self.summary,
            'dataset_id': self.dataset_id,
            'answers': self.answers,
            'debug': self.debug,
            'metrics': self.metrics,
        }


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def discover_datasets() -> list[DatasetConfig]:
    datasets = []
    if not DATASETS_DIR.exists():
        return datasets

    for dataset_dir in sorted(p for p in DATASETS_DIR.iterdir() if p.is_dir()):
        metadata_path = dataset_dir / 'dataset.json'
        ground_truth_path = dataset_dir / 'ground_truth.json'
        if not metadata_path.exists() or not ground_truth_path.exists():
            continue
        metadata = _load_json(metadata_path)
        dataset_id = metadata.get('dataset_id', dataset_dir.name)
        pdf_path = ROOT / metadata['pdf_path']
        datasets.append(
            DatasetConfig(
                dataset_id=dataset_id,
                dataset_dir=dataset_dir,
                pdf_path=pdf_path,
                ground_truth_path=ground_truth_path,
                metadata_path=metadata_path,
                metadata=metadata,
            )
        )
    return datasets


def get_dataset(dataset_id: str = DEFAULT_DATASET_ID) -> DatasetConfig:
    datasets = discover_datasets()
    for dataset in datasets:
        if dataset.dataset_id == dataset_id:
            return dataset
    available = ', '.join(d.dataset_id for d in datasets)
    raise SystemExit(f'Unknown dataset {dataset_id!r}. Available datasets: {available}')


def load_ground_truth_payload(dataset: DatasetConfig) -> dict:
    return _load_json(dataset.ground_truth_path)


def load_ground_truth(dataset: DatasetConfig) -> dict:
    return load_ground_truth_payload(dataset)['answers']


def labeled_ground_truth_answers(dataset: DatasetConfig) -> dict:
    answers = load_ground_truth(dataset)
    return {row: value for row, value in answers.items() if value is not None}


def count_labeled_answers(dataset: DatasetConfig) -> int:
    return len(labeled_ground_truth_answers(dataset))


def dataset_is_benchmarkable(dataset: DatasetConfig) -> bool:
    return count_labeled_answers(dataset) > 0


def ensure_rendered_page(dataset: DatasetConfig) -> Path:
    dataset.out_dir.mkdir(parents=True, exist_ok=True)
    if dataset.rendered_png.exists():
        return dataset.rendered_png
    cmd = ['pdftoppm', '-png', '-r', '200', str(dataset.pdf_path), str(dataset.out_dir / 'page')]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f'Could not render {dataset.pdf_path}. Install pdftoppm and rerun.') from exc
    if not dataset.rendered_png.exists():
        raise SystemExit(f'Could not render {dataset.pdf_path}. Install pdftoppm and rerun.')
    return dataset.rendered_png


def load_page(dataset: DatasetConfig):
    png_path = ensure_rendered_page(dataset)
    gray = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
    rgb = cv2.imread(str(png_path), cv2.IMREAD_COLOR)
    if gray is None or rgb is None:
        raise SystemExit(f'Could not read {png_path}')
    return gray, rgb


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


def evaluate_answers(dataset: DatasetConfig, answers, debug, extra_metrics=None):
    gt = labeled_ground_truth_answers(dataset)
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

    labeled_rows = len(gt)
    metrics = {
        'exact_matches': exact,
        'wrong': wrong,
        'null': nulls,
        'rows': labeled_rows,
        'total_rows': len(load_ground_truth(dataset)),
        'labeled_rows': labeled_rows,
        'accuracy': exact / labeled_rows,
        'accepted_precision': (accepted_correct / accepted_total) if accepted_total else None,
        'accepted_coverage': accepted_total / labeled_rows,
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


def save_result(dataset: DatasetConfig, result: ApproachResult):
    dataset.out_dir.mkdir(parents=True, exist_ok=True)
    out_json = dataset.out_dir / f'{result.approach_id}_results.json'
    out_json.write_text(json.dumps(result.to_json(), indent=2), encoding='utf-8')
    return out_json

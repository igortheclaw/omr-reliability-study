import argparse
import json
from pathlib import Path

from omr_approaches import APPROACHES
from omr_core import OUT, dataset_is_benchmarkable, discover_datasets, get_dataset


def parse_args():
    parser = argparse.ArgumentParser(description='Run deterministic OMR benchmarks per dataset.')
    parser.add_argument('--dataset', help='Run a single dataset by dataset_id.')
    parser.add_argument('--all', action='store_true', help='Run every discovered dataset and skip those without labeled ground truth.')
    return parser.parse_args()


def _format_metric(value):
    return 'n/a' if value is None else f'{value:.4f}'


def _summarize_results(results):
    summary = []
    for result in results:
        metrics = result.metrics
        summary.append({
            'approach_id': result.approach_id,
            'name': result.name,
            'summary': result.summary,
            'dataset_id': result.dataset_id,
            'exact_matches': metrics['exact_matches'],
            'wrong': metrics['wrong'],
            'null': metrics['null'],
            'rows': metrics['rows'],
            'total_rows': metrics['total_rows'],
            'labeled_rows': metrics['labeled_rows'],
            'accuracy': metrics['accuracy'],
            'accepted_precision': metrics['accepted_precision'],
            'accepted_coverage': metrics['accepted_coverage'],
            'failures': metrics['failures'],
        })
    return summary


def run_dataset(dataset):
    dataset.out_dir.mkdir(parents=True, exist_ok=True)
    results = [fn(dataset) for fn in APPROACHES]
    summary = _summarize_results(results)
    best = max(summary, key=lambda x: (x['accuracy'], x['accepted_precision'] or 0.0, x['accepted_coverage']))
    payload = {
        'dataset_id': dataset.dataset_id,
        'pdf_path': str(dataset.pdf_path.relative_to(Path.cwd())),
        'approaches': summary,
        'best_observed': best,
    }
    (dataset.out_dir / 'benchmark_summary.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return payload


def _print_dataset_summary(payload):
    print(f"Dataset: {payload['dataset_id']}")
    for item in payload['approaches']:
        print(
            f"- {item['approach_id']}: {item['exact_matches']}/{item['rows']} exact, "
            f"wrong={item['wrong']}, null={item['null']}, accuracy={item['accuracy']:.4f}, "
            f"accepted_precision={_format_metric(item['accepted_precision'])}, "
            f"coverage={_format_metric(item['accepted_coverage'])}"
        )
    best = payload['best_observed']
    print(f"Best observed approach: {best['approach_id']} ({best['accuracy']:.4f} exact accuracy)")
    print('')


def main():
    args = parse_args()
    OUT.mkdir(exist_ok=True)

    if args.dataset and args.all:
        raise SystemExit('Choose either --dataset <dataset_id> or --all, not both.')

    if args.dataset:
        selected = [get_dataset(args.dataset)]
    else:
        selected = discover_datasets()
        if not selected:
            raise SystemExit('No datasets discovered under datasets/.')

    skipped = []
    payloads = []
    for dataset in selected:
        if not dataset_is_benchmarkable(dataset):
            skipped.append({
                'dataset_id': dataset.dataset_id,
                'reason': 'ground_truth.json has no non-null answers yet',
            })
            continue
        payload = run_dataset(dataset)
        payloads.append(payload)

    if not payloads:
        print('No benchmarkable datasets were run.')
        for item in skipped:
            print(f"- {item['dataset_id']}: {item['reason']}")
        return

    aggregate = {
        'mode': 'single' if len(payloads) == 1 and args.dataset else 'multi',
        'datasets_run': [payload['dataset_id'] for payload in payloads],
        'datasets_skipped': skipped,
        'dataset_summaries': payloads,
    }
    (OUT / 'benchmark_summary.json').write_text(json.dumps(aggregate, indent=2), encoding='utf-8')

    print('Comparative OMR benchmark')
    print('')
    for payload in payloads:
        _print_dataset_summary(payload)
    if skipped:
        print('Skipped datasets')
        for item in skipped:
            print(f"- {item['dataset_id']}: {item['reason']}")


if __name__ == '__main__':
    main()

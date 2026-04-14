import json
from pathlib import Path

from omr_approaches import APPROACHES
from omr_core import OUT


def main():
    OUT.mkdir(exist_ok=True)
    results = [fn() for fn in APPROACHES]
    summary = []
    for result in results:
        metrics = result.metrics
        summary.append({
            'approach_id': result.approach_id,
            'name': result.name,
            'summary': result.summary,
            'exact_matches': metrics['exact_matches'],
            'wrong': metrics['wrong'],
            'null': metrics['null'],
            'rows': metrics['rows'],
            'accuracy': metrics['accuracy'],
            'accepted_precision': metrics['accepted_precision'],
            'accepted_coverage': metrics['accepted_coverage'],
            'failures': metrics['failures'],
        })

    best = max(summary, key=lambda x: (x['accuracy'], x['accepted_precision'] or 0.0, x['accepted_coverage']))
    payload = {
        'approaches': summary,
        'best_observed': best,
    }
    (OUT / 'benchmark_summary.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')

    print('Comparative OMR benchmark')
    print('')
    for item in summary:
        print(f"- {item['approach_id']}: {item['exact_matches']}/{item['rows']} exact, wrong={item['wrong']}, null={item['null']}, accuracy={item['accuracy']:.4f}, accepted_precision={item['accepted_precision']:.4f}, coverage={item['accepted_coverage']:.4f}")
    print('')
    print(f"Best observed approach: {best['approach_id']} ({best['accuracy']:.4f} exact accuracy)")


if __name__ == '__main__':
    main()

import argparse
import json
import shutil

from omr_approaches import approach_1_baseline
from omr_core import get_dataset


def parse_args():
    parser = argparse.ArgumentParser(description='Legacy wrapper for approach 1 only.')
    parser.add_argument('--dataset', default='sample', help='Dataset id to run. Defaults to sample.')
    return parser.parse_args()


def main():
    args = parse_args()
    dataset = get_dataset(args.dataset)
    result = approach_1_baseline(dataset)
    shutil.copyfile(dataset.out_dir / 'approach_1_baseline_results.json', dataset.out_dir / 'baseline_results.json')
    shutil.copyfile(dataset.out_dir / 'approach_1_baseline_overlay.png', dataset.out_dir / 'baseline_overlay.png')
    print(json.dumps({'dataset_id': dataset.dataset_id, 'metrics': result.metrics}, indent=2))


if __name__ == '__main__':
    main()

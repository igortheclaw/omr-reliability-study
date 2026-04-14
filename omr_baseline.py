import json
import shutil

from omr_approaches import approach_1_baseline
from omr_core import OUT


def main():
    result = approach_1_baseline()
    shutil.copyfile(OUT / 'approach_1_baseline_results.json', OUT / 'baseline_results.json')
    shutil.copyfile(OUT / 'approach_1_baseline_overlay.png', OUT / 'baseline_overlay.png')
    print(json.dumps(result.metrics, indent=2))


if __name__ == '__main__':
    main()

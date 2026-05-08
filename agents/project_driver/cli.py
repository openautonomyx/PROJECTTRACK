import argparse
import json

from planning_engine import generate_plan
from publishers import ApprovalRequiredPublisher


def main():
    parser = argparse.ArgumentParser(description='PROJECTTRACK provider-neutral project manager CLI')
    parser.add_argument('task', help='Project management task to run')
    parser.add_argument('--json', action='store_true', help='Print JSON ProjectPlan output')
    parser.add_argument('--publish', action='store_true', help='Export plan artifacts through approval-first publisher')

    args = parser.parse_args()

    plan = generate_plan(args.task)

    if args.publish:
        result = ApprovalRequiredPublisher().publish(plan)
        print('Publish result:')
        print(json.dumps(result, indent=2))

    if args.json:
        print(json.dumps(plan.model_dump(), indent=2))
    else:
        print(plan.summary)
        print('\nNext actions:')
        for action in plan.next_actions:
            print(f'- {action}')


if __name__ == '__main__':
    main()

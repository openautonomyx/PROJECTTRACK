import argparse
import json

from planning_engine import generate_plan
from publishers import ApprovalRequiredPublisher
from approval_workflow import ApprovalWorkflow


workflow = ApprovalWorkflow()


def main():
    parser = argparse.ArgumentParser(description='PROJECTTRACK provider-neutral project manager CLI')

    parser.add_argument('task', nargs='?', help='Project management task to run')

    parser.add_argument('--json', action='store_true', help='Print JSON ProjectPlan output')
    parser.add_argument('--publish', action='store_true', help='Export plan artifacts through approval-first publisher')

    parser.add_argument('--list-approvals', action='store_true', help='List pending approval drafts')

    parser.add_argument('--approve', type=str, help='Approve a draft by ID')

    parser.add_argument('--reject', type=str, help='Reject a draft by ID')
    parser.add_argument('--reason', type=str, help='Optional rejection reason')

    args = parser.parse_args()

    if args.list_approvals:
        print(json.dumps(workflow.list_drafts(), indent=2))
        return

    if args.approve:
        result = workflow.approve(args.approve)
        print(json.dumps(result, indent=2))
        return

    if args.reject:
        result = workflow.reject(args.reject, reason=args.reason)
        print(json.dumps(result, indent=2))
        return

    if not args.task:
        parser.error('task is required unless using approval commands')

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

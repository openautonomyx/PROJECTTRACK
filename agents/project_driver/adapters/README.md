# Adapter Architecture

PROJECTTRACK uses a provider-neutral project management core.

Adapters are optional transport integrations that connect the core runtime to external systems.

## Design principle

The planning engine must not depend on GitHub, Jira, Linear, Slack, Notion, or any other provider.

Instead:

```text
Planning Engine
        ↓
Structured ProjectPlan
        ↓
Adapter Contracts
        ↓
Provider Implementations
```

## Planned adapters

- GitHub
- Jira
- Linear
- Slack
- Discord
- Notion
- CLI
- REST API
- Browser Chat

## Adapter contracts

- TaskAdapter
- MilestoneAdapter
- RiskAdapter
- DecisionAdapter
- PlanPublisher

## Example future structure

```text
adapters/
├─ github/
├─ jira/
├─ linear/
├─ slack/
├─ notion/
└─ cli/
```

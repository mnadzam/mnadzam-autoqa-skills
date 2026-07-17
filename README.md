# autoqa-skills

AI skills for AutoQA CI/CD test failure analysis and triage. These skills are
consumed by the [agentic-ci](https://github.com/opendatahub-io/agentic-ci)
Claude runner image and orchestrated by AutoQA.

## Skills

| Skill | Description |
|---|---|
| [failure-analysis](skills/failure-analysis/) | Analyze a test failure log to identify the root cause |
| [failure-matching](skills/failure-matching/) | Match a test failure against historical Jira tickets to find known issues |
| [false-alarm-detection](skills/false-alarm-detection/) | Classify a test failure as a known infrastructure false alarm or genuine bug |

## Architecture

```text
AutoQA orchestrator
    |
    v
agentic-ci Claude runner (container)
    |
    v
autoqa-skills (this repo, mounted as plugin)
    |
    +-- skills/failure-analysis/
    +-- skills/failure-matching/
    +-- skills/false-alarm-detection/
```

The orchestrator prepares a workspace with context files (`_context/`) and test
logs, then invokes a skill. The skill reads its context, analyzes the log or
data, and produces a `verdict.json` file with structured output.

## Development

```bash
make lint          # Run skillsaw + ruff
make skillsaw      # Run skillsaw only
make skillsaw-fix  # Auto-fix skillsaw issues
```

## License

Apache-2.0

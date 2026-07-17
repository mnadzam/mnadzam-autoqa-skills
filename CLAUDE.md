# autoqa-skills

AI skills for AutoQA CI/CD test failure analysis and triage. Each skill is a
self-contained unit consumed by the agentic-ci Claude runner image.

## Skill format

Each skill lives in `skills/<skill-name>/` and contains:

- `SKILL.md` -- YAML frontmatter (name, description, allowed-tools, metadata) + markdown prompt body
- `schemas/` -- JSON Schema files for verdict validation
- `scripts/` -- executable scripts the skill invokes (validation, JSON writing)
- `patterns/` -- (false-alarm-detection only) pluggable pattern definitions

Skills reference sibling files via `${CLAUDE_SKILL_DIR}`.

## Workspace contract

The orchestrator (AutoQA) prepares:

- `/workspace/_context/<skill>-context.json` -- dynamic context for this invocation
- `/workspace/_context/logs/` -- test log files (where applicable)

Skills read their context JSON first, then operate on the workspace. Each skill
writes a `/workspace/verdict.json` file as its structured output.

## Conventions

- Skills are self-contained: everything needed is in the skill directory
- Each SKILL.md includes an "Authority and Data Boundaries" section
- Context is passed via JSON files, not template variable substitution
- False-alarm patterns are part of the skill definition, not context
- Skills are model-agnostic: the orchestrator selects the model

## Linting

```bash
make lint        # skillsaw + ruff
make skillsaw    # skillsaw only
```

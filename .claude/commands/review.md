---
description: Review a Higgsfield prompt or shot list with parallel reviewers (lint + preflight, craft, continuity) and return one scored report
argument-hint: <prompt text | file path> [model=<id> ar=<ratio> duration=<s> …]
---

Review `$ARGUMENTS`. If it is a file path, read it; if it holds several shots, treat each as a shot.

Launch these subagents **in one message, in parallel**, giving each the prompt(s) and any model/params:

- `hf-lint-reviewer` — per shot
- `hf-craft-reviewer` — per shot
- `hf-continuity-reviewer` — once, only when there are 2+ shots
- `hf-spec-freshness-reviewer` — once; tells you how far the other checks' enum verdicts can be trusted
- `hf-filter-risk-reviewer` — per shot; read-only lookup in the filter memory
- `hf-cost-reviewer` — once, only when the arguments mention a project, a budget, or `cost`

Then merge into one report. Do not edit the prompts unless asked; this is a review.

```
# Prompt review
| Check | Result |
|---|---|
| Lint (seedance_lint) | PASS / WARN / FAIL / NOT RUN |
| Preflight | PASS / FAIL / UNCHECKED / NOT RUN |
| Craft | blockers: N · should-fix: N · nits: N |
| Continuity | clean / N drifts / n/a |
| Spec freshness | FRESH / STALE / UNCHECKED |
| Filter memory | N known trips / no data |
| Cost | est. / NOT AVAILABLE / not requested |

Grade: A (no blockers or warnings) · B (should-fix only) · C (any blocker or lint WARN) · F (lint/preflight FAIL)
A STALE or UNCHECKED spec row never lowers the grade, but say it beside the grade: the grade is only as good as the specs behind it.
```

Then list findings sorted by severity. Each one: shot, quoted text, reason (cite HARD RULE numbers),
replacement wording, and how you will know it worked. Say plainly when a check was UNCHECKED or NOT RUN —
never report those as passing. Do not run anything with `--log`/`--confirmed` (they write to memory).

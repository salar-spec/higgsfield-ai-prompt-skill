---
description: Review a Higgsfield prompt or shot list with parallel reviewers (lint + preflight, craft, continuity) and return one scored report
argument-hint: <prompt text | file path> [model=<id> ar=<ratio> duration=<s> …]
---

Review `$ARGUMENTS`. If it is a file path, read it; if it holds several shots, treat each as a shot.

Launch these subagents **in one message, in parallel**, giving each the prompt(s) and any model/params:

- `hf-lint-reviewer` — per shot
- `hf-craft-reviewer` — per shot
- `hf-continuity-reviewer` — once, only when there are 2+ shots

Then merge into one report. Do not edit the prompts unless asked; this is a review.

```
# Prompt review
| Check | Result |
|---|---|
| Lint (seedance_lint) | PASS / WARN / FAIL / NOT RUN |
| Preflight | PASS / FAIL / UNCHECKED / NOT RUN |
| Craft | blockers: N · should-fix: N · nits: N |
| Continuity | clean / N drifts / n/a |

Grade: A (no blockers or warnings) · B (should-fix only) · C (any blocker or lint WARN) · F (lint/preflight FAIL)
```

Then list findings sorted by severity. Each one: shot, quoted text, reason (cite HARD RULE numbers),
replacement wording, and how you will know it worked. Say plainly when a check was UNCHECKED or NOT RUN —
never report those as passing. Do not run anything with `--log`/`--confirmed` (they write to memory).

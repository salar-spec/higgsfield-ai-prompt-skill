# Using the skill alongside Caveman

[Caveman](https://github.com/JuliusBrussee/caveman) is an Apache-2.0 skill and CLI that cuts
tokens by having the agent answer in terse "caveman" English, and by compressing memory files
and noisy command output. Its README states that code, commands, paths and error messages stay
verbatim.

It can sit beside this skill, but a Higgsfield prompt is the one place it must not reach: the
prompt is the deliverable, and its wording is what the video or image model renders.

## Install

```bash
npx skills add JuliusBrussee/caveman -g
```

or inside Claude Code:

```text
/plugin marketplace add JuliusBrussee/caveman
/plugin install caveman@caveman
```

Turn the voice on with `/caveman` (levels lite / full / ultra) and off with `/caveman off` or
"stop caveman".

## What Caveman may compress, and what it must not

| Text | Caveman? |
|---|---|
| The agent's chat around a prompt (explanations, defaults, next steps) | **Yes**, at any level |
| The prompt itself: the text you paste into Higgsfield or the agent sends to the CLI/MCP | **No.** Keep it word for word as the skill wrote it |
| Files in `workspace/output/` (prompt packs, shot lists, CSVs) | **No.** They are deliverables |
| This skill's own files (`SKILL.md`, `skills/`, `templates/`, `vocab.md`, …) | **No.** Never run `/caveman-compress` or `caveman convert` on them |
| Your project's `CLAUDE.md` | Your call; it is outside the skill |

### Why the prompt must stay whole

The skill's prompts are built from exact cinematic vocabulary, shot grammar and ordering
(`vocab.md`, `prompt-examples.md`), and many models read articles, prepositions and word order
as meaning: "camera slowly pushes in on her face as rain falls" and "cam push face rain" are not
the same shot. Dropped words also defeat the skill's checks: `seedance_lint.py` checks length caps,
structure and content-filter phrasing on the text it is given, and the HARD RULES pre-delivery checklist assumes the
prompt you receive is the prompt it checked.

To keep the prompt verbatim, ask for it in a code block, which Caveman leaves alone:

> *Put each prompt in its own code block.*

If a prompt ever arrives compressed, say "stop caveman" and ask for it again.

### Why the skill's files must stay whole

`/caveman-compress` rewrites a file in place (keeping a backup), and `caveman convert` turns
skills into images for the model to read. On this skill either one would:

- break the checks `scripts/validate.py` runs: required frontmatter, generated CONTENTS blocks
  and INDEX.md, QUICK FACTS anchors, and the HARD RULES drift check between `SKILL.md`,
  `DISCIPLINE.md` and `CLAUDE.md`;
- blur the exact model ids, parameter values and rule wording the agent must copy;
- make every later `git pull` of the skill conflict with your rewritten copies.

If one was already run, restore with `git -C ~/.claude/skills/higgsfield checkout -- .`.

## Through OmniRoute

OmniRoute offers its own Caveman-style compression for traffic it routes. The same line holds:
compressing the agent's chat is fine; the prompt text and the skill's reference files should
reach the model whole. See [`omniroute.md`](omniroute.md).

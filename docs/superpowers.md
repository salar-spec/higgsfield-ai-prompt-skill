# Using the skill alongside Superpowers

[Superpowers](https://github.com/obra/superpowers) is an MIT-licensed Claude Code plugin by Jesse
Vincent: a library of software-development skills (brainstorming, writing-plans,
executing-plans, test-driven-development, systematic-debugging, verification-before-completion,
writing-skills and others) plus a `using-superpowers` bootstrap that tells the agent to check for
a matching skill before it acts. It installs beside this skill; neither needs changes to work
with the other.

## Install

```text
/plugin install superpowers@claude-plugins-official
```

or from the author's marketplace:

```text
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

Install this skill as usual (README → Install → Claude Code). The two do not share files.

## Who handles what

| Task | Skill that should lead |
|---|---|
| Writing, reviewing or fixing a Higgsfield prompt; picking a model; shot lists | **higgsfield** (root `SKILL.md`) |
| A vague creative brief ("make me an ad for…") | Superpowers **brainstorming** may ask the questions first; hand the agreed brief to **higgsfield** for the prompts |
| A multi-shot campaign or full project | Superpowers **writing-plans** for the plan; each shot's prompt still comes from **higgsfield** and its HARD RULES |
| Changing this repo's Python tooling (`scripts/`, `tests/`) | Superpowers **test-driven-development** / **systematic-debugging** |
| Editing this repo's `SKILL.md` files | Superpowers **writing-skills** for structure, but this repo's rules win (below) |

### When they disagree

- **Prompt delivery.** The pre-delivery checklist in root `SKILL.md` § HARD RULES applies to every
  prompt, whatever plan or workflow produced it. A Superpowers plan step that says "write the
  prompt" still ends with that checklist and, before spending credits,
  `python3 scripts/preflight.py --model <id> … --strict`.
- **Quick asks.** For a one-line request ("give me a Kling prompt for a rainy street"), the
  agent should not open a brainstorming or planning round first. If it does, say "just the
  prompt".
- **Editing skills in this repo.** Frontmatter (`name`, `description`, `metadata.version`,
  `metadata.updated`, `metadata.parent: higgsfield` for sub-skills), routing from root
  `SKILL.md`, and `python3 scripts/build_index.py` after any heading change are enforced by
  `scripts/validate.py`. Sub-skill versions stay independent of the root version (see
  `CLAUDE.md`).

## Contributors: verification maps to the release gate

Superpowers' **verification-before-completion** asks for evidence before claiming work is done.
In this repo that evidence is the release gate, all three green:

```bash
python3 scripts/validate.py --strict
python3 -m pytest tests/ -q
python3 scripts/validate.py --evals
```

(`/validate` runs the same three.)

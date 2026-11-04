# Using the skill alongside claude-mem

[claude-mem](https://github.com/thedotmack/claude-mem) is an Apache-2.0 Claude Code plugin that
gives the agent memory across sessions. Lifecycle hooks (SessionStart, UserPromptSubmit,
PostToolUse, Stop and others) record what the agent does, compress it into summaries in a local
SQLite + Chroma store, and inject the relevant parts into later sessions. Its `mem-search` skill
(with the `search`, `timeline` and `get_observations` tools) looks things up on demand.

This skill already has a learning memory of its own. The two can run together. Nothing in either
needs changes, but they remember different things and only one of them is the record.

## Install

```bash
npx claude-mem install
```

or inside Claude Code:

```text
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

Install this skill as usual (README → Install → Claude Code).

## Two memories, two jobs

| | **Skill memory** (`scripts/higgsfield_memory.py`) | **claude-mem** |
|---|---|---|
| What it holds | Structured records: content-filter triggers and fixes, prompt failures and the fix that worked, one ledger row per generation (model, tags, kept/rejected) | AI-written summaries of past sessions: what was discussed, decided, edited |
| Where | `~/.higgsfield-skill/db/` for a Claude Code install (`… where` prints it) | claude-mem's own local store |
| Written by | Explicit commands: `add-filter`, `add-quality`, `log-gen` | Automatically, by hooks |
| Read by | The skill's recall step and preflight, by exact query (`query-filter`, `last-gen`, `ratio`, `budget`) | Injected at session start, or `mem-search` |
| Use it for | Facts the skill acts on: "this phrase trips the filter on Kling", "close-ups keep 1 in 4" | Continuity: "where did we leave the perfume campaign?" |

### Rules when both are installed

- **The skill memory is the record.** A filter trigger, a failed prompt or a generation outcome
  goes into the skill memory with its command, even if claude-mem has already captured the
  conversation about it. Takes-per-kept ratios, credit budgets and the filter recall read only
  the skill memory; a summary in claude-mem does not count toward them.
- **When they disagree, trust the skill memory.** claude-mem's summaries are compressed by a
  model and can blur a model id, a parameter value or which take was kept. Check against
  `query-filter`, `query-quality` or `last-gen` before reusing a recalled detail in a prompt.
- **Model specs come from `specs/`, not from memory.** A remembered "Seedance takes 15 s" may
  predate a spec refresh. Run `python3 scripts/preflight.py --model <id> … --strict` before
  spending credits, whatever either memory says.
- **Don't import one into the other.** Copying claude-mem summaries into `db/` would put
  unstructured, unverified text into a store the scripts parse and count.

## Privacy

claude-mem records tool use and conversation, which can include client briefs, reference-image
paths, unreleased product names or API keys pasted into a prompt. Wrap anything that should not
be stored in `<private>…</private>` tags, which claude-mem leaves out. The skill memory stores
only what its commands are given.

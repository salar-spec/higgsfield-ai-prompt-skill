# Scanning the skill with Claude Security

The [Claude Security plugin](https://code.claude.com/docs/en/claude-security) is Anthropic's
vulnerability scanner for Claude Code. Its `/claude-security` command runs a multi-agent scan of
a repository or a diff, has independent agents verify every finding, and can turn findings into
reviewed patches that you apply yourself. It runs in your session on your session's model and
counts toward your usage.

It does not change how the skill writes prompts. It is for checking the skill's own code: the
Python scripts it runs on your machine, and changes before they are merged.

## Install

In Claude Code:

```text
/plugin install claude-security@claude-plugins-official
```

If the marketplace is not found, run `/plugin marketplace add anthropics/claude-plugins-official`
first; if the plugin is not found, `/plugin marketplace update claude-plugins-official`. Needs a
paid plan or API access, `python3` 3.9+ and git; this skill already needs the last two.

## What is worth scanning here

The skill is mostly Markdown and JSON, which a scan has little to say about. The code that runs
is in `scripts/`, standard-library Python, and these are the parts that touch the outside:

| Area | Why look |
|---|---|
| `scripts/higgsfield_memory.py` | Writes to `~/.higgsfield-skill/db/`, copies and renames folders, takes JSON from the agent on the command line |
| `scripts/refresh_specs.py`, `scripts/validate.py` | Run the Higgsfield CLI and other commands as subprocesses |
| `scripts/generate_user_guide.py`, `scripts/validate_user_guide.py` | Run subprocesses during the PDF build |
| `.github/workflows/` | CI with repository permissions (`validate.yml`, `spec-drift.yml`) |
| `.claude/settings.json` | The permission rules shipped with the repo |

Ask for that scope directly, for example:

```text
/claude-security scan scripts/ and .github/workflows/
```

## When to run it

- **Before installing or updating**, if you want to check what you are about to run: a full
  scan of the clone at `low` effort is a quick first look.
- **Contributors, before a PR** that touches `scripts/` or `.github/`: scan only your branch.

  ```text
  /claude-security scan my branch
  ```

  Only committed changes are scanned; commit or stash first.

The quick built-in `/security-review` is a single pass over the branch; the plugin goes deeper.
Neither replaces the release gate (`validate.py --strict`, `pytest`, `--evals`).

## Results and patches

Each scan writes a `CLAUDE-SECURITY-<timestamp>/` folder in the repo root: a Markdown report,
JSONL, SARIF and a revision stamp, plus `patches/` if you ask for fixes. The folder carries its
own `.gitignore`, so it stays out of commits, and this repo's checks (`validate.py`,
`build_index.py`, `pytest`) ignore it.

Patches are never applied automatically. Apply one with
`git apply CLAUDE-SECURITY-<timestamp>/patches/F1.patch`, one finding per PR, and run the release
gate on it like any other change. A fix in `scripts/` gets a test in `tests/` and a CHANGELOG
entry.

Scans are nondeterministic: two runs can report different findings. Treat a clean report as one
more check, not proof.

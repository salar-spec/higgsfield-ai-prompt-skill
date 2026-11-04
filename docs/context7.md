# Using Context7 beside the skill

[Context7](https://github.com/upstash/context7) is an MIT-licensed service from Upstash that
feeds coding agents current documentation for libraries and frameworks, instead of whatever the
model remembers from training. It works as an MCP server (`resolve-library-id`, `query-docs`) or
as a CLI plus skill (`ctx7`).

## Who it's for

**Contributors to this repo, not prompt writing.** Context7 indexes software libraries. It knows
nothing about Higgsfield's models, so it adds nothing when Claude writes a prompt. Where it
helps is the repo's own tooling:

| Working on | Ask Context7 about |
|---|---|
| `scripts/generate_user_guide.py` | fpdf2 (the one third-party dependency) |
| `tests/` | pytest |
| `.github/workflows/` | GitHub Actions, `actions/checkout`, `actions/setup-python` |
| `scripts/*.py` in general | The Python standard library: the scripts must stay stdlib-only |

If you only use the skill to write prompts, you can skip it.

## Install

Guided setup (Node.js 22.13+; signs you in and creates a free API key):

```bash
npx ctx7 setup --claude
```

It offers CLI + skill mode or MCP mode. Undo with `npx ctx7 remove`.

Or add the MCP server by hand, with a key from context7.com/dashboard:

```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp \
  --header "Authorization: Bearer YOUR_API_KEY"
```

Then add "use context7" to a request, for example *"How do I add a table with a header row in
fpdf2? use context7"*.

### Don't put the always-on rule in this repo

Context7's README suggests a rule in `CLAUDE.md` so it's used without asking. Put that rule in
your **user** file, `~/.claude/CLAUDE.md`, not this repo's `CLAUDE.md`. The repo file is tracked,
loads for every contributor, and every line in it is context the agent reads each session.

## Rules

- **Never a source for Higgsfield facts.** Model ids, parameters, durations, prices and rules come
  from `specs/` (generated from Higgsfield's own catalog) and `preflight.py`. Even if Context7
  returns a page about Higgsfield's CLI or API, `specs/` wins; a mismatch means it's time for
  `/refresh-specs`, not for editing a doc by hand.
- **Keep the scripts stdlib-only.** Documentation for a handy third-party package is not a reason
  to add it: only the PDF generator may use one (`requirements.txt`).
- **Queries leave your machine.** What you ask is sent to Context7's service. Don't paste client
  briefs, unreleased product names or keys into a docs question.
- **The release gate still decides.** A fix written from current docs still has to pass
  `validate.py --strict`, `pytest` and `--evals`.

## It costs tokens

Every docs lookup adds pages to the context. Ask specific questions, and check what a session
cost with `npx ccusage@latest session` ([`ccusage.md`](ccusage.md)).

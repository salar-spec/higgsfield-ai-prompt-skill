# Tracking Claude Code costs with ccusage

[ccusage](https://github.com/ccusage/ccusage) is an MIT-licensed CLI that reads Claude Code's
local usage logs and reports tokens and estimated cost by day, week, month, session or project.
It can also show that usage live in Claude Code's status line. It reads files already on your
machine; nothing in this skill needs changing.

## Two costs, two tools

A Higgsfield production has two separate bills, and each has its own tracker:

| Cost | What it is | Tracked by |
|---|---|---|
| **Writing** | Claude tokens spent reading the skill and writing prompts | **ccusage** |
| **Rendering** | Higgsfield credits spent generating video and images | The skill's generation ledger: `python3 scripts/higgsfield_memory.py ratio <project> --credits` and `budget <project> --shots <manifest>` |

ccusage knows nothing about Higgsfield credits, and the ledger knows nothing about Claude
tokens. For the full cost of a shot or a campaign, add the two.

## Run it

No install needed (Node.js required):

```bash
npx ccusage@latest              # usage by day, every detected agent
npx ccusage@latest claude daily # Claude Code only
npx ccusage@latest session      # by conversation
npx ccusage@latest blocks       # Claude Code's 5-hour usage windows
```

Useful flags: `--since 2026-11-01 --until 2026-11-30`, `--last 1` (today / this week / this
month), `--breakdown` (per model), `--json`, and `--offline` (cached pricing, no network).

### Cost per project

Claude Code logs usage by the folder you ran it in. Run Higgsfield work from its own project
folder (where the skill's `workspace/` lives) and you can pull that project's writing cost on
its own:

```bash
npx ccusage@latest claude daily --instances                 # every project, side by side
npx ccusage@latest claude monthly --project <project-name>  # one project
```

Pair it with `ratio <project> --credits` from the ledger for the rendering side.

## Status line (optional)

To see the session's cost, today's total and the current 5-hour window while you work, add this
to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "npx -y ccusage statusline",
    "padding": 0
  }
}
```

Put it in your user settings, not this repo's `.claude/settings.json`, which is tracked and
shared. Claude Code runs one status line, so this replaces any you already have. The status line
uses cached pricing by default; add `--no-offline` to fetch current prices.

## Reading the numbers

- **Costs are estimates at API prices.** On a Pro or Max subscription you are not billed per
  token, so read the dollar figure as a measure of how heavy the work was, not as a bill.
- **The skill is mostly reading.** Each Higgsfield request makes Claude read root `SKILL.md`
  plus the sub-skill and reference files it routes to, so input and cache-read tokens dominate.
  Long sessions grow because the whole conversation is re-read every turn; starting a fresh
  session per shot list keeps them smaller.
- **Measuring Caveman.** Compare `session` reports for similar work with Caveman on and off to see
  what it actually saves. It only shortens the agent's chat, never the prompts
  ([`caveman.md`](caveman.md)).
- **Through OmniRoute.** Requests routed to non-Anthropic models may be priced wrongly or not at
  all, because ccusage prices by model name. Use OmniRoute's own dashboard for those
  ([`omniroute.md`](omniroute.md)).

## Privacy

ccusage reads the local logs under `~/.claude/` and prints reports on your machine. Pricing
lookups are the only network use; `--offline` turns them off.

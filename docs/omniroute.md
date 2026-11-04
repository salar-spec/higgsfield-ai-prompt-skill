# Running the skill through OmniRoute

[OmniRoute](https://github.com/cheaper-inference/OmniRoute) is an MIT-licensed, self-hosted AI
gateway. It puts many LLM providers behind one local endpoint, with quota-aware fallback between
them. This skill is plain Markdown plus standard-library Python, so it works unchanged when your
agent's LLM calls go through OmniRoute. Nothing in the skill has to be configured.

## What OmniRoute does and does not touch

| Traffic | Goes through OmniRoute? |
|---|---|
| The agent's own LLM calls (reading `SKILL.md`, writing prompts) | **Yes**, once the agent points at OmniRoute |
| Higgsfield generations (Higgsfield CLI, Higgsfield MCP, web UI) | **No**. They go to Higgsfield directly and bill your Higgsfield credits as before |
| `scripts/*.py` (validate, preflight, memory, lint) | **No**. They run locally and make no LLM calls |

OmniRoute changes which model *writes* the prompt. It does not change which Higgsfield model
*renders* it, or what that costs.

## 1. Install and start OmniRoute

```bash
npm install -g omniroute     # needs Node 22.22.2+ (Node 23 is not supported)
omniroute                    # dashboard + endpoint on http://localhost:20128
```

Or with Docker:

```bash
docker run -d --name omniroute --restart unless-stopped \
  -p 20128:20128 -v omniroute-data:/app/data \
  diegosouzapw/omniroute:latest
```

Open `http://localhost:20128`, connect your provider accounts, and copy your OmniRoute key from
**Dashboard → Endpoints**. `omniroute doctor` checks the install if anything fails.

## 2. Point your agent at it

### Claude Code

Install the skill as usual (README → Install → Claude Code), then start Claude Code with:

```bash
export ANTHROPIC_BASE_URL="http://localhost:20128"
export ANTHROPIC_AUTH_TOKEN="<your OmniRoute key>"
claude
```

Claude Code adds `/v1/messages` to the base URL itself, so give the root URL, not `…/v1`.
To make it permanent, put the two variables in the `env` block of `~/.claude/settings.json`
rather than in this repo's `.claude/settings.json`, which is tracked and shared.

### OpenAI-compatible clients (Codex CLI, Cursor, OpenCode, Cline, …)

Use base URL `http://localhost:20128/v1` and your OmniRoute key as the API key. Load the skill
the way that client loads instructions (point it at the root `SKILL.md`).

### OmniRoute as an MCP server (optional)

OmniRoute also serves MCP: `omniroute --mcp` (stdio) or `http://localhost:20128/api/mcp/stream`
(HTTP). This is separate from the Higgsfield MCP and does not replace it; keep the Higgsfield MCP
configured if you generate from the agent.

## 3. Pick the model with care

The skill's discipline (root `SKILL.md` § HARD RULES, `DISCIPLINE.md`) assumes a model that
reads long reference files and follows numbered rules closely. Routed to a small or free-tier
model, expect more rule misses: wrong parameter enums, skipped preflight, prompts over a model's
length limit. Two habits catch most of them:

- Run the free preflight before spending credits:
  `python3 scripts/preflight.py --model <id> [--param K=V …] --strict`
  (and `python3 scripts/seedance_lint.py` for Seedance prompts).
- Keep fallback chains inside one capability tier. A combo that falls back from a frontier model
  to a small one mid-session changes the writer halfway through a shot list.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Claude Code returns 404 on every request | `ANTHROPIC_BASE_URL` ends in `/v1`; drop it |
| 401 / authentication errors | Key missing or wrong: re-copy it from Dashboard → Endpoints |
| Skill not triggered | The skill is loaded by the agent, not the gateway: check the install path, not OmniRoute |
| Higgsfield calls fail | Not an OmniRoute issue: check the Higgsfield CLI/MCP login |

# Using Playwright MCP beside the skill

[Playwright MCP](https://github.com/microsoft/playwright-mcp) is Microsoft's Apache-2.0 MCP server
that lets Claude drive a real browser: open pages, read them as an accessibility tree, click,
type, upload files and take screenshots. It can open higgsfield.ai like you would.

That makes it the **last** way to reach Higgsfield, not the first. Generating, checking costs and
reading model parameters all have a proper route that is cheaper and more reliable:

| You want to | Use | Not Playwright, because |
|---|---|---|
| Generate from the agent | **Higgsfield CLI** (terminal) or **Higgsfield MCP** (claude.ai) | They take exact parameters and report cost; a browser clicks a UI that can change |
| Check a model's parameters | `specs/` + `python3 scripts/preflight.py` | Specs are generated from the platform's own catalog |
| Check a price | CLI `generate cost`, or `get_cost: true` on the MCP | Exact, and creates no job |

## When it does help

- **Reading a UI control the schema doesn't explain.** Some parameters are defined only by the
  web UI, for example the 26 `light_source` position codes noted in `image-models.md` ("read them
  off the UI control"). Claude can open the tool page and read the labels without generating.
- **UI-only features.** Presets and studio screens that the CLI and MCP don't expose: look at
  what the UI offers before writing a prompt for it.
- **Reviewing results in the browser.** Open your history to compare takes before you log them
  kept or rejected.

What the browser shows is an observation, not a spec. Don't edit `specs/` from it (that folder is
generated). Note a UI-only finding where the skill already tracks untested claims
(`docs/field-test-queue.md`) or in the sub-skill it belongs to, with the date you saw it.

## Install

In Claude Code:

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

Needs Node.js 18+. Other clients (Claude Desktop, VS Code, Cursor) are covered in its README.

## Rules for higgsfield.ai

Once you sign in to Higgsfield in that browser, the agent can do anything you can, including
spend credits. So:

1. **Confirm before anything that spends.** The agent asks you before clicking *Generate*,
   *Upscale*, *Extend* or anything else that starts a job, and states the model and settings
   first. Reading pages, opening menus and filling a prompt box don't need asking.
2. **Never touch billing.** No buying credits, changing plan, or entering payment details, even
   when asked to "top up so the job can run". Stop and tell the user.
3. **Same prompt, same checks.** A prompt typed into the browser is still a skill deliverable:
   the HARD RULES pre-delivery checklist and `preflight.py --strict` apply before it is typed,
   and it is pasted word for word.
4. **Log what you generate.** A generation fired from the browser goes into the ledger like any
   other: `higgsfield_memory.py log-gen <project> --model X --tags a,b --outcome kept`.
5. **Check Higgsfield's terms** before automating the site at any volume. Light, supervised use
   for reading and the occasional generation is different from batch automation.

## The browser keeps you signed in

By default Playwright MCP uses a **persistent profile**: cookies, including your Higgsfield
sign-in, are saved between sessions (one profile per project folder):

| OS | Profile location |
|---|---|
| macOS | `~/Library/Caches/ms-playwright/mcp-{channel}-{workspace-hash}` |
| Linux | `~/.cache/ms-playwright/mcp-{channel}-{workspace-hash}` |
| Windows | `%USERPROFILE%\AppData\Local\ms-playwright\mcp-{channel}-{workspace-hash}` |

That is convenient and also a standing logged-in session. Choices:

- **Read-only work:** add `--isolated` so nothing is saved, and don't sign in unless the page
  you need requires it.
- **Signed-in work:** keep the persistent profile, and delete that folder when you're done with
  the project.
- Never commit a profile folder or a `--storage-state` file to this repo: they hold your session.

## It costs tokens

Every page Claude reads arrives as an accessibility snapshot, which is large. A few page visits
can cost more than writing the prompt. Playwright's own README suggests its
[Playwright CLI](https://github.com/microsoft/playwright-cli) for coding agents for this reason.
Use `npx ccusage@latest session` to see what a browsing session cost ([`ccusage.md`](ccusage.md)).

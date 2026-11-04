# Using the skill in claude.ai

How to use the skill in the Claude app (claude.ai in a browser, or the desktop app) without
Claude Code. There are two ways in. Pick one, then optionally connect Higgsfield so Claude can
generate from the chat.

| | **A. Upload as a skill** (recommended) | **B. Project files** (fallback) |
|---|---|---|
| Plan | Pro, Max, Ultra, Team or Enterprise | Any plan with Projects |
| Loads | Automatically, in any chat, when you ask about Higgsfield | Only in chats inside that Project |
| Reference files | All of them, opened as needed | Only the ones you upload |
| Scripts (preflight, lint) | Can run in Claude's code sandbox | Cannot run |

## A. Upload as a skill (recommended)

### 1. Turn on code execution

Skills run in Claude's code sandbox. Go to **Settings > Capabilities** and turn on **Code
execution and file creation**. On Team and Enterprise, an Owner turns it on under
**Organization settings > Capabilities**.

### 2. Build the ZIP

claude.ai wants a ZIP whose top level is one folder named exactly like the skill's `name`,
here `higgsfield`, with `SKILL.md` inside it. On macOS or Linux:

```bash
git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill higgsfield
zip -r higgsfield.zip higgsfield -x 'higgsfield/.git/*'
unzip -l higgsfield.zip | head      # every entry must start with higgsfield/
```

On Windows, download the repo's ZIP from GitHub, unzip it, rename the folder to `higgsfield`,
then right-click that folder → **Compress**. Zip the folder itself, not the files inside it: a
`SKILL.md` at the top of the ZIP is not recognised as a skill.

The ZIP comes to about 3 MB.

### 3. Upload and turn it on

Go to **Customize > Skills**, upload `higgsfield.zip`, and make sure the skill is turned on.
claude.ai does not review uploaded skills, so it asks you to read them first. The skill is this
repo's Markdown, JSON and standard-library Python; the scripts it runs while writing prompts
(preflight, lint, memory) work on local files and make no network calls.

### 4. Check it works

In a new chat, ask: *"Give me a Kling prompt for a slow push-in on a rainy neon street."* Open
Claude's thinking or tool steps: you should see it read `SKILL.md`. To force it, type `/` and
pick **higgsfield**. If it never loads, check the skill is turned on and that code execution is
still on.

### Updating

Build a fresh ZIP from the latest repo and upload it again under **Customize > Skills**,
replacing the old one.

## B. Project files (fallback)

For a plan without skills, or if you'd rather keep it to one Project:

1. Create a Project and paste the whole of the root `SKILL.md` into its **instructions**.
2. Add as Project files the reference files you use most: `model-guide.md`, `vocab.md`,
   `prompt-examples.md`, `image-models.md`, and the `skills/higgsfield-*/SKILL.md` files for
   the models you work with (for example `skills/higgsfield-seedance-2-5/SKILL.md`).
3. Chat inside that Project.

Claude can read only what you uploaded. When it says it would open a file that isn't there,
upload that file too, or expect a less specific answer.

## C. Connect Higgsfield (optional, to generate from the chat)

With the Higgsfield connector, Claude sends the prompt to Higgsfield itself; no copying and
pasting into the website.

1. Go to **Customize > Connectors**. If Higgsfield is in the directory, add it from there.
   Otherwise add a custom connector with the URL `https://mcp.higgsfield.ai/mcp`.
2. Sign in to your Higgsfield account when asked.
3. In a chat, ask Claude to generate. Generations use your Higgsfield credits; see the
   coexistence rules in `skills/higgsfield-stack/SKILL.md` for how the connector and this skill
   share the work.

## What's different from Claude Code

| Feature | claude.ai | What to do instead |
|---|---|---|
| Free preflight (`scripts/preflight.py`) | Runs only with route A and code execution on | On route B, ask Claude to apply the HARD RULES checklist by hand, and check the model's settings in the Higgsfield UI before generating |
| Learning memory and generation ledger | Not kept: each chat's sandbox starts fresh | Note your filter triggers and kept/rejected takes yourself, or use Claude Code for production work you want logged |
| `workspace/` folders | None | Claude gives files as downloads |
| Higgsfield CLI | Not available | Use the connector (C) |
| Companion tools (OmniRoute, Superpowers, claude-mem, Caveman, Claude Security) | Claude Code only | claude.ai has its own memory and runs on Anthropic's models |

For long productions, Claude Code is still the better home: the memory, the ledger and the
preflight run every time. See [`claude-code-setup.md`](claude-code-setup.md).

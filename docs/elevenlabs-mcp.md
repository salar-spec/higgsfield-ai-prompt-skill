# Using the ElevenLabs MCP beside the skill

The [ElevenLabs MCP](https://github.com/elevenlabs/elevenlabs-mcp) is ElevenLabs' own MIT-licensed
MCP server. It gives Claude ElevenLabs' voice and audio tools: text to speech, sound effects,
music, voice design and cloning, speech to text, and isolating a voice from noise. It uses
**your ElevenLabs account and credits**, separate from Higgsfield's.

## Higgsfield first, ElevenLabs for the gaps

Higgsfield already covers a lot of audio, including ElevenLabs' own voice engine: its
`text2speech_v2` model has an `elevenlabs` variant (Eleven v3). See
`skills/higgsfield-audio/SKILL.md` for the full catalog. Pick by job:

| Job | Use | Why |
|---|---|---|
| Dialogue and lip-sync inside the shot | **Higgsfield**, native audio (Kling 3.0, Seedance, Veo) | Generated with the picture, so it's in sync |
| Voiceover you'll reuse in Higgsfield (voice change, lip-sync, reference voices) | **Higgsfield** `text2speech_v2` (variant `elevenlabs` for fine emotional control) or `qwen_audio_tts` | The voice stays a Higgsfield element; one account, one bill |
| Revoice a finished clip | **Higgsfield** `voice_change` | Keeps timing and re-merges the audio |
| **Sound effects** for a cut | **ElevenLabs** `text_to_sound_effects` | Higgsfield's MCP connector is speech-only and declines general SFX |
| **Music bed** for a cut | **ElevenLabs** `compose_music` (plan it first with `create_composition_plan`, which is free) | Same; one master track under the whole edit |
| Clean up a noisy voice recording | **ElevenLabs** `isolate_audio` | Higgsfield has no equivalent |
| Transcribe dialogue (subtitles, checking a lip-sync take) | **ElevenLabs** `speech_to_text` | Higgsfield has no equivalent |
| Design a brand-new voice from a description | **ElevenLabs** `text_to_voice`, then `create_voice_from_preview` | Larger voice-design tooling |

Then lay ElevenLabs audio under the picture with FFmpeg ([`ffmpeg.md`](ffmpeg.md) § Sound), and
cut to the music as `skills/higgsfield-audio/SKILL.md` § Cutting to music describes.

## Install

1. Get an API key at elevenlabs.io → Settings → API keys. There's a free tier with a monthly
   credit allowance.
2. Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
3. Add the server in Claude Code, pointing its file folder at your project's `workspace/`:

```bash
claude mcp add elevenlabs \
  -e ELEVENLABS_API_KEY=YOUR_KEY \
  -e ELEVENLABS_MCP_BASE_PATH="$PWD/workspace" \
  -- uvx elevenlabs-mcp
```

Run it from the project folder so `$PWD/workspace` is the skill's workspace.
`ELEVENLABS_MCP_BASE_PATH` is where generated audio is saved, and also the only folder the
server will read input files from, so keep recordings to clean or transcribe in
`workspace/input/`. Without it, files go to `~/Desktop`.

Claude Desktop setup is in the server's README. If you see `spawn uvx ENOENT`, give the full path
from `which uvx` as the command.

## Rules

- **Confirm before spending.** Generating, cloning and composing use ElevenLabs credits. The
  agent says what it's about to make and asks first; `check_subscription` shows what's left.
- **Consent for every cloned voice.** Only clone (`voice_clone`) or convert to (`speech_to_speech`)
  a voice whose owner has agreed, in writing, to that use. Never a real person's voice without it.
- **Not for calls or agents.** The server can also create phone agents and place outbound calls
  (`create_agent`, `make_outbound_call`). That's outside this skill: don't use them here.
- **Keep the originals.** Generated audio goes to `workspace/output/`; recordings you supply stay in
  `workspace/input/`. Mix into new files with FFmpeg; never overwrite a source.
- **Keep the key out of the repo.** `claude mcp add` stores it in your Claude Code config, not in
  this repo. Never paste it into a prompt, a doc or a commit.
- **Rights for music.** Check ElevenLabs' terms for commercial use of generated music and SFX on
  your plan before a client delivery.

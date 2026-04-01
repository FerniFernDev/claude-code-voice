---
name: voice-output
description: Use when the user asks for text-to-speech, voice output, spoken responses, "give Claude a voice", "read responses aloud", or wants to hear Claude Code responses through speakers. Also use when troubleshooting TTS or changing voice settings.
---

# Voice Output

This plugin gives Claude Code a voice. Every response is spoken aloud automatically via a Stop hook using Microsoft Edge neural TTS — free, no API key, natural-sounding.

## First-Time Setup

The plugin bundles the TTS scripts and Stop hook. The user just needs Python dependencies.

**Run this automatically when the skill is first invoked:**

```bash
pip install edge-tts pygame
```

Verify: `python -c "import edge_tts; import pygame; print('OK')"`

If `python` doesn't work, try `python3`.

**For fastest playback**, the user should also have `ffplay` (comes with ffmpeg):
- **Windows:** `winget install ffmpeg` or `choco install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

If ffplay isn't available, the script falls back to pygame automatically (slightly slower startup).

Then test:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_tts.py" "Voice output is active. You should hear this."
```

If the user hears audio, setup is complete. The Stop hook is already configured by the plugin.

## Changing Voice

Edit `VOICE` in `${CLAUDE_PLUGIN_ROOT}/scripts/claude_tts.py`.

List all voices: `edge-tts --list-voices`

| Voice | Gender | Style |
|-------|--------|-------|
| `en-US-AndrewNeural` | Male | Natural, conversational (default) |
| `en-US-GuyNeural` | Male | Clear, professional |
| `en-US-ChristopherNeural` | Male | Warm |
| `en-US-JennyNeural` | Female | Friendly |
| `en-US-AriaNeural` | Female | Versatile |
| `en-GB-RyanNeural` | Male | British |
| `en-GB-SoniaNeural` | Female | British |

## Tuning Speed and Volume

Edit `${CLAUDE_PLUGIN_ROOT}/scripts/claude_tts.py`:

- `RATE = "+17%"` — default. `"+25%"` for fast, `"+0%"` for standard, `"-10%"` for slow.
- `VOLUME = "+0%"` — default. `"+20%"` for louder.

## Troubleshooting

- **No sound:** Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_tts.py" "test"` manually
- **Slow startup:** Install ffmpeg for streaming playback (see setup above)
- **Linux audio issues:** `sudo apt install libsdl2-mixer-2.0-0`
- **macOS audio issues:** `brew install sdl2 sdl2_mixer` then reinstall pygame
- **Hook not firing:** Check the plugin is enabled in `/plugins` menu
- **Wrong Python:** The hook uses `python` — if your system needs `python3`, edit `hooks/hooks.json`

## Disabling

Disable the plugin in Claude Code's `/plugins` menu, or set `"disableAllHooks": true` in settings.json.

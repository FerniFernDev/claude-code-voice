# Claude Code Voice

Give Claude Code a voice. Every response is spoken aloud automatically using Microsoft Edge's neural text-to-speech — free, high-quality, no API key needed.

## What It Does

After each Claude Code response, a Stop hook extracts the text, strips markdown/code formatting, and speaks it through your speakers using edge-tts neural voices.

- Natural-sounding neural voices (same as Microsoft Edge browser)
- Streaming playback via ffplay — audio starts in ~1-2 seconds
- Falls back to pygame if ffplay isn't installed
- Zero cost, no API keys, no accounts
- Kills previous audio when a new response arrives (no overlap)
- Runs async so it doesn't block your next prompt
- Works on Windows, macOS, and Linux

## Requirements

- Python 3.10+
- `pip install edge-tts pygame`
- **Recommended:** ffmpeg installed for streaming playback (`winget install ffmpeg` / `brew install ffmpeg` / `apt install ffmpeg`)

## Installation

Add to your `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-code-voice": {
      "source": {
        "source": "github",
        "repo": "FerniFernDev/claude-code-voice"
      }
    }
  }
}
```

Then enable the plugin in Claude Code's `/plugins` menu.

## First Run

After enabling the plugin, say "set up voice output" or invoke `/voice-output` — Claude will install dependencies and test it automatically.

## Customization

Edit `scripts/claude_tts.py` in the plugin directory:

- **Voice:** Change `VOICE = "en-US-AndrewNeural"` (run `edge-tts --list-voices` for options)
- **Speed:** Change `RATE = "+17%"` (tested sweet spot — `"+25%"` for fast, `"+0%"` for slow)
- **Volume:** Change `VOLUME = "+0%"` (e.g. `"+20%"` for louder)

## How It Works

```
Claude responds → Stop hook fires → stdin JSON has last_assistant_message
→ Hook kills any previous TTS → Launches new TTS subprocess
→ Markdown/code/paths stripped → edge-tts streams audio into ffplay
→ Audio plays immediately while still generating
```

## License

MIT

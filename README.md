# Claude Code Voice

Give Claude Code a voice. Every response is spoken aloud automatically using Microsoft Edge's neural text-to-speech — free, high-quality, no API key needed.

## What It Does

After each Claude Code response, a Stop hook extracts the text, strips markdown/code formatting, and speaks it through your speakers using edge-tts neural voices.

- Natural-sounding neural voices (same as Microsoft Edge browser)
- Zero cost, no API keys, no accounts
- Automatic markdown/code cleanup so it only speaks readable text
- Runs async so it doesn't block your next prompt
- Works on Windows, macOS, and Linux

## Requirements

- Python 3.10+
- `pip install edge-tts pygame`

## Installation

### From GitHub

Add to your `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-code-voice": {
      "source": {
        "source": "github",
        "repo": "YOUR_USERNAME/claude-code-voice"
      }
    }
  }
}
```

Then enable the plugin in Claude Code's `/plugins` menu.

### Manual

1. Clone this repo
2. Add to your settings.json as a local directory marketplace:

```json
{
  "extraKnownMarketplaces": {
    "claude-code-voice": {
      "source": {
        "source": "directory",
        "path": "/path/to/claude-code-voice"
      }
    }
  }
}
```

## First Run

After enabling the plugin, just say "set up voice output" or invoke `/voice-output` — Claude will install dependencies and test it automatically.

## Customization

Edit `scripts/claude_tts.py`:

- **Voice:** Change `VOICE = "en-US-AndrewNeural"` (run `edge-tts --list-voices` for options)
- **Speed:** Change `RATE = "+17%"` (tested sweet spot — `"+25%"` for fast, `"+0%"` for slow)
- **Volume:** Change `VOLUME = "+0%"` (e.g. `"+20%"` for louder)

## License

MIT

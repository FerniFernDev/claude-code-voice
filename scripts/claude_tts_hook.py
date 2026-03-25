"""Claude Code Stop hook -> TTS. Kills previous TTS before starting new one."""
import sys
import json
import os
import signal
import subprocess
from pathlib import Path

TTS_SCRIPT = Path(__file__).parent / "claude_tts.py"
PID_FILE = Path(__file__).parent / ".tts_pid"


def kill_previous():
    """Kill any running TTS process so responses don't overlap."""
    if not PID_FILE.exists():
        return
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, signal.SIGTERM)
    except (ValueError, OSError, ProcessLookupError):
        pass
    finally:
        try:
            PID_FILE.unlink()
        except OSError:
            pass


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return
    text = data.get("last_assistant_message", "")
    if text and len(text.strip()) > 5:
        kill_previous()
        proc = subprocess.Popen([sys.executable, str(TTS_SCRIPT), text])
        PID_FILE.write_text(str(proc.pid))


if __name__ == "__main__":
    main()

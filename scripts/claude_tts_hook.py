"""Claude Code Stop hook -> TTS. Kills previous TTS before starting new one."""
import sys
import json
import os
import signal
import subprocess
import tempfile
import traceback
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TTS_SCRIPT = SCRIPT_DIR / "claude_tts.py"
PID_FILE = SCRIPT_DIR / ".tts_pid"
TEXT_FILE = SCRIPT_DIR / ".tts_text"
LOG_FILE = SCRIPT_DIR / ".tts_hook.log"


def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def kill_previous():
    """Kill any running TTS process tree so responses don't overlap."""
    if not PID_FILE.exists():
        return
    try:
        pid = int(PID_FILE.read_text().strip())
        # taskkill /T kills entire process tree (python + edge-tts + ffplay)
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except (ValueError, OSError):
        pass
    finally:
        try:
            PID_FILE.unlink()
        except OSError:
            pass


def main():
    try:
        raw = sys.stdin.read()
        log(f"Hook fired, stdin length: {len(raw)}")
        if not raw.strip():
            log("Empty stdin, exiting")
            return
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            log(f"JSON parse error: {e}")
            return
        text = data.get("last_assistant_message", "")
        log(f"Message length: {len(text)}")
        if text and len(text.strip()) > 5:
            kill_previous()
            TEXT_FILE.write_text(text, encoding="utf-8")
            proc = subprocess.Popen(
                [sys.executable, str(TTS_SCRIPT), "--file", str(TEXT_FILE)]
            )
            PID_FILE.write_text(str(proc.pid))
            log(f"Launched TTS pid={proc.pid}, text_len={len(text)}")
        else:
            log("Text too short, skipping")
    except Exception:
        log(traceback.format_exc())


if __name__ == "__main__":
    main()

"""
Claude Code TTS — edge-tts with streaming playback via ffplay.
Falls back to pygame if ffplay isn't available.
"""
import sys
import os
import re
import asyncio
import subprocess
import tempfile
import shutil

# Voice and speed config
VOICE = "en-US-AndrewNeural"  # Run: edge-tts --list-voices
RATE = "+17%"                 # "+25%" fast, "+0%" normal, "-10%" slow
VOLUME = "+0%"                # "+20%" louder


def clean_text(text):
    """Strip markdown, code blocks, file paths, and other non-speakable content."""
    text = re.sub(r'```[\s\S]*?```', ' code block omitted ', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[A-Za-z]:\\[\w\\/.~-]+', 'file path', text)
    text = re.sub(r'/[\w/.~-]{3,}', 'file path', text)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{2,}', '. ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


def find_ffplay():
    """Find ffplay executable."""
    return shutil.which("ffplay")


def speak_streaming(text):
    """Stream edge-tts output directly into ffplay. Fastest startup."""
    ffplay = find_ffplay()
    if not ffplay:
        return False

    tts_cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", VOICE,
        "--rate", RATE,
        "--volume", VOLUME,
        "--text", text,
        "--write-media", "-"
    ]
    player_cmd = [
        ffplay, "-nodisp", "-autoexit", "-loglevel", "quiet", "-i", "pipe:0"
    ]

    tts = subprocess.Popen(tts_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    player = subprocess.Popen(player_cmd, stdin=tts.stdout, stderr=subprocess.DEVNULL)
    tts.stdout.close()
    player.wait()
    tts.wait()
    return True


def speak_pygame(text):
    """Fallback: generate full MP3 then play with pygame."""
    import edge_tts
    import pygame

    async def _generate_and_play():
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME).save(tmp_path)
            pygame.mixer.init(frequency=24000)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.05)
            pygame.mixer.music.unload()
            pygame.mixer.quit()
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    asyncio.run(_generate_and_play())


def get_text():
    """Get text from --file path, CLI args, or stdin."""
    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        try:
            with open(sys.argv[2], "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, IOError):
            return ""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


if __name__ == "__main__":
    text = get_text()
    if not text:
        sys.exit(0)

    text = clean_text(text)
    if not text or len(text) < 2:
        sys.exit(0)

    if len(text) > 3000:
        text = text[:3000] + ". Message truncated for speech."

    # Try streaming first (fastest), fall back to pygame
    if not speak_streaming(text):
        speak_pygame(text)

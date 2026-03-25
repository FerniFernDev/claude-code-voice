"""
Claude Code TTS — edge-tts, single-pass audio, zero gaps.
Free Microsoft neural voices, no API key needed.
"""
import sys
import os
import re
import asyncio
import tempfile
import json

# Voice and speed config — edit these to customize
VOICE = "en-US-AndrewNeural"  # Run: edge-tts --list-voices
RATE = "+17%"                 # Speed: "+25%" fast, "+0%" normal, "-10%" slow
VOLUME = "+0%"                # Volume: "+20%" louder, "-20%" quieter


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


async def speak(text):
    """Generate full audio in one pass, then play. Zero inter-sentence gaps."""
    import edge_tts
    import pygame

    text = clean_text(text)
    if not text or len(text) < 2:
        return

    if len(text) > 3000:
        text = text[:3000] + ". Message truncated for speech."

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


def get_text():
    """Get text from CLI args or stdin."""
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


if __name__ == "__main__":
    text = get_text()
    if text:
        asyncio.run(speak(text))

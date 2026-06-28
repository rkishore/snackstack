"""
Voice I/O layer - play text-to-speech audio.

VoiceSpeaker - text -> TTS -> play audio
"""

from __future__ import annotations

import io
import os
import tempfile
import time
import uuid

import numpy as np
import sounddevice as sd
import soundfile as sf

from snackstack.config import openai_client
from snackstack.logger import get_logger

logger = get_logger(__name__)

VOICE_OPTIONS = {
    "alloy":   "Neutral, professional",
    "echo":    "Male, clear and steady",
    "fable":   "British accent, expressive",
    "onyx":    "Deep male, authoritative",
    "nova":    "Female, warm and friendly",
    "shimmer": "Female, soft and gentle",
}

class VoiceSpeaker:
    """Play text-to-speech audio."""
    
    def __init__(self, voice: str = "onyx", speed: float = 1.0):
        self.voice = voice
        self.speed = speed
        self._out_dir = tempfile.gettempdir()
    
    def synthesize(self, text: str, response_format: str = "wav") -> str:
        """Generate a WAV file and return its path. Each call gets 
        a unique filename so that previous responses are not overwritten."""
        out_path = os.path.join(self._out_dir, f"tts_{uuid.uuid4().hex[:8]}.{response_format}")
        try:
            with openai_client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=self.voice,
                input=text,
                speed=self.speed, 
                response_format=response_format
            ) as response:
                response.stream_to_file(out_path)
            logger.info("TTS saved → %s", out_path)
            return out_path
        except Exception as e:
            logger.error("TTS synthesis failed: %s", e)
            return ""
    
    def play(self, audio_file: str):
        """Play the synthesized speech through the default output device."""
        try:
            data, sr = sf.read(audio_file)
            sd.play(data, sr)
            sd.wait()
        except Exception as e:
            logger.error("Audio playback failed: %s", e)

    def speak(self, text: str, play: bool = True) -> str:
        """Synthesise *text* and optionally play it. Returns the file path."""
        logger.info("Agent says: %s", text[:120])
        path = self.synthesize(text)
        if play and path:
            self.play(path)
        return path
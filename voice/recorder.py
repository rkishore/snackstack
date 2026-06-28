"""
Voice I/O layer - record from the microphone and transcribe with Whisper.

VoiceRecoder - microphone -> WAV -> Whisper STT -> Text
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

# ═══════════════════════════════════════════════════════════
#  Speech-to-Text
# ═══════════════════════════════════════════════════════════

class VoiceRecorder:
    """Record from the microphone and transcribe with Whisper."""
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def record(self, duration: float = 5.0, countdown: bool = True) -> np.ndarray:
        """Record *duration* seconds of mono audio from the microphone."""
        if countdown:
            for i in range(3, 0, -1):
                logger.info(f"Recording in {i}...")
                time.sleep(1)
        
        logger.info("Recording for %f seconds. Speak now.", duration)
        audio_data = sd.rec(
            int(duration * self.sample_rate), 
            samplerate=self.sample_rate, 
            channels=1,
            dtype=np.float32
)
        sd.wait()
        logger.info("Recording complete.")
        return audio_data

    def transcribe(self, audio_data: np.ndarray, language: str = "en") -> str:
        """Send audio to Whisper and return the transcript."""
        buf = io.BytesIO()
        sf.write(buf, audio_data, self.sample_rate, format='WAV')
        buf.seek(0)
        buf.name = "recording.wav"

        try:
            result = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=buf,
                language=language
            )
            logger.info("Transcription result: %s", result.text)
            return result.text
        except Exception as e:
            logger.error("Error occurred while transcribing audio: %s", e)
            return ""
    
    def record_and_transcribe(self, duration: float = 5.0) -> tuple[str, str]:
        """Full pipeline: record -> send WAV -> transcribe.
        
        Returns (wav_path, transcript)
        """
        audio = self.record(duration)
        wav_path = os.path.join(tempfile.gettempdir(), f"rec_{uuid.uuid4().hex[:8]}.wav")
        sf.write(wav_path, audio, self.sample_rate)
        text = self.transcribe(audio)
        return wav_path, text
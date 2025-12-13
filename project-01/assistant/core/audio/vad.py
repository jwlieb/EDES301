# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Voice Activity Detection
--------------------------------------------------------------------------
License:   MIT License

Copyright 2025 - Jackson Lieb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
--------------------------------------------------------------------------

Voice Activity Detection (VAD) wrapper using webrtcvad. Detects speech in
audio chunks to enable hands-free conversation. Requires 10ms, 20ms, or
30ms frames at 8kHz or 16kHz sample rate with 16-bit PCM mono audio.

--------------------------------------------------------------------------
"""

import logging
import webrtcvad
import numpy as np
from typing import Literal

# Audio constants from recorder.py
SR = 16_000  # sample rate (Hz) - matches recorder
CHANNELS = 1  # mono
DTYPE = "int16"  # 16-bit PCM

# VAD frame sizes (in ms) - webrtcvad supports 10, 20, or 30ms
FRAME_MS = 30  # 30ms frames (good balance of latency and accuracy)
FRAME_SIZE = int(SR * FRAME_MS / 1000)  # samples per frame (480 samples for 30ms at 16kHz)


class VAD:
    """
    Voice Activity Detection wrapper around webrtcvad.
    
    Aggressiveness levels:
    - 0: Least aggressive (fewer false positives, may miss some speech)
    - 1: Moderate
    - 2: Most aggressive (more false positives, catches more speech)
    """

    def __init__(self, aggressiveness: Literal[0, 1, 2] = 2, sample_rate: int = SR):
        """
        Initialize VAD.
        
        Args:
            aggressiveness: VAD aggressiveness mode (0-2)
            sample_rate: Audio sample rate (must be 8000 or 16000)
        """
        if sample_rate not in (8000, 16000):
            raise ValueError(f"webrtcvad only supports 8kHz or 16kHz, got {sample_rate}")
        
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = sample_rate
        self.frame_size = int(sample_rate * FRAME_MS / 1000)
        self.log = logging.getLogger("vad")
        
    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """
        Check if an audio chunk contains speech.
        
        Args:
            audio_chunk: Audio data as numpy array (int16, mono)
                        Must be exactly FRAME_SIZE samples (e.g., 480 for 30ms at 16kHz)
        
        Returns:
            True if speech detected, False otherwise
        """
        if len(audio_chunk) != self.frame_size:
            raise ValueError(
                f"Audio chunk must be exactly {self.frame_size} samples "
                f"({FRAME_MS}ms at {self.sample_rate}Hz), got {len(audio_chunk)}"
            )
        
        # Convert to bytes (int16 = 2 bytes per sample)
        audio_bytes = audio_chunk.tobytes()
        
        try:
            return self.vad.is_speech(audio_bytes, self.sample_rate)
        except Exception as e:
            self.log.warning("VAD error: %s", e)
            return False
    


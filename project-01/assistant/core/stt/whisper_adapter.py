# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Whisper STT Adapter
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

Local speech-to-text adapter using faster-whisper. Transcribes WAV files
to text using OpenAI Whisper models. Supports multiple model sizes (tiny,
base, small, medium) with configurable VAD filtering.

--------------------------------------------------------------------------
"""

from faster_whisper import WhisperModel
from pathlib import Path
from typing import Union

def transcribe_file(path: Union[str, Path], model_size: str = "tiny") -> str:  # "tiny", "base", "small", "medium"
    """
    Transcribe a WAV file using faster-whisper. Returns text string.
    
    Note: This function is kept for backward compatibility.
    Consider using WhisperAdapter class for better integration.
    """
    import soundfile as sf
    # Disable VAD filter for short recordings (VAD filter removes too much)
    info = sf.info(str(path))
    duration = info.frames / float(info.samplerate) if info.samplerate else 0
    use_vad = duration > 1.0  # Only use VAD for recordings longer than 1 second
    
    model = WhisperModel(model_size, device="cpu", compute_type="int8")  # simple default
    segments, _info = model.transcribe(str(path), vad_filter=use_vad)
    chunks = []
    for seg in segments:
        if seg.text:
            chunks.append(seg.text.strip())
    return " ".join(chunks).strip()


class WhisperAdapter:
    """
    Local STT adapter using faster-whisper.
    
    Usage:
        adapter = WhisperAdapter(model_size="tiny")
        text = adapter.transcribe("audio.wav")
    """
    
    def __init__(self, model_size: str = "tiny"):  # "tiny", "base", "small", "medium"
        """
        Initialize Whisper adapter.
        
        Args:
            model_size: Whisper model size to use
        """
        self.model_size = model_size
    
    def transcribe(self, path: Union[str, Path]) -> str:
        """
        Transcribe audio file using local Whisper model.
        
        Args:
            path: Path to WAV file
        
        Returns:
            Transcribed text string
        """
        return transcribe_file(path, self.model_size)
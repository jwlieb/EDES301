# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Pyttsx3 Adapter Tests
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

Tests for Pyttsx3 TTS adapter. Verifies text-to-speech synthesis and
audio file generation.

--------------------------------------------------------------------------
"""

import os
import pytest
from assistant.core.tts.pyttsx3_adapter import Pyttsx3Adapter

# A safe minimum size check
MIN_AUDIO_BYTES = 4096 # A short WAV header plus minimal audio data will always be larger than this.

@pytest.fixture
def tts_adapter():
    """Provides a fresh Pyttsx3Adapter instance for testing."""
    return Pyttsx3Adapter()

def test_synth_creates_non_zero_duration_wav_file(tts_adapter):
    """
    Tests that synth() generates a file whose duration is greater than 0.0s 
    by checking its size is greater than a minimal byte count.
    """
    text = "Testing to ensure the file is not empty."
    
    # 1. Execute the synthesis
    path = tts_adapter.synth(text)
    
    # 2. ASSERTION: Check that the file was created
    assert os.path.exists(path), f"File was not created at expected path: {path}"
    
    # 3. ASSERTION: Explicitly check file size to confirm duration > 0.0s
    file_size = os.path.getsize(path)
    
    assert file_size > MIN_AUDIO_BYTES, \
        (f"File size is only {file_size} bytes. "
         f"This indicates a 0.0s duration file (empty content).")
    
    # Clean up the temporary file
    os.remove(path)
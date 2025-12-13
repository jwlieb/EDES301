# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Remote Adapter Tests
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

Tests for remote adapters (STT/TTS). Verifies HTTP communication with
remote servers for speech-to-text and text-to-speech services.

--------------------------------------------------------------------------
"""
import pytest
import tempfile
import os
import numpy as np
import soundfile as sf
from unittest.mock import AsyncMock, patch
import httpx

from assistant.core.stt.remote_stt_adapter import RemoteSTTAdapter
from assistant.core.tts.remote_tts_adapter import RemoteTTSAdapter

pytestmark = pytest.mark.asyncio


@pytest.fixture
def test_wav_file():
    """Create a minimal test WAV file."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
    
    # Create 0.5 seconds of silence at 16kHz
    sample_rate = 16000
    duration = 0.5
    samples = np.zeros(int(sample_rate * duration), dtype=np.float32)
    sf.write(wav_path, samples, sample_rate)
    
    yield wav_path
    
    if os.path.exists(wav_path):
        os.remove(wav_path)


async def test_remote_stt_adapter_success(test_wav_file):
    """Test RemoteSTTAdapter successfully transcribes audio."""
    server_url = "http://localhost:8000"
    
    # Mock successful HTTP response
    mock_response = httpx.Response(
        200,
        json={"text": "test transcription"},
        request=httpx.Request("POST", server_url)
    )
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        adapter = RemoteSTTAdapter(server_url=server_url, timeout=5.0)
        text = adapter.transcribe(test_wav_file)
        
        assert text == "test transcription"
        assert mock_post.called


async def test_remote_stt_adapter_network_error(test_wav_file):
    """Test RemoteSTTAdapter handles network errors gracefully."""
    server_url = "http://localhost:8000"
    
    adapter = RemoteSTTAdapter(server_url=server_url, timeout=0.1)
    
    # Should raise httpx.RequestError when server is unreachable
    with pytest.raises((httpx.RequestError, httpx.ConnectError)):
        adapter.transcribe(test_wav_file)


async def test_remote_tts_adapter_success():
    """Test RemoteTTSAdapter successfully synthesizes text."""
    server_url = "http://localhost:8000"
    
    # Create mock WAV content
    mock_wav_content = b"fake wav file content"
    
    # Mock successful HTTP response with binary WAV
    mock_response = httpx.Response(
        200,
        content=mock_wav_content,
        headers={"content-type": "audio/wav"},
        request=httpx.Request("POST", server_url)
    )
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        adapter = RemoteTTSAdapter(server_url=server_url, timeout=5.0)
        wav_path = adapter.synth("Hello world")
        
        assert os.path.exists(wav_path)
        assert wav_path.endswith(".wav")
        
        # Verify file contains mock content
        with open(wav_path, "rb") as f:
            assert f.read() == mock_wav_content
        
        # Cleanup
        os.remove(wav_path)
        assert mock_post.called


async def test_remote_tts_adapter_empty_text():
    """Test RemoteTTSAdapter rejects empty text."""
    server_url = "http://localhost:8000"
    adapter = RemoteTTSAdapter(server_url=server_url)
    
    with pytest.raises(ValueError, match="empty"):
        adapter.synth("")


async def test_remote_tts_adapter_network_error():
    """Test RemoteTTSAdapter handles network errors gracefully."""
    server_url = "http://localhost:8000"
    adapter = RemoteTTSAdapter(server_url=server_url, timeout=0.1)
    
    # Should raise httpx.RequestError when server is unreachable
    with pytest.raises((httpx.RequestError, httpx.ConnectError)):
        adapter.synth("Hello world")


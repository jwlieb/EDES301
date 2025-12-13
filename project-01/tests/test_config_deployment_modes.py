# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Deployment Mode Configuration Tests
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

Tests for deployment mode configuration. Verifies environment variable
handling and configuration defaults for different deployment modes.

--------------------------------------------------------------------------
"""
import pytest
from assistant.core.config import Config


@pytest.fixture(autouse=True)
def reset_env(monkeypatch):
    """Reset environment variables before each test."""
    # Clear test variables
    for key in ["DEPLOYMENT_MODE", "STT_MODE", "TTS_MODE", "STT_SERVER_URL", 
                "TTS_SERVER_URL", "SERVER_HOST", "SERVER_PORT"]:
        monkeypatch.delenv(key, raising=False)


def test_config_defaults():
    """Test that config has sensible defaults."""
    assert Config.DEPLOYMENT_MODE in ["full", "server", "client"]
    assert Config.STT_MODE in ["local", "remote"]
    assert Config.TTS_MODE in ["local", "remote"]
    assert Config.STT_SERVER_URL.startswith("http")
    assert Config.TTS_SERVER_URL.startswith("http")
    assert isinstance(Config.SERVER_PORT, int)
    assert Config.SERVER_PORT > 0


def test_config_get_stt_adapter_remote():
    """Test that get_stt_adapter returns remote adapter when STT_MODE=remote."""
    Config.STT_MODE = "remote"
    Config.STT_SERVER_URL = "http://localhost:8000"
    adapter = Config.get_stt_adapter()
    
    # Should be RemoteSTTAdapter
    from assistant.core.stt.remote_stt_adapter import RemoteSTTAdapter
    assert isinstance(adapter, RemoteSTTAdapter)
    assert adapter.server_url == "http://localhost:8000"


def test_config_get_tts_adapter_remote():
    """Test that get_tts_adapter returns remote adapter when TTS_MODE=remote."""
    Config.TTS_MODE = "remote"
    Config.TTS_SERVER_URL = "http://localhost:8000"
    adapter = Config.get_tts_adapter()
    
    # Should be RemoteTTSAdapter
    from assistant.core.tts.remote_tts_adapter import RemoteTTSAdapter
    assert isinstance(adapter, RemoteTTSAdapter)
    assert adapter.server_url == "http://localhost:8000"


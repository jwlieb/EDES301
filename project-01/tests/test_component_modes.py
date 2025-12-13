# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Component Mode Tests
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

Tests for component initialization in different deployment modes (full,
server, client). Verifies correct adapter selection and component setup.

--------------------------------------------------------------------------
"""
import pytest
import os
from assistant.core.bus import Bus
from assistant.core.config import Config
from assistant.app import (
    start_full_components,
    start_server_components,
    start_client_components,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def reset_config():
    """Reset config to defaults before each test."""
    original_mode = Config.DEPLOYMENT_MODE
    original_stt_mode = Config.STT_MODE
    original_tts_mode = Config.TTS_MODE
    
    yield
    
    # Restore original values
    Config.DEPLOYMENT_MODE = original_mode
    Config.STT_MODE = original_stt_mode
    Config.TTS_MODE = original_tts_mode


async def test_start_full_components():
    """Test that full mode components start correctly."""
    bus = Bus()
    
    # Set to full mode
    Config.DEPLOYMENT_MODE = "full"
    Config.STT_MODE = "local"
    Config.TTS_MODE = "local"
    
    # Should not raise
    await start_full_components(bus)
    
    # Verify components are subscribed
    assert len(bus._subs) > 0


@pytest.mark.skipif(
    not hasattr(Config, 'STT_MODEL_SIZE'),
    reason="Server dependencies not installed"
)
async def test_start_server_components():
    """Test that server mode components start correctly."""
    bus = Bus()
    
    # Set to server mode
    Config.DEPLOYMENT_MODE = "server"
    
    # Should not raise
    await start_server_components(bus)
    
    # Verify components are subscribed
    assert len(bus._subs) > 0


async def test_start_client_components():
    """Test that client mode components start correctly."""
    bus = Bus()
    
    # Set to client mode with remote adapters
    Config.DEPLOYMENT_MODE = "client"
    Config.STT_MODE = "remote"
    Config.TTS_MODE = "remote"
    Config.STT_SERVER_URL = "http://localhost:8000"
    Config.TTS_SERVER_URL = "http://localhost:8000"
    
    # Should not raise (even if server is not available)
    await start_client_components(bus)
    
    # Verify components are subscribed
    assert len(bus._subs) > 0




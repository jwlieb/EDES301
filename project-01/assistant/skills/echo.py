# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Echo Skill
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

Echo skill for Fish Assistant. Simple skill that echoes back what the user
said. Useful for testing the full pipeline and verifying speech recognition.

--------------------------------------------------------------------------
"""

import logging
from assistant.core.contracts import SkillRequest, SkillResponse, same_trace

logger = logging.getLogger("echo_skill")

class EchoSkill:
    def __init__(self, bus):
        self.bus = bus

    async def start(self):
        self.bus.subscribe("skill.request", self._on_request)

    async def _on_request(self, payload: dict):
        logger.info("EchoSkill: Received skill.request event")
        try:
            req = SkillRequest(**payload)
            logger.info("EchoSkill: Parsed request for skill: %s", req.skill)
        except Exception:
            logger.warning("EchoSkill: Malformed skill.request, skipping")
            return
        
        if req.skill != "echo":
            logger.debug("EchoSkill: Not for echo skill, ignoring")
            return
        
        original_text = req.payload.get("original_text", "").strip()
        if not original_text:
            logger.warning("EchoSkill: No original_text in payload")
            return
        
        logger.info("EchoSkill: Generating response for: '%s'", original_text)
        resp = SkillResponse(skill="echo", say=f"You said: {original_text}")
        same_trace(req, resp)
        logger.info("EchoSkill: Publishing skill.response: '%s'", resp.say)
        await self.bus.publish(resp.topic, resp.dict())
        logger.info("EchoSkill: Published skill.response successfully")
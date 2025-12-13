# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Intent Router
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

Intent router for Fish Assistant. Routes NLU intents to appropriate skills
and forwards skill responses to text-to-speech. Provides configurable intent
to skill mapping with identity mapping as default.

--------------------------------------------------------------------------
"""

import logging
from typing import Dict, Awaitable, Callable

from .bus import Bus
from .contracts import NLUIntent, SkillRequest, SkillResponse, TTSRequest, same_trace

Handler = Callable[[Dict], Awaitable[None]]

class Router:
    """
    Tiny router:
      - Listens for NLUIntent and forwards as SkillRequest (intent name == skill name).
      - If a skill returns a simple 'say', forward it to TTSRequest.
    """

    def __init__(self, bus: Bus):
        self.bus = bus
        # Keep policy empty and identity by default; add overrides only when needed.
        self.intent_to_skill: Dict[str, str] = {}

        self.bus.subscribe("nlu.intent", self._on_nlu_intent)
        self.bus.subscribe("skill.response", self._on_skill_response)

    def _resolve_skill(self, intent: str) -> str:
        # Identity by default; override via self.intent_to_skill[...] when necessary.
        return self.intent_to_skill.get(intent, intent)

    async def _on_nlu_intent(self, payload: Dict) -> None:
        # Parse to regain type safety; drop silently if malformed (simple behavior).
        try:
            e = NLUIntent(**payload)
        except Exception:
            return

        skill = self._resolve_skill(e.intent)
        if not skill:
            return

        req = SkillRequest(
            skill=skill,
            payload={"entities": e.entities, "original_text": e.original_text, "confidence": e.confidence},
        )
        same_trace(e, req)
        logging.info("Router: Routing intent '%s' to skill '%s'", e.intent, skill)
        await self.bus.publish(req.topic, req.dict())
        logging.info("Router: Published skill.request event")

    async def _on_skill_response(self, payload: Dict) -> None:
        try:
            e = SkillResponse(**payload)
        except Exception:
            return

        if not e.say:
            logging.debug("Router: Skill response has no 'say' field, skipping TTS")
            return

        logging.info("Router: Forwarding skill response to TTS: '%s'", e.say[:50])
        tts = TTSRequest(text=e.say)
        same_trace(e, tts)
        await self.bus.publish(tts.topic, tts.dict())
        logging.info("Router: Published tts.request event")

    # Optional: override routes in tests or future plugins
    def register_intent(self, intent: str, skill: str) -> None:
        self.intent_to_skill[intent] = skill

# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Event Bus
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

Simple async pub/sub event bus for Fish Assistant. Provides asynchronous
event publishing and subscription mechanism for decoupled component
communication. Components subscribe to topics and receive events when
published.

--------------------------------------------------------------------------
"""

from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List
import asyncio
import logging

Subscriber = Callable[[Dict[str, Any]], Awaitable[None]]

class Bus:
    def __init__(self):
        self._subs: Dict[str, List[Subscriber]] = defaultdict(list)
        self._log = logging.getLogger("bus")
    
    def subscribe(self, topic: str, fn: callable):
        self._subs[topic].append(fn)
        subscriber_name = getattr(fn, "__name__", str(fn))
        self._log.info("subscribe: %s -> %s (total subscribers: %d)", topic, subscriber_name, len(self._subs[topic]))

    async def publish(self, topic, payload):
        subscribers = self._subs.get(topic, [])
        self._log.info("publish: %s -> %d subscribers %s", topic, len(subscribers), list(payload.keys()) if isinstance(payload, dict) else type(payload).__name__)
        if not subscribers:
            self._log.warning("publish: No subscribers for topic %s", topic)
        tasks = []
        for fn in subscribers:
            try:
                self._log.debug("publish: Scheduling subscriber %s for topic %s", getattr(fn, "__name__", str(fn)), topic)
                tasks.append(asyncio.create_task(fn(payload)))
            except Exception as e:
                self._log.exception("error scheduling subscriber for %s: %s", topic, e)
                
        # Wait briefly for all direct subscribers to START their work
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self._log.error("publish: Subscriber %d raised exception: %s", i, result, exc_info=result) 

    def clear(self):
        self._subs.clear()
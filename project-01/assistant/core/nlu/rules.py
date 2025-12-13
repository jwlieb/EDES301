# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Rules-Based NLU Classifier
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

Rules-based natural language understanding classifier using regex patterns.
Classifies user input into intents such as time, timer, weather, joke, music,
and smalltalk. Extracts entities like duration from timer requests.

--------------------------------------------------------------------------
"""

import re
from typing import Optional
from .types import NLUResult

_TIME = re.compile(r"\b(time|what(?:'s| is) the time|time in)\b", re.I)
_TIMER = re.compile(r"\b(set|start).*\b(timer|alarm)\b|\b(timer|alarm).*\bfor\b|\bin\s+\d+\s*(s|sec|second|min|m|h)\b", re.I)
_WEATHER = re.compile(r"\b(weather|temperature|forecast)\b", re.I)
_JOKE = re.compile(r"\b(joke|funny|make me laugh)\b", re.I)
_MUSIC = re.compile(r"\b(play|music|song|songs|playlist)\b", re.I)
_HELLO = re.compile(r"\b(hi|hello|hey|thanks|bye)\b", re.I)

def _duration_sec(text: str) -> Optional[int]:
    # trivial parser; expand later
    import re
    s = 0
    for n,u in re.findall(r"(\d+)\s*(h|hr|hour|m|min|minute|s|sec|second)s?\b", text.lower()):
        n = int(n)
        s += n*3600 if u.startswith("h") else n*60 if u.startswith(("m","min")) else n
    return s or None

class RulesNLU:
    async def classify(self, text: str) -> NLUResult:
        t = text.strip()
        ent: dict = {}
        if _JOKE.search(t):
            return NLUResult("joke", ent, 0.9, t)
        if _TIMER.search(t):
            dur = _duration_sec(t)
            if dur: ent["duration"] = {"seconds": dur}
            return NLUResult("timer", ent, 0.85 if dur else 0.6, t)
        if _TIME.search(t):    return NLUResult("time", ent, 0.8, t)
        if _WEATHER.search(t): return NLUResult("weather", ent, 0.8, t)
        if _MUSIC.search(t):   return NLUResult("music", ent, 0.7, t)
        if _HELLO.search(t):   return NLUResult("smalltalk", ent, 0.5, t)
        return NLUResult("unknown", ent, 0.1, t)
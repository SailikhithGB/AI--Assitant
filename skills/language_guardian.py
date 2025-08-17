# Real-Time Language Guardian – SAFE: no always-on mic; user pastes text or enables consent.
# For live mode, pair with whisper.cpp and pass text chunks here.

import re

EXPLAIN = {
    "en->hi": "Use polite particles (जी) in formal Hindi; avoid overly literal idioms.",
    "hi->en": "Keep directness but soften imperatives for politeness in English.",
}

class LanguageGuardian:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str, consent: bool = True) -> str:
        if not consent:
            return "Live translation requires explicit consent."
        m = re.match(r"translate live (\w+)->(\w+): (.*)", text, flags=re.I|re.S)
        if m:
            src, dst, payload = m.group(1).lower(), m.group(2).lower(), m.group(3).strip()
            tip = EXPLAIN.get(f"{src}->{dst}", "Mind register, idioms, and cultural politeness.")
            return f"Translation ({src}->{dst}): {payload}\nCultural tip: {tip}"
        return "Say: 'translate live en->hi: <text>' (or hi->en)."

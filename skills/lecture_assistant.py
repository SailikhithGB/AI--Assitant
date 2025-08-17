# Lecture Assistant – local transcript -> summary (no paid APIs)
# You can pair with whisper.cpp externally and drop transcript text here.

import re, textwrap
from config import REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING

class LectureAssistant:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str, consent: bool = True) -> str:
        if not consent:
            return "Recording/transcription requires explicit consent."
        if text.lower().startswith("summarize lecture:"):
            transcript = text.split(":",1)[1].strip()
            if not transcript:
                return "Paste transcript after 'summarize lecture:'."
            bullets = self._summarize(transcript)
            return "Key points:\n" + "\n".join([f"- {b}" for b in bullets])
        return "Say: 'summarize lecture: <transcript text>'."

    def _summarize(self, s: str):
        s = re.sub(r"\s+", " ", s).strip()
        # naive split into sentences and pick top lines by length/keywords
        sents = [x.strip() for x in re.split(r"[.!?]", s) if x.strip()]
        key = [z for z in sents if any(k in z.lower() for k in ["definition", "example", "conclusion", "therefore", "key"])]
        return (key[:5] or sents[:5])

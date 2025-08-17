# nova_v2/skills/predictive_control.py
import collections, re

class Predictor:
    def __init__(self, twin):
        self.twin = twin
        self.freq = collections.Counter()

    def suggest(self, text: str) -> str | None:
        words = re.findall(r"[a-z]{3,}", text.lower())
        for w in words: self.freq[w] += 1
        if not self.freq: return None
        top, _ = self.freq.most_common(1)[0]
        mapping = {
            "open": "open chrome",
            "youtube": "open youtube",
            "screenshot": "take a screenshot",
            "mute": "mute volume",
        }
        return mapping.get(top)

# Adaptive Voice Cloning – SAFE VERSION
# - Local TTS style presets (no real-person impersonation)
# - Blocks requests to imitate real named individuals

import re

PRESETS = {
    "neutral": {"rate": 180, "pitch": 0},
    "warm": {"rate": 170, "pitch": +1},
    "bright": {"rate": 200, "pitch": +2},
    "calm": {"rate": 160, "pitch": -1},
    "robotic": {"rate": 190, "pitch": 0},
}

BANNED_NAMES = ["morgan freeman", "darth vader", "barack obama", "taylor swift"]  # illustrative

class VoiceClone:
    def __init__(self, block_impersonation: bool = True):
        self.block_impersonation = block_impersonation

    def route(self, text: str, require_style_consent: bool = True) -> str:
        t = text.lower()
        if any(n in t for n in BANNED_NAMES) and self.block_impersonation:
            return "I can’t imitate real people. I can switch to safe styles like 'warm', 'calm', or 'robotic'."
        m = re.search(r"(speak|voice).*like (\w+)", t)
        style = m.group(2) if m else None
        style = style if style in PRESETS else "neutral"
        if require_style_consent:
            return f"Consent needed to adapt to your style. If approved, I’ll use the '{style}' preset (local TTS)."
        return f"Using '{style}' voice preset. (Adjust rate/pitch in PRESETS for more flavor.)"

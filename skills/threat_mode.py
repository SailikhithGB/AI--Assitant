# Threat Anticipation Mode – local heuristics + simple ML hooks.
# Includes phishing heuristics, suspicious sound keywords, and auto-defenses with consent.

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class ThreatReport:
    findings: List[str] = field(default_factory=list)

    def add(self, msg: str): self.findings.append(f"- {msg}")
    def render(self) -> str: return "Threat Scan:\n" + ("\n".join(self.findings) if self.findings else "No issues found.")

PHISH_PATTERNS = [
    r"urgent action required",
    r"verify your account",
    r"password expires",
    r"unusual login attempt",
    r"wire transfer",
]

class ThreatMode:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str) -> str:
        t = text.lower()
        rep = ThreatReport()
        if "phishing" in t or "scan email" in t:
            rep.add("Email scan: look for mismatched domains, shortened links, and spelling errors.")
            rep.add(f"Heuristics: {', '.join([p.replace('r\"','').replace('\"','') for p in PHISH_PATTERNS])}.")
        if "suspicious" in t or "background noises" in t:
            rep.add("Audio vigilance: footsteps/lock clicks trigger alert; suggest turning on camera (with consent).")
        if "enable defenses" in t or "defense" in t:
            rep.add("Auto-defense ready: start camera recording, notify trusted contact, lock screen (with consent).")
        if not rep.findings:
            rep.add("Say 'scan email for phishing' or 'enable defenses'.")
        return rep.render()

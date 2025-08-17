# Digital Twin – minimal memory (local)
import json
from pathlib import Path
from config import DATA_DIR

MEM = DATA_DIR / "twin.json"

class DigitalTwin:
    def __init__(self):
        self.mem = []
        self.graph = {}   # concept map
        self.skills = {}  # skill xp

    def remember_chat(self, who: str, text: str):
        self.mem.append({"who": who, "text": text})
        if len(self.mem) > 1000:
            self.mem = self.mem[-1000:]
        self._save()

    def _save(self):
        try:
            MEM.write_text(json.dumps({"mem": self.mem}, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

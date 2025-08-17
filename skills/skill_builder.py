# Skill Builder – track skills, suggest micro-tasks (local only)

import re
from collections import defaultdict

SUGGESTIONS = {
    "python": ["Build a CLI timer", "Parse a CSV and plot results", "Write unit tests for a small module"],
    "math": ["Prove a simple identity", "Solve 5 derivative problems", "Implement Newton’s method"],
    "english": ["Summarize a news article", "Write a 200-word opinion", "Learn 10 new words"],
}

class SkillBuilder:
    def __init__(self, twin):
        self.twin = twin
        if not hasattr(self.twin, "skills"):
            self.twin.skills = defaultdict(int)  # skill -> xp

    def route(self, text: str) -> str:
        t = text.lower()
        m = re.search(r"learning path (.+)", t)
        if m:
            topic = m.group(1).strip().lower()
            ideas = SUGGESTIONS.get(topic, ["Find a free intro playlist on YouTube Edu", "Practice 20 minutes daily"])
            return "Try:\n- " + "\n- ".join(ideas)
        m = re.search(r"log progress (.+)\s+(\d+)", t)
        if m:
            topic, xp = m.group(1).strip().lower(), int(m.group(2))
            self.twin.skills[topic] += xp
            return f"Logged {xp} XP to {topic}. Total: {self.twin.skills[topic]}."
        if "skill tracker" in t:
            if not self.twin.skills: return "No skills tracked yet."
            lines = [f"- {k}: {v} XP" for k,v in self.twin.skills.items()]
            return "Skills:\n" + "\n".join(lines)
        return "Say: 'learning path <topic>' or 'log progress <topic> <xp>' or 'skill tracker'."

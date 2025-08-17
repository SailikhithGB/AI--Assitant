# nova_v2/skills/hyper_context.py
# Lightweight keyword awareness (explicit opt-in).
KEYWORDS = {
    "movie": "I can check BookMyShow showtimes near you.",
    "hungry": "Want me to order your usual from Swiggy or Zomato?",
    "tired": "Shall I enable Focus mode and dim your lights?",
}

class HyperContext:
    def __init__(self, assistant):
        self.assistant = assistant

    def react_to_text(self, text: str) -> str | None:
        t = text.lower()
        for k, v in KEYWORDS.items():
            if k in t:
                return v
        return None

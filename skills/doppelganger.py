# Digital Doppelgänger – SAFE agent
# - Never pretends to be you without disclosure
# - Drafts emails/messages in your style IF you’ve given samples + consent

from dataclasses import dataclass

@dataclass
class PersonaPolicy:
    observe_only: bool = True
    assist: bool = False
    act_with_confirmation: bool = False

class Doppelganger:
    def __init__(self, twin):
        self.twin = twin
        self.policy = PersonaPolicy()

    def route(self, text: str) -> str:
        t = text.lower()
        if "observe" in t:
            self.policy = PersonaPolicy(observe_only=True)
            return "Digital twin set to Observe-only."
        if "assist" in t:
            self.policy = PersonaPolicy(observe_only=False, assist=True)
            return "Digital twin set to Assist (drafts and suggestions)."
        if "act" in t or "full control" in t:
            self.policy = PersonaPolicy(observe_only=False, assist=True, act_with_confirmation=True)
            return "Digital twin set to Act with confirmation."
        if "draft email" in t:
            return "Drafted email in your tone (based on your prior samples). I’ll show it for your approval."
        return "Say: 'digital twin observe/assist/act with confirmation' or 'draft email to <name>'."

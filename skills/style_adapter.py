# nova_v2/skills/style_adapter.py
# Human-like writing style (safe): tone/cadence—no illegal impersonation.
class StyleAdapter:
    def __init__(self, twin):
        self.twin = twin

    def mirror(self, text: str, audience="you", tone="friendly") -> str:
        if tone == "friendly":
            return text
        if tone == "brief":
            return text.split("\n")[0]
        if tone == "enthusiastic":
            return f"{text}\n\n(🚀 Let’s go!)"
        if tone == "formal":
            return "Dear user,\n" + text
        return text

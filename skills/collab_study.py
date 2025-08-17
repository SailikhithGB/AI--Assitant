# Collaborative Study – offline planning + prompts to use free chat platforms

class CollabStudy:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str) -> str:
        if "study group" in text.lower():
            return ("Creating a study plan:\n"
                    "- Define weekly topic + quiz\n"
                    "- Rotate presenters\n"
                    "- Use free Discord/Matrix for voice rooms\n"
                    "I can draft invites and agendas. Say: 'draft study agenda on <topic>'.")
        if text.lower().startswith("draft study agenda on"):
            topic = text.split("on",1)[1].strip()
            return (f"Agenda for {topic}:\n"
                    "- 10m recap\n- 25m main explainer\n- 15m Q&A\n- 10m quiz\n- 5m next steps")
        return "Say: 'study group' or 'draft study agenda on <topic>'."

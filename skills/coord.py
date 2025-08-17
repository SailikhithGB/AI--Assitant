# Real-World Coordination – “calls” and “messages” through desktop automations only
# No direct telephony billing; all actions require explicit confirmation.

import re

class RealWorldCoordinator:
    def __init__(self, require_confirm: bool = True):
        self.require_confirm = require_confirm

    def route(self, text: str, require_confirm: bool = True) -> str:
        t = text.lower()
        if "book table" in t:
            return "Booking flow (manual/desktop automation). I’ll draft a call script or message for confirmation."
        if "order food" in t:
            return "Drafted: 'Hi, I’d like to order the usual. Delivery to saved address.' Confirm to send via WhatsApp Web."
        if "remind" in t:
            return "Reminder set locally. I’ll ping you on desktop notification at the time."
        if "call" in t:
            return "I can open your softphone/WhatsApp Web with a call-ready screen. Confirm to proceed."
        return "Say 'book table', 'order food', 'call <contact>', or 'remind me at <time>'."

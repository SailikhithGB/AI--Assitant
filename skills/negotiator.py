# Autonomous Online Negotiator (free, ToS-safe baseline)
# - Uses heuristic advice + user-confirmed actions.
# - If ALLOW_HEADLESS_BROWSER_AUTOMATION is False, we DO NOT automate checkout.
# - Never auto-purchases without explicit confirmation.

import re
from dataclasses import dataclass
from typing import Optional

from config import ALLOW_HEADLESS_BROWSER_AUTOMATION, REQUIRE_CONFIRMATION_FOR_PAYMENTS

@dataclass
class DealHint:
    site: str
    item: str
    strat: str
    expected_save_pct: int

TEMPLATES = [
    DealHint("eBay", "{item}", "Send respectful offer at 70–85% of ask; search sold listings for fair price.", 15),
    DealHint("Amazon", "{item}", "Use keepa-like price history (free trackers) and wait for dip alerts.", 8),
    DealHint("Local Marketplace", "{item}", "Bundle multiple items for a single offer; propose pickup today.", 20),
]

class Negotiator:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str, require_confirm: bool = True) -> str:
        t = text.lower()
        item = self._extract_item(t)
        if not item:
            return "Say: 'negotiate price for <item>' or 'find a better deal on <item>'."

        hints = [f"- {d.site}: {d.strat}" for d in TEMPLATES]
        advise = "Here’s a free, safe negotiation plan:\n" + "\n".join(hints)
        if require_confirm or REQUIRE_CONFIRMATION_FOR_PAYMENTS or not ALLOW_HEADLESS_BROWSER_AUTOMATION:
            return advise + "\n\nI can draft messages/offers for you. Say: 'draft offer for <site>' to proceed."
        # If you enable headless automation by choice:
        return advise + "\n\nHeadless automation enabled (risky, ToS-sensitive). I will still ask before submitting any purchase."

    def _extract_item(self, t: str) -> Optional[str]:
        m = re.search(r"negotiate .* for (.+)$", t) or re.search(r"deal on (.+)$", t)
        return m.group(1).strip() if m else None

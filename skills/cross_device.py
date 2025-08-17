# Cross-device control via Home Assistant stubs.

import requests
from config import HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN

class CrossDevice:
    def route(self, text: str, require_confirm: bool=True) -> str:
        t = text.lower()
        if "lights" in t and "off" in t:
            if not HOME_ASSISTANT_URL or not HOME_ASSISTANT_TOKEN:
                return "Home Assistant not configured in config.py."
            ok = self._ha_service("light.turn_off", {"entity_id": "light.living_room"})
            return "Turning lights off." if ok else "Failed to control lights."
        if "netflix" in t:
            return "Opening Netflix on TV (stub). Integrate with your TV remote API to make it real."
        return None

    def _ha_service(self, service, payload):
        try:
            url = f"{HOME_ASSISTANT_URL}/api/services/{service}"
            headers = {"Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}", "Content-Type": "application/json"}
            # Stub: not actually posting; return True to simulate success.
            return True
        except Exception:
            return False

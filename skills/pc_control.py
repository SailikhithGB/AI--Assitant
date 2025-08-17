# pc_control.py – basic desktop helpers (open apps/urls etc.)
import webbrowser

class PCControl:
    def route(self, text: str) -> str | None:
        t = text.lower()
        if t.startswith("open "):
            target = t.replace("open ", "").strip()
            if target in ["youtube", "gmail", "maps", "github", "news", "netflix"]:
                urls = {
                    "youtube": "https://youtube.com",
                    "gmail": "https://mail.google.com",
                    "maps": "https://maps.google.com",
                    "github": "https://github.com",
                    "news": "https://news.google.com",
                    "netflix": "https://netflix.com",
                }
                webbrowser.open(urls[target])
                return f"Opening {target}."
            if target.startswith("http"):
                webbrowser.open(target)
                return f"Opening {target}."
        if "screenshot" in t:
            return "Screenshot stub (use pyautogui if allowed)."
        if "mute" in t:
            return "Muting audio stub (platform-specific)."
        return None

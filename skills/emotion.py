# nova_v2/skills/emotion.py
# Optional webcam emotion detection (toggle in config.py)
from fer import FER
import cv2

class EmotionWatcher:
    def __init__(self, twin):
        self.twin = twin

    def detect_once(self) -> str | None:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened(): return None
        ok, frame = cap.read()
        cap.release()
        if not ok: return None
        emo = FER()
        top = emo.top_emotion(frame)
        if not top: return None
        label, score = top
        self.twin.set_pref("last_emotion", label)
        return label

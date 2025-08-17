# Reality Overlay (AR Integration) – local camera CV only.
# This is a stub that describes what it WOULD do using OpenCV/AR.js without paid services.

class AROverlay:
    def route(self, text: str, consent: bool = True) -> str:
        if not consent:
            return "AR overlay requires explicit consent for camera access."
        if "recognize" in text.lower():
            return "Object recognition (local): use OpenCV + pre-trained ONNX models. TODO: implement labels overlay."
        if "who is this" in text.lower():
            return "Person identification is disabled for privacy. I can describe attributes (e.g., clothing color)."
        return "Say: 'AR overlay recognize this object' while camera is on (local-only)."

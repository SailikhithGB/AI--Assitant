# nova_v2/assistant.py
import re
import pyttsx3
from core.knowledge import get_answer

from config import (
    ASSISTANT_NAME,
    ENABLE_HYPER_CONTEXT,
    ENABLE_PREDICTIVE,
    ENABLE_EMOTION,
    ENABLE_DARK_WEB_WATCH,
    ENABLE_CROSS_DEVICE,
    ENABLE_NEGOTIATOR,
    ENABLE_AR_OVERLAY,
    ENABLE_THREAT_MODE,
    ENABLE_VOICE_CLONE,
    ENABLE_DOPPELGANGER,
    ENABLE_REALWORLD_COORD,
    ENABLE_STUDY_COMPANION,
    ENABLE_LECTURE_ASSISTANT,
    ENABLE_KNOWLEDGE_GRAPH,
    ENABLE_EXAM_PREP,
    ENABLE_SKILL_BUILDER,
    ENABLE_COLLAB_STUDY,
    ENABLE_LANGUAGE_GUARDIAN,
    ENABLE_DEEP_RESEARCH,
    ENABLE_LIFE_AUTOPILOT,
    REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS,
    REQUIRE_CONFIRMATION_FOR_PAYMENTS,
    REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING,
    REQUIRE_EXPLICIT_CONSENT_FOR_STYLE_ADAPT,
    BLOCK_REAL_PERSON_IMPERSONATION,
)

from skills.digital_twin import DigitalTwin
from skills.pc_control import PCControl
from skills.predictive_control import Predictor
from skills.hyper_context import HyperContext
from skills.emotion import EmotionWatcher
from skills.dark_web_watch import DarkWebWatch
from skills.cross_device import CrossDevice

# NEW skills
from skills.negotiator import Negotiator
from skills.ar_overlay import AROverlay
from skills.threat_mode import ThreatMode
from skills.voice_clone import VoiceClone
from skills.doppelganger import Doppelganger
from skills.coord import RealWorldCoordinator

# Study/Learning suite
from skills.study_companion import StudyCompanion
from skills.lecture_assistant import LectureAssistant
from skills.knowledge_graph import KnowledgeGraph
from skills.exam_prep import ExamPrep
from skills.skill_builder import SkillBuilder
from skills.collab_study import CollabStudy
from skills.language_guardian import LanguageGuardian
from skills.deep_research import DeepResearch
from skills.life_autopilot import LifeAutopilot


class Assistant:
    def __init__(self, name: str = ASSISTANT_NAME):
        self.name = name
        self.engine = pyttsx3.init()
        # memory / twin
        self.twin = DigitalTwin()

        # core skills
        self.pc = PCControl()
        self.predictor = Predictor(self.twin) if ENABLE_PREDICTIVE else None
        self.context = HyperContext(self) if ENABLE_HYPER_CONTEXT else None
        self.emotion = EmotionWatcher(self.twin) if ENABLE_EMOTION else None
        self.dark = DarkWebWatch() if ENABLE_DARK_WEB_WATCH else None
        self.cross = CrossDevice() if ENABLE_CROSS_DEVICE else None

        # new skills
        self.negotiator = Negotiator(self.twin) if ENABLE_NEGOTIATOR else None
        self.ar = AROverlay() if ENABLE_AR_OVERLAY else None
        self.threat = ThreatMode(self.twin) if ENABLE_THREAT_MODE else None
        self.voice = VoiceClone(
            block_impersonation=BLOCK_REAL_PERSON_IMPERSONATION
        ) if ENABLE_VOICE_CLONE else None

        self.twin_agent = Doppelganger(self.twin) if ENABLE_DOPPELGANGER else None
        self.coord = RealWorldCoordinator(
            require_confirm=REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS
        ) if ENABLE_REALWORLD_COORD else None

        # study suite
        self.study = StudyCompanion(self.twin) if ENABLE_STUDY_COMPANION else None
        self.lecture = LectureAssistant(self.twin) if ENABLE_LECTURE_ASSISTANT else None
        self.kg = KnowledgeGraph(self.twin) if ENABLE_KNOWLEDGE_GRAPH else None
        self.exam = ExamPrep(self.twin) if ENABLE_EXAM_PREP else None
        self.skill = SkillBuilder(self.twin) if ENABLE_SKILL_BUILDER else None
        self.collab = CollabStudy(self.twin) if ENABLE_COLLAB_STUDY else None
        self.lang_guard = LanguageGuardian(self.twin) if ENABLE_LANGUAGE_GUARDIAN else None
        self.research = DeepResearch(self.twin) if ENABLE_DEEP_RESEARCH else None
        self.autopilot = LifeAutopilot(self.twin) if ENABLE_LIFE_AUTOPILOT else None

    # -----------------------------
    # Speech helper (local TTS)
    # -----------------------------
    def say(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    # -----------------------------
    # Core router
    # -----------------------------
    def handle(self, text: str) -> str:
        t = text.strip()
        if not t:
            return "Say something like: 'open youtube' or 'make flashcards on ML'."

        self.twin.remember_chat("user", t)

        # (0) Hyper-context nudges
        if self.context:
            tip = self.context.react_to_text(t)
            if tip:
                self.twin.remember_chat("assistant", tip)
                return tip

        # (1) Device / PC control
        pc_ans = self.pc.route(t)
        if pc_ans:
            self.twin.remember_chat("assistant", pc_ans)
            return pc_ans

        if self.cross:
            cross_ans = self.cross.route(t, REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS)
            if cross_ans:
                self.twin.remember_chat("assistant", cross_ans)
                return cross_ans

        # (2) Predictive suggestions
        if self.predictor:
            sug = self.predictor.suggest(t)
            if sug:
                self.twin.remember_chat("assistant", f"Suggestion: {sug}")
                return f"Suggestion: {sug}"

        # (3) Dark web / breaches
        if self.dark and any(k in t.lower() for k in ["breach", "pwned", "leak", "compromised", "dark web"]):
            ans = self.dark.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (4) Negotiator
        if self.negotiator and any(k in t.lower() for k in ["negotiate", "lower price", "deal", "discount"]):
            ans = self.negotiator.route(t, require_confirm=REQUIRE_CONFIRMATION_FOR_PAYMENTS)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (5) Threat mode
        if self.threat and any(k in t.lower() for k in ["threat mode", "scan threats", "phishing", "suspicious"]):
            ans = self.threat.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (6) AR overlay
        if self.ar and any(k in t.lower() for k in ["ar overlay", "recognize", "what is this object"]):
            ans = self.ar.route(t, consent=REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (7) Voice clone (safe styles)
        if self.voice and any(k in t.lower() for k in ["voice", "speak like", "tone", "style voice"]):
            ans = self.voice.route(t, require_style_consent=REQUIRE_EXPLICIT_CONSENT_FOR_STYLE_ADAPT)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (8) Doppelganger agent
        if self.twin_agent and any(k in t.lower() for k in ["digital twin", "doppelganger", "auto-reply", "attend meeting"]):
            ans = self.twin_agent.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (9) Real-world coordination (calls/messages)
        if self.coord and any(k in t.lower() for k in ["call", "book", "order", "message", "remind"]):
            ans = self.coord.route(t, require_confirm=REQUIRE_CONFIRMATION_FOR_PAYMENTS)
            self.twin.remember_chat("assistant", ans)
            return ans

        # (10) Study suite
        if self.study and "flashcard" in t.lower():
            ans = self.study.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.lecture and any(k in t.lower() for k in ["summarize lecture", "transcribe lecture", "class notes"]):
            ans = self.lecture.route(t, consent=REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.kg and "concept map" in t.lower():
            ans = self.kg.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.exam and any(k in t.lower() for k in ["practice test", "predict score", "exam prep"]):
            ans = self.exam.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.skill and any(k in t.lower() for k in ["learning path", "skill tracker"]):
            ans = self.skill.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.collab and "study group" in t.lower():
            ans = self.collab.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.lang_guard and any(k in t.lower() for k in ["translate live", "language guardian", "whisper translate"]):
            ans = self.lang_guard.route(t, consent=REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.research and any(k in t.lower() for k in ["deep research", "summarize papers", "cross-check sources"]):
            ans = self.research.route(t)
            self.twin.remember_chat("assistant", ans)
            return ans

        if self.autopilot and any(k in t.lower() for k in ["autopilot", "schedule my day", "routine"]):
            ans = self.autopilot.route(t, require_confirm=REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS)
            self.twin.remember_chat("assistant", ans)
            return ans

        # default
        return "I didn’t recognize that yet. Try: 'flashcards on calculus', 'negotiate price on my watchlist', or 'scan threats'."
    def handle_command(self, text):
        try:
        response = get_answer(text)   # call AI/knowledge module
        if not response:
            response = "I'm not sure about that yet."
        return response
    except Exception as e:
        return f"Error processing command: {e}"

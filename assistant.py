"""
Nova AI Assistant - Core Assistant Class
Advanced AI Assistant with comprehensive skill architecture and error handling
"""

import re
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import traceback

# TTS import with graceful fallback
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  pyttsx3 not available. Voice output disabled.")

from core.knowledge import get_answer, initialize_ai_backend
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

# Skills imports with error handling
try:
    from skills.digital_twin import DigitalTwin
    from skills.pc_control import PCControl
    from skills.predictive_control import Predictor
    from skills.hyper_context import HyperContext
    from skills.emotion import EmotionWatcher
    from skills.dark_web_watch import DarkWebWatch
    from skills.cross_device import CrossDevice
    from skills.negotiator import Negotiator
    from skills.ar_overlay import AROverlay
    from skills.threat_mode import ThreatMode
    from skills.voice_clone import VoiceClone
    from skills.doppelganger import Doppelganger
    from skills.coord import RealWorldCoordinator
    from skills.study_companion import StudyCompanion
    from skills.lecture_assistant import LectureAssistant
    from skills.knowledge_graph import KnowledgeGraph
    from skills.exam_prep import ExamPrep
    from skills.skill_builder import SkillBuilder
    from skills.collab_study import CollabStudy
    from skills.language_guardian import LanguageGuardian
    from skills.deep_research import DeepResearch
    from skills.life_autopilot import LifeAutopilot
except ImportError as e:
    print(f"⚠️  Some skills modules not available: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Assistant:
    """
    Nova AI Assistant - Main orchestrator class
    Handles skill coordination, error management, and user interaction
    """
    
    def __init__(self, name: str = ASSISTANT_NAME):
        """Initialize the assistant with all available skills"""
        self.name = name
        self.initialization_errors = []
        
        # Initialize TTS engine
        self._init_tts()
        
        # Initialize AI backend
        try:
            initialize_ai_backend()
            logger.info("AI backend initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI backend: {e}")
            self.initialization_errors.append(f"AI backend: {e}")
        
        # Initialize core memory/twin
        try:
            self.twin = DigitalTwin()
            logger.info("Digital twin initialized")
        except Exception as e:
            logger.error(f"Failed to initialize digital twin: {e}")
            self.twin = None
            self.initialization_errors.append(f"Digital twin: {e}")
        
        # Initialize skills with error handling
        self._init_skills()
        
        # Log initialization status
        if self.initialization_errors:
            logger.warning(f"Assistant initialized with {len(self.initialization_errors)} errors")
        else:
            logger.info("Assistant fully initialized successfully")
    
    def _init_tts(self):
        """Initialize text-to-speech engine with error handling"""
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                # Configure TTS settings
                voices = self.engine.getProperty('voices')
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
                self.engine.setProperty('rate', 150)  # Speed
                self.engine.setProperty('volume', 0.8)  # Volume
                logger.info("TTS engine initialized")
            except Exception as e:
                logger.warning(f"TTS initialization failed: {e}")
                self.engine = None
        else:
            self.engine = None
    
    def _init_skills(self):
        """Initialize all skills with individual error handling"""
        # Core skills
        self.pc = self._safe_init(PCControl, "PC Control")
        
        # Conditional skills based on config
        self.predictor = self._safe_init(
            lambda: Predictor(self.twin) if self.twin else None, 
            "Predictor"
        ) if ENABLE_PREDICTIVE else None
        
        self.context = self._safe_init(
            lambda: HyperContext(self) if self else None,
            "Hyper Context"
        ) if ENABLE_HYPER_CONTEXT else None
        
        self.emotion = self._safe_init(
            lambda: EmotionWatcher(self.twin) if self.twin else None,
            "Emotion Watcher"
        ) if ENABLE_EMOTION else None
        
        self.dark = self._safe_init(DarkWebWatch, "Dark Web Watch") if ENABLE_DARK_WEB_WATCH else None
        self.cross = self._safe_init(CrossDevice, "Cross Device") if ENABLE_CROSS_DEVICE else None
        
        # Advanced skills
        self.negotiator = self._safe_init(
            lambda: Negotiator(self.twin) if self.twin else None,
            "Negotiator"
        ) if ENABLE_NEGOTIATOR else None
        
        self.ar = self._safe_init(AROverlay, "AR Overlay") if ENABLE_AR_OVERLAY else None
        
        self.threat = self._safe_init(
            lambda: ThreatMode(self.twin) if self.twin else None,
            "Threat Mode"
        ) if ENABLE_THREAT_MODE else None
        
        self.voice = self._safe_init(
            lambda: VoiceClone(block_impersonation=BLOCK_REAL_PERSON_IMPERSONATION),
            "Voice Clone"
        ) if ENABLE_VOICE_CLONE else None
        
        self.twin_agent = self._safe_init(
            lambda: Doppelganger(self.twin) if self.twin else None,
            "Doppelganger"
        ) if ENABLE_DOPPELGANGER else None
        
        self.coord = self._safe_init(
            lambda: RealWorldCoordinator(require_confirm=REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS),
            "Real World Coordinator"
        ) if ENABLE_REALWORLD_COORD else None
        
        # Study suite
        self._init_study_skills()
    
    def _init_study_skills(self):
        """Initialize study-related skills"""
        self.study = self._safe_init(
            lambda: StudyCompanion(self.twin) if self.twin else None,
            "Study Companion"
        ) if ENABLE_STUDY_COMPANION else None
        
        self.lecture = self._safe_init(
            lambda: LectureAssistant(self.twin) if self.twin else None,
            "Lecture Assistant"
        ) if ENABLE_LECTURE_ASSISTANT else None
        
        self.kg = self._safe_init(
            lambda: KnowledgeGraph(self.twin) if self.twin else None,
            "Knowledge Graph"
        ) if ENABLE_KNOWLEDGE_GRAPH else None
        
        self.exam = self._safe_init(
            lambda: ExamPrep(self.twin) if self.twin else None,
            "Exam Prep"
        ) if ENABLE_EXAM_PREP else None
        
        self.skill = self._safe_init(
            lambda: SkillBuilder(self.twin) if self.twin else None,
            "Skill Builder"
        ) if ENABLE_SKILL_BUILDER else None
        
        self.collab = self._safe_init(
            lambda: CollabStudy(self.twin) if self.twin else None,
            "Collaborative Study"
        ) if ENABLE_COLLAB_STUDY else None
        
        self.lang_guard = self._safe_init(
            lambda: LanguageGuardian(self.twin) if self.twin else None,
            "Language Guardian"
        ) if ENABLE_LANGUAGE_GUARDIAN else None
        
        self.research = self._safe_init(
            lambda: DeepResearch(self.twin) if self.twin else None,
            "Deep Research"
        ) if ENABLE_DEEP_RESEARCH else None
        
        self.autopilot = self._safe_init(
            lambda: LifeAutopilot(self.twin) if self.twin else None,
            "Life Autopilot"
        ) if ENABLE_LIFE_AUTOPILOT else None
    
    def _safe_init(self, skill_class, skill_name: str):
        """Safely initialize a skill with error handling"""
        try:
            if callable(skill_class):
                result = skill_class()
            else:
                result = skill_class()
            logger.info(f"{skill_name} initialized successfully")
            return result
        except Exception as e:
            logger.error(f"Failed to initialize {skill_name}: {e}")
            self.initialization_errors.append(f"{skill_name}: {e}")
            return None
    
    def speak(self, text: str) -> bool:
        """
        Text-to-speech output with error handling
        Returns True if successful, False otherwise
        """
        if not self.engine:
            return False
            
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            return False
    
    def handle_command(self, text: str) -> str:
        """
        Main command handler with comprehensive routing and error handling
        """
        if not text or not text.strip():
            return "Please provide a command or question."
        
        text = text.strip()
        
        try:
            # Log the interaction
            if self.twin:
                self.twin.remember_chat("user", text)
            
            # Route to appropriate handler
            response = self._route_command(text)
            
            # Log the response
            if self.twin:
                self.twin.remember_chat("assistant", response)
            
            return response
            
        except Exception as e:
            error_msg = f"I encountered an error processing your request: {str(e)}"
            logger.error(f"Command handling error: {e}\n{traceback.format_exc()}")
            return error_msg
    
    def _route_command(self, text: str) -> str:
        """Route commands to appropriate skills or AI backend"""
        t = text.lower()
        
        # System commands
        if any(keyword in t for keyword in ["status", "health", "diagnostic"]):
            return self._get_system_status()
        
        # (0) Hyper-context suggestions
        if self.context:
            try:
                tip = self.context.react_to_text(text)
                if tip:
                    return tip
            except Exception as e:
                logger.error(f"Hyper context error: {e}")
        
        # (1) PC/Device control
        if self.pc and any(keyword in t for keyword in ["open", "close", "launch", "start", "stop"]):
            try:
                pc_ans = self.pc.route(text)
                if pc_ans:
                    return pc_ans
            except Exception as e:
                logger.error(f"PC control error: {e}")
        
        if self.cross and any(keyword in t for keyword in ["device", "phone", "tablet"]):
            try:
                cross_ans = self.cross.route(text, REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS)
                if cross_ans:
                    return cross_ans
            except Exception as e:
                logger.error(f"Cross device error: {e}")
        
        # (2) Predictive suggestions
        if self.predictor and any(keyword in t for keyword in ["predict", "suggest", "recommend"]):
            try:
                sug = self.predictor.suggest(text)
                if sug:
                    return f"Prediction: {sug}"
            except Exception as e:
                logger.error(f"Predictor error: {e}")
        
        # (3) Security features
        if self.dark and any(keyword in t for keyword in ["breach", "pwned", "leak", "compromised", "dark web"]):
            try:
                return self.dark.route(text)
            except Exception as e:
                logger.error(f"Dark web watch error: {e}")
        
        if self.threat and any(keyword in t for keyword in ["threat", "scan threats", "phishing", "suspicious"]):
            try:
                return self.threat.route(text)
            except Exception as e:
                logger.error(f"Threat mode error: {e}")
        
        # (4) Advanced features
        if self.negotiator and any(keyword in t for keyword in ["negotiate", "lower price", "deal", "discount"]):
            try:
                return self.negotiator.route(text, require_confirm=REQUIRE_CONFIRMATION_FOR_PAYMENTS)
            except Exception as e:
                logger.error(f"Negotiator error: {e}")
        
        if self.ar and any(keyword in t for keyword in ["ar overlay", "recognize", "what is this object"]):
            try:
                return self.ar.route(text, consent=REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING)
            except Exception as e:
                logger.error(f"AR overlay error: {e}")
        
        if self.voice and any(keyword in t for keyword in ["voice", "speak like", "tone", "style voice"]):
            try:
                return self.voice.route(text, require_style_consent=REQUIRE_EXPLICIT_CONSENT_FOR_STYLE_ADAPT)
            except Exception as e:
                logger.error(f"Voice clone error: {e}")
        
        if self.twin_agent and any(keyword in t for keyword in ["digital twin", "doppelganger", "auto-reply", "attend meeting"]):
            try:
                return self.twin_agent.route(text)
            except Exception as e:
                logger.error(f"Doppelganger error: {e}")
        
        if self.coord and any(keyword in t for keyword in ["call", "book", "order", "message", "remind"]):
            try:
                return self.coord.route(text, require_confirm=REQUIRE_CONFIRMATION_FOR_PAYMENTS)
            except Exception as e:
                logger.error(f"Real world coordinator error: {e}")
        
        # (5) Study suite
        study_response = self._route_study_commands(text, t)
        if study_response:
            return study_response
        
        # Default: Use AI backend for general queries
        try:
            response = get_answer(text)
            if response:
                return response
            else:
                return "I'm not sure about that. Could you rephrase your question or try a more specific command?"
        except Exception as e:
            logger.error(f"AI backend error: {e}")
            return "I'm having trouble accessing my knowledge base right now. Please try again later."
    
    def _route_study_commands(self, text: str, t: str) -> Optional[str]:
        """Route study-related commands"""
        try:
            if self.study and any(keyword in t for keyword in ["flashcard", "study card", "quiz"]):
                return self.study.route(text)
            
            if self.lecture and any(keyword in t for keyword in ["summarize lecture", "transcribe lecture", "class notes"]):
                return self.lecture.route(text, consent=REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING)
            
            if self.kg and any(keyword in t for keyword in ["concept map", "knowledge graph", "mind map"]):
                return self.kg.route(text)
            
            if self.exam and any(keyword in t for keyword in ["practice test", "predict score", "exam prep"]):
                return self.exam.route(text)
            
            if self.skill and any(keyword in t for keyword in ["learning path", "skill tracker", "progress"]):
                return self.skill.route(text)
            
            if self.collab and any(keyword in t for keyword in ["study group", "collaborate", "group study"]):
                return self.collab.route(text)
            
            if self.lang_guard and any(keyword in t for keyword in ["translate live", "language guardian", "whisper translate"]):
                return self.lang_guard.route(text, consent=REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING)
            
            if self.research and any(keyword in t for keyword in ["deep research", "summarize papers", "cross-check sources"]):
                return self.research.route(text)
            
            if self.autopilot and any(keyword in t for keyword in ["autopilot", "schedule my day", "routine", "automate"]):
                return self.autopilot.route(text, require_confirm=REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS)
                
        except Exception as e:
            logger.error(f"Study suite routing error: {e}")
            return None
        
        return None
    
    def _get_system_status(self) -> str:
        """Get comprehensive system status"""
        status_lines = [f"🤖 {self.name} System Status Report"]
        status_lines.append("=" * 40)
        
        # Core systems
        status_lines.append(f"💾 Digital Twin: {'✅ Active' if self.twin else '❌ Offline'}")
        status_lines.append(f"🔊 TTS Engine: {'✅ Active' if self.engine else '❌ Offline'}")
        
        # Skills status
        skills_status = []
        skill_mapping = {
            'PC Control': self.pc,
            'Hyper Context': self.context,
            'Predictor': self.predictor,
            'Emotion Watcher': self.emotion,
            'Dark Web Watch': self.dark,
            'Cross Device': self.cross,
            'Negotiator': self.negotiator,
            'AR Overlay': self.ar,
            'Threat Mode': self.threat,
            'Voice Clone': self.voice,
            'Doppelganger': self.twin_agent,
            'Real World Coord': self.coord,
            'Study Companion': self.study,
            'Lecture Assistant': self.lecture,
            'Knowledge Graph': self.kg,
            'Exam Prep': self.exam,
            'Skill Builder': self.skill,
            'Collaborative Study': self.collab,
            'Language Guardian': self.lang_guard,
            'Deep Research': self.research,
            'Life Autopilot': self.autopilot
        }
        
        active_skills = sum(1 for skill in skill_mapping.values() if skill is not None)
        total_skills = len(skill_mapping)
        
        status_lines.append(f"🛠️  Active Skills: {active_skills}/{total_skills}")
        
        if self.initialization_errors:
            status_lines.append(f"⚠️  Initialization Errors: {len(self.initialization_errors)}")
            for error in self.initialization_errors[:3]:  # Show first 3 errors
                status_lines.append(f"   • {error}")
        
        # Memory stats if available
        if self.twin:
            try:
                stats = self.twin.get_stats()
                status_lines.append(f"💬 Total Conversations: {stats.get('total_chats', 0)}")
                status_lines.append(f"📊 Memory Usage: {stats.get('memory_mb', 0):.1f} MB")
            except:
                status_lines.append("📊 Memory stats unavailable")
        
        status_lines.append("=" * 40)
        status_lines.append("Status: 🟢 Operational" if active_skills > 0 else "Status: 🟡 Limited")
        
        return "\n".join(status_lines)

    # Legacy compatibility methods
    def handle(self, text: str) -> str:
        """Legacy method for backward compatibility"""
        return self.handle_command(text)
    
    def say(self, text: str):
        """Legacy method for backward compatibility"""
        self.speak(text)

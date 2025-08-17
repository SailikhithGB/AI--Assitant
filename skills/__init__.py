"""
Nova AI Assistant - Skills Module
Contains all specialized skill implementations for the assistant
"""

# Import all skills for easy access
from .digital_twin import DigitalTwin
from .pc_control import PCControl
from .predictive_control import Predictor
from .hyper_context import HyperContext
from .emotion import EmotionWatcher
from .dark_web_watch import DarkWebWatch
from .cross_device import CrossDevice
from .negotiator import Negotiator
from .ar_overlay import AROverlay
from .threat_mode import ThreatMode
from .voice_clone import VoiceClone
from .doppelganger import Doppelganger
from .coord import RealWorldCoordinator
from .study_companion import StudyCompanion
from .lecture_assistant import LectureAssistant
from .knowledge_graph import KnowledgeGraph
from .exam_prep import ExamPrep
from .skill_builder import SkillBuilder
from .collab_study import CollabStudy
from .language_guardian import LanguageGuardian
from .deep_research import DeepResearch
from .life_autopilot import LifeAutopilot

__all__ = [
    'DigitalTwin',
    'PCControl', 
    'Predictor',
    'HyperContext',
    'EmotionWatcher',
    'DarkWebWatch',
    'CrossDevice',
    'Negotiator',
    'AROverlay',
    'ThreatMode',
    'VoiceClone',
    'Doppelganger',
    'RealWorldCoordinator',
    'StudyCompanion',
    'LectureAssistant',
    'KnowledgeGraph',
    'ExamPrep',
    'SkillBuilder',
    'CollabStudy',
    'LanguageGuardian',
    'DeepResearch',
    'LifeAutopilot'
]

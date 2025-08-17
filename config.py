"""
Nova AI Assistant Configuration
Centralized configuration with enhanced settings and better organization
"""

import os
from pathlib import Path

# -------------------------
# Core Settings
# -------------------------
ASSISTANT_NAME = "Nova"

# Data directories
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

STUDY_DIR = DATA_DIR / "study"
STUDY_DIR.mkdir(exist_ok=True)

VDB_DIR = DATA_DIR / "vdb"
VDB_DIR.mkdir(exist_ok=True)

ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# API Keys (from environment with fallbacks)
OPENAI_API_KEY = "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"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# AI Model preferences
DEFAULT_AI_PROVIDER = "openai"  # "openai" or "anthropic"
OPENAI_MODEL = "anthropic/claude-3-opus"  # Latest OpenAI model
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"  # Latest Anthropic model

# AI Behavior settings
MAX_TOKENS = 4000
TEMPERATURE = 0.7
AI_TIMEOUT = 30  # seconds

# -------------------------
# Feature Toggles
# -------------------------

# Core features (generally safe to enable)
ENABLE_HYPER_CONTEXT = True
ENABLE_PREDICTIVE = True
ENABLE_EMOTION = False

# Security features (require careful consideration)
ENABLE_DARK_WEB_WATCH = False
ENABLE_THREAT_MODE = False

# Device integration (requires user consent)
ENABLE_CROSS_DEVICE = False
ENABLE_REALWORLD_COORD = False

# Advanced AI features (experimental)
ENABLE_NEGOTIATOR = False
ENABLE_AR_OVERLAY = False
ENABLE_VOICE_CLONE = False
ENABLE_DOPPELGANGER = False
ENABLE_LIFE_AUTOPILOT = False

# Study suite (educational features)
ENABLE_STUDY_COMPANION = True
ENABLE_LECTURE_ASSISTANT = False
ENABLE_KNOWLEDGE_GRAPH = True
ENABLE_EXAM_PREP = True
ENABLE_SKILL_BUILDER = True
ENABLE_COLLAB_STUDY = False
ENABLE_LANGUAGE_GUARDIAN = False
ENABLE_DEEP_RESEARCH = True

# -------------------------
# Safety & Privacy Settings
# -------------------------

# Confirmation requirements
REQUIRE_CONFIRMATION_FOR_PAYMENTS = True
REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS = True
REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING = True
REQUIRE_EXPLICIT_CONSENT_FOR_STYLE_ADAPT = True

# Privacy protections
BLOCK_REAL_PERSON_IMPERSONATION = True
ENABLE_CONVERSATION_LOGGING = True
ANONYMIZE_LOGS = True

# Data retention
MAX_CONVERSATION_HISTORY = 1000  # messages
AUTO_CLEANUP_DAYS = 30

# -------------------------
# Performance Settings
# -------------------------

# Memory management
MAX_MEMORY_MB = 500
SKILL_LOAD_TIMEOUT = 10  # seconds
MAX_CONCURRENT_SKILLS = 5

# Response settings
DEFAULT_RESPONSE_TIMEOUT = 30  # seconds
MAX_RESPONSE_LENGTH = 2000  # characters
ENABLE_STREAMING_RESPONSES = True

# -------------------------
# External Integrations
# -------------------------

# Security services
HAVEIBEENPWNED_API_KEY = os.getenv("HAVEIBEENPWNED_API_KEY", "")

# Smart home integration
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL", "")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN", "")

# Communication services
WHATSAPP_DEFAULT_COUNTRY_CODE = "+1"
DEFAULT_LANGUAGE = "en"

# Web automation settings
ALLOW_HEADLESS_BROWSER_AUTOMATION = False
RESPECT_ROBOTS_TXT = True
USER_AGENT = "Nova-AI-Assistant/2.0 (+https://github.com/SailikhithGB/AI--Assistant)"

# -------------------------
# Database Configuration
# -------------------------

# SQLite settings
DB_PATH = DATA_DIR / "nova.db"
DB_BACKUP_INTERVAL = 24  # hours
MAX_DB_SIZE_MB = 100

# Connection settings
DB_TIMEOUT = 30  # seconds
DB_CHECK_SAME_THREAD = False

# -------------------------
# Logging Configuration
# -------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "nova.log"
MAX_LOG_SIZE_MB = 10
LOG_BACKUP_COUNT = 5

# What to log
LOG_USER_COMMANDS = True
LOG_ASSISTANT_RESPONSES = True
LOG_SKILL_USAGE = True
LOG_ERRORS = True
LOG_PERFORMANCE = False

# -------------------------
# Web Interface Settings
# -------------------------

WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = False

# Streamlit specific
STREAMLIT_THEME = "dark"
ENABLE_VOICE_INPUT = False  # Requires additional setup
ENABLE_FILE_UPLOAD = True

# -------------------------
# Voice & Audio Settings
# -------------------------

# TTS Configuration
TTS_ENGINE = "pyttsx3"  # or "gTTS" for cloud-based
TTS_RATE = 150  # words per minute
TTS_VOLUME = 0.8  # 0.0 to 1.0

# STT Configuration
STT_ENGINE = "google"  # speech_recognition engine
STT_TIMEOUT = 5  # seconds
STT_PHRASE_TIMEOUT = 1  # seconds

# -------------------------
# Development Settings
# -------------------------

DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
ENABLE_PROFILING = False
MOCK_EXTERNAL_APIS = os.getenv("MOCK_APIS", "false").lower() == "true"

# Testing
RUN_STARTUP_TESTS = True
ENABLE_SKILL_TESTS = True

# -------------------------
# Validation Functions
# -------------------------

def validate_config():
    """Validate configuration settings and warn about issues"""
    issues = []
    
    # Check API keys
    if not OPENAI_API_KEY and not ANTHROPIC_API_KEY:
        issues.append("No AI API keys configured. Add OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables.")
    
    # Check directory permissions
    for directory in [DATA_DIR, STUDY_DIR, VDB_DIR, ASSETS_DIR]:
        if not directory.exists():
            try:
                directory.mkdir(exist_ok=True)
            except PermissionError:
                issues.append(f"Cannot create directory: {directory}")
    
    # Check conflicting settings
    if ENABLE_VOICE_CLONE and BLOCK_REAL_PERSON_IMPERSONATION:
        pass  # This is actually good - voice clone with safety
    
    if ENABLE_LIFE_AUTOPILOT and not REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS:
        issues.append("Life autopilot enabled without device action confirmation - security risk")
    
    return issues

def get_active_features():
    """Get list of currently enabled features"""
    features = []
    
    # Core features
    if ENABLE_HYPER_CONTEXT:
        features.append("Hyper Context")
    if ENABLE_PREDICTIVE:
        features.append("Predictive Control")
    if ENABLE_EMOTION:
        features.append("Emotion Watcher")
    
    # Security features
    if ENABLE_DARK_WEB_WATCH:
        features.append("Dark Web Watch")
    if ENABLE_THREAT_MODE:
        features.append("Threat Mode")
    
    # Advanced features
    if ENABLE_NEGOTIATOR:
        features.append("Negotiator")
    if ENABLE_AR_OVERLAY:
        features.append("AR Overlay")
    if ENABLE_VOICE_CLONE:
        features.append("Voice Clone")
    if ENABLE_DOPPELGANGER:
        features.append("Doppelganger")
    if ENABLE_LIFE_AUTOPILOT:
        features.append("Life Autopilot")
    
    # Study features
    if ENABLE_STUDY_COMPANION:
        features.append("Study Companion")
    if ENABLE_LECTURE_ASSISTANT:
        features.append("Lecture Assistant")
    if ENABLE_KNOWLEDGE_GRAPH:
        features.append("Knowledge Graph")
    if ENABLE_EXAM_PREP:
        features.append("Exam Prep")
    if ENABLE_SKILL_BUILDER:
        features.append("Skill Builder")
    if ENABLE_COLLAB_STUDY:
        features.append("Collaborative Study")
    if ENABLE_LANGUAGE_GUARDIAN:
        features.append("Language Guardian")
    if ENABLE_DEEP_RESEARCH:
        features.append("Deep Research")
    
    return features

# Run validation on import
if __name__ == "__main__":
    issues = validate_config()
    if issues:
        print("Configuration Issues:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
    else:
        print("✅ Configuration validated successfully")
    
    print(f"\nActive Features ({len(get_active_features())}):")
    for feature in get_active_features():
        print(f"  🟢 {feature}")

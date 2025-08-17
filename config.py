from pathlib import Path

ASSISTANT_NAME = "Nova"

# Data dir for memory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# -------------------------
# Feature toggles (opt-in)
# -------------------------
ENABLE_HYPER_CONTEXT = True
ENABLE_PREDICTIVE = True
ENABLE_EMOTION = False
ENABLE_DARK_WEB_WATCH = False
ENABLE_CROSS_DEVICE = False

# NEW FEATURES (all default off for safety)
ENABLE_NEGOTIATOR = False            # autonomous online negotiator (scraping-friendly sites only)
ENABLE_AR_OVERLAY = False            # AR live overlay (local CV only)
ENABLE_THREAT_MODE = False           # proactive threat anticipation
ENABLE_VOICE_CLONE = False           # local TTS voice styles, NOT real-person impersonation
ENABLE_DOPPELGANGER = False          # digital persona (observe->assist->act)
ENABLE_REALWORLD_COORD = False       # calls/messages via local/desktop automations only
ENABLE_STUDY_COMPANION = False
ENABLE_LECTURE_ASSISTANT = False
ENABLE_KNOWLEDGE_GRAPH = False
ENABLE_EXAM_PREP = False
ENABLE_SKILL_BUILDER = False
ENABLE_COLLAB_STUDY = False
ENABLE_LANGUAGE_GUARDIAN = False
ENABLE_DEEP_RESEARCH = False
ENABLE_LIFE_AUTOPILOT = False

# -------------------------
# Safety confirmations
# -------------------------
REQUIRE_CONFIRMATION_FOR_PAYMENTS = True
REQUIRE_CONFIRMATION_FOR_DEVICE_ACTIONS = True
REQUIRE_EXPLICIT_CONSENT_FOR_RECORDING = True
REQUIRE_EXPLICIT_CONSENT_FOR_STYLE_ADAPT = True  # emails/text tone mimic
BLOCK_REAL_PERSON_IMPERSONATION = True           # disallow cloning/impersonation of real people

# -------------------------
# Integrations (leave empty if unused)
# -------------------------
# HaveIBeenPwned (email breach) – optional
HAVEIBEENPWNED_API_KEY = ""

# Home Assistant (smart home) – optional
HOME_ASSISTANT_URL = ""              # e.g., http://192.168.1.20:8123
HOME_ASSISTANT_TOKEN = ""

# Study data storage
STUDY_DIR = DATA_DIR / "study"
STUDY_DIR.mkdir(exist_ok=True)

# Local Vector Store (FAISS-like; fallback JSON index)
VDB_DIR = DATA_DIR / "vdb"
VDB_DIR.mkdir(exist_ok=True)

# Locale & defaults
DEFAULT_LANGUAGE = "en"
WHATSAPP_DEFAULT_COUNTRY_CODE = "+91"

# Browser automation flags (respect site ToS)
ALLOW_HEADLESS_BROWSER_AUTOMATION = False
RESPECT_ROBOTS_TXT = True

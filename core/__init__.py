"""
Nova AI Assistant - Core Module
Contains the essential components for AI processing and knowledge management
"""

from .knowledge import get_answer, initialize_ai_backend
from .database import DatabaseManager

__all__ = ['get_answer', 'initialize_ai_backend', 'DatabaseManager']

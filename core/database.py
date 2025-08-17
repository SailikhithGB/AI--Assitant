import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import threading
from contextlib import contextmanager

from config import DB_PATH, DB_TIMEOUT, MAX_DB_SIZE_MB, DB_BACKUP_INTERVAL

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Centralized database management for Nova AI Assistant
    Handles conversations, user preferences, skill data, and system metrics
    """
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_database()
        
    def _init_database(self):
        """Initialize database with required tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Conversations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                # User preferences table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)  # Fixed: Closing parenthesis added here

                # (You can continue with other table creations or logic below)

        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def get_connection(self):
        """Get a database connection with a timeout"""
        return sqlite3.connect(self.db_path, timeout=DB_TIMEOUT)

_db_instance = None

def get_db_manager():
    """Singleton-style access to the database manager."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager("assistant.db")
    return _db_instance

"""
Digital Twin - Memory and User Modeling System
Maintains persistent memory of user interactions and preferences
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from core.database import get_db_manager

logger = logging.getLogger(__name__)

class DigitalTwin:
    """
    Digital Twin system for maintaining user memory and behavioral modeling
    Stores conversation history, preferences, and patterns for personalized assistance
    """
    
    def __init__(self):
        self.db = get_db_manager()
        self.session_id = "default"  # Can be made dynamic for multi-user support
        
    def remember_chat(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Remember a chat interaction"""
        try:
            # Add timestamp and basic metadata
            enhanced_metadata = metadata or {}
            enhanced_metadata.update({
                'word_count': len(content.split()),
                'char_count': len(content)
            })
            
            self.db.add_conversation(role, content, self.session_id, enhanced_metadata)
            logger.debug(f"Remembered {role} message: {content[:50]}...")
            
        except Exception as e:
            logger.error(f"Error remembering chat: {e}")
    
    def get_recent_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context"""
        try:
            return self.db.get_conversation_history(self.session_id, limit)
        except Exception as e:
            logger.error(f"Error getting recent context: {e}")
            return []
    
    def get_conversation_summary(self, hours: int = 24) -> str:
        """Get a summary of recent conversations"""
        try:
            conversations = self.db.get_conversation_history(self.session_id, 50)
            
            # Filter by time
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_conversations = [
                conv for conv in conversations 
                if datetime.fromisoformat(conv['timestamp']) > cutoff_time
            ]
            
            if not recent_conversations:
                return "No recent conversations."
            
            # Create summary
            user_messages = [conv['content'] for conv in recent_conversations if conv['role'] == 'user']
            assistant_messages = [conv['content'] for conv in recent_conversations if conv['role'] == 'assistant']
            
            summary = f"Recent Activity Summary ({hours} hours):\n"
            summary += f"- Total interactions: {len(recent_conversations)}\n"
            summary += f"- User messages: {len(user_messages)}\n"
            summary += f"- Assistant responses: {len(assistant_messages)}\n"
            
            if user_messages:
                # Common topics/keywords
                all_text = " ".join(user_messages).lower()
                words = all_text.split()
                
                # Simple frequency analysis
                word_freq = {}
                for word in words:
                    if len(word) > 3 and word.isalpha():  # Filter meaningful words
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                if word_freq:
                    top_topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
                    summary += f"- Common topics: {', '.join([word for word, count in top_topics])}\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return "Unable to generate conversation summary."
    
    def learn_preference(self, category: str, preference: Any):
        """Learn and store a user preference"""
        try:
            current_prefs = self.db.get_preference(category, {})
            
            # Update preference with timestamp
            if isinstance(current_prefs, dict):
                current_prefs.update({
                    'value': preference,
                    'learned_at': datetime.now().isoformat(),
                    'confidence': 0.8  # Default confidence
                })
            else:
                current_prefs = {
                    'value': preference,
                    'learned_at': datetime.now().isoformat(),
                    'confidence': 0.8
                }
            
            self.db.set_preference(category, current_prefs)
            logger.info(f"Learned preference: {category} = {preference}")
            
        except Exception as e:
            logger.error(f"Error learning preference: {e}")
    
    def get_preference(self, category: str, default: Any = None) -> Any:
        """Get a learned user preference"""
        try:
            pref_data = self.db.get_preference(category)
            
            if pref_data and isinstance(pref_data, dict) and 'value' in pref_data:
                return pref_data['value']
            
            return default
            
        except Exception as e:
            logger.error(f"Error getting preference: {e}")
            return default
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        try:
            conversations = self.db.get_conversation_history(self.session_id, 100)
            
            if not conversations:
                return {"status": "insufficient_data"}
            
            patterns = {
                'total_interactions': len(conversations),
                'interaction_times': [],
                'common_requests': {},
                'response_patterns': {},
                'engagement_level': 'unknown'
            }
            
            # Analyze interaction times
            timestamps = [datetime.fromisoformat(conv['timestamp']) for conv in conversations]
            if timestamps:
                hours = [ts.hour for ts in timestamps]
                hour_freq = {}
                for hour in hours:
                    hour_freq[hour] = hour_freq.get(hour, 0) + 1
                
                most_active_hour = max(hour_freq.items(), key=lambda x: x[1])
                patterns['most_active_hour'] = most_active_hour[0]
                patterns['interaction_times'] = hour_freq
            
            # Analyze request types
            user_messages = [conv['content'] for conv in conversations if conv['role'] == 'user']
            for message in user_messages:
                words = message.lower().split()
                for word in words:
                    if len(word) > 4:  # Meaningful words
                        patterns['common_requests'][word] = patterns['common_requests'].get(word, 0) + 1
            
            # Sort common requests
            if patterns['common_requests']:
                sorted_requests = sorted(patterns['common_requests'].items(), key=lambda x: x[1], reverse=True)
                patterns['top_requests'] = sorted_requests[:10]
            
            # Determine engagement level
            if len(conversations) > 50:
                patterns['engagement_level'] = 'high'
            elif len(conversations) > 20:
                patterns['engagement_level'] = 'medium'
            else:
                patterns['engagement_level'] = 'low'
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing patterns: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_personalization_data(self) -> Dict[str, Any]:
        """Get data for personalizing responses"""
        try:
            patterns = self.analyze_patterns()
            recent_context = self.get_recent_context(5)
            
            # Get stored preferences
            preferences = {}
            common_pref_keys = ['language', 'communication_style', 'expertise_level', 'interests']
            for key in common_pref_keys:
                pref_value = self.get_preference(key)
                if pref_value:
                    preferences[key] = pref_value
            
            personalization = {
                'behavioral_patterns': patterns,
                'recent_context': recent_context,
                'preferences': preferences,
                'engagement_level': patterns.get('engagement_level', 'unknown'),
                'expertise_indicators': self._assess_expertise_level(recent_context)
            }
            
            return personalization
            
        except Exception as e:
            logger.error(f"Error getting personalization data: {e}")
            return {}
    
    def _assess_expertise_level(self, conversations: List[Dict]) -> Dict[str, str]:
        """Assess user expertise level in different domains"""
        expertise = {
            'technical': 'unknown',
            'academic': 'unknown',
            'general': 'unknown'
        }
        
        try:
            all_text = " ".join([conv['content'] for conv in conversations if conv['role'] == 'user']).lower()
            
            # Technical indicators
            tech_keywords = ['api', 'code', 'programming', 'algorithm', 'database', 'server', 'python', 'javascript']
            tech_score = sum(1 for keyword in tech_keywords if keyword in all_text)
            
            if tech_score > 5:
                expertise['technical'] = 'advanced'
            elif tech_score > 2:
                expertise['technical'] = 'intermediate'
            elif tech_score > 0:
                expertise['technical'] = 'beginner'
            
            # Academic indicators
            academic_keywords = ['research', 'study', 'thesis', 'paper', 'academic', 'university', 'analysis']
            academic_score = sum(1 for keyword in academic_keywords if keyword in all_text)
            
            if academic_score > 3:
                expertise['academic'] = 'advanced'
            elif academic_score > 1:
                expertise['academic'] = 'intermediate'
            elif academic_score > 0:
                expertise['academic'] = 'beginner'
            
            # General complexity assessment
            avg_sentence_length = len(all_text.split()) / max(1, len(conversations))
            if avg_sentence_length > 15:
                expertise['general'] = 'advanced'
            elif avg_sentence_length > 8:
                expertise['general'] = 'intermediate'
            else:
                expertise['general'] = 'beginner'
            
        except Exception as e:
            logger.error(f"Error assessing expertise: {e}")
        
        return expertise
    
    def clear_memory(self):
        """Clear conversation memory (with user consent)"""
        try:
            self.db.clear_conversation_history(self.session_id)
            logger.info("Digital twin memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the digital twin"""
        try:
            conversations = self.db.get_conversation_history(self.session_id, 1000)
            db_stats = self.db.get_database_stats()
            
            stats = {
                'total_chats': len(conversations),
                'memory_mb': db_stats.get('db_size_mb', 0),
                'active_skills': 5,  # This would be dynamically calculated
                'last_interaction': conversations[0]['timestamp'] if conversations else 'Never',
                'personality_traits': self._get_personality_traits(),
                'learning_progress': self._get_learning_progress()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                'total_chats': 0,
                'memory_mb': 0,
                'active_skills': 0,
                'last_interaction': 'Error',
                'personality_traits': {},
                'learning_progress': 0
            }
    
    def _get_personality_traits(self) -> Dict[str, float]:
        """Infer personality traits from interaction patterns"""
        # Simplified personality assessment
        patterns = self.analyze_patterns()
        
        traits = {
            'curiosity': 0.5,
            'technical_orientation': 0.5,
            'detail_focus': 0.5,
            'creativity': 0.5
        }
        
        if patterns.get('total_interactions', 0) > 0:
            # Adjust based on interaction patterns
            if 'question' in str(patterns.get('top_requests', [])):
                traits['curiosity'] = min(1.0, traits['curiosity'] + 0.3)
            
            if any(word in str(patterns.get('top_requests', [])) for word in ['code', 'technical', 'api']):
                traits['technical_orientation'] = min(1.0, traits['technical_orientation'] + 0.4)
        
        return traits
    
    def _get_learning_progress(self) -> float:
        """Calculate learning progress based on interaction complexity"""
        try:
            conversations = self.db.get_conversation_history(self.session_id, 50)
            
            if not conversations:
                return 0.0
            
            # Simple progress metric based on interaction frequency and complexity
            recent_week = datetime.now() - timedelta(days=7)
            recent_conversations = [
                conv for conv in conversations
                if datetime.fromisoformat(conv['timestamp']) > recent_week
            ]
            
            # Progress based on recent activity and question complexity
            progress = min(1.0, len(recent_conversations) / 20.0)  # Max at 20 interactions per week
            
            return progress
            
        except Exception as e:
            logger.error(f"Error calculating learning progress: {e}")
            return 0.0

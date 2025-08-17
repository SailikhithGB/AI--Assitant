"""
Hyper Context Skill - Contextual Awareness and Smart Suggestions
Provides contextual awareness and intelligent suggestions based on user behavior
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import re

logger = logging.getLogger(__name__)

class HyperContext:
    """
    Hyper Context system that provides intelligent contextual awareness
    Analyzes user behavior patterns to provide timely suggestions and insights
    """
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.context_memory = []
        self.max_context_items = 50
        
    def react_to_text(self, text: str) -> Optional[str]:
        """React to user text with contextual suggestions"""
        try:
            # Store the interaction
            self._store_context_item(text)
            
            # Analyze for contextual opportunities
            context_response = self._analyze_context(text)
            
            if context_response:
                return context_response
            
            # Check for patterns that warrant suggestions
            pattern_response = self._check_behavioral_patterns(text)
            
            return pattern_response
            
        except Exception as e:
            logger.error(f"Error in hyper context reaction: {e}")
            return None
    
    def _store_context_item(self, text: str):
        """Store context item for pattern analysis"""
        context_item = {
            'text': text,
            'timestamp': datetime.now(),
            'hour': datetime.now().hour,
            'day_of_week': datetime.now().weekday(),
            'word_count': len(text.split()),
            'intent_markers': self._extract_intent_markers(text)
        }
        
        self.context_memory.append(context_item)
        
        # Keep memory within limits
        if len(self.context_memory) > self.max_context_items:
            self.context_memory = self.context_memory[-self.max_context_items:]
    
    def _extract_intent_markers(self, text: str) -> List[str]:
        """Extract intent markers from text"""
        markers = []
        text_lower = text.lower()
        
        # Task markers
        if any(word in text_lower for word in ['todo', 'task', 'remind', 'schedule']):
            markers.append('task_management')
        
        # Learning markers
        if any(word in text_lower for word in ['learn', 'study', 'understand', 'explain']):
            markers.append('learning')
        
        # Creative markers
        if any(word in text_lower for word in ['create', 'write', 'design', 'make']):
            markers.append('creative')
        
        # Information seeking
        if any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where']):
            markers.append('information_seeking')
        
        # Problem solving
        if any(word in text_lower for word in ['problem', 'issue', 'fix', 'solve', 'debug']):
            markers.append('problem_solving')
        
        return markers
    
    def _analyze_context(self, text: str) -> Optional[str]:
        """Analyze current context for immediate suggestions"""
        text_lower = text.lower()
        
        # Time-based suggestions
        current_hour = datetime.now().hour
        
        # Early morning (6-9 AM)
        if 6 <= current_hour <= 9 and any(word in text_lower for word in ['good morning', 'start', 'begin']):
            return self._get_morning_context_suggestion()
        
        # Late night (22-2 AM)
        elif (current_hour >= 22 or current_hour <= 2) and 'sleep' not in text_lower:
            return "🌙 It's getting late. Consider wrapping up for better productivity tomorrow."
        
        # Work hours productivity
        elif 9 <= current_hour <= 17 and any(word in text_lower for word in ['focus', 'work', 'productive']):
            return self._get_work_hours_suggestion()
        
        # Learning context
        if any(word in text_lower for word in ['study', 'learn', 'practice']):
            return self._get_learning_context_suggestion(text)
        
        # Multi-tasking detection
        if self._detect_context_switching():
            return "🔄 I notice you're switching between different types of tasks. Consider finishing one before moving to the next for better focus."
        
        return None
    
    def _get_morning_context_suggestion(self) -> str:
        """Get morning-specific contextual suggestions"""
        suggestions = [
            "🌅 Good morning! Would you like to review your goals for today?",
            "☕ Morning! Consider starting with the most important task while your mind is fresh.",
            "🎯 New day, new possibilities! What's your main priority today?"
        ]
        
        # Check if user has established morning patterns
        morning_patterns = self._analyze_time_patterns(6, 9)
        if morning_patterns.get('common_activities'):
            return f"🌅 Good morning! Based on your usual routine, you often work on {morning_patterns['common_activities'][0]} in the morning."
        
        return suggestions[datetime.now().day % len(suggestions)]
    
    def _get_work_hours_suggestion(self) -> str:
        """Get work hours contextual suggestions"""
        # Analyze recent productivity patterns
        recent_work = [item for item in self.context_memory[-10:] 
                      if any(marker in item.get('intent_markers', []) 
                            for marker in ['task_management', 'problem_solving'])]
        
        if len(recent_work) > 3:
            return "💪 You're in a productive flow! Consider using the Pomodoro technique to maintain this momentum."
        else:
            return "🎯 Perfect time for focused work. Would you like help prioritizing your tasks?"
    
    def _get_learning_context_suggestion(self, text: str) -> str:
        """Get learning-specific contextual suggestions"""
        text_lower = text.lower()
        
        # Subject-specific suggestions
        if any(subject in text_lower for subject in ['math', 'physics', 'chemistry']):
            return "📊 For STEM subjects, consider creating concept maps or practice problems. Would you like me to generate some?"
        
        elif any(subject in text_lower for subject in ['history', 'literature', 'language']):
            return "📚 For humanities, try creating timelines or summary notes. Flashcards work great too!"
        
        elif any(subject in text_lower for subject in ['programming', 'coding', 'software']):
            return "💻 For programming, hands-on practice is key. Consider building small projects to reinforce concepts."
        
        # General learning suggestions
        learning_items = [item for item in self.context_memory[-5:] 
                         if 'learning' in item.get('intent_markers', [])]
        
        if len(learning_items) > 2:
            return "🧠 You're on a learning streak! Remember to take breaks and review previous topics for better retention."
        
        return "📖 Learning something new? I can help create study materials or explain concepts in different ways."
    
    def _check_behavioral_patterns(self, text: str) -> Optional[str]:
        """Check for behavioral patterns that warrant suggestions"""
        if len(self.context_memory) < 5:
            return None
        
        # Analyze recent activity patterns
        recent_items = self.context_memory[-10:]
        
        # Detect repetitive requests
        repetitive_pattern = self._detect_repetitive_pattern(recent_items)
        if repetitive_pattern:
            return repetitive_pattern
        
        # Detect procrastination patterns
        procrastination_pattern = self._detect_procrastination_pattern(recent_items)
        if procrastination_pattern:
            return procrastination_pattern
        
        # Detect learning fatigue
        fatigue_pattern = self._detect_learning_fatigue(recent_items)
        if fatigue_pattern:
            return fatigue_pattern
        
        # Detect productive streaks
        productive_pattern = self._detect_productive_streak(recent_items)
        if productive_pattern:
            return productive_pattern
        
        return None
    
    def _detect_repetitive_pattern(self, items: List[Dict]) -> Optional[str]:
        """Detect if user is asking similar questions repeatedly"""
        if len(items) < 3:
            return None
        
        # Simple similarity check based on common words
        recent_texts = [item['text'].lower() for item in items[-3:]]
        
        # Check for common words across recent requests
        word_sets = [set(text.split()) for text in recent_texts]
        common_words = word_sets[0]
        for word_set in word_sets[1:]:
            common_words = common_words.intersection(word_set)
        
        # If many words are common and they're meaningful
        meaningful_common = [word for word in common_words if len(word) > 3]
        
        if len(meaningful_common) >= 2:
            return f"🔄 I notice you're asking about similar topics. Would you like me to provide a comprehensive overview of {' and '.join(meaningful_common[:2])}?"
        
        return None
    
    def _detect_procrastination_pattern(self, items: List[Dict]) -> Optional[str]:
        """Detect procrastination patterns"""
        # Look for switching between many different topics without follow-through
        if len(items) < 5:
            return None
        
        intent_switches = 0
        last_intent = None
        
        for item in items:
            current_intents = item.get('intent_markers', [])
            if current_intents and current_intents != last_intent:
                intent_switches += 1
                last_intent = current_intents
        
        # High number of intent switches might indicate procrastination
        if intent_switches > len(items) * 0.7:
            return "🎯 I notice you're jumping between different topics. Sometimes focusing on one thing at a time can be more productive. Would you like help prioritizing?"
        
        return None
    
    def _detect_learning_fatigue(self, items: List[Dict]) -> Optional[str]:
        """Detect signs of learning fatigue"""
        learning_items = [item for item in items if 'learning' in item.get('intent_markers', [])]
        
        if len(learning_items) >= 4:
            # Check time span
            if learning_items:
                time_span = learning_items[-1]['timestamp'] - learning_items[0]['timestamp']
                if time_span > timedelta(hours=2):
                    return "🧠 You've been learning for a while! Consider taking a break to let your brain process the information."
        
        return None
    
    def _detect_productive_streak(self, items: List[Dict]) -> Optional[str]:
        """Detect productive streaks to encourage continuation"""
        productive_markers = ['task_management', 'problem_solving', 'creative']
        productive_items = [item for item in items 
                           if any(marker in item.get('intent_markers', []) 
                                 for marker in productive_markers)]
        
        if len(productive_items) >= 3:
            return "🚀 You're on a productive streak! Keep up the great momentum. Remember to stay hydrated and take short breaks."
        
        return None
    
    def _detect_context_switching(self) -> bool:
        """Detect if user is rapidly switching contexts"""
        if len(self.context_memory) < 4:
            return False
        
        recent_items = self.context_memory[-4:]
        intent_changes = 0
        
        for i in range(1, len(recent_items)):
            prev_intents = set(recent_items[i-1].get('intent_markers', []))
            curr_intents = set(recent_items[i].get('intent_markers', []))
            
            # If intents are completely different
            if prev_intents and curr_intents and not prev_intents.intersection(curr_intents):
                intent_changes += 1
        
        return intent_changes >= 2
    
    def _analyze_time_patterns(self, start_hour: int, end_hour: int) -> Dict[str, Any]:
        """Analyze patterns within specific time ranges"""
        time_items = []
        
        for item in self.context_memory:
            item_hour = item['timestamp'].hour
            if start_hour <= item_hour <= end_hour:
                time_items.append(item)
        
        if not time_items:
            return {}
        
        # Analyze common activities
        all_intents = []
        for item in time_items:
            all_intents.extend(item.get('intent_markers', []))
        
        intent_freq = {}
        for intent in all_intents:
            intent_freq[intent] = intent_freq.get(intent, 0) + 1
        
        sorted_intents = sorted(intent_freq.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_activities': len(time_items),
            'common_activities': [intent for intent, count in sorted_intents[:3]],
            'activity_frequency': intent_freq
        }
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of context analysis"""
        try:
            if not self.context_memory:
                return {'status': 'no_context_data'}
            
            # Analyze all stored context
            total_interactions = len(self.context_memory)
            
            # Intent distribution
            all_intents = []
            for item in self.context_memory:
                all_intents.extend(item.get('intent_markers', []))
            
            intent_freq = {}
            for intent in all_intents:
                intent_freq[intent] = intent_freq.get(intent, 0) + 1
            
            # Time patterns
            hour_freq = {}
            for item in self.context_memory:
                hour = item['timestamp'].hour
                hour_freq[hour] = hour_freq.get(hour, 0) + 1
            
            most_active_hour = max(hour_freq.items(), key=lambda x: x[1])[0] if hour_freq else None
            
            # Recent activity
            recent_activity = len([item for item in self.context_memory 
                                 if datetime.now() - item['timestamp'] < timedelta(hours=1)])
            
            return {
                'total_interactions': total_interactions,
                'intent_distribution': dict(sorted(intent_freq.items(), key=lambda x: x[1], reverse=True)),
                'most_active_hour': most_active_hour,
                'recent_activity_count': recent_activity,
                'context_memory_size': len(self.context_memory),
                'top_intents': list(dict(sorted(intent_freq.items(), key=lambda x: x[1], reverse=True)).keys())[:3]
            }
            
        except Exception as e:
            logger.error(f"Error getting context summary: {e}")
            return {'error': str(e)}

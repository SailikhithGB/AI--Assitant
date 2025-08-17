"""
Emotion Watcher Skill - Emotional Intelligence and Mood Analysis
Monitors user emotional state and provides empathetic responses
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import re

logger = logging.getLogger(__name__)

class EmotionWatcher:
    """
    Emotion Watcher system that analyzes user emotional state
    Provides empathetic responses and mood-based suggestions
    """
    
    def __init__(self, digital_twin):
        self.twin = digital_twin
        self.emotion_history = []
        self.max_emotion_history = 20
        
        # Emotion detection patterns
        self.emotion_patterns = self._init_emotion_patterns()
        
    def _init_emotion_patterns(self) -> Dict[str, Dict]:
        """Initialize emotion detection patterns"""
        return {
            'happy': {
                'keywords': ['happy', 'excited', 'great', 'awesome', 'amazing', 'fantastic', 'wonderful', 'excellent', 'thrilled', 'delighted'],
                'punctuation': ['!', '😊', '😃', '😄', '🎉', '👏'],
                'intensity_multipliers': ['very', 'extremely', 'super', 'really']
            },
            'sad': {
                'keywords': ['sad', 'depressed', 'down', 'upset', 'disappointed', 'heartbroken', 'miserable', 'gloomy', 'blue'],
                'punctuation': ['😢', '😭', '💔', '😞', '😔'],
                'intensity_multipliers': ['very', 'extremely', 'really', 'deeply']
            },
            'frustrated': {
                'keywords': ['frustrated', 'annoyed', 'irritated', 'angry', 'mad', 'furious', 'livid', 'aggravated', 'bothered'],
                'punctuation': ['!!!', '😡', '😠', '🤬', '💢'],
                'intensity_multipliers': ['so', 'extremely', 'really', 'very']
            },
            'anxious': {
                'keywords': ['anxious', 'worried', 'nervous', 'stressed', 'overwhelmed', 'panic', 'scared', 'frightened', 'concerned'],
                'punctuation': ['😰', '😱', '😨', '🤯'],
                'intensity_multipliers': ['very', 'extremely', 'really', 'totally']
            },
            'confused': {
                'keywords': ['confused', 'lost', 'puzzled', 'perplexed', 'bewildered', 'unclear', 'uncertain', 'baffled'],
                'punctuation': ['?', '🤔', '😕', '😵'],
                'intensity_multipliers': ['completely', 'totally', 'really', 'very']
            },
            'confident': {
                'keywords': ['confident', 'sure', 'certain', 'determined', 'ready', 'prepared', 'capable', 'able'],
                'punctuation': ['💪', '🔥', '✨'],
                'intensity_multipliers': ['very', 'extremely', 'totally', 'completely']
            },
            'tired': {
                'keywords': ['tired', 'exhausted', 'drained', 'weary', 'fatigued', 'sleepy', 'worn out', 'beat'],
                'punctuation': ['😴', '😪', '🥱'],
                'intensity_multipliers': ['very', 'extremely', 'really', 'so']
            }
        }
    
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotional content of text"""
        try:
            text_lower = text.lower()
            detected_emotions = {}
            
            for emotion, patterns in self.emotion_patterns.items():
                score = 0
                
                # Check keywords
                for keyword in patterns['keywords']:
                    if keyword in text_lower:
                        score += 1
                        
                        # Check for intensity multipliers
                        for multiplier in patterns['intensity_multipliers']:
                            if f"{multiplier} {keyword}" in text_lower or f"{keyword} {multiplier}" in text_lower:
                                score += 0.5
                
                # Check punctuation/emojis
                for punct in patterns['punctuation']:
                    score += text.count(punct) * 0.5
                
                if score > 0:
                    detected_emotions[emotion] = score
            
            # Normalize scores
            if detected_emotions:
                total_score = sum(detected_emotions.values())
                for emotion in detected_emotions:
                    detected_emotions[emotion] = detected_emotions[emotion] / total_score
            
            # Determine primary emotion
            primary_emotion = max(detected_emotions.items(), key=lambda x: x[1])[0] if detected_emotions else 'neutral'
            confidence = max(detected_emotions.values()) if detected_emotions else 0.0
            
            emotion_data = {
                'primary_emotion': primary_emotion,
                'confidence': confidence,
                'all_emotions': detected_emotions,
                'timestamp': datetime.now(),
                'text_sample': text[:100]  # Store sample for context
            }
            
            # Store in emotion history
            self._store_emotion(emotion_data)
            
            return emotion_data
            
        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            return {
                'primary_emotion': 'neutral',
                'confidence': 0.0,
                'all_emotions': {},
                'timestamp': datetime.now(),
                'error': str(e)
            }
    
    def _store_emotion(self, emotion_data: Dict[str, Any]):
        """Store emotion data in history"""
        self.emotion_history.append(emotion_data)
        
        # Keep history within limits
        if len(self.emotion_history) > self.max_emotion_history:
            self.emotion_history = self.emotion_history[-self.max_emotion_history:]
        
        # Store in digital twin if available
        if self.twin:
            try:
                self.twin.db.record_metric('user_emotion', emotion_data['confidence'], {
                    'emotion': emotion_data['primary_emotion'],
                    'all_emotions': emotion_data['all_emotions']
                })
            except Exception as e:
                logger.error(f"Error storing emotion in twin: {e}")
    
    def get_empathetic_response(self, emotion_data: Dict[str, Any]) -> Optional[str]:
        """Generate empathetic response based on detected emotion"""
        try:
            emotion = emotion_data['primary_emotion']
            confidence = emotion_data['confidence']
            
            # Only respond if confidence is reasonable
            if confidence < 0.3:
                return None
            
            responses = self._get_emotion_responses(emotion)
            
            # Select appropriate response based on context and history
            response = self._select_contextual_response(emotion, responses)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating empathetic response: {e}")
            return None
    
    def _get_emotion_responses(self, emotion: str) -> List[str]:
        """Get appropriate responses for each emotion"""
        response_map = {
            'happy': [
                "🌟 That's wonderful! I'm glad you're feeling so positive!",
                "😊 Your happiness is contagious! Keep that great energy going!",
                "🎉 It's great to hear you're doing well! What's made your day so good?",
                "✨ I love your enthusiasm! How can I help you make the most of this positive mood?"
            ],
            'sad': [
                "💙 I'm sorry you're feeling down. Remember that it's okay to feel this way sometimes.",
                "🤗 I'm here for you. Would you like to talk about what's bothering you?",
                "💜 Tough times don't last, but resilient people like you do. You've got this.",
                "🌈 It's okay to feel sad. Sometimes we need these moments to appreciate the good times more."
            ],
            'frustrated': [
                "😮‍💨 I can sense your frustration. Let's take a step back and see how I can help.",
                "🧘‍♀️ Frustration is natural when things don't go as planned. Want to talk through what's bothering you?",
                "💪 I understand you're feeling frustrated. Sometimes a different approach can make all the difference.",
                "🎯 Let's channel that frustration into finding a solution. What's the main issue you're facing?"
            ],
            'anxious': [
                "🌸 I notice you might be feeling anxious. Take a deep breath - you're not alone in this.",
                "🕊️ Anxiety can be overwhelming, but you're stronger than you think. One step at a time.",
                "🧘 When anxiety hits, grounding techniques can help. Focus on what you can control right now.",
                "💚 It's completely normal to feel anxious sometimes. Would you like some strategies to help manage it?"
            ],
            'confused': [
                "🤝 I can see you're feeling confused. Let's break this down together step by step.",
                "💡 Confusion often comes before clarity. What specific part would you like me to explain?",
                "🗺️ It's okay to feel lost sometimes. Let's find your way through this together.",
                "🔍 When things seem unclear, asking the right questions can help. What's puzzling you most?"
            ],
            'confident': [
                "🚀 I love your confidence! That positive energy will take you far.",
                "💫 Your confidence is inspiring! How can I help you channel this energy effectively?",
                "🌟 It's great to see you feeling so sure of yourself! What's your next move?",
                "🔥 That's the spirit! Confidence like yours opens many doors."
            ],
            'tired': [
                "😴 I can tell you're feeling tired. Rest is just as important as productivity.",
                "🌙 Being tired is your body's way of asking for care. Have you been getting enough rest?",
                "☕ Fatigue happens to everyone. Maybe it's time for a break or a change of pace?",
                "🛋️ Sometimes the most productive thing you can do is rest. Listen to your body."
            ]
        }
        
        return response_map.get(emotion, [
            "I'm here to help however I can. How are you feeling right now?",
            "Thank you for sharing with me. What would be most helpful for you today?"
        ])
    
    def _select_contextual_response(self, emotion: str, responses: List[str]) -> str:
        """Select most appropriate response based on context"""
        # Check recent emotion history for patterns
        recent_emotions = [e['primary_emotion'] for e in self.emotion_history[-3:]]
        
        # If user has been consistently in the same emotional state
        if len(recent_emotions) >= 2 and all(e == emotion for e in recent_emotions):
            if emotion in ['sad', 'frustrated', 'anxious']:
                return f"I notice you've been feeling {emotion} for a while. Sometimes talking about it or trying a different approach can help. I'm here to support you."
            elif emotion == 'happy':
                return "I love seeing your continued positive energy! You're really in a great zone."
        
        # Default to rotating through responses
        response_index = len(self.emotion_history) % len(responses)
        return responses[response_index]
    
    def get_mood_trend(self, hours: int = 24) -> Dict[str, Any]:
        """Analyze mood trends over time"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Get recent emotions
            recent_emotions = [
                e for e in self.emotion_history 
                if e['timestamp'] > cutoff_time
            ]
            
            if not recent_emotions:
                return {'status': 'no_recent_data', 'hours_analyzed': hours}
            
            # Analyze trends
            emotion_counts = {}
            total_confidence = 0
            
            for emotion_data in recent_emotions:
                emotion = emotion_data['primary_emotion']
                confidence = emotion_data['confidence']
                
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                total_confidence += confidence
            
            # Determine overall mood
            dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
            avg_confidence = total_confidence / len(recent_emotions)
            
            # Classify mood trend
            positive_emotions = ['happy', 'confident']
            negative_emotions = ['sad', 'frustrated', 'anxious']
            
            positive_count = sum(emotion_counts.get(e, 0) for e in positive_emotions)
            negative_count = sum(emotion_counts.get(e, 0) for e in negative_emotions)
            
            if positive_count > negative_count:
                trend = 'positive'
            elif negative_count > positive_count:
                trend = 'negative'
            else:
                trend = 'neutral'
            
            return {
                'hours_analyzed': hours,
                'total_interactions': len(recent_emotions),
                'dominant_emotion': dominant_emotion,
                'emotion_distribution': emotion_counts,
                'overall_trend': trend,
                'average_confidence': avg_confidence,
                'positive_interactions': positive_count,
                'negative_interactions': negative_count,
                'stability': self._calculate_emotional_stability(recent_emotions)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing mood trend: {e}")
            return {'error': str(e)}
    
    def _calculate_emotional_stability(self, emotions: List[Dict]) -> str:
        """Calculate emotional stability based on emotion changes"""
        if len(emotions) < 3:
            return 'insufficient_data'
        
        # Count emotion changes
        changes = 0
        for i in range(1, len(emotions)):
            if emotions[i]['primary_emotion'] != emotions[i-1]['primary_emotion']:
                changes += 1
        
        change_rate = changes / (len(emotions) - 1)
        
        if change_rate < 0.3:
            return 'stable'
        elif change_rate < 0.6:
            return 'moderate'
        else:
            return 'variable'
    
    def get_emotion_suggestions(self, current_emotion: str) -> List[str]:
        """Get suggestions based on current emotional state"""
        suggestions_map = {
            'sad': [
                "Consider taking a short walk outside - fresh air can help improve mood",
                "Try listening to uplifting music or connecting with a friend",
                "Engage in a small activity you enjoy to lift your spirits",
                "Practice gratitude by thinking of three things you're thankful for"
            ],
            'frustrated': [
                "Take a few deep breaths and step away from the problem briefly",
                "Try breaking the issue into smaller, manageable parts",
                "Consider a different approach or ask for help if needed",
                "Physical exercise can help release frustration in a healthy way"
            ],
            'anxious': [
                "Practice the 5-4-3-2-1 grounding technique: 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
                "Try some deep breathing exercises or meditation",
                "Focus on what you can control and let go of what you can't",
                "Consider writing down your worries to externalize them"
            ],
            'tired': [
                "Consider taking a short power nap (15-20 minutes) if possible",
                "Make sure you're staying hydrated and eating nutritious food",
                "Take breaks from screen time and go outside for natural light",
                "Plan for better sleep tonight - good rest is crucial"
            ],
            'confused': [
                "Break down complex problems into smaller, clearer parts",
                "Don't hesitate to ask questions - clarity comes through inquiry",
                "Try explaining the problem to someone else (or even to yourself out loud)",
                "Research from multiple sources to gain different perspectives"
            ]
        }
        
        return suggestions_map.get(current_emotion, [
            "Stay mindful of your emotional state and be kind to yourself",
            "Remember that all emotions are temporary and serve a purpose",
            "Consider what might help you feel more balanced right now"
        ])
    
    def route(self, text: str) -> Optional[str]:
        """Main routing method for emotion-related requests"""
        try:
            text_lower = text.lower()
            
            # Analyze emotion in the text
            emotion_data = self.analyze_emotion(text)
            
            # Check if user is asking about emotions directly
            if any(phrase in text_lower for phrase in ['how am i feeling', 'my mood', 'emotional state', 'analyze my emotion']):
                return self._provide_emotion_analysis(emotion_data)
            
            # Check if user wants mood suggestions
            if any(phrase in text_lower for phrase in ['mood suggestions', 'feel better', 'emotional help']):
                return self._provide_mood_suggestions(emotion_data)
            
            # Provide empathetic response for strong emotions
            if emotion_data['confidence'] > 0.5:
                empathetic_response = self.get_empathetic_response(emotion_data)
                if empathetic_response:
                    return empathetic_response
            
            return None
            
        except Exception as e:
            logger.error(f"Error in emotion routing: {e}")
            return f"I'm having trouble analyzing emotions right now: {e}"
    
    def _provide_emotion_analysis(self, emotion_data: Dict[str, Any]) -> str:
        """Provide detailed emotion analysis"""
        emotion = emotion_data['primary_emotion']
        confidence = emotion_data['confidence']
        
        analysis = f"Based on your message, I detect that you're feeling primarily **{emotion}**"
        
        if confidence > 0.7:
            analysis += " with high confidence."
        elif confidence > 0.4:
            analysis += " with moderate confidence."
        else:
            analysis += ", though the signals are subtle."
        
        # Add other detected emotions
        other_emotions = {k: v for k, v in emotion_data['all_emotions'].items() if k != emotion and v > 0.2}
        if other_emotions:
            other_list = ', '.join(other_emotions.keys())
            analysis += f" I also detect some traces of: {other_list}."
        
        # Add trend analysis
        trend_data = self.get_mood_trend(6)  # Last 6 hours
        if trend_data.get('total_interactions', 0) > 1:
            analysis += f"\n\nOver the past few hours, your overall emotional trend has been **{trend_data['overall_trend']}**."
        
        return analysis
    
    def _provide_mood_suggestions(self, emotion_data: Dict[str, Any]) -> str:
        """Provide mood-based suggestions"""
        emotion = emotion_data['primary_emotion']
        suggestions = self.get_emotion_suggestions(emotion)
        
        response = f"Based on your current emotional state ({emotion}), here are some suggestions that might help:\n\n"
        
        for i, suggestion in enumerate(suggestions[:3], 1):
            response += f"{i}. {suggestion}\n"
        
        response += "\nRemember, it's completely normal to experience different emotions. You're doing great by being aware of how you feel! 💙"
        
        return response

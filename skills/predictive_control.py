"""
Predictive Control Skill - Behavior Prediction and Suggestions
Analyzes user patterns to predict and suggest next actions
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json
import re

logger = logging.getLogger(__name__)

class Predictor:
    """
    Predictive Control system that learns user patterns and suggests actions
    """
    
    def __init__(self, digital_twin):
        self.twin = digital_twin
        self.prediction_confidence_threshold = 0.6
        
    def suggest(self, current_input: str) -> Optional[str]:
        """Generate predictive suggestions based on user patterns"""
        try:
            # Get user patterns and context
            patterns = self.twin.analyze_patterns() if self.twin else {}
            recent_context = self.twin.get_recent_context(10) if self.twin else []
            
            # Analyze current input
            input_analysis = self._analyze_input(current_input)
            
            # Generate predictions
            predictions = self._generate_predictions(input_analysis, patterns, recent_context)
            
            # Select best prediction
            best_prediction = self._select_best_prediction(predictions)
            
            if best_prediction and best_prediction['confidence'] > self.prediction_confidence_threshold:
                return self._format_suggestion(best_prediction)
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating prediction: {e}")
            return None
    
    def _analyze_input(self, input_text: str) -> Dict[str, Any]:
        """Analyze the current input for patterns"""
        analysis = {
            'intent': 'unknown',
            'entities': [],
            'context_type': 'general',
            'urgency': 'normal',
            'complexity': 'medium'
        }
        
        input_lower = input_text.lower()
        
        # Intent detection
        if any(word in input_lower for word in ['open', 'launch', 'start']):
            analysis['intent'] = 'launch_application'
        elif any(word in input_lower for word in ['create', 'make', 'generate']):
            analysis['intent'] = 'create_content'
        elif any(word in input_lower for word in ['find', 'search', 'look']):
            analysis['intent'] = 'search_information'
        elif any(word in input_lower for word in ['help', 'how', 'what', 'explain']):
            analysis['intent'] = 'get_help'
        elif any(word in input_lower for word in ['study', 'learn', 'practice']):
            analysis['intent'] = 'educational'
        
        # Entity extraction (simple keyword-based)
        entities = []
        if 'youtube' in input_lower:
            entities.append('youtube')
        if 'google' in input_lower:
            entities.append('google')
        if any(word in input_lower for word in ['calculator', 'math', 'calculate']):
            entities.append('calculator')
        if any(word in input_lower for word in ['note', 'text', 'write']):
            entities.append('text_editor')
        
        analysis['entities'] = entities
        
        # Context type
        if any(word in input_lower for word in ['work', 'job', 'meeting', 'email']):
            analysis['context_type'] = 'work'
        elif any(word in input_lower for word in ['study', 'homework', 'research', 'learn']):
            analysis['context_type'] = 'study'
        elif any(word in input_lower for word in ['game', 'play', 'fun', 'entertainment']):
            analysis['context_type'] = 'entertainment'
        
        # Complexity assessment
        word_count = len(input_text.split())
        if word_count > 15:
            analysis['complexity'] = 'high'
        elif word_count < 5:
            analysis['complexity'] = 'low'
        
        return analysis
    
    def _generate_predictions(self, input_analysis: Dict, patterns: Dict, context: List) -> List[Dict]:
        """Generate possible predictions based on analysis"""
        predictions = []
        
        # Pattern-based predictions
        if patterns.get('top_requests'):
            for request, frequency in patterns['top_requests'][:5]:
                if request in input_analysis.get('entities', []):
                    predictions.append({
                        'type': 'pattern_match',
                        'suggestion': f"Based on your history, you might want to {request}",
                        'confidence': min(0.9, frequency / 10.0),
                        'reasoning': 'frequent_usage'
                    })
        
        # Intent-based predictions
        intent = input_analysis['intent']
        if intent == 'launch_application':
            predictions.extend(self._predict_application_workflow(input_analysis, context))
        elif intent == 'create_content':
            predictions.extend(self._predict_content_workflow(input_analysis, context))
        elif intent == 'educational':
            predictions.extend(self._predict_study_workflow(input_analysis, context))
        
        # Time-based predictions
        current_hour = datetime.now().hour
        time_predictions = self._predict_time_based_actions(current_hour, patterns)
        predictions.extend(time_predictions)
        
        # Context-based predictions
        context_predictions = self._predict_context_actions(input_analysis, context)
        predictions.extend(context_predictions)
        
        return predictions
    
    def _predict_application_workflow(self, analysis: Dict, context: List) -> List[Dict]:
        """Predict follow-up actions for application launches"""
        predictions = []
        
        entities = analysis.get('entities', [])
        
        if 'youtube' in entities:
            predictions.append({
                'type': 'workflow_prediction',
                'suggestion': "After opening YouTube, you might want to search for educational content or music",
                'confidence': 0.7,
                'reasoning': 'common_workflow'
            })
        
        if 'calculator' in entities:
            predictions.append({
                'type': 'workflow_prediction', 
                'suggestion': "You might also need to open a notepad to record calculations",
                'confidence': 0.6,
                'reasoning': 'complementary_tools'
            })
        
        if 'text_editor' in entities:
            predictions.append({
                'type': 'workflow_prediction',
                'suggestion': "Consider opening a file manager to locate or save documents",
                'confidence': 0.5,
                'reasoning': 'complementary_tools'
            })
        
        return predictions
    
    def _predict_content_workflow(self, analysis: Dict, context: List) -> List[Dict]:
        """Predict actions for content creation"""
        predictions = []
        
        if analysis['context_type'] == 'study':
            predictions.append({
                'type': 'content_prediction',
                'suggestion': "For study content, consider creating flashcards or mind maps",
                'confidence': 0.8,
                'reasoning': 'educational_best_practice'
            })
        
        if analysis['context_type'] == 'work':
            predictions.append({
                'type': 'content_prediction',
                'suggestion': "For work content, you might need presentation or document templates",
                'confidence': 0.7,
                'reasoning': 'professional_workflow'
            })
        
        return predictions
    
    def _predict_study_workflow(self, analysis: Dict, context: List) -> List[Dict]:
        """Predict study-related follow-up actions"""
        predictions = []
        
        # Check recent study activity
        recent_study_topics = set()
        for conv in context:
            if conv['role'] == 'user' and any(word in conv['content'].lower() for word in ['study', 'learn', 'flashcard']):
                # Extract potential topics (simplified)
                words = conv['content'].split()
                for word in words:
                    if len(word) > 4 and word.isalpha():
                        recent_study_topics.add(word.lower())
        
        if recent_study_topics:
            predictions.append({
                'type': 'study_continuation',
                'suggestion': f"Continue studying {', '.join(list(recent_study_topics)[:3])} or test your knowledge with a quiz",
                'confidence': 0.8,
                'reasoning': 'study_continuity'
            })
        
        predictions.append({
            'type': 'study_enhancement',
            'suggestion': "Consider creating a concept map to visualize connections between topics",
            'confidence': 0.6,
            'reasoning': 'learning_technique'
        })
        
        return predictions
    
    def _predict_time_based_actions(self, hour: int, patterns: Dict) -> List[Dict]:
        """Predict actions based on time of day"""
        predictions = []
        
        # Most active hour pattern
        most_active_hour = patterns.get('most_active_hour', 12)
        
        # Morning predictions (6-12)
        if 6 <= hour <= 12:
            predictions.append({
                'type': 'time_based',
                'suggestion': "Good morning! You might want to check your calendar or plan your day",
                'confidence': 0.5,
                'reasoning': 'morning_routine'
            })
        
        # Afternoon predictions (12-18)
        elif 12 <= hour <= 18:
            if hour == most_active_hour:
                predictions.append({
                    'type': 'time_based',
                    'suggestion': "This is typically your most active time. Perfect for focused work or study",
                    'confidence': 0.7,
                    'reasoning': 'peak_activity_time'
                })
        
        # Evening predictions (18-22)
        elif 18 <= hour <= 22:
            predictions.append({
                'type': 'time_based',
                'suggestion': "Evening time - good for reviewing the day or preparing for tomorrow",
                'confidence': 0.5,
                'reasoning': 'evening_routine'
            })
        
        return predictions
    
    def _predict_context_actions(self, analysis: Dict, context: List) -> List[Dict]:
        """Predict based on conversation context"""
        predictions = []
        
        # Look for unfinished conversations or topics
        if context:
            last_assistant_msg = None
            for conv in reversed(context):
                if conv['role'] == 'assistant':
                    last_assistant_msg = conv['content']
                    break
            
            if last_assistant_msg:
                # If last response was incomplete or suggestive
                if any(phrase in last_assistant_msg.lower() for phrase in ['would you like', 'you might', 'consider']):
                    predictions.append({
                        'type': 'context_follow_up',
                        'suggestion': "You might want to follow up on the previous suggestion",
                        'confidence': 0.6,
                        'reasoning': 'incomplete_interaction'
                    })
        
        return predictions
    
    def _select_best_prediction(self, predictions: List[Dict]) -> Optional[Dict]:
        """Select the best prediction from available options"""
        if not predictions:
            return None
        
        # Sort by confidence and reasoning quality
        scored_predictions = []
        for pred in predictions:
            score = pred['confidence']
            
            # Boost score for certain reasoning types
            if pred['reasoning'] in ['frequent_usage', 'peak_activity_time']:
                score += 0.1
            elif pred['reasoning'] in ['educational_best_practice', 'study_continuity']:
                score += 0.05
            
            scored_predictions.append((score, pred))
        
        # Return highest scoring prediction
        scored_predictions.sort(key=lambda x: x[0], reverse=True)
        return scored_predictions[0][1] if scored_predictions else None
    
    def _format_suggestion(self, prediction: Dict) -> str:
        """Format prediction as user-friendly suggestion"""
        suggestion = prediction['suggestion']
        confidence = prediction['confidence']
        
        # Add confidence indicator
        if confidence > 0.8:
            prefix = "💡 Suggestion: "
        elif confidence > 0.6:
            prefix = "🤔 You might consider: "
        else:
            prefix = "💭 Perhaps: "
        
        return f"{prefix}{suggestion}"
    
    def learn_from_interaction(self, user_input: str, user_action: str, success: bool):
        """Learn from user interactions to improve predictions"""
        try:
            # This would update prediction models based on user feedback
            # For now, we'll log the interaction for future model training
            
            learning_data = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'user_action': user_action,
                'success': success,
                'context': 'prediction_learning'
            }
            
            if self.twin:
                self.twin.db.record_metric('prediction_accuracy', 1.0 if success else 0.0, learning_data)
            
            logger.info(f"Learned from interaction - Success: {success}")
            
        except Exception as e:
            logger.error(f"Error learning from interaction: {e}")
    
    def get_prediction_stats(self) -> Dict[str, Any]:
        """Get statistics about prediction performance"""
        try:
            if not self.twin:
                return {'error': 'No digital twin available'}
            
            # Get recent prediction metrics
            metrics = self.twin.db.get_metrics('prediction_accuracy', 24)
            
            if not metrics:
                return {'status': 'no_data', 'total_predictions': 0}
            
            accuracy_values = [value for _, value in metrics]
            
            stats = {
                'total_predictions': len(accuracy_values),
                'accuracy_rate': sum(accuracy_values) / len(accuracy_values) if accuracy_values else 0,
                'confidence_threshold': self.prediction_confidence_threshold,
                'last_24h_predictions': len(accuracy_values)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting prediction stats: {e}")
            return {'error': str(e)}

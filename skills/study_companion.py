"""
Study Companion Skill - Educational Learning Assistant
Provides comprehensive study assistance, flashcards, and learning support
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json
import re

logger = logging.getLogger(__name__)

class StudyCompanion:
    """
    Study Companion system for educational assistance and learning support
    Provides flashcards, study planning, progress tracking, and learning techniques
    """
    
    def __init__(self, digital_twin):
        self.twin = digital_twin
        self.study_sessions = []
        self.flashcard_sets = {}
        self.study_goals = {}
        self.learning_preferences = {}
        
        # Study techniques and methods
        self.study_techniques = {
            'flashcards': {
                'description': 'Spaced repetition memory cards',
                'best_for': ['vocabulary', 'definitions', 'facts', 'formulas'],
                'time_needed': '15-30 minutes',
                'effectiveness': 'high'
            },
            'active_recall': {
                'description': 'Testing yourself without looking at notes',
                'best_for': ['concepts', 'problem_solving', 'critical thinking'],
                'time_needed': '20-45 minutes',
                'effectiveness': 'very_high'
            },
            'spaced_repetition': {
                'description': 'Reviewing material at increasing intervals',
                'best_for': ['long_term_retention', 'exam_preparation'],
                'time_needed': 'varies',
                'effectiveness': 'very_high'
            },
            'pomodoro': {
                'description': '25-minute focused study sessions with breaks',
                'best_for': ['concentration', 'avoiding_burnout', 'productivity'],
                'time_needed': '25 minutes + 5 minute break',
                'effectiveness': 'high'
            },
            'mind_mapping': {
                'description': 'Visual representation of information connections',
                'best_for': ['visual_learners', 'complex_topics', 'overview'],
                'time_needed': '30-60 minutes',
                'effectiveness': 'high'
            },
            'practice_testing': {
                'description': 'Taking practice exams and quizzes',
                'best_for': ['exam_preparation', 'identifying_gaps', 'confidence'],
                'time_needed': '30-90 minutes',
                'effectiveness': 'very_high'
            }
        }
        
        # Subject categories
        self.subject_categories = {
            'stem': ['mathematics', 'physics', 'chemistry', 'biology', 'computer_science', 'engineering'],
            'languages': ['english', 'spanish', 'french', 'german', 'chinese', 'japanese'],
            'humanities': ['history', 'philosophy', 'literature', 'art', 'music', 'religion'],
            'social_sciences': ['psychology', 'sociology', 'economics', 'political_science', 'anthropology'],
            'business': ['accounting', 'finance', 'marketing', 'management', 'entrepreneurship'],
            'health': ['medicine', 'nursing', 'pharmacy', 'dentistry', 'public_health']
        }
    
    def route(self, text: str) -> str:
        """Route study companion requests"""
        try:
            text_lower = text.lower()
            
            # Flashcard creation and management
            if any(phrase in text_lower for phrase in ['flashcard', 'flash card', 'memory card']):
                return self._handle_flashcard_request(text)
            
            # Study planning and scheduling
            elif any(phrase in text_lower for phrase in ['study plan', 'study schedule', 'learning plan']):
                return self._handle_study_planning(text)
            
            # Learning technique recommendations
            elif any(phrase in text_lower for phrase in ['study technique', 'learning method', 'how to study']):
                return self._provide_study_techniques(text)
            
            # Progress tracking and analytics
            elif any(phrase in text_lower for phrase in ['study progress', 'learning analytics', 'study stats']):
                return self._provide_progress_tracking()
            
            # Quiz and practice testing
            elif any(phrase in text_lower for phrase in ['quiz', 'practice test', 'test me']):
                return self._handle_practice_testing(text)
            
            # Note-taking and organization
            elif any(phrase in text_lower for phrase in ['note taking', 'organize notes', 'study notes']):
                return self._provide_note_taking_guidance()
            
            # Subject-specific study help
            elif any(phrase in text_lower for phrase in ['math', 'science', 'history', 'language']):
                return self._provide_subject_specific_help(text)
            
            # General study assistance
            else:
                return self._provide_study_overview()
                
        except Exception as e:
            logger.error(f"Error in study companion routing: {e}")
            return f"Study companion error: {e}"
    
    def _handle_flashcard_request(self, text: str) -> str:
        """Handle flashcard creation and management"""
        try:
            # Extract topic from text
            topic = self._extract_topic_from_text(text)
            
            if 'create' in text.lower() or 'make' in text.lower():
                return self._create_flashcards(topic)
            elif 'review' in text.lower() or 'practice' in text.lower():
                return self._review_flashcards(topic)
            else:
                return self._provide_flashcard_overview()
                
        except Exception as e:
            logger.error(f"Error handling flashcard request: {e}")
            return f"Flashcard error: {e}"
    
    def _create_flashcards(self, topic: str) -> str:
        """Create flashcards for a specific topic"""
        try:
            # Use AI to generate flashcards
            from core.knowledge import generate_flashcards
            
            flashcards = generate_flashcards(topic, count=10)
            
            if not flashcards:
                return self._provide_manual_flashcard_guidance(topic)
            
            # Store flashcards
            flashcard_set_id = f"flashcards_{datetime.now().timestamp()}"
            self.flashcard_sets[flashcard_set_id] = {
                'topic': topic,
                'cards': flashcards,
                'created_at': datetime.now().isoformat(),
                'study_count': 0,
                'mastery_level': 0.0
            }
            
            # Format response
            response = f"📚 **Flashcards Created for {topic.title()}**\n\n"
            response += f"**Generated {len(flashcards)} flashcards:**\n\n"
            
            for i, card in enumerate(flashcards[:3], 1):  # Show first 3 as preview
                response += f"**Card {i}:**\n"
                response += f"Q: {card['question']}\n"
                response += f"A: {card['answer']}\n\n"
            
            if len(flashcards) > 3:
                response += f"...and {len(flashcards) - 3} more cards.\n\n"
            
            response += "**Study Options:**\n"
            response += "- Say 'review flashcards' to start studying\n"
            response += "- Say 'flashcard quiz' for spaced repetition\n"
            response += "- Say 'study progress' to track mastery\n\n"
            
            response += "**Study Tips:**\n"
            response += "✅ Review regularly for best retention\n"
            response += "✅ Focus on cards you find difficult\n"
            response += "✅ Use spaced repetition for long-term memory\n"
            response += "✅ Test yourself before looking at answers"
            
            return response
            
        except Exception as e:
            logger.error(f"Error creating flashcards: {e}")
            return self._provide_manual_flashcard_guidance(topic)
    
    def _provide_manual_flashcard_guidance(self, topic: str) -> str:
        """Provide guidance for manual flashcard creation"""
        return f"""📚 **Flashcard Creation Guide for {topic.title()}**

**Manual Flashcard Creation:**

**🎯 Effective Flashcard Principles:**

**Question Types:**
- **Definition Cards:** "What is [term]?" → Definition
- **Example Cards:** "Give an example of [concept]" → Example
- **Application Cards:** "How would you use [concept]?" → Application
- **Comparison Cards:** "What's the difference between X and Y?" → Differences

**📝 Creating Quality Flashcards:**

**Front Side (Question) Best Practices:**
✅ Keep questions clear and specific
✅ Use simple, direct language
✅ Include context when needed
✅ Make questions testable
✅ Avoid yes/no questions

**Back Side (Answer) Best Practices:**
✅ Provide complete but concise answers
✅ Include key details and examples
✅ Use consistent formatting
✅ Add memory aids or mnemonics
✅ Include related concepts when relevant

**📊 Topic-Specific Suggestions for {topic.title()}:**

**If studying Science/Math:**
- Formula cards: "What is the formula for [concept]?"
- Process cards: "What are the steps to [procedure]?"
- Problem-solving cards: "How do you solve [type of problem]?"

**If studying Languages:**
- Vocabulary cards: "[foreign word]" → "English translation"
- Grammar cards: "How do you form [grammar rule]?"
- Phrase cards: "How do you say [phrase] in [language]?"

**If studying History/Social Studies:**
- Date cards: "When did [event] occur?"
- Cause-effect cards: "What caused [event]?"
- People cards: "Who was [person] and why were they important?"

**If studying Literature:**
- Character cards: "Who is [character] in [work]?"
- Theme cards: "What is the theme of [work]?"
- Quote cards: "Who said '[quote]' and in what context?"

**🔄 Study Method:**

**Spaced Repetition Schedule:**
- Day 1: Learn new cards
- Day 2: Review all cards
- Day 4: Review difficult cards
- Day 7: Review all cards
- Day 14: Review difficult cards
- Day 30: Final review

**Active Recall Technique:**
1. Read the question
2. Think of the answer without looking
3. Check your answer
4. Rate difficulty (Easy/Medium/Hard)
5. Adjust review frequency based on difficulty

**📱 Digital Flashcard Tools:**
- Anki (advanced spaced repetition)
- Quizlet (user-friendly, collaborative)
- Brainscape (cognitive science-based)
- RemNote (note-taking + flashcards)

**🎯 Study Session Structure:**
1. **Warm-up (5 min):** Review easy cards
2. **Main Study (20 min):** Focus on difficult cards
3. **Cool-down (5 min):** Quick review of all cards

**📊 Tracking Progress:**
- Keep track of cards mastered
- Note which topics need more review
- Adjust study frequency based on retention
- Celebrate learning milestones

Would you like help creating specific flashcards for any particular aspect of {topic}?"""
    
    def _review_flashcards(self, topic: str = None) -> str:
        """Review existing flashcards"""
        if not self.flashcard_sets:
            return """📚 **No Flashcards Available**

You haven't created any flashcards yet. Would you like to:
- Create flashcards for a specific topic
- Learn how to make effective flashcards
- Explore other study techniques

Say something like "create flashcards for [topic]" to get started!"""
        
        # Find relevant flashcard sets
        relevant_sets = []
        if topic:
            for set_id, flashcard_set in self.flashcard_sets.items():
                if topic.lower() in flashcard_set['topic'].lower():
                    relevant_sets.append((set_id, flashcard_set))
        else:
            relevant_sets = list(self.flashcard_sets.items())
        
        if not relevant_sets:
            return f"No flashcards found for topic '{topic}'. Available topics: {', '.join([fs['topic'] for fs in self.flashcard_sets.values()])}"
        
        # Select first relevant set for review
        set_id, flashcard_set = relevant_sets[0]
        cards = flashcard_set['cards']
        
        response = f"""📚 **Flashcard Review: {flashcard_set['topic'].title()}**

**Study Session Starting...**

**Set Statistics:**
- Total Cards: {len(cards)}
- Times Studied: {flashcard_set['study_count']}
- Mastery Level: {flashcard_set['mastery_level']:.1%}

**📝 Sample Cards for Review:**

"""
        
        # Show 3 sample cards
        for i, card in enumerate(cards[:3], 1):
            response += f"**Card {i}:**\n"
            response += f"❓ **Question:** {card['question']}\n"
            response += f"💡 **Answer:** {card['answer']}\n\n"
        
        response += """**🎯 Study Instructions:**

**Active Recall Method:**
1. Read each question carefully
2. Think of the answer before revealing it
3. Compare your answer with the correct one
4. Rate yourself: ✅ Easy | 🟡 Medium | ❌ Hard

**Spaced Repetition:**
- Focus more time on cards you rate as Hard
- Review Easy cards less frequently
- Medium cards need regular practice

**Study Tips:**
- Cover the answer while thinking
- Say answers out loud when possible
- Connect new information to what you know
- Use mnemonics for difficult items

**Next Steps:**
- Continue with remaining cards
- Track which cards need more review
- Schedule follow-up study sessions
- Consider creating additional cards for weak areas

Ready to continue studying? Say 'next card' or 'quiz me' to proceed!"""
        
        # Update study count
        flashcard_set['study_count'] += 1
        flashcard_set['last_studied'] = datetime.now().isoformat()
        
        return response
    
    def _provide_flashcard_overview(self) -> str:
        """Provide overview of flashcard functionality"""
        return """📚 **Flashcard Study System**

**What Are Flashcards?**
Flashcards are a powerful study tool using active recall and spaced repetition to help you memorize and understand information effectively.

**🎯 When to Use Flashcards:**

**Perfect For:**
✅ Vocabulary and definitions
✅ Facts and dates
✅ Formulas and equations
✅ Language learning
✅ Medical terminology
✅ Historical events
✅ Scientific processes

**Less Ideal For:**
❌ Complex problem-solving
❌ Essay writing skills
❌ Creative thinking
❌ Long explanations
❌ Practical skills

**🔬 Science Behind Flashcards:**

**Active Recall:**
- Forces your brain to retrieve information
- Strengthens memory pathways
- Identifies knowledge gaps
- More effective than passive reading

**Spaced Repetition:**
- Reviews information at optimal intervals
- Fights the forgetting curve
- Maximizes long-term retention
- Efficiently uses study time

**📊 Flashcard Commands:**

**Creation:**
- "Create flashcards for [topic]"
- "Make flashcards about [subject]"
- "Generate memory cards for [concept]"

**Review:**
- "Review flashcards"
- "Study my flashcards"
- "Quiz me on [topic]"

**Management:**
- "Show my flashcard sets"
- "Delete flashcards for [topic]"
- "Update flashcards"

**🎯 Flashcard Best Practices:**

**Creating Effective Cards:**
- One concept per card
- Clear, specific questions
- Complete but concise answers
- Include examples when helpful
- Use images when possible

**Studying Effectively:**
- Regular, short sessions (15-30 min)
- Mix old and new cards
- Focus on difficult cards
- Use the rating system
- Take breaks to avoid fatigue

**📈 Progress Tracking:**
- Mastery percentages for each set
- Study frequency analytics
- Difficult card identification
- Long-term retention metrics
- Study streak tracking

**🚀 Getting Started:**
Ready to create your first flashcard set? Just tell me:
- What subject you're studying
- Specific topics you want to focus on
- How many cards you'd like to start with

Example: "Create flashcards for biology cell structure"

**Advanced Features:**
- Spaced repetition scheduling
- Difficulty-based card sorting
- Progress analytics and insights
- Custom card templates
- Collaborative study sets

What topic would you like to create flashcards for?"""
    
    def _handle_study_planning(self, text: str) -> str:
        """Handle study planning and scheduling"""
        return """📅 **Study Planning & Scheduling**

**Creating Your Personalized Study Plan:**

**🎯 Study Plan Components:**

**Goal Setting:**
- **Short-term goals** (daily/weekly targets)
- **Medium-term goals** (monthly objectives)
- **Long-term goals** (semester/year outcomes)
- **SMART criteria** (Specific, Measurable, Achievable, Relevant, Time-bound)

**Time Management:**
- **Available study hours** per day/week
- **Peak performance times** (when you focus best)
- **Break scheduling** (Pomodoro, longer breaks)
- **Deadline tracking** (exams, assignments, projects)

**Subject Prioritization:**
- **Difficulty assessment** (hardest subjects get more time)
- **Importance ranking** (critical vs. supplementary)
- **Interest level** (balance challenging with enjoyable)
- **Upcoming deadlines** (urgent vs. important matrix)

**📊 Study Schedule Templates:**

**Daily Study Schedule:**

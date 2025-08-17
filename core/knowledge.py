"""
Nova AI Assistant - Knowledge Processing Module
Handles AI interactions, knowledge retrieval, and intelligent responses
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
import traceback

# AI provider imports with graceful fallbacks
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config import (
    OPENAI_API_KEY, 
    ANTHROPIC_API_KEY,
    DEFAULT_AI_PROVIDER,
    OPENAI_MODEL,
    ANTHROPIC_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    AI_TIMEOUT
)

# Configure logging
logger = logging.getLogger(__name__)

# Global AI client instances
_openai_client = None
_anthropic_client = None
_active_provider = None

def initialize_ai_backend():
    """Initialize AI backend clients based on available API keys"""
    global _openai_client, _anthropic_client, _active_provider
    
    # Initialize OpenAI client
    if OPENAI_API_KEY and OPENAI_AVAILABLE:
        try:
            _openai_client = OpenAI(api_key=OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            _openai_client = None
    
    # Initialize Anthropic client  
    if ANTHROPIC_API_KEY and ANTHROPIC_AVAILABLE:
        try:
            _anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            logger.info("Anthropic client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            _anthropic_client = None
    
    # Determine active provider
    if DEFAULT_AI_PROVIDER == "anthropic" and _anthropic_client:
        _active_provider = "anthropic"
    elif DEFAULT_AI_PROVIDER == "openai" and _openai_client:
        _active_provider = "openai"
    elif _anthropic_client:
        _active_provider = "anthropic"
    elif _openai_client:
        _active_provider = "openai"
    else:
        _active_provider = None
        logger.warning("No AI providers available")

def get_answer(query: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Get an intelligent response to a user query using available AI providers
    
    Args:
        query: User's question or command
        context: Optional context information for better responses
        
    Returns:
        AI-generated response string
    """
    if not query or not query.strip():
        return "Please provide a question or command."
    
    if not _active_provider:
        return "I'm sorry, but I don't have access to an AI backend right now. Please check your API key configuration."
    
    try:
        # Prepare the prompt with context
        enhanced_query = _prepare_query(query, context)
        
        # Route to appropriate AI provider
        if _active_provider == "anthropic":
            return _get_anthropic_response(enhanced_query)
        elif _active_provider == "openai":
            return _get_openai_response(enhanced_query)
        else:
            return "No AI provider available."
            
    except Exception as e:
        logger.error(f"Error getting AI response: {e}\n{traceback.format_exc()}")
        return f"I encountered an error processing your request: {str(e)}"

def _prepare_query(query: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Prepare the query with system context and instructions"""
    
    system_prompt = """You are Nova, an advanced AI assistant with comprehensive capabilities. 
You are helpful, knowledgeable, and always strive to provide accurate, detailed responses.

Key guidelines:
- Be conversational but professional
- Provide specific, actionable advice when possible
- If you're uncertain, say so clearly
- For technical topics, explain at an appropriate level
- Always prioritize user safety and privacy

If the user asks about your capabilities, mention that you can help with:
- General knowledge and research
- Study assistance and flashcards
- Writing and communication
- Problem-solving and analysis
- Technical questions and coding
- Creative tasks and brainstorming"""

    if context:
        context_str = f"\nContext: {json.dumps(context, indent=2)}\n"
        return f"{system_prompt}\n{context_str}\nUser: {query}"
    else:
        return f"{system_prompt}\n\nUser: {query}"

def _get_anthropic_response(query: str) -> str:
    """Get response from Anthropic Claude"""
    try:
        # The newest Anthropic model is "claude-sonnet-4-20250514", not "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022" nor "claude-3-sonnet-20240229"
        message = _anthropic_client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        
        return message.content[0].text.strip()
        
    except Exception as e:
        logger.error(f"Anthropic API error: {e}")
        raise Exception(f"Anthropic API error: {str(e)}")

def _get_openai_response(query: str) -> str:
    """Get response from OpenAI GPT"""
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = _openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "user", 
                    "content": query
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            timeout=AI_TIMEOUT
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise Exception(f"OpenAI API error: {str(e)}")

def analyze_intent(query: str) -> Dict[str, Any]:
    """
    Analyze user intent to better route requests
    
    Returns:
        Dictionary with intent analysis results
    """
    query_lower = query.lower()
    
    intent_analysis = {
        "primary_intent": "general",
        "confidence": 0.5,
        "entities": [],
        "suggested_skill": None
    }
    
    # Study-related intents
    if any(keyword in query_lower for keyword in ["flashcard", "study", "learn", "quiz", "test"]):
        intent_analysis.update({
            "primary_intent": "study",
            "confidence": 0.8,
            "suggested_skill": "study_companion"
        })
    
    # Control/automation intents
    elif any(keyword in query_lower for keyword in ["open", "close", "launch", "start", "stop"]):
        intent_analysis.update({
            "primary_intent": "control",
            "confidence": 0.9,
            "suggested_skill": "pc_control"
        })
    
    # Research intents
    elif any(keyword in query_lower for keyword in ["research", "analyze", "investigate", "summarize"]):
        intent_analysis.update({
            "primary_intent": "research", 
            "confidence": 0.7,
            "suggested_skill": "deep_research"
        })
    
    # Security intents
    elif any(keyword in query_lower for keyword in ["threat", "security", "breach", "scan"]):
        intent_analysis.update({
            "primary_intent": "security",
            "confidence": 0.8,
            "suggested_skill": "threat_mode"
        })
    
    return intent_analysis

def get_knowledge_summary() -> Dict[str, Any]:
    """Get summary of knowledge capabilities and status"""
    return {
        "ai_providers": {
            "anthropic": {
                "available": ANTHROPIC_AVAILABLE and bool(ANTHROPIC_API_KEY),
                "active": _active_provider == "anthropic",
                "model": ANTHROPIC_MODEL
            },
            "openai": {
                "available": OPENAI_AVAILABLE and bool(OPENAI_API_KEY),
                "active": _active_provider == "openai", 
                "model": OPENAI_MODEL
            }
        },
        "active_provider": _active_provider,
        "settings": {
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "timeout": AI_TIMEOUT
        },
        "capabilities": [
            "General knowledge queries",
            "Technical assistance", 
            "Creative writing",
            "Problem solving",
            "Research assistance",
            "Educational support"
        ]
    }

# Specialized knowledge functions

def generate_flashcards(topic: str, count: int = 5) -> List[Dict[str, str]]:
    """Generate flashcards for a given topic"""
    try:
        prompt = f"""Create {count} educational flashcards about {topic}. 
        
Return the response as a JSON array where each flashcard has 'question' and 'answer' fields.
Make the questions challenging but fair, and answers comprehensive but concise.

Example format:
[
    {{"question": "What is...", "answer": "The answer is..."}},
    ...
]"""
        
        response = get_answer(prompt)
        
        # Try to parse JSON response
        try:
            # Extract JSON from response if it's wrapped in markdown
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "[" in response and "]" in response:
                json_start = response.find("[")
                json_end = response.rfind("]") + 1
                json_str = response[json_start:json_end]
            else:
                json_str = response
            
            flashcards = json.loads(json_str)
            return flashcards if isinstance(flashcards, list) else []
            
        except json.JSONDecodeError:
            # Fallback: parse manually or return simple cards
            return [{"question": f"Study question about {topic}", "answer": response}]
            
    except Exception as e:
        logger.error(f"Error generating flashcards: {e}")
        return [{"question": f"What should I know about {topic}?", "answer": "Unable to generate flashcards at this time."}]

def summarize_text(text: str, max_length: int = 200) -> str:
    """Summarize a long text into a concise summary"""
    try:
        prompt = f"""Please provide a concise summary of the following text in about {max_length} characters:

{text}

Summary:"""
        
        return get_answer(prompt)
        
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return "Unable to summarize text at this time."

def explain_concept(concept: str, level: str = "intermediate") -> str:
    """Explain a concept at the specified level"""
    try:
        prompt = f"""Please explain the concept of "{concept}" at a {level} level.
        
Guidelines:
- If beginner: Use simple language, avoid jargon, include examples
- If intermediate: Balance detail with clarity, some technical terms OK
- If advanced: Be comprehensive, use appropriate terminology

Explanation:"""
        
        return get_answer(prompt)
        
    except Exception as e:
        logger.error(f"Error explaining concept: {e}")
        return f"Unable to explain {concept} at this time."

# Initialize on module import
try:
    initialize_ai_backend()
except Exception as e:
    logger.error(f"Failed to initialize AI backend on import: {e}")

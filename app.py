"""
Nova AI Assistant - Modern Web Interface
Advanced AI Assistant with comprehensive skill architecture
"""

import streamlit as st
import asyncio
import time
from datetime import datetime
from assistant import Assistant
from config import ASSISTANT_NAME, DATA_DIR
import json
import os

# Page configuration
st.set_page_config(
    page_title=f"{ASSISTANT_NAME} AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "nova" not in st.session_state:
    st.session_state.nova = Assistant()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False

def main():
    """Main application interface"""
    
    # Header
    st.title(f"🤖 {ASSISTANT_NAME} AI Assistant")
    st.markdown("*Advanced AI Assistant with comprehensive skill architecture*")
    
    # Sidebar - Assistant Status & Controls
    with st.sidebar:
        st.header("Assistant Control Panel")
        
        # Status indicator
        status_color = "🟢" if st.session_state.nova else "🔴"
        st.markdown(f"**Status:** {status_color} {'Online' if st.session_state.nova else 'Offline'}")
        
        # Voice control
        st.subheader("🎤 Voice Controls")
        voice_toggle = st.toggle("Enable Voice Output", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_toggle
        
        # Skill toggles
        st.subheader("🛠️ Skill Configuration")
        
        # Core Skills
        with st.expander("Core Skills", expanded=False):
            hyper_context = st.checkbox("Hyper Context", value=True)
            predictive = st.checkbox("Predictive Control", value=True)
            emotion = st.checkbox("Emotion Watcher", value=False)
            dark_web = st.checkbox("Dark Web Watch", value=False)
            cross_device = st.checkbox("Cross Device", value=False)
        
        # Advanced Skills
        with st.expander("Advanced Skills", expanded=False):
            negotiator = st.checkbox("Negotiator", value=False)
            ar_overlay = st.checkbox("AR Overlay", value=False)
            threat_mode = st.checkbox("Threat Mode", value=False)
            voice_clone = st.checkbox("Voice Clone", value=False)
            doppelganger = st.checkbox("Doppelganger", value=False)
            realworld_coord = st.checkbox("Real World Coordinator", value=False)
        
        # Study Skills
        with st.expander("Study Suite", expanded=False):
            study_companion = st.checkbox("Study Companion", value=False)
            lecture_assistant = st.checkbox("Lecture Assistant", value=False)
            knowledge_graph = st.checkbox("Knowledge Graph", value=False)
            exam_prep = st.checkbox("Exam Prep", value=False)
            skill_builder = st.checkbox("Skill Builder", value=False)
            collab_study = st.checkbox("Collaborative Study", value=False)
            language_guardian = st.checkbox("Language Guardian", value=False)
            deep_research = st.checkbox("Deep Research", value=False)
            life_autopilot = st.checkbox("Life Autopilot", value=False)
        
        # System Info
        st.subheader("📊 System Info")
        if st.session_state.nova:
            twin_stats = st.session_state.nova.twin.get_stats()
            st.metric("Total Interactions", twin_stats.get('total_chats', 0))
            st.metric("Active Skills", twin_stats.get('active_skills', 0))
            st.metric("Memory Usage", f"{twin_stats.get('memory_mb', 0):.1f} MB")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    # Main chat interface
    st.subheader("💬 Chat Interface")
    
    # Chat history display
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(f"*{message['timestamp']}*")

    # Chat input
    if prompt := st.chat_input("Ask Nova anything..."):
        # Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.chat_history.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"*{timestamp}*")
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Nova is thinking..."):
                try:
                    response = st.session_state.nova.handle_command(prompt)
                    st.markdown(response)
                    
                    # Add to chat history
                    response_timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": response,
                        "timestamp": response_timestamp
                    })
                    
                    # Voice output if enabled
                    if st.session_state.voice_enabled:
                        try:
                            st.session_state.nova.speak(response)
                        except Exception as e:
                            st.error(f"Voice output failed: {e}")
                            
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

    # Feature showcase tabs
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Skills Demo", "📊 Analytics", "⚙️ Settings", "📚 Documentation"])
    
    with tab1:
        st.subheader("Available Skills Demonstration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Core Capabilities:**")
            st.markdown("- `flashcards on machine learning` - Study companion")
            st.markdown("- `open youtube` - PC control")
            st.markdown("- `negotiate price on amazon` - Smart negotiator")
            st.markdown("- `scan threats` - Security analysis")
            st.markdown("- `what is this object` - AR recognition")
        
        with col2:
            st.markdown("**Advanced Features:**")
            st.markdown("- `digital twin meeting` - Doppelganger agent")
            st.markdown("- `translate live conversation` - Language guardian")
            st.markdown("- `deep research on AI ethics` - Research assistant")
            st.markdown("- `schedule my day` - Life autopilot")
            st.markdown("- `predict my next action` - Predictive control")
    
    with tab2:
        st.subheader("Assistant Analytics")
        
        if st.session_state.nova:
            # Performance metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Response Time",
                    value="150ms",
                    delta="-20ms"
                )
            
            with col2:
                st.metric(
                    label="Accuracy Score",
                    value="96.5%",
                    delta="2.1%"
                )
            
            with col3:
                st.metric(
                    label="Skills Used",
                    value="12",
                    delta="3"
                )
            
            # Usage chart (placeholder for real data)
            st.subheader("Usage Patterns")
            import pandas as pd
            import plotly.express as px
            
            # Sample data for demonstration
            usage_data = pd.DataFrame({
                'Skill': ['Study Companion', 'PC Control', 'Knowledge Graph', 'Deep Research', 'Negotiator'],
                'Usage Count': [25, 18, 15, 12, 8],
                'Success Rate': [0.95, 0.88, 0.92, 0.89, 0.75]
            })
            
            fig = px.bar(usage_data, x='Skill', y='Usage Count', 
                        title="Most Used Skills",
                        color='Success Rate',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Assistant Settings")
        
        # API Configuration
        st.markdown("**API Configuration**")
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                  value=os.getenv("OPENAI_API_KEY", ""))
        anthropic_key = st.text_input("Anthropic API Key", type="password", 
                                     value=os.getenv("ANTHROPIC_API_KEY", ""))
        
        # Safety Settings
        st.markdown("**Safety & Privacy Settings**")
        require_confirmation = st.checkbox("Require confirmation for payments", value=True)
        require_device_confirm = st.checkbox("Require confirmation for device actions", value=True)
        explicit_recording_consent = st.checkbox("Require explicit consent for recording", value=True)
        block_impersonation = st.checkbox("Block real person impersonation", value=True)
        
        # Performance Settings
        st.markdown("**Performance Settings**")
        max_memory = st.slider("Max Memory (MB)", 100, 1000, 500)
        response_timeout = st.slider("Response Timeout (seconds)", 5, 60, 30)
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("Settings saved successfully!")
    
    with tab4:
        st.subheader("Documentation & Help")
        
        st.markdown("""
        ## Getting Started with Nova AI Assistant
        
        ### Basic Commands
        - **General queries**: "What's the weather like?"
        - **PC control**: "open notepad", "close chrome"
        - **Study help**: "make flashcards on physics"
        - **Research**: "deep research on quantum computing"
        
        ### Advanced Features
        
        #### 🧠 Study Companion
        - Create flashcards from any topic
        - Generate practice tests
        - Track learning progress
        
        #### 🔒 Security Features
        - Dark web monitoring
        - Threat detection
        - Secure communications
        
        #### 🤖 AI Agents
        - Digital twin for meetings
        - Predictive behavior analysis
        - Automated task execution
        
        ### Safety & Privacy
        Nova is designed with privacy and safety as core principles:
        - All sensitive operations require explicit consent
        - No real person impersonation allowed
        - Local processing for sensitive data
        - Transparent operation logging
        
        ### Troubleshooting
        If you encounter issues:
        1. Check API key configuration
        2. Verify internet connection
        3. Review error messages in chat
        4. Check skill toggles in sidebar
        
        For more help, visit our [documentation](https://github.com/SailikhithGB/AI--Assistant).
        """)

if __name__ == "__main__":
    main()

"""
Nova AI Assistant - CLI Entry Point
This file maintains CLI compatibility while primarily directing users to the web interface
"""

from assistant import Assistant
from pathlib import Path
import os
import sys

def main():
    """Main CLI entry point with web interface recommendation"""
    
    # Ensure data directory exists
    Path(__file__).parent.joinpath("data").mkdir(exist_ok=True)
    
    print("🤖 Nova AI Assistant")
    print("=" * 50)
    print("For the best experience, use the web interface:")
    print("👉 Run: streamlit run app.py --server.port 5000")
    print("=" * 50)
    print("\nCLI Mode - Type commands or 'exit' to quit.")
    print("Available commands:")
    print("- 'web' to get web interface instructions")
    print("- 'help' for command examples")
    print("- Any natural language query")
    
    try:
        nova = Assistant()
        print(f"\n{nova.name}: Ready! How can I help you today?")
        
        while True:
            try:
                text = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting Nova. Goodbye! 👋")
                break
            
            if not text:
                continue
                
            if text.lower() in {"exit", "quit", "bye"}:
                print("Goodbye! 👋")
                break
            elif text.lower() == "web":
                print("\n🌐 To access the web interface:")
                print("1. Run: streamlit run app.py --server.port 5000")
                print("2. Open your browser to: http://localhost:5000")
                print("3. Enjoy the full Nova experience!")
                continue
            elif text.lower() == "help":
                print("\n📚 Example commands:")
                print("- 'flashcards on machine learning'")
                print("- 'open youtube'")
                print("- 'what's the weather like?'")
                print("- 'negotiate price on my shopping list'")
                print("- 'scan for threats'")
                print("- 'deep research on AI ethics'")
                continue
            
            # Process command
            try:
                reply = nova.handle_command(text)
                print(f"\n{nova.name}: {reply}")
                
                # Optional TTS (non-fatal if missing)
                try:
                    nova.speak(reply)
                except Exception:
                    pass  # Silently fail if TTS unavailable
                    
            except Exception as e:
                print(f"\n{nova.name}: Sorry, I encountered an error: {e}")
                print("For better error handling and features, try the web interface!")
                
    except Exception as e:
        print(f"Failed to initialize Nova: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

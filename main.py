# nova_v2/main.py
from assistant import Assistant
from pathlib import Path

def main():
    Path(__file__).parent.joinpath("assets").mkdir(exist_ok=True)
    nova = Assistant()
    print(f"{nova.name}: Ready. Type commands. Type 'exit' to quit.")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not text:
            continue
        if text.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        reply = nova.handle_command(text)
        print(f"{nova.name}: {reply}")
        # speak (non-fatal if TTS missing)
        try:
            nova.speak(reply)
        except Exception:
            pass

if __name__ == "__main__":
    main()

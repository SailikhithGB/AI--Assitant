# Study Companion – flashcards + spaced repetition (local JSON)
# Free alternative to Anki via simple JSON scheduling

import json, re, time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List
from config import STUDY_DIR

DB = STUDY_DIR / "flashcards.json"

@dataclass
class Card:
    q: str
    a: str
    ease: float = 2.5
    ivl: int = 1           # days
    due: float = time.time()

def _load() -> List[Card]:
    if DB.exists():
        return [Card(**x) for x in json.loads(DB.read_text(encoding="utf-8"))]
    return []

def _save(cards: List[Card]):
    DB.write_text(json.dumps([asdict(c) for c in cards], ensure_ascii=False, indent=2), encoding="utf-8")

def _parse_qa_block(text: str):
    # expects: "flashcards: Q:... A:... | Q:... A:..."
    pairs = re.findall(r"Q:(.*?)A:(.*?)(?:\||$)", text, flags=re.S)
    return [(q.strip(), a.strip()) for q,a in pairs]

def _review(cards: List[Card]) -> List[Card]:
    now = time.time()
    return [c for c in cards if c.due <= now]

def _schedule(card: Card, grade: int):
    # SM-2 like
    if grade < 3:
        card.ivl = 1
    else:
        card.ease = max(1.3, card.ease + 0.1*(5 - grade))
        card.ivl = int(card.ivl * card.ease)
    card.due = time.time() + card.ivl * 86400

class StudyCompanion:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str) -> str:
        t = text.lower()
        if t.startswith("flashcards:"):
            cards = _load()
            for q,a in _parse_qa_block(text):
                cards.append(Card(q=q, a=a))
            _save(cards)
            return f"Added {len(_parse_qa_block(text))} cards."
        if "review flashcards" in t:
            cards = _load()
            due = _review(cards)[:10]
            if not due: return "No cards due. Great job!"
            out = "\n".join([f"Q{idx+1}: {c.q}" for idx,c in enumerate(due)])
            return "Cards due:\n" + out + "\nSay: 'grade <n> <1-5>' per card."
        m = re.match(r"grade (\d+)\s+([1-5])", t)
        if m:
            idx, g = int(m.group(1))-1, int(m.group(2))
            cards = _load()
            due = _review(cards)
            if 0 <= idx < len(due):
                _schedule(due[idx], g)
                _save(cards)
                return f"Graded card {idx+1} with {g}. Next due updated."
            return "Invalid card index."
        return "Use: 'flashcards: Q:.. A:.. | Q:.. A:..' or 'review flashcards' or 'grade <n> <1-5>'."

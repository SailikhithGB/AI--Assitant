# Exam Prep – practice test generator (heuristic) + simple score predictor

import re, random

SUBJECT_TEMPLATES = {
    "math": [
        ("What is derivative of x^2?", "2x"),
        ("Solve: integral of 2x dx", "x^2 + C"),
        ("What is limit of (1+1/n)^n as n→∞?", "e"),
    ],
    "python": [
        ("What does list comprehension [x*x for x in range(3)] return?", "[0, 1, 4]"),
        ("What is a dictionary in Python?", "Key-value mapping"),
        ("What is PEP8?", "Style guide for Python code"),
    ],
}

class ExamPrep:
    def __init__(self, twin):
        self.twin = twin

    def route(self, text: str) -> str:
        t = text.lower()
        m = re.search(r"practice test (.+)", t)
        if m:
            subject = m.group(1).strip().lower()
            qs = SUBJECT_TEMPLATES.get(subject)
            if not qs: return f"No template for '{subject}'. Available: {', '.join(SUBJECT_TEMPLATES)}"
            sample = random.sample(qs, min(3, len(qs)))
            out = "\n".join([f"Q{i+1}: {q}" for i,(q,_) in enumerate(sample)])
            self.twin.last_exam = sample
            return f"Practice Test ({subject}):\n{out}\nReply: 'answers: A1=..., A2=..., A3=...'"
        if t.startswith("answers:"):
            if not getattr(self.twin, "last_exam", None):
                return "No active test. Say 'practice test math' first."
            ans = re.findall(r"A(\d)=(.*?)(?:,|$)", text)
            correct = 0
            for i, user_a in ans:
                i = int(i)-1
                if 0 <= i < len(self.twin.last_exam):
                    truth = self.twin.last_exam[i][1].strip().lower()
                    if truth in user_a.strip().lower():
                        correct += 1
            score = int((correct / len(self.twin.last_exam)) * 100)
            pred = "Likely pass" if score >= 60 else "Needs improvement"
            return f"Score: {score}%. {pred}."
        if "predict score" in t:
            return "Take a practice test first. I’ll estimate based on your answers."
        return "Say: 'practice test <subject>' or 'answers: A1=..., A2=...'."

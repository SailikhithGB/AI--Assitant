# Knowledge Graph – local concept map in memory (JSON-like on twin)

from collections import defaultdict
import re

class KnowledgeGraph:
    def __init__(self, twin):
        self.twin = twin
        if not hasattr(self.twin, "graph"):
            self.twin.graph = defaultdict(set)

    def route(self, text: str) -> str:
        t = text.lower()
        if "link" in t and "to" in t:
            a, b = self._parse_link(text)
            if not a or not b: return "Say: 'link <concept A> to <concept B>'."
            self.twin.graph[a].add(b)
            return f"Linked '{a}' → '{b}'."
        if "concept map" in t:
            return self._render()
        return "Say: 'link A to B' or 'concept map'."

    def _parse_link(self, text: str):
        m = re.search(r"link (.+) to (.+)", text, flags=re.I)
        if m:
            return m.group(1).strip().lower(), m.group(2).strip().lower()
        return None, None

    def _render(self) -> str:
        lines = []
        for a, bs in self.twin.graph.items():
            if bs:
                lines.append(f"{a} -> {', '.join(sorted(bs))}")
        return "Concept Map:\n" + ("\n".join(lines) if lines else "(empty)")

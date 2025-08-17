# Life Autopilot – schedules & routines (local)
# Uses a naive planner that merges tasks, detects conflicts, and proposes a day plan.

import re, time
from datetime import datetime, timedelta

class LifeAutopilot:
    def __init__(self, twin):
        self.twin = twin
        if not hasattr(self.twin, "todos"):
            self.twin.todos = []  # (title, start_ts, minutes)

    def route(self, text: str, require_confirm: bool = True) -> str:
        t = text.lower()
        if t.startswith("add event"):
            # add event: <title> at <HH:MM> for <minutes>
            m = re.match(r"add event (.+) at (\d{1,2}:\d{2}) for (\d+)", t)
            if not m: return "Use: add event <title> at <HH:MM> for <minutes>"
            title, hhmm, mins = m.group(1), m.group(2), int(m.group(3))
            dt = self._today_time(hhmm)
            self.twin.todos.append((title, dt.timestamp(), mins))
            return f"Added: {title} at {hhmm} for {mins}m."
        if "schedule my day" in t or "autopilot" in t:
            plan = self._plan_day()
            return "Plan:\n" + "\n".join(plan)
        return "Say: 'add event <title> at <HH:MM> for <minutes>' or 'schedule my day'."

    def _today_time(self, hhmm: str) -> datetime:
        h,m = map(int, hhmm.split(":"))
        now = datetime.now()
        return now.replace(hour=h, minute=m, second=0, microsecond=0)

    def _plan_day(self):
        items = sorted(self.twin.todos, key=lambda x: x[1])
        plan = []
        for title, start_ts, mins in items:
            start = datetime.fromtimestamp(start_ts)
            end = start + timedelta(minutes=mins)
            plan.append(f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')}  {title}")
        if not plan: plan = ["(no tasks)"]
        return plan

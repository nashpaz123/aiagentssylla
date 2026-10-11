"""
mini_crew.py — Multi-Agent בלי מודל שפה ובלי מפתח API.

מטרה: להבין את מבנה CrewAI (Agent · Task · Crew · Process) ואת שלוש תבניות התזמור
(sequential / hierarchical / writer-reviewer loop) כשהכל דטרמיניסטי וקריא בלוג.

כל "סוכן" כאן הוא פונקציית פייתון שמדמה את ההחלטה של המודל. בפרוד — אותו מבנה,
רק ש-handler הופך לקריאה ל-LLM (ראו crew_demo.py).

הרצה:
    python3 mini_crew.py sequential
    python3 mini_crew.py hierarchical
    python3 mini_crew.py loop
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Callable

# ---------- "מודל" מדומה: תקציב טוקנים לכל סוכן ----------

TOKEN_BUDGET_PER_AGENT = 1_200
MAX_ROUNDS = 3  # תקרת סבבי Writer <-> Reviewer


@dataclass
class Agent:
    role: str
    goal: str
    handler: Callable[["Task", dict], str]
    tools: list[str] = field(default_factory=list)
    tokens_used: int = 0
    max_iter: int = 3

    def run(self, task: "Task", context: dict) -> str:
        # מדמים "עלות": אורך הקלט + אורך הפלט
        out = self.handler(task, context)
        cost = len(task.description) + len(out)
        self.tokens_used += cost
        print(f"  [{self.role}] task={task.name!r} tokens+={cost} total={self.tokens_used}")
        if self.tokens_used > TOKEN_BUDGET_PER_AGENT:
            raise RuntimeError(f"BUDGET_EXCEEDED: {self.role} ({self.tokens_used} > {TOKEN_BUDGET_PER_AGENT})")
        return out


@dataclass
class Task:
    name: str
    description: str
    expected_output: str
    agent: Agent | None = None          # ב-hierarchical המנהל ממלא את זה
    context: list[str] = field(default_factory=list)  # שמות משימות קודמות שהפלט שלהן נכנס


@dataclass
class Crew:
    agents: list[Agent]
    tasks: list[Task]
    process: str = "sequential"  # sequential | hierarchical

    def kickoff(self, inputs: dict) -> dict:
        outputs: dict[str, str] = {}
        print(f"\n== Crew.kickoff process={self.process} inputs={inputs}")
        for t in self.tasks:
            ctx = {"inputs": inputs, **{k: outputs[k] for k in t.context if k in outputs}}
            agent = t.agent if self.process == "sequential" else self._manager_pick(t)
            print(f"-> {t.name}: assigned to {agent.role}")
            outputs[t.name] = agent.run(t, ctx)
        return outputs

    def _manager_pick(self, task: Task) -> Agent:
        """מנהל דטרמיניסטי: בוחר סוכן לפי מילת מפתח בתיאור המשימה.
        ב-CrewAI אמיתי זה LLM (manager_llm) — ולכן צריך max_iter ותקציב."""
        text = task.description.lower()
        for a in self.agents:
            keyword = a.role.lower()[:5]  # research / write / review
            if keyword in text:
                return a
        print("   (manager found no match — falling back to first agent)")
        return self.agents[0]


# ---------- handlers: ההיגיון של כל תפקיד ----------

def research(task: Task, ctx: dict) -> str:
    order = ctx["inputs"]["order_id"]
    # "כלי" מדומה — בפרוד זה get_order ממפגש 3
    db = {"A-100": ("shipped", 40.0), "A-249": ("delivered", 249.0)}
    status, amount = db.get(order, ("unknown", 0.0))
    return f"FACTS: order={order} status={status} amount={amount} refund_window_days=14"


def write(task: Task, ctx: dict) -> str:
    facts = ctx.get("research", "")
    notes = ctx.get("review", "")
    draft = f"DRAFT: שלום! ההזמנה שלך ({facts.split('order=')[1].split()[0]}) בסטטוס " \
            f"{facts.split('status=')[1].split()[0]}. ניתן לבקש החזר תוך 14 יום."
    if "REVISE" in notes:
        draft += " סכום ההחזר יאושר על ידי נציג."
    return draft


def review(task: Task, ctx: dict) -> str:
    draft = ctx.get("write", "")
    facts = ctx.get("research", "")
    amount = float(facts.split("amount=")[1].split()[0]) if "amount=" in facts else 0.0
    if amount > 100 and "נציג" not in draft:
        return "REVISE: סכום מעל 100 — חובה לציין אישור נציג (HITL) לפני התחייבות."
    return "APPROVE"


researcher = Agent("Researcher", "לאסוף עובדות מאומתות בלבד", research, tools=["get_order"])
writer = Agent("Writer", "לנסח תשובה ללקוח מהעובדות בלבד", write)
reviewer = Agent("Reviewer", "לבדוק מול מדיניות ולהחזיר APPROVE/REVISE", review)


def build_tasks() -> list[Task]:
    return [
        Task("research", "research the order facts", "bullets with status/amount", researcher),
        Task("write", "write a customer reply", "short Hebrew reply", writer, context=["research"]),
        Task("review", "review the reply vs policy", "APPROVE or REVISE: reason", reviewer, context=["research", "write"]),
    ]


def run_sequential() -> None:
    crew = Crew([researcher, writer, reviewer], build_tasks(), process="sequential")
    out = crew.kickoff({"order_id": "A-100"})
    print("\nRESULT:", out["review"])


def run_hierarchical() -> None:
    tasks = build_tasks()
    for t in tasks:
        t.agent = None  # המנהל יחליט
    crew = Crew([researcher, writer, reviewer], tasks, process="hierarchical")
    out = crew.kickoff({"order_id": "A-100"})
    print("\nRESULT:", out["review"])


def run_loop() -> None:
    """Writer <-> Reviewer עד APPROVE — או עד MAX_ROUNDS ואז הסלמה לאדם."""
    inputs = {"order_id": "A-249"}
    ctx: dict = {"inputs": inputs}
    t_research, t_write, t_review = build_tasks()
    print(f"\n== Loop demo inputs={inputs} MAX_ROUNDS={MAX_ROUNDS}")
    ctx["research"] = researcher.run(t_research, ctx)
    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"-- round {round_no}")
        ctx["write"] = writer.run(t_write, ctx)
        ctx["review"] = reviewer.run(t_review, ctx)
        print(f"   reviewer -> {ctx['review']}")
        if ctx["review"] == "APPROVE":
            print("\nRESULT: APPROVED after", round_no, "round(s)")
            print("FINAL:", ctx["write"])
            return
    print("\nRESULT: ESCALATE_TO_HUMAN — no APPROVE within MAX_ROUNDS")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sequential"
    {"sequential": run_sequential, "hierarchical": run_hierarchical, "loop": run_loop}[mode]()
    print("GOAL_COMPLETE: True")

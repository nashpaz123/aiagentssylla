"""
crew_demo.py — אותו צוות (Researcher · Writer · Reviewer) ב-CrewAI אמיתי.

דורש מפתח API למודל שפה. CrewAI משתמש ב-LiteLLM, לכן שם המודל הוא "ספק/מודל".
ברירת המחדל: openai/gpt-4o-mini — לכן בלי CREW_MODEL יידרש OPENAI_API_KEY גם אם יש ANTHROPIC_API_KEY.

    # OpenAI — מפתח + מודל מאותו ספק:
    export OPENAI_API_KEY=...
    export CREW_MODEL=openai/gpt-4o-mini

    # Anthropic — חובה: (1) pip install "crewai[anthropic]"  (2) CREW_MODEL (המפתח לבד לא מספיק):
    # בתוך ה-venv:  pip install -r requirements.txt   ← לא uv add (אין pyproject.toml כאן)
    export ANTHROPIC_API_KEY=...
    export CREW_MODEL=anthropic/claude-sonnet-4-5

הרצה:
    python3 crew_demo.py                 # Process.sequential (ברירת מחדל)
    python3 crew_demo.py hierarchical    # מנהל LLM מחלק משימות
    python3 crew_demo.py --dry-run       # בונה את הצוות בלי לקרוא למודל (בדיקת מבנה)
"""

from __future__ import annotations

import os
import sys

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool

MODEL = os.environ.get("CREW_MODEL", "openai/gpt-4o-mini")
llm = LLM(model=MODEL, temperature=0)


# ---------- כלי ממפגש 3: סכימה נגזרת מהחתימה ומה-docstring ----------

@tool("get_order")
def get_order(order_id: str) -> str:
    """Return order status and amount for a given order_id. Read-only."""
    db = {"A-100": ("shipped", 40.0), "A-249": ("delivered", 249.0)}
    status, amount = db.get(order_id, ("unknown", 0.0))
    return f"order={order_id} status={status} amount={amount} refund_window_days=14"


# ---------- Agents: תפקיד + מטרה + רקע + כלים + תקציב ----------

researcher = Agent(
    role="Support Researcher",
    goal="Collect verified facts about the customer's order using tools only.",
    backstory="You never guess. Every fact must come from a tool call. You output bullets with the source.",
    tools=[get_order],
    llm=llm,
    max_iter=4,              # תקציב סיבובים לסוכן — חובה
    allow_delegation=False,
    verbose=True,
)

writer = Agent(
    role="Customer Reply Writer",
    goal="Write a short, warm Hebrew reply to the customer based ONLY on the researcher's facts.",
    backstory="You write clear Hebrew. You never invent facts, amounts or dates.",
    llm=llm,
    max_iter=3,
    allow_delegation=False,
    verbose=True,
)

reviewer = Agent(
    role="Policy Reviewer",
    goal="Check the reply against policy and return APPROVE or REVISE with a reason.",
    backstory=(
        "Policy: refunds above 100 require explicit human-agent approval and the reply must say so. "
        "You are read-only: you never rewrite the reply yourself."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False,
    verbose=True,
)


# ---------- Tasks: תיאור + חוזה פלט + מי אחראי + הקשר ----------

t_research = Task(
    name="research",
    description="Get the facts for order {order_id}. Use the get_order tool.",
    expected_output="3-5 bullets: status, amount, refund window, each with the tool it came from.",
    agent=researcher,
)

t_write = Task(
    name="write",
    description="Write the Hebrew customer reply for order {order_id} about: {question}",
    expected_output="A 2-4 sentence Hebrew reply. No facts that are not in the research bullets.",
    agent=writer,
    context=[t_research],
)

t_review = Task(
    name="review",
    description="Review the reply for policy compliance. Amounts above 100 must mention human approval.",
    expected_output="One line: 'APPROVE' or 'REVISE: <reason>'.",
    agent=reviewer,
    context=[t_research, t_write],
    # human_input=True,  # להדלקה: עצירה לאישור אדם אחרי המשימה (HITL)
)


def build_crew(process: str) -> Crew:
    if process == "hierarchical":
        return Crew(
            agents=[researcher, writer, reviewer],
            tasks=[t_research, t_write, t_review],
            process=Process.hierarchical,
            manager_llm=llm,     # המנהל הוא LLM — לכן max_iter ותקציב קריטיים
            verbose=True,
        )
    return Crew(
        agents=[researcher, writer, reviewer],
        tasks=[t_research, t_write, t_review],
        process=Process.sequential,
        verbose=True,
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    process = "hierarchical" if "hierarchical" in args else "sequential"
    crew = build_crew(process)
    if "--dry-run" in args:
        print(f"DRY RUN OK: model={MODEL} process={process} agents={len(crew.agents)} tasks={len(crew.tasks)}")
        sys.exit(0)

    result = crew.kickoff(inputs={"order_id": "A-249", "question": "Can I get a refund?"})
    print("\n==== FINAL (reviewer) ====")
    print(result.raw)
    print("\n==== PER TASK ====")
    for out in result.tasks_output:
        print(f"- {out.name} [{out.agent}]: {out.raw[:160]!r}")
    print("GOAL_COMPLETE: True")

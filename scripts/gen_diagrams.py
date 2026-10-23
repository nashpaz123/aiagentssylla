#!/usr/bin/env python3
"""Generate presentation diagrams for AI Agents course sessions 1–5."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/stuff/prj/aiagentssylla/assets")
W, H = 1920, 1080

# Shared palette — dark enterprise, blue accents (matches course visual notes)
BG = (18, 22, 30)
CARD = (28, 34, 46)
CARD2 = (36, 44, 60)
ACCENT = (79, 140, 255)
ACCENT2 = (120, 100, 255)
GREEN = (72, 187, 140)
ORANGE = (237, 137, 54)
RED = (245, 101, 101)
TEXT = (236, 240, 246)
MUTED = (160, 170, 190)
LINE = (70, 80, 100)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def new_img() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def rounded(draw: ImageDraw.ImageDraw, box, fill, radius=24, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, xy, text, fnt, fill=TEXT):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x - tw / 2, y - th / 2), text, font=fnt, fill=fill)


def multiline_center(draw, xy, lines, fnt, fill=TEXT, gap=8):
    x, y = xy
    heights = []
    widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    total_h = sum(heights) + gap * (len(lines) - 1)
    cy = y - total_h / 2
    for line, th in zip(lines, heights):
        bbox = draw.textbbox((0, 0), line, font=fnt)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw / 2, cy), line, font=fnt, fill=fill)
        cy += th + gap


def arrow(draw, start, end, color=ACCENT, width=4):
    draw.line([start, end], fill=color, width=width)
    # simple arrow head
    x1, y1 = start
    x2, y2 = end
    import math

    angle = math.atan2(y2 - y1, x2 - x1)
    size = 16
    left = (x2 - size * math.cos(angle - 0.5), y2 - size * math.sin(angle - 0.5))
    right = (x2 - size * math.cos(angle + 0.5), y2 - size * math.sin(angle + 0.5))
    draw.polygon([end, left, right], fill=color)


def save(img: Image.Image, rel: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


# ---------- Session 01 ----------

def v01_human_agent():
    img, d = new_img()
    title = font(48, True)
    body = font(28)
    small = font(24)
    center_text(d, (W / 2, 70), "Human + AI Agent + Tools", title)
    # human
    rounded(d, (120, 320, 420, 620), CARD, outline=ACCENT)
    multiline_center(d, (270, 470), ["Human", "Goal / Intent"], body)
    # agent
    rounded(d, (720, 280, 1200, 660), CARD2, outline=ACCENT2, radius=28)
    multiline_center(d, (960, 470), ["AI Agent", "Decide · Act · Observe"], body)
    # tools
    tools = ["Email", "DB", "CRM", "Web", "Calendar"]
    for i, t in enumerate(tools):
        x0 = 1380
        y0 = 220 + i * 120
        rounded(d, (x0, y0, x0 + 420, y0 + 90), CARD, outline=LINE)
        center_text(d, (x0 + 210, y0 + 45), t, small)
        arrow(d, (1200, 470), (x0, y0 + 45), ACCENT, 3)
    arrow(d, (420, 470), (720, 470))
    arrow(d, (720, 470), (420, 470), MUTED, 2)
    save(img, "01/01-human-agent-tools.png")


def v02_chat_vs_agent():
    img, d = new_img()
    title = font(48, True)
    h = font(36, True)
    body = font(26)
    center_text(d, (W / 2, 60), "Chat vs Agent", title)
    # left
    rounded(d, (80, 160, 900, 980), CARD)
    center_text(d, (490, 220), "Chat / LLM", h, ACCENT)
    steps = ["User Prompt", "LLM", "Answer", "User Prompt", "Answer"]
    for i, s in enumerate(steps):
        y = 300 + i * 110
        rounded(d, (200, y, 780, y + 80), CARD2, outline=LINE, radius=16)
        center_text(d, (490, y + 40), s, body)
        if i < len(steps) - 1:
            arrow(d, (490, y + 80), (490, y + 110), MUTED, 3)
    # right
    rounded(d, (1020, 160, 1840, 980), CARD)
    center_text(d, (1430, 220), "Agent", h, GREEN)
    steps2 = ["Goal", "Decide", "Act (Tool)", "Observe", "Continue / Done"]
    for i, s in enumerate(steps2):
        y = 300 + i * 110
        color = GREEN if i == 4 else ACCENT
        rounded(d, (1140, y, 1720, y + 80), CARD2, outline=color, radius=16)
        center_text(d, (1430, y + 40), s, body)
        if i < len(steps2) - 1:
            arrow(d, (1430, y + 80), (1430, y + 110), color, 3)
    save(img, "01/02-chat-vs-agent.png")


def v03_agent_loop():
    img, d = new_img()
    title = font(48, True)
    body = font(30, True)
    center_text(d, (W / 2, 60), "Agent Loop", title)
    nodes = [
        (960, 220, "GOAL"),
        (960, 400, "DECIDE"),
        (960, 580, "ACT"),
        (960, 760, "OBSERVE"),
    ]
    for x, y, label in nodes:
        rounded(d, (x - 180, y - 55, x + 180, y + 55), CARD2, outline=ACCENT, radius=20)
        center_text(d, (x, y), label, body)
    for i in range(len(nodes) - 1):
        arrow(d, (nodes[i][0], nodes[i][1] + 55), (nodes[i + 1][0], nodes[i + 1][1] - 55))
    # continue branch
    rounded(d, (1280, 705, 1680, 815), CARD, outline=GREEN, radius=18)
    center_text(d, (1480, 760), "CONTINUE → DECIDE", font(26, True), GREEN)
    arrow(d, (1140, 760), (1280, 760), GREEN, 4)
    arrow(d, (1480, 705), (1480, 400), GREEN, 3)
    arrow(d, (1480, 400), (1140, 400), GREEN, 3)
    rounded(d, (240, 705, 640, 815), CARD, outline=ORANGE, radius=18)
    center_text(d, (440, 760), "STOP / DONE", font(26, True), ORANGE)
    arrow(d, (780, 760), (640, 760), ORANGE, 4)
    save(img, "01/03-agent-loop.png")


def v04_llm_tools():
    img, d = new_img()
    title = font(48, True)
    body = font(28, True)
    small = font(24)
    center_text(d, (W / 2, 60), "LLM + Tools", title)
    rounded(d, (760, 380, 1160, 620), CARD2, outline=ACCENT2, radius=28)
    multiline_center(d, (960, 500), ["LLM", "Reasoning"], body)
    tools = [
        (200, 220, "Database"),
        (200, 450, "API"),
        (200, 680, "Web"),
        (1480, 220, "Email"),
        (1480, 450, "K8s"),
        (1480, 680, "CRM"),
    ]
    for x, y, label in tools:
        rounded(d, (x, y, x + 280, y + 100), CARD, outline=LINE, radius=16)
        center_text(d, (x + 140, y + 50), label, small)
        arrow(d, (960, 500), (x + 140, y + 50), ACCENT, 3)
    save(img, "01/04-llm-tools.png")


def v05_workflow_vs_agent():
    img, d = new_img()
    title = font(48, True)
    h = font(34, True)
    body = font(24)
    center_text(d, (W / 2, 55), "Workflow vs Agent", title)
    center_text(d, (480, 150), "Workflow", h, ACCENT)
    steps = ["Input", "Extract", "Summarize", "Save", "Notify"]
    for i, s in enumerate(steps):
        x = 120 + i * 150
        rounded(d, (x, 280, x + 130, 380), CARD2, outline=LINE, radius=14)
        center_text(d, (x + 65, 330), s, body)
        if i < len(steps) - 1:
            arrow(d, (x + 130, 330), (x + 150, 330), MUTED, 3)
    center_text(d, (480, 460), "Fixed path · known steps", font(22), MUTED)

    center_text(d, (1440, 150), "Agent", h, GREEN)
    # loop visual
    cx, cy = 1440, 420
    labels = ["Goal", "Decide", "Act", "Observe"]
    positions = [(cx, cy - 160), (cx + 200, cy), (cx, cy + 160), (cx - 200, cy)]
    for (x, y), lab in zip(positions, labels):
        rounded(d, (x - 90, y - 40, x + 90, y + 40), CARD2, outline=GREEN, radius=14)
        center_text(d, (x, y), lab, body)
    for i in range(4):
        a = positions[i]
        b = positions[(i + 1) % 4]
        arrow(d, a, b, GREEN, 3)
    center_text(d, (1440, 680), "Adaptive path · decisions", font(22), MUTED)
    save(img, "01/05-workflow-vs-agent.png")


def v06_autonomy():
    """Do NOT overwrite the Cathey-style spectrum PNGs (hand-curated educational art).

    Those files live at assets/01/06-agent-spectrum-l0-l6.png and
    assets/01/06-autonomy-spectrum.png. Regenerating the dark placeholder was a
    regression — skip silently if the curated files already exist.
    """
    curated = [
        ROOT / "01/06-agent-spectrum-l0-l6.png",
        ROOT / "01/06-autonomy-spectrum.png",
    ]
    if all(p.exists() and p.stat().st_size > 200_000 for p in curated):
        print("skip v06_autonomy — curated spectrum images present")
        return
    print("warn: curated spectrum missing; not synthesizing dark replacement")


def v07_approval():
    img, d = new_img()
    title = font(48, True)
    body = font(28)
    center_text(d, (W / 2, 60), "Human Approval Flow", title)
    boxes = [
        (200, 400, "Agent proposes\naction"),
        (700, 400, "Policy check"),
        (1200, 250, "Auto-allow\n(read)"),
        (1200, 450, "Ask human\n(write)"),
        (1200, 650, "Block\n(delete)"),
    ]
    colors = [ACCENT, ACCENT2, GREEN, ORANGE, RED]
    for (x, y, text), c in zip(boxes, colors):
        rounded(d, (x, y, x + 360, y + 160), CARD2, outline=c, radius=18)
        multiline_center(d, (x + 180, y + 80), text.split("\n"), body)
    arrow(d, (560, 480), (700, 480))
    arrow(d, (1060, 450), (1200, 330), GREEN, 3)
    arrow(d, (1060, 480), (1200, 530), ORANGE, 3)
    arrow(d, (1060, 510), (1200, 730), RED, 3)
    save(img, "01/07-human-approval.png")


def v08_guardrails():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 60), "Guardrails", title)
    rounded(d, (660, 380, 1260, 700), CARD2, outline=ACCENT, radius=28)
    center_text(d, (960, 540), "AI Agent", font(36, True))
    # fence
    fence = [
        (180, 220, "Permissions"),
        (700, 160, "Policies"),
        (1220, 220, "Rate limits"),
        (180, 780, "Allow-list tools"),
        (700, 840, "Stop conditions"),
        (1220, 780, "Audit / Trace"),
    ]
    for x, y, label in fence:
        rounded(d, (x, y, x + 400, y + 100), CARD, outline=ORANGE, radius=16)
        center_text(d, (x + 200, y + 50), label, body, ORANGE)
    save(img, "01/08-guardrails.png")


def v09_trace():
    img, d = new_img()
    title = font(48, True)
    body = font(24)
    center_text(d, (W / 2, 55), "Agent Trace", title)
    events = [
        ("t0", "Goal received", ACCENT),
        ("t1", "Plan: check pods", ACCENT2),
        ("t2", "Tool: get_pods", GREEN),
        ("t3", "Obs: 1 CrashLoop", ORANGE),
        ("t4", "Tool: get_logs", GREEN),
        ("t5", "Answer + evidence", TEXT),
    ]
    for i, (t, label, color) in enumerate(events):
        y = 160 + i * 140
        d.ellipse([160, y + 20, 220, y + 80], fill=color)
        center_text(d, (190, y + 50), "", body)
        if i < len(events) - 1:
            d.line([(190, y + 80), (190, y + 140)], fill=LINE, width=4)
        rounded(d, (280, y, 1600, y + 100), CARD, outline=color, radius=16)
        center_text(d, (360, y + 50), t, font(26, True), color)
        d.text((480, y + 32), label, font=body, fill=TEXT)
    save(img, "01/09-agent-trace.png")


def v10_devops():
    img, d = new_img()
    title = font(44, True)
    small = font(24)
    center_text(d, (W / 2, 55), "DevOps Troubleshooting Agent", title)
    rounded(d, (760, 400, 1160, 640), CARD2, outline=ACCENT, radius=28)
    center_text(d, (960, 520), "Agent", font(34, True))
    systems = [
        (160, 220, "Prometheus"),
        (160, 480, "Logs"),
        (160, 740, "Events"),
        (1480, 220, "Kubernetes"),
        (1480, 480, "Deployments"),
        (1480, 740, "Runbooks"),
    ]
    for x, y, label in systems:
        rounded(d, (x, y, x + 300, y + 100), CARD, outline=LINE, radius=14)
        center_text(d, (x + 150, y + 50), label, small)
        arrow(d, (960, 520), (x + 150, y + 50), ACCENT, 3)
    save(img, "01/10-devops-agent.png")


def v11_support():
    img, d = new_img()
    title = font(44, True)
    small = font(24)
    center_text(d, (W / 2, 55), "Support Agent", title)
    rounded(d, (760, 400, 1160, 640), CARD2, outline=GREEN, radius=28)
    center_text(d, (960, 520), "Support\nAgent", font(32, True))
    systems = [
        (160, 250, "CRM"),
        (160, 520, "Ticketing"),
        (160, 790, "Knowledge"),
        (1480, 250, "Email"),
        (1480, 520, "Orders DB"),
        (1480, 790, "Policy"),
    ]
    for x, y, label in systems:
        rounded(d, (x, y, x + 300, y + 100), CARD, outline=LINE, radius=14)
        center_text(d, (x + 150, y + 50), label, small)
        arrow(d, (960, 520), (x + 150, y + 50), GREEN, 3)
    save(img, "01/11-support-agent.png")


def v12_multi():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Multi-Agent (preview)", title)
    rounded(d, (710, 180, 1210, 360), CARD2, outline=ACCENT2, radius=22)
    center_text(d, (960, 270), "Manager / Orchestrator", font(30, True))
    agents = [("Researcher", 200), ("Coder", 710), ("Reviewer", 1220), ("Ops", 1730)]
    # fix width
    agents = [("Researcher", 180), ("Coder", 620), ("Reviewer", 1060), ("Writer", 1500)]
    for label, x in agents:
        rounded(d, (x, 620, x + 280, 820), CARD, outline=ACCENT, radius=18)
        center_text(d, (x + 140, 720), label, body)
        arrow(d, (960, 360), (x + 140, 620), MUTED, 3)
    save(img, "01/12-multi-agent.png")


def v13_context():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "What is Context?", title)
    rounded(d, (710, 400, 1210, 640), CARD2, outline=ACCENT, radius=24)
    center_text(d, (960, 520), "Agent Decision", font(32, True))
    parts = [
        (200, 200, "User request"),
        (760, 160, "Tools"),
        (1320, 200, "State"),
        (200, 780, "Memory"),
        (760, 840, "Policy"),
        (1320, 780, "Observations"),
    ]
    for x, y, label in parts:
        rounded(d, (x, y, x + 360, y + 100), CARD, outline=LINE, radius=16)
        center_text(d, (x + 180, y + 50), label, body)
        arrow(d, (x + 180, y + 50), (960, 520), MUTED, 2)
    save(img, "01/13-context.png")


def v14_permissions():
    img, d = new_img()
    title = font(44, True)
    body = font(24)
    center_text(d, (W / 2, 55), "Same Tools · Different Permissions", title)
    headers = [("Read", GREEN), ("Write", ORANGE), ("Dangerous", RED)]
    tools = ["get_logs", "restart_service", "delete_resource"]
    for i, (h, c) in enumerate(headers):
        x = 200 + i * 550
        rounded(d, (x, 180, x + 480, 900), CARD, outline=c, radius=20)
        center_text(d, (x + 240, 250), h, font(34, True), c)
        for j, t in enumerate(tools):
            y = 360 + j * 150
            allowed = (i == 0 and j == 0) or (i == 1 and j <= 1) or (i == 2)
            fill = CARD2 if allowed else (40, 30, 30)
            outline = c if allowed else LINE
            label = t if allowed else f"{t} ✕"
            rounded(d, (x + 40, y, x + 440, y + 100), fill, outline=outline, radius=14)
            center_text(d, (x + 240, y + 50), label, body, TEXT if allowed else MUTED)
    save(img, "01/14-tool-permissions.png")


def v15_failure():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Failure Loop", title)
    rounded(d, (760, 180, 1160, 320), CARD2, outline=RED, radius=18)
    center_text(d, (960, 250), "Tool failure", font(30, True), RED)
    branches = [
        (200, 520, "Retry", ORANGE),
        (760, 520, "Alternate tool", ACCENT),
        (1320, 520, "Escalate to human", GREEN),
    ]
    for x, y, label, c in branches:
        rounded(d, (x, y, x + 400, y + 140), CARD, outline=c, radius=18)
        center_text(d, (x + 200, y + 70), label, body, c)
        arrow(d, (960, 320), (x + 200, y), c, 3)
    save(img, "01/15-failure-loop.png")


def v01_architecture():
    img, d = new_img()
    title = font(44, True)
    body = font(24)
    center_text(d, (W / 2, 50), "Agent Architecture", title)
    layers = [
        (W / 2, 160, "USER", ACCENT),
        (W / 2, 320, "AGENT RUNTIME", ACCENT2),
        (W / 2, 480, "LLM", TEXT),
    ]
    for x, y, label, c in layers:
        rounded(d, (x - 280, y - 55, x + 280, y + 55), CARD2, outline=c, radius=18)
        center_text(d, (x, y), label, font(28, True))
        if label != "LLM":
            arrow(d, (x, y + 55), (x, y + 105), MUTED, 3)
    bottoms = [("TOOLS", 320), ("STATE", 760), ("MEMORY", 1200), ("POLICY", 1640)]
    for label, x in bottoms:
        # fix - use better spacing
        pass
    bottoms = [("TOOLS", 280), ("STATE", 720), ("MEMORY", 1160), ("POLICY", 1600)]
    for label, x in bottoms:
        rounded(d, (x, 700, x + 280, 880), CARD, outline=LINE, radius=16)
        center_text(d, (x + 140, 790), label, body)
        arrow(d, (960, 535), (x + 140, 700), MUTED, 3)
    save(img, "01/16-agent-architecture.png")


# ---------- Session 02 ----------

def s02_planning_hero():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Planning & Execution", title)
    rounded(d, (120, 400, 420, 620), CARD2, outline=ACCENT)
    center_text(d, (270, 510), "GOAL", font(32, True))
    rounded(d, (560, 400, 920, 620), CARD2, outline=ACCENT2)
    multiline_center(d, (740, 510), ["PLAN", "decompose"], body)
    rounded(d, (1060, 300, 1420, 460), CARD, outline=GREEN)
    center_text(d, (1240, 380), "Action 1", body)
    rounded(d, (1060, 500, 1420, 660), CARD, outline=GREEN)
    center_text(d, (1240, 580), "Action 2", body)
    rounded(d, (1060, 700, 1420, 860), CARD, outline=GREEN)
    center_text(d, (1240, 780), "Action N", body)
    rounded(d, (1560, 400, 1860, 620), CARD2, outline=ORANGE)
    center_text(d, (1710, 510), "RESULT", font(28, True))
    arrow(d, (420, 510), (560, 510))
    arrow(d, (920, 510), (1060, 380), MUTED, 3)
    arrow(d, (920, 510), (1060, 580), MUTED, 3)
    arrow(d, (920, 510), (1060, 780), MUTED, 3)
    arrow(d, (1420, 580), (1560, 510))
    save(img, "02/01-goal-plan-actions.png")


def s02_decompose():
    img, d = new_img()
    title = font(48, True)
    body = font(24)
    center_text(d, (W / 2, 55), "Task Decomposition", title)
    rounded(d, (660, 140, 1260, 280), CARD2, outline=ACCENT, radius=18)
    center_text(d, (960, 210), "Investigate CI failure", font(30, True))
    tasks = [
        "Get job status",
        "Read console log",
        "Check recent changes",
        "Inspect runner",
        "Compare past failures",
        "Propose root cause",
    ]
    for i, t in enumerate(tasks):
        col = i % 3
        row = i // 3
        x = 200 + col * 560
        y = 400 + row * 220
        rounded(d, (x, y, x + 480, y + 140), CARD, outline=LINE, radius=16)
        center_text(d, (x + 240, y + 70), t, body)
        arrow(d, (960, 280), (x + 240, y), MUTED, 2)
    save(img, "02/02-task-decomposition.png")


def s02_open_closed():
    img, d = new_img()
    title = font(44, True)
    body = font(24)
    center_text(d, (W / 2, 50), "Open-Loop vs Closed-Loop Planning", title)
    # open
    rounded(d, (80, 140, 920, 980), CARD)
    center_text(d, (500, 200), "Open Loop", font(34, True), ORANGE)
    steps = ["Plan all", "Execute 1", "Execute 2", "Execute 3", "Done"]
    for i, s in enumerate(steps):
        y = 280 + i * 120
        rounded(d, (200, y, 800, y + 90), CARD2, outline=LINE, radius=14)
        center_text(d, (500, y + 45), s, body)
    # closed
    rounded(d, (1000, 140, 1840, 980), CARD)
    center_text(d, (1420, 200), "Closed Loop", font(34, True), GREEN)
    steps2 = ["Plan", "Act", "Observe", "Re-plan?", "Act / Stop"]
    for i, s in enumerate(steps2):
        y = 280 + i * 120
        rounded(d, (1120, y, 1720, y + 90), CARD2, outline=GREEN if i == 3 else LINE, radius=14)
        center_text(d, (1420, y + 45), s, body)
    save(img, "02/03-open-vs-closed-loop.png")


def s02_react():
    img, d = new_img()
    title = font(48, True)
    body = font(28, True)
    center_text(d, (W / 2, 55), "ReAct: Reason → Act → Observe", title)
    nodes = [("Thought", 300), ("Action", 760), ("Observation", 1220)]
    colors = [ACCENT2, ACCENT, GREEN]
    for (label, x), c in zip(nodes, colors):
        rounded(d, (x, 420, x + 400, 620), CARD2, outline=c, radius=22)
        center_text(d, (x + 200, 520), label, body, c)
    arrow(d, (700, 520), (760, 520))
    arrow(d, (1160, 520), (1220, 520))
    # feedback
    d.arc([300, 300, 1620, 820], start=200, end=340, fill=GREEN, width=5)
    center_text(d, (960, 280), "repeat until done", font(26), MUTED)
    save(img, "02/04-react.png")


def s02_plan_execute():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Plan-and-Execute", title)
    rounded(d, (200, 350, 700, 650), CARD2, outline=ACCENT2, radius=22)
    multiline_center(d, (450, 500), ["PLANNER", "creates plan"], body)
    rounded(d, (1220, 350, 1720, 650), CARD2, outline=GREEN, radius=22)
    multiline_center(d, (1470, 500), ["EXECUTOR", "runs steps"], body)
    arrow(d, (700, 500), (1220, 500))
    rounded(d, (760, 720, 1160, 900), CARD, outline=ORANGE, radius=18)
    center_text(d, (960, 810), "Feedback / Re-plan", body, ORANGE)
    arrow(d, (1470, 650), (1060, 720), MUTED, 3)
    arrow(d, (860, 720), (450, 650), MUTED, 3)
    save(img, "02/05-plan-and-execute.png")


def s02_failure():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Failure Handling", title)
    rounded(d, (710, 160, 1210, 300), CARD2, outline=RED, radius=18)
    center_text(d, (960, 230), "Step failed", font(32, True), RED)
    options = [
        (160, 480, "Retry\n(+ backoff)", ORANGE),
        (620, 480, "Different tool", ACCENT),
        (1080, 480, "Local re-plan", ACCENT2),
        (1540, 480, "Escalate", GREEN),
    ]
    for x, y, label, c in options:
        rounded(d, (x, y, x + 280, y + 200), CARD, outline=c, radius=16)
        multiline_center(d, (x + 140, y + 100), label.split("\n"), body, c)
        arrow(d, (960, 300), (x + 140, y), c, 3)
    save(img, "02/06-failure-handling.png")


def s02_policy():
    img, d = new_img()
    title = font(48, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Plan → Policy Gate → Execute", title)
    rounded(d, (160, 420, 560, 620), CARD2, outline=ACCENT, radius=18)
    center_text(d, (360, 520), "Candidate plan", body)
    rounded(d, (720, 360, 1200, 680), CARD2, outline=ORANGE, radius=22)
    multiline_center(d, (960, 520), ["POLICY GATE", "constraints", "permissions"], body, ORANGE)
    rounded(d, (1360, 300, 1760, 450), CARD, outline=GREEN, radius=16)
    center_text(d, (1560, 375), "Allowed", body, GREEN)
    rounded(d, (1360, 520, 1760, 670), CARD, outline=RED, radius=16)
    center_text(d, (1560, 595), "Blocked / HITL", body, RED)
    arrow(d, (560, 520), (720, 520))
    arrow(d, (1200, 450), (1360, 375), GREEN, 3)
    arrow(d, (1200, 560), (1360, 595), RED, 3)
    save(img, "02/07-policy-gate.png")


def s02_state():
    img, d = new_img()
    title = font(48, True)
    body = font(24)
    center_text(d, (W / 2, 55), "Execution State", title)
    rounded(d, (710, 400, 1210, 640), CARD2, outline=ACCENT, radius=24)
    center_text(d, (960, 520), "Agent", font(34, True))
    fields = [
        (160, 200, "current_step"),
        (760, 160, "completed[]"),
        (1360, 200, "failed[]"),
        (160, 780, "findings"),
        (760, 840, "pending[]"),
        (1360, 780, "budget left"),
    ]
    for x, y, label in fields:
        rounded(d, (x, y, x + 400, y + 100), CARD, outline=LINE, radius=14)
        center_text(d, (x + 200, y + 50), label, body)
        arrow(d, (x + 200, y + 50), (960, 520), MUTED, 2)
    save(img, "02/08-execution-state.png")


def s02_incident():
    img, d = new_img()
    title = font(44, True)
    small = font(22)
    center_text(d, (W / 2, 55), "Incident Investigation Agent", title)
    rounded(d, (760, 420, 1160, 620), CARD2, outline=ACCENT, radius=24)
    center_text(d, (960, 520), "Incident\nAgent", font(30, True))
    systems = [
        (140, 220, "K8s"),
        (140, 480, "Metrics"),
        (140, 740, "Logs"),
        (1480, 220, "Deploy hist"),
        (1480, 480, "Incidents DB"),
        (1480, 740, "On-call"),
    ]
    for x, y, label in systems:
        rounded(d, (x, y, x + 300, y + 100), CARD, outline=LINE, radius=14)
        center_text(d, (x + 150, y + 50), label, small)
        arrow(d, (960, 520), (x + 150, y + 50), ACCENT, 3)
    save(img, "02/09-incident-agent.png")


def s02_validation():
    img, d = new_img()
    title = font(44, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Three kinds of success", title)
    items = [
        (160, "Tool success", "API returned 200", ACCENT),
        (700, "Step success", "Got useful evidence", ACCENT2),
        (1240, "Goal success", "Root cause found", GREEN),
    ]
    for x, title_t, sub, c in items:
        rounded(d, (x, 320, x + 480, 720), CARD, outline=c, radius=22)
        center_text(d, (x + 240, 420), title_t, font(30, True), c)
        multiline_center(d, (x + 240, 560), [sub], body, MUTED)
    save(img, "02/10-three-success.png")


def demo_terminal(path: str, title: str, lines: list[tuple[str, tuple[int, int, int]]]):
    """Fake Claude Code / terminal demo screenshot."""
    img = Image.new("RGB", (W, H), (12, 14, 18))
    d = ImageDraw.Draw(img)
    # window chrome
    rounded(d, (80, 80, 1840, 1000), (22, 26, 34), radius=20, outline=(50, 55, 70))
    d.ellipse([120, 120, 160, 160], fill=(255, 95, 86))
    d.ellipse([180, 120, 220, 160], fill=(255, 189, 46))
    d.ellipse([240, 120, 280, 160], fill=(39, 201, 63))
    d.text((340, 118), title, font=font(28, True), fill=MUTED)
    mono = font(26)
    y = 200
    for text, color in lines:
        d.text((140, y), text, font=mono, fill=color)
        y += 48
    save(img, path)


def demos():
    demo_terminal(
        "01/demo-k8s-agent.png",
        "demo · agent session",
        [
            ("> Check the current state of the API service", TEXT),
            ("  and tell me if anything looks wrong.", TEXT),
            ("", TEXT),
            ("thought: I need deployment status first.", ACCENT2),
            ("tool → get_deployments(\"api\")", ACCENT),
            ("obs  ← desired:3 ready:3 available:3", GREEN),
            ("", TEXT),
            ("thought: Deployments look fine. Check pods.", ACCENT2),
            ("tool → get_pods(\"api\")", ACCENT),
            ("obs  ← 2 Running, 1 CrashLoopBackOff", ORANGE),
            ("", TEXT),
            ("thought: One pod is unhealthy. Fetch logs.", ACCENT2),
            ("tool → get_logs(\"api-7f9d\")", ACCENT),
            ("obs  ← NullPointerException in handler", RED),
            ("", TEXT),
            ("answer: API has 1 crashing pod; NPE in handler.", TEXT),
        ],
    )
    demo_terminal(
        "02/demo-plan-execute.png",
        "demo · plan then execute",
        [
            ("> Find why the CI job failed.", TEXT),
            ("", TEXT),
            ("plan:", ACCENT2),
            ("  1. get_job_status()", MUTED),
            ("  2. get_console_log() if failed", MUTED),
            ("  3. get_recent_changes()", MUTED),
            ("  4. hypothesize root cause", MUTED),
            ("", TEXT),
            ("exec 1 → get_job_status()", ACCENT),
            ("obs   ← status=FAILED  exit=1", ORANGE),
            ("exec 2 → get_console_log()", ACCENT),
            ("obs   ← ERROR: ModuleNotFoundError: pytest", RED),
            ("", TEXT),
            ("re-plan: skip runner check; inspect requirements.", ACCENT2),
            ("exec 3 → get_recent_changes()", ACCENT),
            ("obs   ← requirements.txt dropped pytest", ORANGE),
            ("answer: Missing test dependency after recent commit.", TEXT),
        ],
    )



# ---------- Session 03 ----------

def s03_tool_hero():
    img, d = new_img()
    title = font(46, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Tool Use & Function Calling", title)
    boxes = [
        (120, 320, 480, 560, "LLM", "proposes call", ACCENT2),
        (720, 320, 1080, 560, "Host", "validate + run", ACCENT),
        (1320, 320, 1680, 560, "Tool", "side effect / data", GREEN),
    ]
    for x1, y1, x2, y2, t, s, c in boxes:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=20)
        center_text(d, ((x1 + x2) / 2, (y1 + y2) / 2 - 30), t, font(34, True), c)
        center_text(d, ((x1 + x2) / 2, (y1 + y2) / 2 + 40), s, body, MUTED)
    arrow(d, (480, 440), (720, 440))
    arrow(d, (1080, 440), (1320, 440))
    # observe back
    d.arc([200, 200, 1600, 780], start=200, end=340, fill=ORANGE, width=5)
    center_text(d, (960, 220), "Observation → back to LLM", font(26), ORANGE)
    save(img, "03/01-tool-calling-loop.png")


def s03_protocol():
    img, d = new_img()
    title = font(42, True)
    body = font(24)
    small = font(22)
    center_text(d, (W / 2, 50), "Function Calling Protocol", title)
    steps = [
        ("1", "Send schemas\n+ user goal", ACCENT),
        ("2", "Model returns\ntool_calls", ACCENT2),
        ("3", "Host executes\n(not the model)", GREEN),
        ("4", "tool results\nwith call ids", ORANGE),
        ("5", "Model answers\nor calls again", ACCENT),
    ]
    for i, (n, label, c) in enumerate(steps):
        x = 80 + i * 370
        rounded(d, (x, 380, x + 320, 720), CARD2, outline=c, radius=18)
        center_text(d, (x + 160, 460), n, font(40, True), c)
        multiline_center(d, (x + 160, 580), label.split("\n"), body)
        if i < 4:
            arrow(d, (x + 320, 550), (x + 370, 550), MUTED, 3)
    center_text(d, (W / 2, 900), "Model proposes · Code executes · Observation returns", small, MUTED)
    save(img, "03/02-protocol-steps.png")


def s03_schema():
    img, d = new_img()
    title = font(44, True)
    body = font(24)
    center_text(d, (W / 2, 50), "Tool Schema = Contract", title)
    rounded(d, (100, 160, 900, 980), CARD)
    center_text(d, (500, 220), "Good schema", font(32, True), GREEN)
    lines = [
        'name: get_order',
        'description: Fetch order by id',
        '  (support only; not refunds)',
        'params:',
        '  order_id: string  required',
        '  fields: enum[status,total]',
    ]
    y = 300
    for line in lines:
        d.text((160, y), line, font=body, fill=TEXT)
        y += 70
    rounded(d, (1020, 160, 1820, 980), CARD)
    center_text(d, (1420, 220), "Bad schema", font(32, True), RED)
    bad = [
        'name: do_stuff',
        'description: helpful tool',
        'params:',
        '  data: string',
        '  options: object',
        '  → hallucinated args',
    ]
    y = 300
    for line in bad:
        d.text((1080, y), line, font=body, fill=TEXT)
        y += 70
    save(img, "03/03-schema-good-bad.png")


def s03_tool_choice():
    img, d = new_img()
    title = font(44, True)
    body = font(26)
    center_text(d, (W / 2, 55), "tool_choice", title)
    items = [
        ("auto", "Model decides", ACCENT),
        ("required", "Must call a tool", ACCENT2),
        ("named", "Force one tool", GREEN),
        ("none", "Text only", ORANGE),
    ]
    for i, (k, v, c) in enumerate(items):
        x = 120 + (i % 2) * 900
        y = 200 + (i // 2) * 380
        rounded(d, (x, y, x + 800, y + 300), CARD2, outline=c, radius=20)
        center_text(d, (x + 400, y + 110), k, font(40, True), c)
        center_text(d, (x + 400, y + 200), v, body)
    save(img, "03/04-tool-choice.png")


def s03_parallel():
    img, d = new_img()
    title = font(42, True)
    body = font(24)
    center_text(d, (W / 2, 50), "Parallel vs Sequential Tools", title)
    # sequential
    rounded(d, (80, 140, 920, 980), CARD)
    center_text(d, (500, 200), "Sequential", font(32, True), ORANGE)
    seq = ["get_customer", "get_orders(customer)", "summarize"]
    for i, s in enumerate(seq):
        y = 300 + i * 180
        rounded(d, (200, y, 800, y + 120), CARD2, outline=LINE, radius=14)
        center_text(d, (500, y + 60), s, body)
        if i < 2:
            arrow(d, (500, y + 120), (500, y + 180), MUTED, 3)
    # parallel
    rounded(d, (1000, 140, 1840, 980), CARD)
    center_text(d, (1420, 200), "Parallel", font(32, True), GREEN)
    rounded(d, (1180, 300, 1660, 420), CARD2, outline=ACCENT, radius=14)
    center_text(d, (1420, 360), "get_metrics", body)
    rounded(d, (1180, 480, 1660, 600), CARD2, outline=ACCENT, radius=14)
    center_text(d, (1420, 540), "get_logs", body)
    rounded(d, (1180, 660, 1660, 780), CARD2, outline=ACCENT, radius=14)
    center_text(d, (1420, 720), "get_deploys", body)
    rounded(d, (1180, 840, 1660, 960), CARD2, outline=GREEN, radius=14)
    center_text(d, (1420, 900), "fan-in → reason", body)
    save(img, "03/05-parallel-vs-sequential.png")


def s03_validate():
    img, d = new_img()
    title = font(42, True)
    body = font(26)
    center_text(d, (W / 2, 55), "Validate → Execute → Observe", title)
    nodes = [
        (200, "tool_call\nJSON", ACCENT2),
        (700, "validate\nschema+policy", ORANGE),
        (1200, "execute\nhandler", ACCENT),
        (1580, "observation\nstructured", GREEN),
    ]
    for x, label, c in nodes:
        rounded(d, (x, 420, x + 280, 660), CARD2, outline=c, radius=18)
        multiline_center(d, (x + 140, 540), label.split("\n"), body, c)
    for i in range(3):
        x1 = nodes[i][0] + 280
        x2 = nodes[i + 1][0]
        arrow(d, (x1, 540), (x2, 540))
    center_text(d, (W / 2, 850), "Reject bad args before side effects", font(28), MUTED)
    save(img, "03/06-validate-execute.png")


def s03_mcp():
    img, d = new_img()
    title = font(44, True)
    body = font(26)
    center_text(d, (W / 2, 55), "MCP (intro): portable tools", title)
    boxes = [
        (150, 380, 550, 700, "Host App", "Agent runtime", ACCENT),
        (700, 380, 1100, 700, "MCP Client", "connects", ACCENT2),
        (1250, 380, 1750, 700, "MCP Server", "exposes tools", GREEN),
    ]
    for x1, y1, x2, y2, t, s, c in boxes:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=20)
        center_text(d, ((x1 + x2) / 2, (y1 + y2) / 2 - 40), t, font(32, True), c)
        center_text(d, ((x1 + x2) / 2, (y1 + y2) / 2 + 40), s, body, MUTED)
    arrow(d, (550, 540), (700, 540))
    arrow(d, (1100, 540), (1250, 540))
    center_text(d, (W / 2, 860), "Same tool contract · many servers · many hosts", font(26), MUTED)
    save(img, "03/07-mcp-intro.png")


def s03_catalog():
    img, d = new_img()
    title = font(42, True)
    body = font(24)
    center_text(d, (W / 2, 50), "Tool Catalog Tradeoffs", title)
    rows = [
        ("Few sharp tools", "Clear choice · low tokens", GREEN),
        ("Many vague tools", "Confusion · high cost", ORANGE),
        ("Dangerous tools", "Policy / HITL / allow-list", RED),
        ("Idempotent tools", "Safe retries", ACCENT),
    ]
    for i, (a, b, c) in enumerate(rows):
        y = 180 + i * 200
        rounded(d, (200, y, 1720, y + 160), CARD2, outline=c, radius=16)
        center_text(d, (600, y + 80), a, font(30, True), c)
        center_text(d, (1300, y + 80), b, body)
    save(img, "03/08-catalog-tradeoffs.png")




# ---------- Session 04 ----------

def _s04_legend(d, items, x=80, y=980):
    """items: list of (color, label)."""
    f = font(20)
    cx = x
    for color, label in items:
        d.ellipse([cx, y - 10, cx + 18, y + 8], fill=color)
        d.text((cx + 26, y - 12), label, font=f, fill=MUTED)
        bbox = d.textbbox((0, 0), label, font=f)
        cx += 40 + (bbox[2] - bbox[0]) + 28


def _s04_panel(d, box, title, lines, outline=LINE, title_color=TEXT):
    rounded(d, box, CARD, outline=outline, radius=14, width=2)
    x1, y1, x2, y2 = box
    center_text(d, ((x1 + x2) / 2, y1 + 28), title, font(22, True), title_color)
    f = font(20)
    ty = y1 + 58
    for line in lines:
        d.text((x1 + 18, ty), line, font=f, fill=MUTED)
        ty += 28


def s04_hero():
    """Rich support-agent graph: nodes, loop, HITL branch, State sidebar."""
    img, d = new_img()
    center_text(d, (W / 2, 42), "LangGraph — Support Agent as a State Graph", font(40, True))
    center_text(
        d,
        (W / 2, 88),
        "Nodes do work · Edges choose the next step · State is the shared memory of the run",
        font(22),
        MUTED,
    )

    _s04_panel(
        d,
        (40, 140, 420, 900),
        "Shared State (example)",
        [
            "customer_id: C-9912",
            "question: refund?",
            "messages[]  (+ Reducer)",
            "order_status: shipped",
            "draft_reply: …",
            "needs_hitl: True",
            "step_count: 3",
            "",
            "Each node returns UPDATES",
            "(not always the full object).",
            "Graph merges updates into",
            "this State after every step.",
        ],
        outline=ACCENT,
        title_color=ACCENT,
    )

    nodes = [
        (520, 200, 780, 320, "START", ACCENT, ["entry", "load input"]),
        (860, 160, 1180, 320, "lookup_order", GREEN, ["Tool / API", "writes order_status"]),
        (1260, 160, 1580, 320, "draft_reply", ACCENT2, ["LLM node", "writes draft + messages"]),
        (900, 420, 1220, 560, "route", ORANGE, ["Conditional Edge", "reads State flags"]),
        (520, 640, 820, 820, "tools", GREEN, ["Validate→Execute", "Session-3 host"]),
        (900, 640, 1220, 820, "hitl_approve", ORANGE, ["interrupt()", "wait for human"]),
        (1380, 640, 1720, 820, "END", MUTED, ["final answer", "or deny"]),
    ]
    for x1, y1, x2, y2, label, c, subs in nodes:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=16, width=3)
        center_text(d, ((x1 + x2) / 2, y1 + 36), label, font(24, True), c)
        multiline_center(d, ((x1 + x2) / 2, (y1 + y2) / 2 + 22), subs, font(18), MUTED, gap=4)

    arrow(d, (780, 260), (860, 240), ACCENT, 4)
    arrow(d, (1180, 240), (1260, 240), ACCENT, 4)
    arrow(d, (1420, 320), (1060, 420), ACCENT, 4)
    arrow(d, (900, 520), (700, 640), GREEN, 4)
    arrow(d, (1060, 560), (1060, 640), ORANGE, 4)
    arrow(d, (1220, 520), (1500, 640), MUTED, 4)
    arrow(d, (670, 640), (670, 360), GREEN, 3)
    arrow(d, (670, 360), (860, 240), GREEN, 3)
    center_text(d, (620, 480), "loop", font(18), GREEN)
    arrow(d, (1220, 730), (1380, 730), ORANGE, 3)

    center_text(d, (700, 580), "has tool_calls", font(18), GREEN)
    center_text(d, (1180, 600), "needs_hitl", font(18), ORANGE)
    center_text(d, (1380, 560), "done", font(18), MUTED)

    _s04_legend(
        d,
        [
            (ACCENT, "control / LLM"),
            (GREEN, "tools"),
            (ORANGE, "decision / HITL"),
            (MUTED, "terminal"),
        ],
        x=480,
        y=980,
    )
    save(img, "04/01-langgraph-hero.png")


def s04_graph_basics():
    img, d = new_img()
    center_text(d, (W / 2, 42), "Directed Graph — Nodes, Edges, Direction", font(40, True))
    center_text(
        d,
        (W / 2, 88),
        "Everyday example (café) mapped to Agent vocabulary",
        font(22),
        MUTED,
    )

    cafe = [
        (80, 180, 380, 340, "1. Order", "customer request", ACCENT),
        (460, 180, 760, 340, "2. Prepare", "barista action", GREEN),
        (840, 180, 1140, 340, "3. Pay", "checkout", ACCENT2),
        (1220, 180, 1520, 340, "4. Deliver", "hand-off", ORANGE),
    ]
    for x1, y1, x2, y2, t, sub, c in cafe:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=16, width=3)
        center_text(d, ((x1 + x2) / 2, y1 + 50), t, font(26, True), c)
        center_text(d, ((x1 + x2) / 2, y1 + 110), sub, font(20), MUTED)
    for x in (380, 760, 1140):
        arrow(d, (x, 260), (x + 80, 260), ACCENT, 4)
        center_text(d, (x + 40, 220), "Edge", font(18), MUTED)

    rounded(d, (840, 420, 1140, 560), CARD2, outline=RED, radius=14, width=3)
    multiline_center(d, (990, 490), ["Cancel branch", "Conditional Edge"], font(22, True), RED)
    arrow(d, (990, 340), (990, 420), RED, 3)
    center_text(d, (1120, 380), "if cancelled", font(18), RED)

    cards = [
        (80, 620, 600, 900, "Node", ACCENT, [
            "A named step / function",
            "Does the real work:",
            "  · call LLM",
            "  · call Tool / API",
            "  · validate / compute",
            "Returns State updates",
        ]),
        (660, 620, 1180, 900, "Edge", GREEN, [
            "Who runs next",
            "Normal edge: always A→B",
            "Conditional: function picks",
            "  one of several targets",
            "Edges should NOT call APIs",
            "(routing only)",
        ]),
        (1240, 620, 1840, 900, "Directed + Loops", ORANGE, [
            "Arrows have direction",
            "A→B does NOT imply B→A",
            "Loops ARE allowed in",
            "  LangGraph (not a DAG)",
            "Always pair loops with",
            "  MAX_STEPS / Budget",
        ]),
    ]
    for x1, y1, x2, y2, title, c, lines in cards:
        rounded(d, (x1, y1, x2, y2), CARD, outline=c, radius=16, width=3)
        center_text(d, ((x1 + x2) / 2, y1 + 36), title, font(24, True), c)
        f = font(20)
        ty = y1 + 70
        for line in lines:
            d.text((x1 + 24, ty), line, font=f, fill=MUTED)
            ty += 32
    save(img, "04/02-graph-basics.png")


def s04_state():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Shared State — read, update, merge", font(40, True))
    center_text(
        d,
        (W / 2, 84),
        "One memory box for the whole run · each node touches only what it owns",
        font(22),
        MUTED,
    )

    rounded(d, (620, 130, 1300, 980), CARD2, outline=ACCENT, radius=20, width=3)
    center_text(d, (960, 170), "AgentState", font(30, True), ACCENT)
    fields = [
        ("messages[]", "Annotated + add_messages (Reducer)", GREEN),
        ("customer_id", "from user input", MUTED),
        ("question", "from user input", MUTED),
        ("order_status", "written by lookup_order", GREEN),
        ("draft_reply", "written by draft node / LLM", ACCENT2),
        ("needs_hitl", "written by policy / draft", ORANGE),
        ("step_count", "budget counter (++ each loop)", ORANGE),
    ]
    for i, (name, note, c) in enumerate(fields):
        y = 220 + i * 95
        rounded(d, (660, y, 1260, y + 78), CARD, outline=c, radius=12, width=2)
        d.text((690, y + 12), name, font=font(22, True), fill=c)
        d.text((690, y + 42), note, font=font(18), fill=MUTED)

    _s04_panel(
        d,
        (40, 160, 560, 500),
        "Node: lookup_order",
        [
            "READS  customer_id",
            "CALLS  get_order tool",
            "WRITES order_status",
            "",
            "return {",
            '  "order_status": "shipped"',
            "}",
        ],
        outline=GREEN,
        title_color=GREEN,
    )
    _s04_panel(
        d,
        (40, 540, 560, 900),
        "Node: draft_reply",
        [
            "READS  question, order_status",
            "CALLS  LLM",
            "WRITES draft_reply, messages",
            "        maybe needs_hitl",
            "",
            "Partial updates only —",
            "customer_id stays untouched.",
        ],
        outline=ACCENT2,
        title_color=ACCENT2,
    )

    _s04_panel(
        d,
        (1360, 160, 1880, 520),
        "Why Reducer matters",
        [
            "Without add_messages:",
            "  messages=[new] WIPES history",
            "",
            "With add_messages:",
            "  new messages are APPENDED",
            "",
            "Symptom of the bug:",
            "  after step 2, early turns vanish",
            "  → model 'forgets' context",
        ],
        outline=RED,
        title_color=RED,
    )
    _s04_panel(
        d,
        (1360, 560, 1880, 900),
        "Merge rule of thumb",
        [
            "Growing lists → need Reducer",
            "Scalar flags → overwrite OK",
            "  (status, needs_hitl)",
            "",
            "Parallel nodes in one step",
            "all read the SAME snapshot,",
            "then updates merge by rule.",
        ],
        outline=ORANGE,
        title_color=ORANGE,
    )
    save(img, "04/03-shared-state.png")


def s04_conditional():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Conditional Edge — should_continue router", font(38, True))
    center_text(
        d,
        (W / 2, 84),
        "Routing function reads State · returns a key · graph jumps to that node",
        font(22),
        MUTED,
    )

    rounded(d, (660, 120, 1260, 280), CARD2, outline=ACCENT2, radius=18, width=3)
    multiline_center(
        d,
        (960, 200),
        ["agent (LLM node)", "may emit tool_calls · may set needs_hitl · may answer"],
        font(22),
        ACCENT2,
        gap=8,
    )

    rounded(d, (720, 340, 1200, 500), CARD2, outline=ORANGE, radius=18, width=3)
    multiline_center(
        d,
        (960, 420),
        ["should_continue(state) -> str", "pure function · no network · easy to unit-test"],
        font(22, True),
        ORANGE,
        gap=8,
    )
    arrow(d, (960, 280), (960, 340), ACCENT, 4)

    targets = [
        (80, 580, 560, 820, "tools", GREEN, [
            'return "tools"',
            "when last message",
            "has tool_calls",
            "",
            "then: Validate -> Execute",
            "write Observations",
            "EDGE back -> agent",
        ]),
        (680, 580, 1240, 820, "hitl", ORANGE, [
            'return "hitl"',
            "when needs_hitl is True",
            "(and no open tool_calls)",
            "",
            "then: interrupt(payload)",
            "wait for approve/reject",
            "resume same thread_id",
        ]),
        (1360, 580, 1840, 820, "end", MUTED, [
            'return "end"',
            "when answer ready",
            "and no tools / HITL",
            "",
            "also: step_count >= MAX",
            "-> stop_budget path",
            "(prevents infinite loops)",
        ]),
    ]
    for x1, y1, x2, y2, title, c, lines in targets:
        rounded(d, (x1, y1, x2, y2), CARD, outline=c, radius=16, width=3)
        center_text(d, ((x1 + x2) / 2, y1 + 32), title, font(26, True), c)
        f = font(18)
        ty = y1 + 70
        for line in lines:
            d.text((x1 + 24, ty), line, font=f, fill=MUTED)
            ty += 26

    arrow(d, (800, 500), (320, 580), GREEN, 4)
    arrow(d, (960, 500), (960, 580), ORANGE, 4)
    arrow(d, (1120, 500), (1600, 580), MUTED, 4)

    center_text(d, (180, 400), "loop until", font(18), GREEN)
    center_text(d, (180, 430), "done / budget", font(18), GREEN)

    center_text(
        d,
        (W / 2, 980),
        'add_conditional_edges("agent", should_continue, {"tools":..., "hitl":..., "end": END})',
        font(20),
        MUTED,
    )
    save(img, "04/04-conditional-edges.png")


def s04_checkpoint():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Checkpoint — snapshot after every super-step", font(38, True))
    center_text(
        d,
        (W / 2, 84),
        "Not a text log · a loadable State photo keyed by thread_id",
        font(22),
        MUTED,
    )

    steps = [
        (100, "super-step 1", "lookup_order", "order_status=shipped"),
        (520, "super-step 2", "draft_reply", "draft ready · needs_hitl"),
        (940, "super-step 3", "hitl interrupt", "PAUSED for human"),
        (1360, "super-step 4", "resume -> END", "approved · answered"),
    ]
    for x, title, node, detail in steps:
        rounded(d, (x, 150, x + 380, 360), CARD2, outline=ACCENT, radius=14, width=3)
        center_text(d, (x + 190, 190), title, font(20, True), ACCENT)
        center_text(d, (x + 190, 250), node, font(24, True), TEXT)
        center_text(d, (x + 190, 310), detail, font(18), MUTED)
    for x in (480, 900, 1320):
        arrow(d, (x, 255), (x + 40, 255), ACCENT, 4)

    for x in (240, 660, 1080, 1500):
        rounded(d, (x - 70, 400, x + 70, 460), CARD, outline=GREEN, radius=10, width=2)
        center_text(d, (x, 430), "ckpt", font(18), GREEN)

    _s04_panel(
        d,
        (80, 520, 640, 920),
        "thread_id",
        [
            'config = {"configurable": {',
            '  "thread_id": "ticket-9912"',
            "}}",
            "",
            "Same id -> continue / resume",
            "New id -> brand-new memory",
            "Shared id across users -> leak",
            "",
            "Use stable ticket / chat id.",
        ],
        outline=ORANGE,
        title_color=ORANGE,
    )
    _s04_panel(
        d,
        (680, 520, 1240, 920),
        "Checkpointer choices",
        [
            "InMemorySaver",
            "  · demos & unit tests",
            "  · dies with the process",
            "",
            "Sqlite / Postgres / ...",
            "  · production + HITL",
            "  · survives restarts",
            "  · needed with multiple workers",
            "",
            "compile(checkpointer=...)",
        ],
        outline=GREEN,
        title_color=GREEN,
    )
    _s04_panel(
        d,
        (1280, 520, 1840, 920),
        "What it unlocks",
        [
            "+ resume after crash",
            "+ Human-In-The-Loop",
            "+ debug / time-travel*",
            "+ durable long runs",
            "",
            "* depending on tooling",
            "",
            "!= long-term Memory (S6)",
            "Checkpoint = this run's film",
            "Memory = lasting knowledge",
        ],
        outline=ACCENT2,
        title_color=ACCENT2,
    )
    save(img, "04/05-checkpoint.png")


def s04_hitl():
    img, d = new_img()
    center_text(d, (W / 2, 40), "HITL — interrupt -> human -> resume", font(40, True))
    center_text(
        d,
        (W / 2, 84),
        "Human In The Loop · requires Checkpointer + stable thread_id",
        font(22),
        MUTED,
    )

    flow = [
        (60, 140, 400, 320, "1. Graph runs", ACCENT, ["lookup -> draft", "policy sets needs_hitl"]),
        (460, 140, 820, 320, "2. interrupt()", ORANGE, ["pause at sensitive node", "save Checkpoint"]),
        (880, 140, 1260, 320, "3. Human UI", ACCENT2, ["see risk payload", "Approve / Reject"]),
        (1320, 140, 1860, 320, "4. resume", GREEN, ["Command(resume=...)", "same thread_id"]),
    ]
    for x1, y1, x2, y2, title, c, lines in flow:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=14, width=3)
        center_text(d, ((x1 + x2) / 2, y1 + 40), title, font(22, True), c)
        multiline_center(d, ((x1 + x2) / 2, y1 + 120), lines, font(18), MUTED, gap=4)
    for x in (400, 820, 1260):
        arrow(d, (x, 230), (x + 60, 230), ACCENT, 4)

    rounded(d, (60, 360, 1860, 450), CARD, outline=GREEN, radius=12, width=2)
    center_text(
        d,
        (W / 2, 405),
        "Checkpointer underneath the whole timeline — without it, resume starts from zero",
        font(22),
        GREEN,
    )

    _s04_panel(
        d,
        (60, 490, 920, 920),
        "Good interrupt payload (for humans)",
        [
            "action: issue_refund",
            "amount: 249 ILS",
            "order_id: ORD-441",
            "risk: irreversible money move",
            "options: approve | reject",
            "",
            "NOT a raw dump of entire State.",
            "NOT a place to bypass a hard deny.",
            "",
            "If policy says FORBIDDEN -> END deny",
            "(do not ask the human to override).",
        ],
        outline=ORANGE,
        title_color=ORANGE,
    )
    _s04_panel(
        d,
        (980, 490, 1860, 920),
        "When to interrupt (policy examples)",
        [
            "Read logs / metrics          -> usually NO",
            "Draft email to customer      -> often YES",
            "Refund / delete / deploy     -> YES or FORBID",
            "High-confidence FAQ answer   -> NO",
            "",
            "Also define timeout:",
            "  if no human in 2h -> escalate / cancel",
            "",
            "UI validates approve|reject BEFORE",
            "the value reaches the graph.",
        ],
        outline=ACCENT2,
        title_color=ACCENT2,
    )
    save(img, "04/06-hitl-interrupt.png")


def s04_agent_loop():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Agent <-> Tools loop — Session 3 inside a graph", font(36, True))
    center_text(
        d,
        (W / 2, 84),
        "Function Calling protocol stays the same · Host becomes explicit Nodes + Edges",
        font(22),
        MUTED,
    )

    rounded(d, (80, 200, 280, 320), CARD2, outline=ACCENT, radius=14, width=3)
    center_text(d, (180, 260), "START", font(24, True), ACCENT)

    rounded(d, (400, 160, 860, 380), CARD2, outline=ACCENT2, radius=18, width=3)
    multiline_center(
        d,
        (630, 270),
        ["agent node", "LLM reasons", "may request tools"],
        font(22, True),
        ACCENT2,
        gap=6,
    )

    rounded(d, (400, 520, 860, 780), CARD2, outline=GREEN, radius=18, width=3)
    multiline_center(
        d,
        (630, 650),
        ["tools node", "1) Validate args", "2) Execute allow-listed tools", "3) Observations + tool_call_id"],
        font(20),
        GREEN,
        gap=6,
    )

    rounded(d, (1000, 240, 1400, 400), CARD2, outline=ORANGE, radius=16, width=3)
    multiline_center(
        d,
        (1200, 320),
        ["should_continue", "tools | hitl | end"],
        font(22, True),
        ORANGE,
        gap=6,
    )

    rounded(d, (1480, 160, 1840, 320), CARD2, outline=ORANGE, radius=14, width=3)
    center_text(d, (1660, 240), "HITL", font(26, True), ORANGE)
    rounded(d, (1480, 400, 1840, 560), CARD2, outline=MUTED, radius=14, width=3)
    center_text(d, (1660, 480), "END", font(26, True), MUTED)

    rounded(d, (1000, 520, 1400, 780), CARD2, outline=RED, radius=16, width=3)
    multiline_center(
        d,
        (1200, 650),
        ["Budget guard", "step_count++", "if >= MAX_STEPS -> END", "stop_budget reason"],
        font(20),
        RED,
        gap=6,
    )

    arrow(d, (280, 260), (400, 260), ACCENT, 4)
    arrow(d, (860, 270), (1000, 300), ORANGE, 4)
    arrow(d, (1100, 400), (700, 520), GREEN, 4)
    center_text(d, (820, 460), "tool_calls", font(18), GREEN)
    arrow(d, (630, 520), (630, 380), GREEN, 3)
    center_text(d, (760, 450), "observations", font(18), GREEN)
    arrow(d, (1400, 280), (1480, 240), ORANGE, 3)
    arrow(d, (1400, 340), (1480, 460), MUTED, 3)
    arrow(d, (1200, 520), (1200, 400), RED, 3)

    rounded(d, (80, 840, 1840, 1000), CARD, outline=LINE, radius=14, width=2)
    center_text(d, (W / 2, 875), "Session 3 mapping (unchanged contracts)", font(22, True), TEXT)
    center_text(
        d,
        (W / 2, 940),
        "Schema -> tool_calls -> Validate -> Execute -> Observation(+tool_call_id) -> model  |  LangGraph makes the loop visible & stoppable",
        font(20),
        MUTED,
    )
    save(img, "04/07-agent-tools-loop.png")


# ---------- Session 05 ----------

def _s05_agent_card(d, box, role, color, lines):
    x1, y1, x2, y2 = box
    rounded(d, box, CARD2, outline=color, radius=16, width=3)
    center_text(d, ((x1 + x2) / 2, y1 + 32), role, font(26, True), color)
    f = font(18)
    ty = y1 + 68
    for line in lines:
        d.text((x1 + 22, ty), line, font=f, fill=MUTED)
        ty += 26


def s05_hero():
    """Crew of specialised agents + orchestrator + shared artifacts."""
    img, d = new_img()
    center_text(d, (W / 2, 42), "Multi-Agent System — a crew of specialists, not one giant prompt", font(38, True))
    center_text(
        d,
        (W / 2, 88),
        "Each agent = role + goal + tools · Orchestrator hands work over · Artifacts are the shared memory",
        font(22),
        MUTED,
    )

    rounded(d, (700, 140, 1220, 290), CARD, outline=ACCENT, radius=18, width=3)
    multiline_center(
        d,
        (960, 215),
        ["Orchestrator / Crew", "owns the plan · decides hand-offs · enforces budget & HITL"],
        font(22, True),
        ACCENT,
        gap=8,
    )

    cards = [
        ((80, 400, 600, 720), "Researcher", GREEN, [
            "goal: collect verified facts",
            "tools: Read, Grep, get_order",
            "input: brief.md + policy.md",
            "output: facts.md (bullets + sources)",
            "",
            "never writes customer text",
        ]),
        ((700, 400, 1220, 720), "Writer", ACCENT2, [
            "goal: customer-facing Hebrew FAQ",
            "tools: Read, Write",
            "input: facts.md only",
            "output: faq.md",
            "",
            "no new facts allowed",
        ]),
        ((1320, 400, 1840, 720), "Reviewer", ORANGE, [
            "goal: catch policy violations",
            "tools: Read (read-only!)",
            "input: faq.md vs policy.md",
            "output: review.md + verdict",
            "",
            "APPROVE / REVISE (max 2 rounds)",
        ]),
    ]
    for box, role, c, lines in cards:
        _s05_agent_card(d, box, role, c, lines)

    arrow(d, (860, 290), (340, 400), GREEN, 4)
    arrow(d, (960, 290), (960, 400), ACCENT2, 4)
    arrow(d, (1060, 290), (1580, 400), ORANGE, 4)
    arrow(d, (600, 560), (700, 560), MUTED, 4)
    arrow(d, (1220, 560), (1320, 560), MUTED, 4)
    center_text(d, (650, 530), "facts.md", font(18), MUTED)
    center_text(d, (1270, 530), "faq.md", font(18), MUTED)

    rounded(d, (80, 790, 1840, 930), CARD, outline=LINE, radius=14, width=2)
    multiline_center(
        d,
        (960, 860),
        [
            "Same loop as sessions 1–4 inside every agent: think -> tool -> observe -> answer",
            "What is new: WHO does each part, WHAT they may touch, and HOW the result moves on",
        ],
        font(22),
        TEXT,
        gap=10,
    )
    _s04_legend(d, [(ACCENT, "orchestration"), (GREEN, "read / research"), (ACCENT2, "write"), (ORANGE, "review / gate")], x=560, y=990)
    save(img, "05/01-multi-agent-hero.png")


def s05_single_vs_crew():
    img, d = new_img()
    center_text(d, (W / 2, 42), "One agent vs. a crew — when splitting actually helps", font(38, True))

    rounded(d, (80, 120, 920, 900), CARD, outline=RED, radius=18, width=3)
    center_text(d, (500, 160), "Single agent, one huge prompt", font(28, True), RED)
    rounded(d, (140, 210, 860, 560), CARD2, outline=LINE, radius=14, width=2)
    f = font(19)
    lines = [
        "system: you are researcher + writer + reviewer + ...",
        "tools: 23 tools (read, write, deploy, refund, ...)",
        "context: policy.md + 40 tickets + style guide + ...",
        "",
        "-> context window fills up",
        "-> instructions compete (be creative / be strict)",
        "-> reviewer 'forgets' to review its own text",
        "-> one bad step poisons everything after it",
    ]
    ty = 236
    for line in lines:
        d.text((170, ty), line, font=f, fill=MUTED)
        ty += 36
    _s04_panel(d, (140, 600, 860, 860), "Fine for", [
        "small, single-skill tasks",
        "short context, few tools",
        "no need for independent review",
        "",
        "Cheapest option — start here.",
    ], outline=GREEN, title_color=GREEN)

    rounded(d, (1000, 120, 1840, 900), CARD, outline=GREEN, radius=18, width=3)
    center_text(d, (1420, 160), "Crew of specialists", font(28, True), GREEN)
    for i, (role, c, what) in enumerate([
        ("Researcher", GREEN, "facts only · read tools"),
        ("Writer", ACCENT2, "text only · no new facts"),
        ("Reviewer", ORANGE, "verdict only · read-only"),
    ]):
        y = 210 + i * 110
        rounded(d, (1060, y, 1780, y + 86), CARD2, outline=c, radius=12, width=2)
        d.text((1084, y + 14), role, font=font(22, True), fill=c)
        d.text((1084, y + 48), what, font=font(18), fill=MUTED)
    _s04_panel(d, (1060, 560, 1780, 860), "Helps when", [
        "roles need different instructions / tools",
        "context would not fit one window",
        "independent review has real value",
        "parts can run in parallel",
        "",
        "Costs: N x tokens, hand-off bugs, latency.",
    ], outline=ORANGE, title_color=ORANGE)

    center_text(d, (W / 2, 970), "Rule: split by RESPONSIBILITY, not by sentence count. If one prompt still works — keep one agent.", font(22), TEXT)
    save(img, "05/02-single-vs-crew.png")


def s05_patterns():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Four orchestration patterns", font(38, True))
    center_text(d, (W / 2, 84), "Sequential · Hierarchical (manager) · Parallel fan-out / merge · Writer-Reviewer loop", font(22), MUTED)

    def node(x, y, label, c, w=150, h=64):
        rounded(d, (x, y, x + w, y + h), CARD2, outline=c, radius=12, width=3)
        center_text(d, (x + w / 2, y + h / 2), label, font(20, True), c)

    # Sequential
    rounded(d, (60, 130, 940, 480), CARD, outline=LINE, radius=16, width=2)
    d.text((84, 146), "1. Sequential (CrewAI Process.sequential)", font=font(24, True), fill=ACCENT)
    node(100, 240, "Research", GREEN); arrow(d, (250, 272), (330, 272), ACCENT)
    node(330, 240, "Write", ACCENT2); arrow(d, (480, 272), (560, 272), ACCENT)
    node(560, 240, "Review", ORANGE); arrow(d, (710, 272), (790, 272), ACCENT)
    node(790, 240, "Done", MUTED, w=120)
    f = font(18)
    d.text((100, 340), "output of task N becomes context of task N+1", font=f, fill=MUTED)
    d.text((100, 368), "simple · predictable · easy to trace · no parallelism", font=f, fill=MUTED)
    d.text((100, 396), "use first — covers most real cases", font=f, fill=GREEN)

    # Hierarchical
    rounded(d, (980, 130, 1860, 480), CARD, outline=LINE, radius=16, width=2)
    d.text((1004, 146), "2. Hierarchical (manager delegates)", font=font(24, True), fill=ACCENT)
    node(1330, 200, "Manager", ACCENT, w=180)
    node(1040, 330, "Research", GREEN); node(1300, 330, "Write", ACCENT2); node(1560, 330, "Review", ORANGE)
    arrow(d, (1380, 264), (1115, 330), ACCENT); arrow(d, (1420, 264), (1375, 330), ACCENT); arrow(d, (1470, 264), (1635, 330), ACCENT)
    d.text((1020, 420), "manager LLM picks who works next · flexible · extra tokens · harder to predict", font=f, fill=MUTED)
    d.text((1020, 448), "needs max_iter + budget — manager can loop", font=f, fill=ORANGE)

    # Parallel
    rounded(d, (60, 520, 940, 900), CARD, outline=LINE, radius=16, width=2)
    d.text((84, 536), "3. Parallel fan-out / merge", font=font(24, True), fill=ACCENT)
    node(100, 660, "Split", ACCENT, w=120)
    node(330, 590, "fetch_metrics", GREEN, w=190); node(330, 690, "fetch_logs", GREEN, w=190); node(330, 790, "fetch_deploys", GREEN, w=190)
    arrow(d, (220, 692), (330, 622), GREEN); arrow(d, (220, 692), (330, 722), GREEN); arrow(d, (220, 692), (330, 822), GREEN)
    node(640, 660, "Merge", ACCENT2, w=140)
    arrow(d, (520, 622), (640, 692), ACCENT2); arrow(d, (520, 722), (640, 692), ACCENT2); arrow(d, (520, 822), (640, 692), ACCENT2)
    d.text((100, 860), "read-only work in parallel · merge needs a Reducer (session 4)", font=f, fill=MUTED)

    # Loop
    rounded(d, (980, 520, 1860, 900), CARD, outline=LINE, radius=16, width=2)
    d.text((1004, 536), "4. Writer <-> Reviewer loop (bounded!)", font=font(24, True), fill=ACCENT)
    node(1100, 650, "Writer", ACCENT2, w=180); node(1500, 650, "Reviewer", ORANGE, w=180)
    arrow(d, (1280, 668), (1500, 668), ACCENT2); arrow(d, (1500, 700), (1280, 700), ORANGE)
    center_text(d, (1390, 640), "draft", font(18), ACCENT2)
    center_text(d, (1390, 728), "REVISE + notes", font(18), ORANGE)
    arrow(d, (1680, 682), (1760, 682), GREEN); center_text(d, (1800, 682), "OK", font(20, True), GREEN)
    d.text((1020, 800), "quality goes up for 1-2 rounds, then flat", font=f, fill=MUTED)
    d.text((1020, 828), "MAX_ROUNDS is mandatory — otherwise infinite debate", font=f, fill=RED)
    d.text((1020, 856), "after MAX: escalate to human (HITL)", font=f, fill=ORANGE)

    center_text(d, (W / 2, 980), "Pick the simplest pattern that satisfies the task. Combine only when a real need appears.", font(22), TEXT)
    save(img, "05/03-orchestration-patterns.png")


def s05_crewai_concepts():
    img, d = new_img()
    center_text(d, (W / 2, 40), "CrewAI building blocks — Agent · Task · Crew · Process · Tools", font(38, True))

    _s05_agent_card(d, (60, 130, 640, 520), "Agent", GREEN, [
        "role: 'Support Researcher'",
        "goal: 'collect verified order facts'",
        "backstory: who it is, how it works",
        "tools: [get_order, search_policy]",
        "llm: model for THIS agent",
        "allow_delegation: False (default safe)",
        "max_iter: 5   <- loop budget",
        "verbose: True <- trace",
        "",
        "= system prompt + tools + budget",
    ])
    _s05_agent_card(d, (680, 130, 1260, 520), "Task", ACCENT2, [
        "description: what to do (concrete)",
        "expected_output: shape of the result",
        "agent: who owns it",
        "context: [previous_tasks]",
        "output_pydantic / output_json",
        "human_input: True (HITL gate)",
        "",
        "Task = unit of work + contract",
        "expected_output is the real spec:",
        "'bullets with source per fact'",
    ])
    _s05_agent_card(d, (1300, 130, 1860, 520), "Crew", ACCENT, [
        "agents: [researcher, writer, reviewer]",
        "tasks: [t_research, t_write, t_review]",
        "process: Process.sequential",
        "        | Process.hierarchical",
        "manager_llm: for hierarchical",
        "memory: False (session 6!)",
        "verbose: True",
        "",
        "crew.kickoff(inputs={...})",
        "-> CrewOutput (raw, tasks_output)",
    ])

    rounded(d, (60, 580, 1860, 900), CARD, outline=LINE, radius=16, width=2)
    d.text((84, 598), "kickoff() — what happens at runtime (sequential)", font=font(24, True), fill=TEXT)
    steps = [
        ("inputs", ACCENT, "{order_id, question}"),
        ("Task 1", GREEN, "researcher: think -> tool -> facts"),
        ("Task 2", ACCENT2, "writer: context=[T1] -> faq text"),
        ("Task 3", ORANGE, "reviewer: context=[T2] -> verdict"),
        ("CrewOutput", MUTED, "raw + per-task outputs"),
    ]
    x = 100
    for i, (label, c, sub) in enumerate(steps):
        rounded(d, (x, 660, x + 300, 760), CARD2, outline=c, radius=12, width=3)
        center_text(d, (x + 150, 690), label, font(22, True), c)
        center_text(d, (x + 150, 730), sub, font(16), MUTED)
        if i < len(steps) - 1:
            arrow(d, (x + 300, 710), (x + 350, 710), ACCENT, 4)
        x += 350
    d.text((100, 800), "Every task runs the session-1 loop inside the agent. The Crew only decides ORDER and CONTEXT passing.", font=font(20), fill=MUTED)
    d.text((100, 832), "Tools are the session-3 contract: @tool def get_order(order_id: str) -> str  — schema from the signature + docstring.", font=font(20), fill=MUTED)
    d.text((100, 864), "No Checkpointer by default: a crash mid-crew restarts from Task 1. For resumable flows wrap the crew in a LangGraph node.", font=font(20), fill=ORANGE)
    save(img, "05/04-crewai-concepts.png")


def s05_subagents():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Claude Code / Cursor subagents — Multi-Agent inside your coding tool", font(36, True))
    center_text(d, (W / 2, 84), "Same idea as CrewAI: an orchestrator session delegates to role-specific agents with isolated context", font(22), MUTED)

    rounded(d, (60, 130, 700, 900), CARD, outline=ACCENT, radius=18, width=3)
    center_text(d, (380, 170), "Orchestrator session (you + main agent)", font(24, True), ACCENT)
    f = font(19)
    lines = [
        "reads prompt.md:",
        "  1. researcher -> facts.md",
        "  2. writer     -> faq.md",
        "  3. reviewer   -> review.md",
        "",
        "calls the Task tool per step",
        "gets back a SHORT summary",
        "(not the subagent's whole context)",
        "",
        "enforces order, retries, HITL",
        "keeps its own context small",
    ]
    ty = 210
    for line in lines:
        d.text((90, ty), line, font=f, fill=MUTED)
        ty += 32

    for i, (name, c, tools, model) in enumerate([
        ("researcher", GREEN, "tools: Read, Grep, Glob", "model: sonnet"),
        ("writer", ACCENT2, "tools: Read, Write", "model: sonnet"),
        ("reviewer", ORANGE, "tools: Read   (read-only)", "model: opus / sonnet"),
    ]):
        y = 150 + i * 250
        rounded(d, (820, y, 1340, y + 210), CARD2, outline=c, radius=16, width=3)
        center_text(d, (1080, y + 30), f".claude/agents/{name}.md", font(22, True), c)
        d.text((846, y + 66), "---  (frontmatter)", font=font(18), fill=MUTED)
        d.text((846, y + 92), f"name: {name}", font=font(18), fill=TEXT)
        d.text((846, y + 118), tools, font=font(18), fill=TEXT)
        d.text((846, y + 144), model, font=font(18), fill=TEXT)
        d.text((846, y + 170), "--- then: the role prompt (markdown body)", font=font(18), fill=MUTED)
        arrow(d, (700, 300 + i * 200), (820, y + 105), c, 4)

    _s04_panel(d, (1400, 150, 1860, 520), "Isolated context", [
        "subagent starts fresh",
        "sees only: its prompt +",
        "what the orchestrator passed",
        "+ files it reads itself",
        "",
        "returns: one final message",
        "",
        "=> the reviewer cannot be",
        "   'convinced' by the writer's",
        "   reasoning — it only sees",
        "   the artifact (faq.md)",
    ], outline=GREEN, title_color=GREEN)
    _s04_panel(d, (1400, 560, 1860, 900), "Cursor equivalent", [
        "Agent chat -> Task / subagents",
        "parallel subagents for read-only",
        "work, then a merge step",
        "",
        "Rules & allowed tools per role",
        "via prompt + .cursor/rules",
        "",
        "Same guardrails apply:",
        "budget, bounded rounds,",
        "human approves before writes",
    ], outline=ACCENT, title_color=ACCENT)
    save(img, "05/05-claude-code-subagents.png")


def s05_crew_vs_graph():
    img, d = new_img()
    center_text(d, (W / 2, 40), "CrewAI vs LangGraph — different questions, same loop", font(38, True))

    rows = [
        ("Mental model", "roles & tasks (who does what)", "nodes & edges (what happens next)"),
        ("Control flow", "process: sequential / hierarchical", "explicit graph, conditional edges, loops"),
        ("Shared memory", "task outputs passed as context", "typed State + Reducers"),
        ("Pause / resume", "human_input per task; no checkpoint", "Checkpointer + thread_id + interrupt()"),
        ("Parallelism", "async tasks (limited)", "fan-out / Send / subgraphs"),
        ("Best for", "fast prototypes, content pipelines", "production flows needing HITL & audit"),
        ("Learning curve", "hours", "days"),
        ("Debuggability", "verbose logs per agent", "state snapshot per step"),
    ]
    x0, y0 = 80, 130
    colw = [360, 700, 700]
    hdr = ["", "CrewAI", "LangGraph"]
    for ci, h in enumerate(hdr):
        x = x0 + sum(colw[:ci])
        rounded(d, (x, y0, x + colw[ci] - 10, y0 + 56), CARD2, outline=LINE, radius=10, width=2)
        center_text(d, (x + colw[ci] / 2 - 5, y0 + 28), h, font(24, True), [TEXT, ORANGE, ACCENT][ci])
    f = font(20)
    for ri, row in enumerate(rows):
        y = y0 + 70 + ri * 74
        for ci, cell in enumerate(row):
            x = x0 + sum(colw[:ci])
            rounded(d, (x, y, x + colw[ci] - 10, y + 62), CARD, outline=LINE, radius=10, width=1)
            d.text((x + 18, y + 18), cell, font=font(20, ci == 0), fill=TEXT if ci == 0 else MUTED)

    rounded(d, (80, 760, 1840, 960), CARD, outline=GREEN, radius=16, width=3)
    center_text(d, (960, 792), "Combine: a Crew as ONE node inside a LangGraph", font(26, True), GREEN)
    def node(x, y, label, c, w=200):
        rounded(d, (x, y, x + w, y + 60), CARD2, outline=c, radius=12, width=3)
        center_text(d, (x + w / 2, y + 30), label, font(20, True), c)
    node(140, 850, "lookup_order", GREEN); arrow(d, (340, 880), (420, 880))
    node(420, 850, "content_crew (CrewAI)", ACCENT2, w=320); arrow(d, (740, 880), (820, 880))
    node(820, 850, "route", ORANGE); arrow(d, (1020, 880), (1100, 880))
    node(1100, 850, "hitl_approve", ORANGE, w=240); arrow(d, (1340, 880), (1420, 880))
    node(1420, 850, "send / END", MUTED, w=240)
    center_text(d, (960, 935), "Graph keeps State, checkpoint and HITL; the crew does the multi-role content work inside one step.", font(19), MUTED)
    save(img, "05/06-crew-vs-graph.png")


def s05_guardrails():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Guardrails for a crew — where multi-agent systems break", font(38, True))
    panels = [
        ((60, 130, 640, 500), "Budget per agent & per crew", ORANGE, [
            "max_iter on every Agent",
            "MAX_ROUNDS on every loop",
            "token / cost counter per role",
            "",
            "Failure it prevents:",
            "manager re-delegates forever,",
            "writer-reviewer debate x 40",
        ]),
        ((680, 130, 1260, 500), "HITL before any write", RED, [
            "reviewer verdict != permission",
            "human approves: refund, email,",
            "deploy, delete, post",
            "",
            "CrewAI: human_input=True on task",
            "LangGraph: interrupt() node",
            "Claude Code: permission prompt",
        ]),
        ((1300, 130, 1860, 500), "Output contracts", ACCENT2, [
            "expected_output written as a spec",
            "output_pydantic / JSON schema",
            "validate BEFORE hand-off",
            "",
            "Failure it prevents:",
            "writer receives prose instead",
            "of facts; reviewer gets no verdict",
        ]),
        ((60, 540, 640, 900), "Trace: who said what", GREEN, [
            "log fields: run_id, agent, task,",
            "round, tool, latency_ms, tokens",
            "",
            "one line per hand-off",
            "",
            "Without it a crew is a",
            "black box of N black boxes",
        ]),
        ((680, 540, 1260, 900), "Context isolation", ACCENT, [
            "reviewer sees artifact, not chat",
            "writer sees facts, not raw tickets",
            "least privilege for tools",
            "",
            "Failure it prevents:",
            "prompt-injection in a ticket",
            "steering the whole crew",
        ]),
        ((1300, 540, 1860, 900), "Escalation path", MUTED, [
            "after MAX_ROUNDS -> human",
            "after tool failure x2 -> stop",
            "never 'try again' silently",
            "",
            "Say it in the output:",
            "'needs human: reason'",
            "— that is a valid result",
        ]),
    ]
    for box, title, c, lines in panels:
        _s04_panel(d, box, title, lines, outline=c, title_color=c)
    center_text(d, (W / 2, 975), "Session 2 (Budget, Policy Gate) + Session 3 (Validate) + Session 4 (HITL, State) — applied to N agents at once.", font(21), TEXT)
    save(img, "05/07-crew-guardrails.png")


# ---------- Session 06 ----------

def s06_hero():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Checkpoint vs Memory — two clocks, two jobs", font(38, True))
    center_text(d, (W / 2, 84), "Same agent loop · different lifetime · different failure mode if missing", font(22), MUTED)

    _s04_panel(d, (60, 140, 920, 720), "Checkpoint (run memory)", [
        "lifetime: one thread / one run",
        "key: thread_id",
        "holds: State snapshot after steps",
        "enables: pause, resume, HITL",
        "",
        "without it:",
        "  interrupt() cannot resume",
        "  crash => restart from zero",
        "",
        "LangGraph: compile(checkpointer=…)",
        "Session 4 concept — revisited",
    ], outline=ACCENT, title_color=ACCENT)

    _s04_panel(d, (1000, 140, 1860, 720), "Memory / Store (cross-run)", [
        "lifetime: across runs & days",
        "key: user_id / customer_id / entity",
        "holds: facts, prefs, prior cases",
        "enables: 'what about my refund?'",
        "",
        "without it:",
        "  every session starts blank",
        "  customer repeats everything",
        "",
        "file / sqlite / vector DB / Store API",
        "Session 6 focus",
    ], outline=ORANGE, title_color=ORANGE)

    rounded(d, (60, 760, 1860, 980), CARD, outline=GREEN, radius=16, width=3)
    multiline_center(
        d,
        (960, 870),
        [
            "Rule of thumb: Checkpoint = WHERE we are in THIS run · Memory = WHAT we know ABOUT the world",
            "Lab 06: InMemorySaver(thread_id) + profiles.json(customer_id) — change either knob, result changes",
        ],
        font(22),
        TEXT,
        gap=12,
    )
    save(img, "06/01-checkpoint-vs-memory.png")


def s06_layers():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Four layers of agent memory", font(40, True))
    layers = [
        (120, ACCENT, "Working / State", "current State fields · tool results this step · cleared when run ends"),
        (280, GREEN, "Thread / Checkpoint", "messages[] for this thread_id · resume after HITL · same conversation"),
        (440, ORANGE, "Profile / Entity Store", "customer prefs, open refunds, account flags · keyed by user_id"),
        (600, ACCENT2, "Long-term / RAG corpus", "docs, past tickets (retrieved) · not 'remembered' verbatim in prompt"),
    ]
    for y, c, title, body in layers:
        rounded(d, (120, y, 1800, y + 130), CARD2, outline=c, radius=14, width=3)
        d.text((160, y + 28), title, font=font(28, True), fill=c)
        d.text((160, y + 78), body, font=font(22), fill=MUTED)
    center_text(d, (W / 2, 800), "Higher layer ≠ always better. Prefer the lowest layer that solves the product need.", font(22), TEXT)
    center_text(d, (W / 2, 860), "Privacy filter applies at EVERY layer: card numbers, secrets, irrelevant gossip — do not store.", font(22), RED)
    save(img, "06/02-memory-layers.png")


def s06_thread_vs_user():
    img, d = new_img()
    center_text(d, (W / 2, 40), "thread_id vs user_id — the bug that looks like amnesia", font(36, True))
    _s04_panel(d, (60, 130, 920, 520), "Same user, NEW thread_id", [
        "Checkpoint: empty (new conversation)",
        "Store(user_id): still has profile",
        "",
        "Symptom: 'bot forgot my chat'",
        "but still knows 'open refund 101'",
        "",
        "Fix: map UI session carefully;",
        "don't mint a random thread every click",
    ], outline=ORANGE, title_color=ORANGE)
    _s04_panel(d, (1000, 130, 1860, 520), "Same thread, WRONG user_id", [
        "Checkpoint: old messages leak",
        "Store: writes into another profile",
        "",
        "Symptom: privacy incident",
        "",
        "Fix: bind thread_id <-> user_id",
        "in your gateway; never trust client alone",
    ], outline=RED, title_color=RED)
    _s04_panel(d, (60, 560, 1860, 900), "Lab experiment", [
        "1) chat --customer C-101 --amount 101",
        "2) chat --customer C-101 --message 'status' --thread other",
        "   => Checkpoint empty for 'other', Store still answers from profile",
        "3) forget --customer C-101  => Store blank; status fails even on old thread",
        "",
        "Say out loud: which knob did I turn — thread or store?",
    ], outline=GREEN, title_color=GREEN)
    save(img, "06/03-thread-vs-user.png")


def s06_retention():
    img, d = new_img()
    center_text(d, (W / 2, 40), "What to remember · what to forget · when", font(38, True))
    cols = [
        ((60, 130, 640, 900), "Remember", GREEN, [
            "open case id + amount band",
            "language / channel preference",
            "policy version used",
            "last human decision (approve)",
            "",
            "TTL: case lifetime + 30d",
        ]),
        ((680, 130, 1260, 900), "Summarize, don't dump", ORANGE, [
            "long chat => rolling summary",
            "keep last N raw turns only",
            "entity facts extracted once",
            "",
            "Cost: tokens scale with dump",
            "Quality: dump hides the signal",
        ]),
        ((1300, 130, 1860, 900), "Never store", RED, [
            "full PAN / CVV / passwords",
            "raw secrets from tools",
            "other customers' data",
            "one-off rants as 'prefs'",
            "",
            "If tool returned it once,",
            "redact before write-to-Store",
        ]),
    ]
    for box, title, c, lines in cols:
        _s04_panel(d, box, title, lines, outline=c, title_color=c)
    center_text(d, (W / 2, 970), "Memory without retention policy is a compliance bug waiting for a date.", font(22), TEXT)
    save(img, "06/04-retention.png")


def s06_lab_flow():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Lab 06 flow — StateGraph + Store", font(38, True))
    nodes = [
        (80, 200, 420, 360, "START", ACCENT),
        (520, 200, 900, 360, "lookup_profile", GREEN),
        (1000, 200, 1400, 360, "decide", ORANGE),
        (1500, 200, 1840, 360, "END", MUTED),
    ]
    for x1, y1, x2, y2, label, c in nodes:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=16, width=3)
        center_text(d, ((x1 + x2) / 2, (y1 + y2) / 2), label, font(26, True), c)
    arrow(d, (420, 280), (520, 280), ACCENT)
    arrow(d, (900, 280), (1000, 280), ACCENT)
    arrow(d, (1400, 280), (1500, 280), ACCENT)

    _s04_panel(d, (80, 420, 900, 900), "Checkpointer", [
        "InMemorySaver + thread_id",
        "keeps messages for THIS chat",
        "get_state(config) after invoke",
        "",
        "change --thread => new blank chat",
        "Store may still answer",
    ], outline=ACCENT, title_color=ACCENT)
    _s04_panel(d, (980, 420, 1840, 900), "Store (profiles.json)", [
        "key: customer_id",
        "fields: amount, route, status",
        "99 => auto / 101 => hitl",
        "",
        "forget --customer C-99",
        "=> next status turn has no memory",
        "reset => wipe store + thread log",
    ], outline=ORANGE, title_color=ORANGE)
    save(img, "06/05-lab-flow.png")


# ---------- Session 07 ----------

def s07_hero():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Business automation with Agents — Revenue Ops loop", font(36, True))
    center_text(d, (W / 2, 84), "CRM facts + pricebook + policy  →  quote  →  money gate  →  draft (not send)", font(22), MUTED)
    steps = [
        (80, 160, 360, 340, "Lead\nCRM", ACCENT),
        (400, 160, 680, 340, "Score\nICP", GREEN),
        (720, 160, 1000, 340, "Price\nbook", ORANGE),
        (1040, 160, 1320, 340, "Quote\ncalc", ACCENT2),
        (1360, 160, 1640, 340, "Route\nauto/HITL", RED),
        (1680, 160, 1860, 340, "Draft\nemail", MUTED),
    ]
    for x1, y1, x2, y2, label, c in steps:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=14, width=3)
        multiline_center(d, ((x1 + x2) / 2, (y1 + y2) / 2), label.split("\n"), font(24, True), c, gap=6)
    for i in range(len(steps) - 1):
        arrow(d, (steps[i][2], 250), (steps[i + 1][0], 250), ACCENT, width=3)
    _s04_panel(d, (80, 400, 920, 980), "What the agent owns", [
        "read CRM fields (never invent)",
        "score with transparent rules",
        "compute totals from pricebook",
        "apply discount policy",
        "write quote + stage + draft",
        "",
        "Session 7 focus: money + CRM",
        "writes are product decisions",
    ], outline=GREEN, title_color=GREEN)
    _s04_panel(d, (1000, 400, 1860, 980), "What stays human", [
        "discount > 10% (manager HITL)",
        "discount > 25% (blocked — renegotiate)",
        "actually SEND email / contract",
        "legal exceptions, custom SKUs",
        "relationship calls",
        "",
        "Agent accelerates; policy decides",
        "who may spend margin",
    ], outline=ORANGE, title_color=ORANGE)
    save(img, "07/01-sales-ops-loop.png")


def s07_gates():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Money gates — same agent, different outcomes", font(36, True))
    cols = [
        ((60, 120, 640, 520), "≤ 10% discount", GREEN, [
            "route = auto",
            "status = approved",
            "CRM stage = quoted",
            "",
            "Demo: L-SMB @ 5%",
            "AE may send after glance",
        ]),
        ((680, 120, 1260, 520), "10% < d ≤ 25%", ORANGE, [
            "route = hitl",
            "status = pending_manager",
            "CRM stage = pending_approval",
            "",
            "Demo: L-ENT @ 18%",
            "manager_decide required",
        ]),
        ((1300, 120, 1860, 520), "> 25% OR no email", RED, [
            "route = blocked",
            "need_email OR rejected",
            "CRM stage = blocked",
            "",
            "Demo: L-STEAL @ 40%",
            "Demo: L-NOMAIL",
        ]),
    ]
    for box, title, c, lines in cols:
        _s04_panel(d, box, title, lines, outline=c, title_color=c)
    _s04_panel(d, (60, 560, 1860, 980), "Knob demo (Lab)", [
        "1) run L-SMB           → auto",
        "2) run L-SMB --discount 22  → suddenly HITL (same lead, new policy pressure)",
        "3) approve L-ENT       → pending_manager becomes quoted",
        "4) set-email on L-NOMAIL then re-run → unblocks quote",
        "",
        "Say out loud: which business rule fired — discount band, missing data, or manager?",
    ], outline=ACCENT, title_color=ACCENT)
    save(img, "07/02-money-gates.png")


def s07_agent_vs_workflow():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Workflow vs Agent vs Human — pick per step", font(36, True))
    _s04_panel(d, (60, 120, 640, 900), "Fixed workflow", [
        "known steps, stable forms",
        "invoice sync, stage rename",
        "cheap + auditable",
        "",
        "Use when:",
        "  input schema is closed",
        "  no judgment / language",
    ], outline=ACCENT, title_color=ACCENT)
    _s04_panel(d, (680, 120, 1260, 900), "Agent + tools", [
        "messy language → structured",
        "choose tools, explain quote",
        "draft outreach in Hebrew",
        "",
        "Use when:",
        "  AE request is free-text",
        "  policy still code-enforced",
    ], outline=ORANGE, title_color=ORANGE)
    _s04_panel(d, (1300, 120, 1860, 900), "Human", [
        "margin & legal risk",
        "relationship / politics",
        "exceptions to policy",
        "",
        "Use when:",
        "  money gate / HITL",
        "  send / sign / commit",
    ], outline=RED, title_color=RED)
    save(img, "07/03-workflow-vs-agent.png")


def s07_tool_catalog():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Revenue-ops tool catalog (Lab 07)", font(38, True))
    tools = [
        ("get_lead", "CRM read", ACCENT),
        ("score_lead", "0–100 rules", GREEN),
        ("lookup_price", "pricebook only", ORANGE),
        ("create_quote", "math + route", ACCENT2),
        ("manager_decide", "HITL write", RED),
        ("draft_email", "file only", MUTED),
        ("set_lead_email", "unblock data", GREEN),
    ]
    x, y = 80, 140
    for i, (name, desc, c) in enumerate(tools):
        col = i % 2
        row = i // 2
        x1 = 80 + col * 920
        y1 = 140 + row * 180
        rounded(d, (x1, y1, x1 + 880, y1 + 150), CARD2, outline=c, radius=14, width=3)
        d.text((x1 + 30, y1 + 35), name, font=font(28, True), fill=c)
        d.text((x1 + 30, y1 + 85), desc, font=font(22), fill=MUTED)
    center_text(d, (W / 2, 980), "Every money number must come from a tool result — never from model memory.", font(22), TEXT)
    save(img, "07/04-tool-catalog.png")


def s07_roi():
    img, d = new_img()
    center_text(d, (W / 2, 40), "What business buyers ask — and what to measure", font(34, True))
    _s04_panel(d, (60, 120, 920, 520), "Time saved (AE)", [
        "minutes to first quote",
        "% quotes with correct price",
        "handoffs to manager / week",
        "rework from bad CRM fields",
    ], outline=GREEN, title_color=GREEN)
    _s04_panel(d, (1000, 120, 1860, 520), "Risk controlled", [
        "discount > policy auto-rate",
        "emails sent without draft review",
        "invented prices (should be 0)",
        "PII written outside CRM",
    ], outline=RED, title_color=RED)
    _s04_panel(d, (60, 560, 1860, 980), "Story for stakeholders", [
        "We do not 'replace sales'. We enforce pricebook + discount bands,",
        "and we draft faster. Manager still owns margin above 10%.",
        "Missing email blocks the deal path — data quality becomes a product feature.",
        "",
        "Capstone hint (session 10): pick ONE funnel step with clear ROI + clear gate.",
    ], outline=ACCENT, title_color=ACCENT)
    save(img, "07/05-roi-metrics.png")


# ---------- Session 08 ----------

def s08_hero():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Hosts run agents · agents use tools · surfaces show output", font(32, True))
    center_text(d, (W / 2, 84), "Cursor / Claude Code = envelopes  ·  agent = loop inside  ·  HTML & Telegram for humans", font(20), MUTED)
    cols = [
        ((60, 140, 640, 900), "Cursor (host)", ACCENT, [
            "IDE envelope / host",
            "runs an Agent chat",
            "diff · rules · MCP",
            "",
            "Not 'the tool' —",
            "it hosts the agent",
        ]),
        ((680, 140, 1260, 900), "Claude Code (host)", ORANGE, [
            "CLI envelope / host",
            "claude -p + subagents",
            "agent calls Tools",
            "",
            "Not 'the tool' —",
            "it hosts the agent",
        ]),
        ((1300, 140, 1860, 900), "Surfaces", GREEN, [
            "HTML card (browser)",
            "Telegram message",
            "not terminal dump",
            "",
            "What AE / manager",
            "actually sees",
        ]),
    ]
    for box, title, c, lines in cols:
        _s04_panel(d, box, title, lines, outline=c, title_color=c)
    save(img, "08/01-coding-agents-surfaces.png")


def s08_pipeline():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Quote → Surface pipeline", font(40, True))
    steps = [
        (80, 200, 400, 380, "Quote\nJSON", ACCENT),
        (460, 200, 780, 380, "Agent\n+ tools", ORANGE),
        (840, 200, 1160, 380, "HTML\ncard", GREEN),
        (1220, 200, 1540, 380, "TG\ndraft", ACCENT2),
        (1600, 200, 1860, 380, "Send?\nHITL", RED),
    ]
    for x1, y1, x2, y2, label, c in steps:
        rounded(d, (x1, y1, x2, y2), CARD2, outline=c, radius=14, width=3)
        multiline_center(d, ((x1 + x2) / 2, (y1 + y2) / 2), label.split("\n"), font(24, True), c, gap=6)
    for i in range(len(steps) - 1):
        arrow(d, (steps[i][2], 290), (steps[i + 1][0], 290), ACCENT, width=3)
    _s04_panel(d, (80, 460, 1860, 960), "Draft ≠ Send still applies", [
        "render_html_card / render_telegram_message = files on disk",
        "send_telegram = network side-effect — needs token + explicit user ask",
        "Same policy lesson as session 7 email drafts — different channel",
        "",
        "Lab 08: surface_claude.py  ·  Demo: demos/08-surface-opening/",
    ], outline=GREEN, title_color=GREEN)
    save(img, "08/02-quote-to-surface.png")


def s08_telegram():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Telegram as an agent surface", font(38, True))
    _s04_panel(d, (60, 120, 920, 900), "Why Telegram", [
        "Push to phone — AE sees it",
        "Markdown-ish short cards",
        "Bot token = clear secret",
        "Chat ID = destination gate",
        "",
        "Good for: alerts, HITL pings,",
        "ops briefings — not long docs",
    ], outline=ACCENT, title_color=ACCENT)
    _s04_panel(d, (1000, 120, 1860, 900), "Safety checklist", [
        "Never commit TELEGRAM_BOT_TOKEN",
        "Separate draft file vs send tool",
        "Log sendMessage HTTP status",
        "Don't dump PII to public chats",
        "",
        "Missing env => tool returns error",
        "(do not fake 'sent=true')",
    ], outline=RED, title_color=RED)
    save(img, "08/03-telegram-surface.png")


def s08_cursor_claude():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Two hosts, same idea — pick the envelope", font(34, True))
    _s04_panel(d, (60, 120, 920, 520), "Cursor host when…", [
        "editing many files in a repo",
        "you want IDE review + diff",
        "rules in .cursor/ apply",
        "pairing on UI CSS/layout",
        "",
        "Host runs the coding agent",
    ], outline=ACCENT, title_color=ACCENT)
    _s04_panel(d, (1000, 120, 1860, 520), "Claude Code host when…", [
        "recording a terminal demo",
        "folder-scoped agent + subagents",
        "scripted claude -p runs",
        "CI-like repeatable prompts",
        "",
        "Host runs the coding agent",
    ], outline=ORANGE, title_color=ORANGE)
    _s04_panel(d, (60, 560, 1860, 960), "This course: no Copilot track", [
        "Cursor & Claude Code = envelopes that RUN agents (not the tools themselves).",
        "Tools = Read/Write/Edit… or Lab tools like render_html_card / send_telegram.",
        "Runtime agent (Lab) needs ANTHROPIC_API_KEY; TELEGRAM_* optional for send.",
    ], outline=GREEN, title_color=GREEN)
    save(img, "08/04-cursor-vs-claude.png")


def s08_lab_flow():
    img, d = new_img()
    center_text(d, (W / 2, 40), "Lab 08 — surface_claude.py tools", font(36, True))
    tools = [
        ("get_quote", "CRM/quote facts"),
        ("render_html_card", "out/briefing.html"),
        ("render_telegram_message", "out/telegram.txt"),
        ("send_telegram", "Bot API (optional)"),
    ]
    for i, (name, desc) in enumerate(tools):
        x1 = 80 + (i % 2) * 920
        y1 = 140 + (i // 2) * 280
        rounded(d, (x1, y1, x1 + 880, y1 + 230), CARD2, outline=ACCENT if i < 3 else RED, radius=14, width=3)
        d.text((x1 + 36, y1 + 60), name, font=font(28, True), fill=ACCENT if i < 3 else RED)
        d.text((x1 + 36, y1 + 120), desc, font=font(22), fill=MUTED)
    center_text(d, (W / 2, 980), "Knobs: L-SMB / L-ENT / L-UPSELL · ask to send only when token is set", font(22), TEXT)
    save(img, "08/05-lab-tools.png")


def main():
    gens = [
        v01_human_agent,
        v02_chat_vs_agent,
        v03_agent_loop,
        v04_llm_tools,
        v05_workflow_vs_agent,
        v06_autonomy,
        v07_approval,
        v08_guardrails,
        v09_trace,
        v10_devops,
        v11_support,
        v12_multi,
        v13_context,
        v14_permissions,
        v15_failure,
        v01_architecture,
        s02_planning_hero,
        s02_decompose,
        s02_open_closed,
        s02_react,
        s02_plan_execute,
        s02_failure,
        s02_policy,
        s02_state,
        s02_incident,
        s02_validation,
        demos,
        s03_tool_hero,
        s03_protocol,
        s03_schema,
        s03_tool_choice,
        s03_parallel,
        s03_validate,
        s03_mcp,
        s03_catalog,
        s04_hero,
        s04_graph_basics,
        s04_state,
        s04_conditional,
        s04_checkpoint,
        s04_hitl,
        s04_agent_loop,
        s05_hero,
        s05_single_vs_crew,
        s05_patterns,
        s05_crewai_concepts,
        s05_subagents,
        s05_crew_vs_graph,
        s05_guardrails,
        s06_hero,
        s06_layers,
        s06_thread_vs_user,
        s06_retention,
        s06_lab_flow,
        s07_hero,
        s07_gates,
        s07_agent_vs_workflow,
        s07_tool_catalog,
        s07_roi,
        s08_hero,
        s08_pipeline,
        s08_telegram,
        s08_cursor_claude,
        s08_lab_flow,
    ]
    for g in gens:
        g()
    print("done", len(gens), "generators")


if __name__ == "__main__":
    main()

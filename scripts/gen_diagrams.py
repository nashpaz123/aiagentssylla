#!/usr/bin/env python3
"""Generate presentation diagrams for AI Agents course sessions 1–4."""

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
    ]
    for g in gens:
        g()
    print("done", len(gens), "generators")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate presentation diagrams for AI Agents course sessions 1–2."""

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
    """Cathey-style L0–L6 spectrum."""
    img, d = new_img()
    title = font(40, True)
    body = font(18)
    center_text(d, (W / 2, 45), "AI Agent Spectrum (L0–L6)", title)
    levels = [
        ("L0", "Rules\nAutomation", LINE),
        ("L1", "AI-Assisted\nTools", MUTED),
        ("L2", "Custom\nAssistants", ACCENT),
        ("L3", "AI\nWorkflows", ORANGE),
        ("L4", "Task\nAgents", GREEN),
        ("L5", "Multi-\nAgent", ACCENT2),
        ("L6", "Agent\nEcosystems", RED),
    ]
    n = len(levels)
    gap = 16
    box_w = (W - 120 - gap * (n - 1)) // n
    y0, y1 = 160, 780
    for i, (lvl, desc, color) in enumerate(levels):
        x = 60 + i * (box_w + gap)
        rounded(d, (x, y0, x + box_w, y1), CARD, outline=color, radius=16)
        center_text(d, (x + box_w / 2, y0 + 80), lvl, font(32, True), color)
        multiline_center(d, (x + box_w / 2, 420), desc.split("\n"), body)
    x_line = 60 + 4 * (box_w + gap) - gap // 2
    d.line([(x_line, y0 - 10), (x_line, y1 + 10)], fill=GREEN, width=4)
    center_text(d, (W / 2, 860), "scripts (L0–L3) | genuine agency (L4+) — higher is not always better", font(22), MUTED)
    center_text(d, (W / 2, 920), "Adapted from Glen Cathey — The AI Agent Spectrum", font(18), MUTED)
    save(img, "01/06-autonomy-spectrum.png")


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
    ]
    for g in gens:
        g()
    print("done", len(gens), "generators")


if __name__ == "__main__":
    main()

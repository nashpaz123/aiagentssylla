#!/usr/bin/env python3
"""Generate mock product UIs that look like live system demos (no real integrations)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/stuff/prj/aiagentssylla/assets")
W, H = 1920, 1080

# Shared dark UI chrome
BG = (16, 18, 24)
PANEL = (24, 28, 36)
PANEL2 = (32, 38, 50)
BORDER = (55, 62, 78)
TEXT = (230, 234, 240)
MUTED = (140, 150, 170)
BLUE = (66, 133, 244)
GREEN = (52, 168, 83)
ORANGE = (242, 153, 74)
RED = (234, 67, 53)
PURPLE = (155, 109, 255)
CYAN = (78, 201, 176)
YELLOW = (246, 190, 0)


def font(size: int, bold: bool = False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mono(size: int):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return font(size)


def save(img: Image.Image, rel: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print("wrote", path)


def window(title: str, subtitle: str = ""):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # outer
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=18, fill=PANEL, outline=BORDER, width=2)
    # traffic lights
    d.ellipse([70, 62, 100, 92], fill=(255, 95, 86))
    d.ellipse([120, 62, 150, 92], fill=(255, 189, 46))
    d.ellipse([170, 62, 200, 92], fill=(39, 201, 63))
    d.text((240, 62), title, font=font(28, True), fill=TEXT)
    if subtitle:
        d.text((240, 98), subtitle, font=font(18), fill=MUTED)
    # top divider
    d.line([(40, 140), (W - 40, 140)], fill=BORDER, width=2)
    return img, d


def badge(d, xy, text, bg, fg=TEXT):
    x, y = xy
    f = font(18, True)
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 14, 8
    d.rounded_rectangle([x, y, x + tw + pad_x * 2, y + th + pad_y * 2], radius=10, fill=bg)
    d.text((x + pad_x, y + pad_y), text, font=f, fill=fg)


def sidebar(d, items, active=0, x0=60, y0=170, w=280):
    d.rounded_rectangle([x0, y0, x0 + w, H - 70], radius=12, fill=PANEL2, outline=BORDER)
    for i, label in enumerate(items):
        y = y0 + 30 + i * 70
        if i == active:
            d.rounded_rectangle([x0 + 12, y - 10, x0 + w - 12, y + 42], radius=10, fill=(40, 55, 90))
            color = BLUE
        else:
            color = MUTED
        d.text((x0 + 28, y), label, font=font(22), fill=color)


# ---------- Mock UIs ----------

def mock_crm():
    img, d = window("AcmeCRM · Customer 48291", "Production · eu-west-1")
    sidebar(d, ["Accounts", "Contacts", "Tickets", "Orders", "Notes"], active=0)
    # main card
    d.rounded_rectangle([380, 170, 1860, 1010], radius=14, fill=PANEL2, outline=BORDER)
    d.text((420, 200), "Nova Retail Ltd.", font=font(40, True), fill=TEXT)
    badge(d, (420, 270), "Customer since 2021", (45, 55, 75))
    badge(d, (640, 270), "Tier: Gold", (40, 70, 50), GREEN)
    badge(d, (800, 270), "Open tickets: 2", (70, 45, 40), ORANGE)

    rows = [
        ("Owner", "Maya Cohen · CS"),
        ("Email", "ops@novaretail.example"),
        ("Phone", "+972-3-555-0199"),
        ("ARR", "$84,000"),
        ("Last contact", "Today 09:14 · Email"),
        ("Health", "At risk · 2 escalations this month"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 360 + i * 70
        d.text((420, y), k, font=font(22), fill=MUTED)
        d.text((700, y), v, font=font(24, True), fill=TEXT)

    d.rounded_rectangle([1200, 360, 1800, 960], radius=12, fill=PANEL, outline=BORDER)
    d.text((1240, 390), "Recent activity", font=font(26, True), fill=TEXT)
    acts = [
        ("09:14", "Email inbound: invoice mismatch"),
        ("Yesterday", "Ticket #8831 opened"),
        ("Mon", "Order #NR-2201 delayed"),
        ("Last week", "CSAT survey: 3/5"),
    ]
    for i, (t, a) in enumerate(acts):
        y = 460 + i * 100
        d.text((1240, y), t, font=font(20), fill=MUTED)
        d.text((1240, y + 32), a, font=font(22), fill=TEXT)
    save(img, "screens/crm-customer.png")


def mock_tickets():
    img, d = window("Helpdesk · Tickets", "Queue · live")
    sidebar(d, ["Queue", "Mine", "Waiting", "Closed", "SLA"], active=0)
    d.rounded_rectangle([380, 170, 1860, 1010], radius=14, fill=PANEL2, outline=BORDER)
    d.text((420, 200), "Open queue", font=font(34, True), fill=TEXT)
    headers = ["ID", "Subject", "Customer", "Priority", "Status", "Age"]
    xs = [420, 560, 980, 1300, 1500, 1700]
    for x, h in zip(xs, headers):
        d.text((x, 280), h, font=font(20, True), fill=MUTED)
    d.line([(400, 320), (1840, 320)], fill=BORDER, width=1)

    tickets = [
        ("#8831", "Invoice amount mismatch", "Nova Retail", "High", "Investigating", "2h", ORANGE),
        ("#8827", "Cannot reset password", "BlueCart", "Med", "Waiting customer", "5h", YELLOW),
        ("#8819", "API 500 on /orders", "Shiply", "Crit", "Escalated", "1d", RED),
        ("#8812", "Add second admin user", "LeafCo", "Low", "Open", "2d", MUTED),
        ("#8804", "Wrong shipping address", "Nova Retail", "High", "In progress", "3d", ORANGE),
    ]
    for i, (tid, sub, cust, pri, st, age, c) in enumerate(tickets):
        y = 350 + i * 110
        if i == 0:
            d.rounded_rectangle([400, y - 20, 1840, y + 70], radius=10, fill=(40, 50, 70))
        vals = [tid, sub, cust, pri, st, age]
        for x, v in zip(xs, vals):
            col = c if v == pri or v == st and i == 0 else TEXT
            d.text((x, y), v, font=font(22, True if x == 420 else False), fill=col)
    save(img, "screens/ticketing-queue.png")


def mock_kb():
    img, d = window("Knowledge Base · Search", "Internal docs")
    d.rounded_rectangle([120, 180, 1800, 280], radius=14, fill=PANEL2, outline=BLUE, width=2)
    d.text((150, 210), "🔍  invoice mismatch OR billing discrepancy", font=font(28), fill=TEXT)
    d.text((120, 320), "3 results", font=font(22), fill=MUTED)

    results = [
        ("KB-214", "How we handle invoice mismatches", "If amount differs by < 2%, auto-credit…", "Updated 12 days ago"),
        ("KB-188", "Billing SLA for Gold customers", "Gold: first response < 2 business hours…", "Updated 1 month ago"),
        ("KB-091", "When to escalate to Finance", "Escalate if credit > $500 or tax dispute…", "Updated 3 months ago"),
    ]
    for i, (kid, title, snip, meta) in enumerate(results):
        y = 380 + i * 200
        d.rounded_rectangle([120, y, 1800, y + 170], radius=12, fill=PANEL2, outline=BORDER)
        badge(d, (150, y + 24), kid, (45, 55, 80), CYAN)
        d.text((280, y + 28), title, font=font(28, True), fill=TEXT)
        d.text((150, y + 90), snip, font=font(24), fill=MUTED)
        d.text((150, y + 130), meta, font=font(20), fill=MUTED)
    save(img, "screens/knowledge-search.png")


def mock_k8s():
    img, d = window("kubectl · cluster prod-eu-1", "namespace: api")
    d.rounded_rectangle([80, 170, 1840, 1010], radius=12, fill=(12, 14, 18), outline=BORDER)
    m = mono(24)
    lines = [
        ("$ kubectl get pods -n api", CYAN),
        ("NAME                         READY   STATUS             RESTARTS   AGE", MUTED),
        ("api-7f9d8c4b6-xw2qk          1/1     Running            0          4h", GREEN),
        ("api-7f9d8c4b6-m3n1p          1/1     Running            0          4h", GREEN),
        ("api-7f9d8c4b6-9kz2a          0/1     CrashLoopBackOff   11         4h", RED),
        ("", TEXT),
        ("$ kubectl logs api-7f9d8c4b6-9kz2a -n api --tail=8", CYAN),
        ("2026-09-14T08:11:02Z ERROR handler: NullPointerException", RED),
        ("    at com.acme.api.OrderHandler.process(OrderHandler.java:214)", MUTED),
        ("    at com.acme.api.HttpServer.dispatch(HttpServer.java:88)", MUTED),
        ("2026-09-14T08:11:02Z WARN  readiness probe failed", ORANGE),
        ("", TEXT),
        ("$ kubectl get events -n api --field-selector involvedObject.name=api-7f9d8c4b6-9kz2a", CYAN),
        ("4m   Warning   BackOff   Back-off restarting failed container", ORANGE),
    ]
    y = 200
    for text, color in lines:
        d.text((120, y), text, font=m, fill=color)
        y += 42
    save(img, "screens/k8s-pods-logs.png")


def mock_metrics():
    img, d = window("Observability · api service", "Last 60 minutes")
    # KPI cards
    kpis = [
        ("Error rate", "4.8%", RED, "↑ from 0.2%"),
        ("p95 latency", "1.42s", ORANGE, "↑ from 320ms"),
        ("RPS", "1.1k", GREEN, "steady"),
        ("Pods ready", "2 / 3", ORANGE, "1 crashing"),
    ]
    for i, (title, val, c, sub) in enumerate(kpis):
        x = 100 + i * 450
        d.rounded_rectangle([x, 180, x + 420, 360], radius=14, fill=PANEL2, outline=BORDER)
        d.text((x + 30, 210), title, font=font(22), fill=MUTED)
        d.text((x + 30, 260), val, font=font(48, True), fill=c)
        d.text((x + 30, 320), sub, font=font(20), fill=MUTED)

    # fake chart area
    d.rounded_rectangle([100, 400, 1820, 1000], radius=14, fill=PANEL2, outline=BORDER)
    d.text((140, 430), "HTTP 5xx · last 60 minutes", font=font(26, True), fill=TEXT)
    # axes
    d.line([(180, 920), (1760, 920)], fill=BORDER, width=2)
    d.line([(180, 500), (180, 920)], fill=BORDER, width=2)
    # line chart points - spike
    pts = []
    import math
    for i in range(40):
        x = 200 + i * 38
        base = 880 - (8 if i < 25 else 0)
        spike = 0
        if 26 <= i <= 34:
            spike = 280 * math.sin((i - 26) / 8 * math.pi)
        y = base - spike - (i % 5) * 3
        pts.append((x, y))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=RED, width=4)
    d.text((200, 940), "08:00", font=font(18), fill=MUTED)
    d.text((900, 940), "08:30", font=font(18), fill=MUTED)
    d.text((1600, 940), "09:00", font=font(18), fill=MUTED)
    save(img, "screens/metrics-dashboard.png")


def mock_email():
    img, d = window("Mail · Inbox (support@acme.example)", "Inbox")
    sidebar(d, ["Inbox", "Starred", "Sent", "Agent drafts", "Spam"], active=0)
    d.rounded_rectangle([380, 170, 1860, 1010], radius=14, fill=PANEL2, outline=BORDER)
    d.text((420, 200), "Invoice question from Nova Retail", font=font(32, True), fill=TEXT)
    d.text((420, 260), "From: ops@novaretail.example  ·  Today 09:14", font=font(22), fill=MUTED)
    d.line([(400, 310), (1840, 310)], fill=BORDER, width=1)
    body = [
        "Hi support,",
        "",
        "Our August invoice shows $12,400 but our PO was $11,950.",
        "Can you check and correct the difference?",
        "",
        "We also still see order NR-2201 as delayed in the portal.",
        "",
        "Thanks,",
        "Dana · Nova Retail Ops",
    ]
    y = 350
    for line in body:
        d.text((420, y), line, font=font(26), fill=TEXT)
        y += 48
    badge(d, (420, 900), "Agent draft ready · waiting approval", (60, 50, 30), ORANGE)
    save(img, "screens/email-inbound.png")


def mock_ci():
    img, d = window("CI · pipeline #4412", "main · a31c9e2")
    d.rounded_rectangle([80, 170, 1840, 1010], radius=12, fill=(12, 14, 18), outline=BORDER)
    m = mono(24)
    lines = [
        ("pipeline: build-and-test  ·  branch: main  ·  commit: a31c9e2", MUTED),
        ("", TEXT),
        ("[stage] install dependencies", CYAN),
        ("$ pip install -r requirements.txt", TEXT),
        ("Successfully installed flask-3.0.2 requests-2.32.3", GREEN),
        ("", TEXT),
        ("[stage] unit tests", CYAN),
        ("$ pytest -q", TEXT),
        ("collected 42 items", MUTED),
        ("..........F...............................", ORANGE),
        ("", TEXT),
        ("======= FAILURES =======", RED),
        ("E   ModuleNotFoundError: No module named 'pytest'", RED),
        ("HINT: requirements.txt no longer pins pytest (changed in a31c9e2)", ORANGE),
        ("", TEXT),
        ("Job status: FAILED  ·  exit code: 1", RED),
    ]
    y = 200
    for text, color in lines:
        d.text((120, y), text, font=m, fill=color)
        y += 44
    save(img, "screens/ci-console.png")


def mock_agent_workbench():
    """Split view: agent chat + mock tool results — looks like a live agent session."""
    img, d = window("Agent Workbench · support", "session · live tools")
    # left chat
    d.rounded_rectangle([80, 170, 920, 1010], radius=14, fill=PANEL2, outline=BORDER)
    d.text((110, 200), "Session", font=font(26, True), fill=TEXT)
    bubbles = [
        ("user", "Customer asks about invoice mismatch. Help me respond."),
        ("agent", "I'll look up the customer, open tickets, and billing KB."),
        ("tool", "→ crm.get_customer(\"Nova Retail\")"),
        ("obs", "← Tier Gold · 2 open tickets · health At risk"),
        ("tool", "→ tickets.search(customer=\"Nova Retail\")"),
        ("obs", "← #8831 Invoice amount mismatch (High)"),
        ("tool", "→ kb.search(\"invoice mismatch\")"),
        ("obs", "← KB-214: auto-credit if delta < 2%"),
        ("agent", "Draft ready. Delta is ~3.6% → needs Finance approval."),
    ]
    y = 260
    for role, text in bubbles:
        if role == "user":
            bg, fg = (45, 70, 110), TEXT
        elif role == "agent":
            bg, fg = (40, 55, 50), TEXT
        elif role == "tool":
            bg, fg = (50, 45, 70), PURPLE
        else:
            bg, fg = (35, 40, 50), CYAN
        d.rounded_rectangle([110, y, 880, y + 58], radius=10, fill=bg)
        d.text((130, y + 16), text[:72], font=font(20), fill=fg)
        y += 72

    # right: stacked mock panels
    d.rounded_rectangle([960, 170, 1840, 430], radius=12, fill=PANEL2, outline=BORDER)
    d.text((990, 190), "CRM · customer card", font=font(22, True), fill=MUTED)
    d.text((990, 240), "Nova Retail Ltd. · Gold · ARR $84k", font=font(26, True), fill=TEXT)
    d.text((990, 290), "ops@novaretail.example · Owner: Maya Cohen", font=font(22), fill=MUTED)
    d.text((990, 340), "Open tickets: #8831, #8804", font=font(22), fill=ORANGE)

    d.rounded_rectangle([960, 460, 1840, 720], radius=12, fill=PANEL2, outline=BORDER)
    d.text((990, 480), "Ticket #8831", font=font(22, True), fill=MUTED)
    d.text((990, 530), "Invoice amount mismatch", font=font(28, True), fill=TEXT)
    d.text((990, 590), "Priority High · Status Investigating · Age 2h", font=font(22), fill=ORANGE)
    d.text((990, 650), "Linked order: NR-2201 delayed", font=font(22), fill=MUTED)

    d.rounded_rectangle([960, 750, 1840, 1010], radius=12, fill=PANEL2, outline=BORDER)
    d.text((990, 770), "Knowledge Base", font=font(22, True), fill=MUTED)
    d.text((990, 820), "KB-214 · How we handle invoice mismatches", font=font(24, True), fill=TEXT)
    d.text((990, 880), "If delta < 2%: auto-credit. Else: Finance approval.", font=font(22), fill=MUTED)
    d.text((990, 940), "Policy: never promise a credit without approval.", font=font(22), fill=ORANGE)
    save(img, "screens/agent-workbench-support.png")


def mock_agent_devops():
    img, d = window("Agent Workbench · devops", "session · live tools")
    d.rounded_rectangle([80, 170, 920, 1010], radius=14, fill=PANEL2, outline=BORDER)
    d.text((110, 200), "Session", font=font(26, True), fill=TEXT)
    bubbles = [
        ("user", "API feels flaky. Is something wrong?"),
        ("agent", "Checking deployments, pods, then logs."),
        ("tool", "→ k8s.get_deployments(\"api\")"),
        ("obs", "← desired 3 / ready 3 / available 3"),
        ("tool", "→ k8s.get_pods(\"api\")"),
        ("obs", "← 2 Running, 1 CrashLoopBackOff"),
        ("tool", "→ k8s.get_logs(\"api-…-9kz2a\")"),
        ("obs", "← NullPointerException in OrderHandler"),
        ("agent", "One pod crashing; NPE in OrderHandler:214."),
    ]
    y = 260
    for role, text in bubbles:
        if role == "user":
            bg, fg = (45, 70, 110), TEXT
        elif role == "agent":
            bg, fg = (40, 55, 50), TEXT
        elif role == "tool":
            bg, fg = (50, 45, 70), PURPLE
        else:
            bg, fg = (35, 40, 50), CYAN
        d.rounded_rectangle([110, y, 880, y + 58], radius=10, fill=bg)
        d.text((130, y + 16), text[:72], font=font(20), fill=fg)
        y += 72

    d.rounded_rectangle([960, 170, 1840, 480], radius=12, fill=(12, 14, 18), outline=BORDER)
    m = mono(22)
    term = [
        ("$ kubectl get pods -n api", CYAN),
        ("api-…-xw2qk   1/1  Running           0", GREEN),
        ("api-…-m3n1p   1/1  Running           0", GREEN),
        ("api-…-9kz2a   0/1  CrashLoopBackOff 11", RED),
        ("", TEXT),
        ("$ kubectl logs api-…-9kz2a --tail=3", CYAN),
        ("ERROR NullPointerException", RED),
        ("  at OrderHandler.process:214", MUTED),
    ]
    y = 200
    for t, c in term:
        d.text((990, y), t, font=m, fill=c)
        y += 34

    d.rounded_rectangle([960, 510, 1840, 1010], radius=12, fill=PANEL2, outline=BORDER)
    d.text((990, 540), "Metrics snapshot", font=font(24, True), fill=TEXT)
    d.text((990, 620), "Error rate  4.8%   ·   p95  1.42s   ·   Ready 2/3", font=font(26), fill=ORANGE)
    d.text((990, 700), "Hypothesis: bad deploy introduced NPE in order path", font=font(24), fill=TEXT)
    d.text((990, 780), "Next (would need approval): rollback OR hotfix", font=font(24), fill=MUTED)
    d.text((990, 880), "Waiting on human approval before rollback", font=font(22), fill=ORANGE)
    save(img, "screens/agent-workbench-devops.png")


def mock_approval():
    img, d = window("Policy Gate · action approval", "Human in the loop")
    d.rounded_rectangle([360, 220, 1560, 900], radius=18, fill=PANEL2, outline=ORANGE, width=3)
    d.text((420, 280), "Approval required", font=font(40, True), fill=ORANGE)
    d.text((420, 360), "Agent wants to run:", font=font(24), fill=MUTED)
    d.rounded_rectangle([420, 420, 1500, 520], radius=12, fill=(20, 22, 28), outline=BORDER)
    d.text((450, 450), "finance.create_credit(customer=\"Nova Retail\", amount=450)", font=mono(24), fill=CYAN)
    d.text((420, 560), "Reason: invoice delta 3.6% exceeds auto-credit policy (2%).", font=font(24), fill=TEXT)
    d.text((420, 620), "Risk: monetary write — requires human.", font=font(24), fill=MUTED)

    # buttons
    d.rounded_rectangle([420, 720, 720, 820], radius=12, fill=GREEN)
    d.text((500, 750), "Approve", font=font(28, True), fill=(10, 20, 10))
    d.rounded_rectangle([760, 720, 1060, 820], radius=12, fill=RED)
    d.text((850, 750), "Deny", font=font(28, True), fill=TEXT)
    d.rounded_rectangle([1100, 720, 1500, 820], radius=12, fill=PANEL, outline=BORDER)
    d.text((1160, 750), "Edit & retry", font=font(28, True), fill=TEXT)
    save(img, "screens/approval-dialog.png")


def main():
    mock_crm()
    mock_tickets()
    mock_kb()
    mock_k8s()
    mock_metrics()
    mock_email()
    mock_ci()
    mock_agent_workbench()
    mock_agent_devops()
    mock_approval()
    print("done mocks")


if __name__ == "__main__":
    main()

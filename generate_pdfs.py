"""
Generate Wiom OS Cheat Sheet + Story Bank PDFs
Output: os-sandbox/ folder
"""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, Frame, PageTemplate, BaseDocTemplate)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen.canvas import Canvas
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Colors
PINK = HexColor('#d92b90')
PURPLE = HexColor('#9333ea')
DARK = HexColor('#1a1a2e')
GREY = HexColor('#475569')
LIGHTGREY = HexColor('#f1f5f9')
GREEN = HexColor('#15803d')
RED = HexColor('#dc2626')
AMBER = HexColor('#a16207')
BLUE = HexColor('#0369a1')
WHITE = white

# =====================================================================
# 1. CHEAT SHEET -- one-page landscape
# =====================================================================
def make_cheat_sheet():
    c = Canvas(os.path.join(OUT, "os_cheat_sheet.pdf"), pagesize=landscape(A4))
    w, h = landscape(A4)

    # Header bar
    c.setFillColor(PINK)
    c.rect(0, h - 28*mm, w, 28*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(12*mm, h - 12*mm, "WIOM OS CHEAT SHEET")
    c.setFont("Helvetica", 9)
    c.drawString(12*mm, h - 19*mm, "10 Operating Systems  |  Plain Language  |  What it does, what triggers it, what happens")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(w - 12*mm, h - 12*mm, "March 2026  |  System Design Reboot")
    c.setFont("Helvetica", 7)
    c.drawRightString(w - 12*mm, h - 19*mm, "For standup reference. Full specs: ask @Wiom OS Guide on Slack")

    # OS data -- plain language
    os_data = [
        ("Quality OS", "Scores every partner every 7 days",
         "3 checks: Uptime >=90%, Fix issues <=8hrs, Install quality >=85%",
         "COMPLIANT -> AT_RISK -> NON_COMPLIANT",
         "Fail checks -> less routing, lower bonus. Chronic failure (4+ times) -> enforcement kicks in."),
        ("Enforcement OS", "Acts when quality problems become a pattern",
         "Two tracks run in parallel:\n• Performance: repeated quality failures\n• Integrity: fraud/manipulation (FPV)",
         "ACTIVE -> RESTRICTED -> SUSPENDED -> TERMINATED",
         "Performance: 1 NC->watch, 3 more->restricted, 2 more->pre-exit.\nIntegrity: verified fraud = immediate suspension, no warnings."),
        ("Demand & Allocation", "Decides which partner serves each new customer",
         "4-step ranking: Eligible? -> Quality rank -> Lowest load -> Earliest onboarding",
         "8 exposure bands from ELIGIBLE_FULL to INELIGIBLE",
         "Better quality = more customers routed to you. Non-compliant = zero new customers.\nPartners never choose their customers -- the system assigns."),
        ("Compensation OS", "Calculates what partners earn",
         "Rs300 base per customer recharge. Bonus tiers: NONE / GOOD / VERY GOOD / EXCELLENT",
         "Per-credit tracking, monthly settlement",
         "Quality state drives bonus tier. Restricted/suspended = bonus drops to NONE.\nEvery credit logged individually -- no silent adjustments."),
        ("Connection Lifecycle", "Tracks every customer connection from request to deactivation",
         "Customer requests WiFi -> assigned to partner -> installed -> active -> paused (if recharge expires) -> deactivated",
         "REQUESTED -> PENDING_INSTALL -> ACTIVE -> PAUSED -> DEACTIVATED",
         "ACTIVE = counts for stock, quality, compensation.\nPAUSED = recharge expired. 90 day max pause, then auto-deactivated."),
        ("Exit OS", "Manages how partners leave the system",
         "3 types: Voluntary (partner quits), B1 (system removes -- bad performance), B2 (fraud -- immediate)",
         "S0 Active -> S1 Declared -> S2 Notice -> S3 Restricted -> S4 Execution -> S5 Offboarding -> S6 Complete",
         "Voluntary/B1: 14-day notice, then gradual wind-down.\nB2 (fraud): skip notice, immediate restriction. Risk overlay: R0->R1->R2 (never goes down)."),
        ("Capacity & Coverage", "Controls how many connections a partner can have per zone",
         "Cap starts at 50. Expands if 3 consecutive compliant cycles at >=80% load. Contracts if degraded.",
         "Zone classes: ZC-A (urban), ZC-B (peri-urban), ZC-C (rural)",
         "If one partner >60% of zone -> concentration alert -> escalation.\nAt Tier 3: system auto-caps that partner, routes to others."),
        ("Payment & Settlement", "Handles deposits, device charges, and final payouts",
         "Rs20,000 initial deposit + Rs200 per device. Returns credited, damages/losses deducted.",
         "PENDING -> IN_PROGRESS -> SETTLED / FROZEN / FAILED",
         "During tenure: return credits are pending.\nAt exit: Tranche 1 (earnings) -> Tranche 2 (deposit after devices returned)."),
        ("Asset Custody OS", "Tracks every NetBox device assigned to a partner",
         "Devices move: ASSIGNED -> DEPLOYED -> IDLE -> RETURNED/DAMAGED/LOST",
         "Idle counter tracks unused devices. Carry-fee accrues after threshold.",
         "All devices must reach terminal state before exit completes (S5 gate).\nLost device = full recovery deducted from deposit."),
        ("Visibility OS", "Controls what each role can see",
         "4 roles: R1 (Partner), R2 (Ops), R3 (Strategy), R4 (Engineering)",
         "3 levels: EXPOSED / ABSTRACTED / SUPPRESSED",
         "Partners see their own scores & earnings -- never see routing logic, thresholds, or other partners.\nAllocation logic is PERMANENTLY hidden from ALL roles."),
    ]

    # Table layout
    col_widths = [38*mm, 50*mm, 72*mm, 52*mm, 72*mm]
    header = [
        Paragraph("<b>OS</b>", ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=7, textColor=WHITE)),
        Paragraph("<b>What it does</b>", ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=7, textColor=WHITE)),
        Paragraph("<b>How it works</b>", ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=7, textColor=WHITE)),
        Paragraph("<b>States / Structure</b>", ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=7, textColor=WHITE)),
        Paragraph("<b>What happens to the partner</b>", ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=7, textColor=WHITE)),
    ]

    cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=6.2, leading=7.8, textColor=DARK)
    name_style = ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=PINK)

    rows = [header]
    for name, does, how, states, happens in os_data:
        rows.append([
            Paragraph(name, name_style),
            Paragraph(does, cell_style),
            Paragraph(how.replace('\n', '<br/>'), cell_style),
            Paragraph(states.replace('\n', '<br/>'), cell_style),
            Paragraph(happens.replace('\n', '<br/>'), cell_style),
        ])

    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PINK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHTGREY]),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    tw, th = t.wrap(0, 0)
    t.drawOn(c, 10*mm, h - 30*mm - th)

    # Footer
    c.setFont("Helvetica", 6)
    c.setFillColor(GREY)
    c.drawString(12*mm, 6*mm, "Key principle: System-led demand. Partners don't choose customers. Quality drives routing. Pattern-based enforcement. No territory entitlement.")
    c.drawRightString(w - 12*mm, 6*mm, "Full OS docs: Engineering folder  |  Questions: @Wiom OS Guide on Slack")

    c.save()
    print(f"[OK] Cheat sheet: {os.path.join(OUT, 'os_cheat_sheet.pdf')}")


# =====================================================================
# 2. STORY BANK -- Version 1: Visual one-pagers
# =====================================================================
def draw_story_header(c, w, h, num, title, subtitle, color):
    c.setFillColor(color)
    c.rect(0, h - 24*mm, w, 24*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(12*mm, h - 11*mm, f"STORY {num}: {title}")
    c.setFont("Helvetica", 9)
    c.drawString(12*mm, h - 18*mm, subtitle)
    c.setFont("Helvetica", 7)
    c.drawRightString(w - 12*mm, h - 11*mm, "Wiom OS -- Standup Story Bank")

def draw_flow_box(c, x, y, w_box, h_box, label, detail, color, text_color=DARK):
    c.setFillColor(color)
    c.roundRect(x, y, w_box, h_box, 3*mm, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 3*mm, y + h_box - 5*mm, label)
    c.setFont("Helvetica", 6.5)
    lines = detail.split('\n')
    for i, line in enumerate(lines):
        c.drawString(x + 3*mm, y + h_box - 11*mm - i*3.2*mm, line)

def draw_arrow(c, x1, y1, x2, y2):
    c.setStrokeColor(GREY)
    c.setLineWidth(1)
    c.line(x1, y1, x2, y2)
    # arrowhead
    c.setFillColor(GREY)
    if x2 > x1:  # right arrow
        c.drawString(x2 - 2*mm, y2 - 1*mm, "->")
    elif y2 < y1:  # down arrow
        c.drawString(x2 - 1*mm, y2 + 0.5*mm, "↓")

def make_visual_stories():
    c = Canvas(os.path.join(OUT, "story_bank_visual.pdf"), pagesize=A4)
    w, h = A4

    # ---- STORY 1: The Good Partner Who Has One Bad Month ----
    draw_story_header(c, w, h, 1, "THE RECOVERING PARTNER",
                     "A good partner has one bad month. What does the system do?", PINK)

    y_start = h - 32*mm
    box_w = 82*mm
    box_h = 22*mm
    gap = 6*mm

    steps = [
        ("WEEK 1-3: COMPLIANT", "Partner running well\nUptime 94% | Fix time 6hrs | IQ 88%\nAll 3 SLA checks pass", HexColor('#d1fae5'), "Quality OS evaluates -> COMPLIANT"),
        ("WEEK 4: INSTALL QUALITY DROPS", "New technician makes mistakes\nIQ drops to 72% (threshold: 85%)\nQuality OS -> NON_COMPLIANT (IQ domain)", HexColor('#fef3c7'), "D&A: exposure drops to INELIGIBLE_QUALITY\nNo new customers routed"),
        ("ENFORCEMENT: PATTERN_WATCH", "1 NC window -> E01 triggers\nEnforcement moves to PATTERN_WATCH\nThis is a warning -- not restriction yet", HexColor('#fee2e2'), "Compensation: bonus tier -> NONE\nPartner sees score dropped, fewer customers"),
        ("WEEK 5-6: PARTNER FIXES IT", "Retrains technician. IQ back to 89%\nNext evaluation: COMPLIANT again\nRecovery window: 2 cycles at reduced exposure", HexColor('#dbeafe'), "D&A: ELIGIBLE_REDUCED (50% routing)\nEnforcement: back to ACTIVE after pattern clears"),
        ("WEEK 8+: FULL RECOVERY", "3 consecutive COMPLIANT cycles\nExposure back to ELIGIBLE_FULL\nBonus tier restored based on quality", HexColor('#d1fae5'), "Full routing restored\nCompensation bonus eligible again\nCapacity cap may expand if at >=80% load"),
    ]

    for i, (title, detail, color, annotation) in enumerate(steps):
        col = i % 2
        row = i // 2
        x = 10*mm + col * (box_w + 14*mm)
        y = y_start - row * (box_h + gap + 12*mm)

        draw_flow_box(c, x, y, box_w, box_h, title, detail, color)

        # Annotation
        c.setFont("Helvetica-Oblique", 6)
        c.setFillColor(GREY)
        ann_lines = annotation.split('\n')
        for j, line in enumerate(ann_lines):
            c.drawString(x + 2*mm, y - 4*mm - j*3*mm, line)

    # Arrow flow numbers
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor('#e2e8f0'))
    for i in range(5):
        col = i % 2
        row = i // 2
        x = 10*mm + col * (box_w + 14*mm)
        y = y_start - row * (box_h + gap + 12*mm)
        c.drawString(x + box_w - 7*mm, y + box_h - 7*mm, str(i + 1))

    # Key takeaway
    c.setFillColor(HexColor('#fdf2f8'))
    c.roundRect(10*mm, 18*mm, w - 20*mm, 18*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(PINK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(14*mm, 30*mm, "KEY TAKEAWAY")
    c.setFillColor(DARK)
    c.setFont("Helvetica", 7)
    c.drawString(14*mm, 24*mm, "The system doesn't punish one bad week. It watches for patterns. A partner who fixes the problem recovers fully --")
    c.drawString(14*mm, 20*mm, "but recovery takes time (2-3 cycles at reduced routing). The system rewards consistency, not perfection.")

    c.showPage()

    # ---- STORY 2: The Bad Actor ----
    draw_story_header(c, w, h, 2, "THE BAD ACTOR",
                     "A partner is caught disintermediating. How does the system respond?", RED)

    y_start = h - 32*mm
    steps2 = [
        ("NORMAL OPERATIONS", "Partner has 48 active connections\nScores look fine -- 91% uptime\nBut something is off...", HexColor('#d1fae5'), "Quality OS: COMPLIANT\nD&A: ELIGIBLE_FULL -- everything looks normal"),
        ("FPV INVESTIGATION TRIGGERED", "Field team reports: partner directing\ncustomers to a competitor's service\nFPV (First Principle Violation) flagged", HexColor('#fef3c7'), "Enforcement OS: Integrity track activates\nE04 = 7 day investigation window\nPerformance track unaffected (runs parallel)"),
        ("FPV CONFIRMED -- SUSPENDED", "Investigation confirms disintermediation\nEnforcement: SUSPENDED immediately\nNo warnings. No second chance.", HexColor('#fee2e2'), "D&A: INELIGIBLE_ENFORCEMENT -- zero routing\nVisibility: partner sees posture = SUSPENDED\nCompensation: upside paused immediately"),
        ("B2 EXIT TRIGGERED", "FPV confirmed -> Exit OS: B2 Integrity\nSkips notice period entirely\nRisk overlay: R2 (Hostile) -- no grace", HexColor('#7f1d1d'), "S0 -> S1 -> S3 (skip S2 notice)\nAll customers queued for reallocation\nBatch limit bypassed -- immediate reroute"),
        ("EXECUTION & OFFBOARDING", "S4: All 48 connections rerouted to\nother eligible partners in the zone\nS5: Device reconciliation + settlement", HexColor('#374151'), "Asset Custody: all NetBoxes -> RETRIEVAL_PENDING\nPayment: Tranche 1 (earnings) settled\nTranche 2 waits for device return"),
    ]

    for i, (title, detail, color, annotation) in enumerate(steps2):
        col = i % 2
        row = i // 2
        x = 10*mm + col * (box_w + 14*mm)
        y = y_start - row * (box_h + gap + 12*mm)
        text_color = WHITE if color in [HexColor('#7f1d1d'), HexColor('#374151')] else DARK
        draw_flow_box(c, x, y, box_w, box_h, title, detail, color, text_color)

        c.setFont("Helvetica-Oblique", 6)
        c.setFillColor(GREY)
        ann_lines = annotation.split('\n')
        for j, line in enumerate(ann_lines):
            c.drawString(x + 2*mm, y - 4*mm - j*3*mm, line)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor('#e2e8f0'))
    for i in range(5):
        col = i % 2
        row = i // 2
        x = 10*mm + col * (box_w + 14*mm)
        y = y_start - row * (box_h + gap + 12*mm)
        c.drawString(x + box_w - 7*mm, y + box_h - 7*mm, str(i + 1))

    c.setFillColor(HexColor('#fef2f2'))
    c.roundRect(10*mm, 18*mm, w - 20*mm, 18*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(14*mm, 30*mm, "KEY TAKEAWAY")
    c.setFillColor(DARK)
    c.setFont("Helvetica", 7)
    c.drawString(14*mm, 24*mm, "Integrity violations bypass everything -- no warnings, no notice period, no grace. The system treats fraud differently from poor performance.")
    c.drawString(14*mm, 20*mm, "Performance track = patience + patterns. Integrity track = one verified violation = done. The two tracks run independently.")

    c.showPage()

    # ---- STORY 3: The Zone Concentration Crisis ----
    draw_story_header(c, w, h, 3, "THE ZONE CRISIS",
                     "One partner dominates a zone. Another partner exits. What does the system do?", PURPLE)

    y_start = h - 32*mm
    steps3 = [
        ("THE SETUP", "Meerut zone ZC-A: 3 partners\nPartner A: 35 connections (58%)\nPartner B: 18 connections (30%)\nPartner C: 7 connections (12%)", HexColor('#ede9fe'), "Concentration alert at 60% -- Partner A is at 58%\nClose to threshold but not yet triggered\nCapacity OS watching"),
        ("PARTNER B DECLARES EXIT", "Partner B: voluntary exit (14-day notice)\nSystem checks: is the zone still viable?\nCOVERAGE_STATE_ALTERNATE_AVAILABLE?", HexColor('#fef3c7'), "Exit OS: S0 -> S1 -> S2 (notice period)\nCapacity OS calculates: can A+C absorb B's 18?\nA has cap 50, currently 35 -> headroom 15\nC has cap 50, currently 7 -> headroom 43"),
        ("REALLOCATION BEGINS", "S2 expires -> S3 -> S4 (execution)\nB's 18 connections rerouted\nRouting: quality rank then load ratio", HexColor('#dbeafe'), "D&A routes based on quality + utilization\nIf A and C both COMPLIANT: lower load wins\nC (12% load) gets priority over A (70% load)\nBut A may get some if C can't absorb all"),
        ("CONCENTRATION SPIKES", "After reallocation: A now has 42 (65%)\nConcentration >60% = alert triggered\nTier 1 escalation: advisory", HexColor('#fef3c7'), "If sustained 3 cycles (P58): Tier 2 -> binding\nCapacity OS demands remediation plan\nIf no fix after 3x more: Tier 3 -> auto-cap"),
        ("SYSTEM SELF-CORRECTS", "D&A auto-applies ELIGIBLE_CAPPED to A\nNew customers only routed to C\nCapacity OS onboards new partner D for zone", HexColor('#d1fae5'), "Zone moves from CONCENTRATED -> REDUNDANT\nA keeps existing 42 but gets no new ones\nC and D grow. Zone diversifies naturally."),
    ]

    for i, (title, detail, color, annotation) in enumerate(steps3):
        col = i % 2
        row = i // 2
        x = 10*mm + col * (box_w + 14*mm)
        y = y_start - row * (box_h + gap + 12*mm)
        draw_flow_box(c, x, y, box_w, box_h, title, detail, color)

        c.setFont("Helvetica-Oblique", 6)
        c.setFillColor(GREY)
        ann_lines = annotation.split('\n')
        for j, line in enumerate(ann_lines):
            c.drawString(x + 2*mm, y - 4*mm - j*3*mm, line)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(HexColor('#e2e8f0'))
    for i in range(5):
        col = i % 2
        row = i // 2
        x = 10*mm + col * (box_w + 14*mm)
        y = y_start - row * (box_h + gap + 12*mm)
        c.drawString(x + box_w - 7*mm, y + box_h - 7*mm, str(i + 1))

    c.setFillColor(HexColor('#f3e8ff'))
    c.roundRect(10*mm, 18*mm, w - 20*mm, 18*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(14*mm, 30*mm, "KEY TAKEAWAY")
    c.setFillColor(DARK)
    c.setFont("Helvetica", 7)
    c.drawString(14*mm, 24*mm, "No partner owns a zone. The system actively prevents concentration through escalating pressure (advisory -> binding -> auto-cap).")
    c.drawString(14*mm, 20*mm, "When a partner exits, the system routes based on quality and load -- not relationship. The zone self-heals.")

    c.save()
    print(f"[OK] Visual stories: {os.path.join(OUT, 'story_bank_visual.pdf')}")


# =====================================================================
# 3. STORY BANK -- Version 2: Written two-pagers
# =====================================================================
def make_written_stories():
    path = os.path.join(OUT, "story_bank_written.pdf")

    # Legible styles -- 10pt body, fills the page
    title_style = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=16, textColor=PINK,
                                  spaceAfter=1.5*mm, leading=19)
    subtitle_style = ParagraphStyle('subtitle', fontName='Helvetica', fontSize=10, textColor=GREY,
                                     spaceAfter=5*mm, leading=13)
    heading_style = ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=11, textColor=DARK,
                                    spaceBefore=4.5*mm, spaceAfter=2*mm, leading=13)
    body_style = ParagraphStyle('body', fontName='Helvetica', fontSize=10, textColor=DARK,
                                 spaceAfter=2*mm, leading=14)
    os_callout_style = ParagraphStyle('oscall', fontName='Helvetica-Bold', fontSize=8.5, textColor=PINK,
                                       spaceBefore=1*mm, spaceAfter=1*mm, leading=11.5,
                                       leftIndent=6*mm, backColor=HexColor('#fdf2f8'), borderPadding=4)
    takeaway_style = ParagraphStyle('takeaway', fontName='Helvetica-Bold', fontSize=10.5, textColor=PINK,
                                     spaceBefore=4*mm, spaceAfter=1.5*mm, leading=13)
    takeaway_body = ParagraphStyle('tbody', fontName='Helvetica', fontSize=10, textColor=DARK,
                                    spaceAfter=2*mm, leading=14, leftIndent=3*mm)
    footer_style = ParagraphStyle('footer', fontName='Helvetica', fontSize=7, textColor=GREY,
                                   alignment=TA_CENTER, spaceBefore=3*mm)

    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=10*mm, bottomMargin=8*mm,
                            leftMargin=14*mm, rightMargin=14*mm)
    story = []

    # ---- STORY 1: The Recovering Partner ---- (CORRECTED)
    story.append(Paragraph("STORY 1: The Recovering Partner", title_style))
    story.append(Paragraph("A good partner has one bad month. How does the system respond -- and how do they recover?", subtitle_style))

    story.append(Paragraph("The Setup", heading_style))
    story.append(Paragraph(
        "A partner in Agra runs 45 active connections. For three consecutive evaluation cycles (7 days each), "
        "they've been COMPLIANT on all three SLA checks: uptime 94%, service resolution 6 hours, installation "
        "quality 88%. They're in the ELIGIBLE_FULL exposure band -- full routing priority. Bonus tier is GOOD.", body_style))

    story.append(Paragraph("Quality OS evaluates every 7 days across 3 SLA domains. All must pass. "
                           "Quality thresholds are published to partners.", os_callout_style))

    story.append(Paragraph("The Problem", heading_style))
    story.append(Paragraph(
        "In week 4, a new untrained technician causes installation quality to drop to 72% -- well below the "
        "85% threshold. Uptime and resolution are still fine. But one domain failing is enough. Quality OS "
        "moves the partner to NON_COMPLIANT. This triggers a cascade across the system.", body_style))

    story.append(Paragraph("NON_COMPLIANT triggers D&amp;A to set INELIGIBLE_QUALITY. Zero new customers routed.", os_callout_style))

    story.append(Paragraph("The Cascade", heading_style))
    story.append(Paragraph(
        "D&amp;A immediately sets INELIGIBLE_QUALITY -- no new customers routed, existing connections unaffected. "
        "Enforcement OS receives the NC signal: the first NC window triggers ENFORCE_EVAL on the performance "
        "track. This isn't restriction yet -- the system is evaluating. Compensation: "
        "bonus is suspended. Base Rs300 per recharge still earned, but no upside.", body_style))

    story.append(Paragraph("Enforcement: First NC triggers ENFORCE_EVAL. Repeated NC windows escalate toward RESTRICTED.", os_callout_style))

    story.append(Paragraph("What the Partner Sees", heading_style))
    story.append(Paragraph(
        "On their dashboard: quality score dropped, fewer customers, bonus gone. They can see their quality "
        "thresholds (published), but enforcement thresholds, routing formula, and how many failures trigger "
        "restriction are hidden. Visibility OS suppresses enforcement methodology -- focus on improving, "
        "not gaming thresholds.", body_style))

    story.append(Paragraph("Visibility OS: Quality thresholds = EXPOSED. Enforcement thresholds &amp; routing logic = SUPPRESSED.", os_callout_style))

    story.append(Paragraph("The Recovery", heading_style))
    story.append(Paragraph(
        "Partner retrains their technician. Next evaluation: IQ back to 89%, Quality OS -> COMPLIANT. "
        "But recovery isn't instant. D&amp;A moves them to ELIGIBLE_REDUCED -- 50% routing for 2 cycles "
        "(P43). The system needs sustained improvement. After 3 consecutive COMPLIANT cycles (P42), "
        "they return to ELIGIBLE_FULL. Enforcement clears. Bonus restores.", body_style))

    story.append(Paragraph("D&amp;A: Recovery = 2 cycles at 50% routing, then 3 COMPLIANT cycles for full restoration.", os_callout_style))

    story.append(Paragraph("Key Takeaway", takeaway_style))
    story.append(Paragraph(
        "The system doesn't punish one bad week -- it watches for patterns. Recovery is possible but takes "
        "time (2-3 cycles). Consistency over perfection. Repeated NC windows escalate to RESTRICTED -- "
        "not just zero new customers, but active review of the entire operation.", takeaway_body))

    story.append(Paragraph("Wiom OS Story Bank  |  March 2026  |  For standup use", footer_style))
    story.append(PageBreak())

    # ---- STORY 2: The Bad Actor ---- (CORRECTED)
    story.append(Paragraph("STORY 2: The Bad Actor", title_style))
    story.append(Paragraph("A partner is caught disintermediating -- directing Wiom customers to a competitor. What happens?", subtitle_style))

    story.append(Paragraph("The Setup", heading_style))
    story.append(Paragraph(
        "A partner in Meerut has 48 active connections. Everything looks fine on paper: uptime 91%, IQ 86%, "
        "COMPLIANT, routing active, bonus tier GOOD. Nothing in the data suggests a problem.", body_style))

    story.append(Paragraph("The Discovery", heading_style))
    story.append(Paragraph(
        "A field visit reveals the partner has been telling customers to switch to a competitor's service -- "
        "using Wiom's infrastructure but redirecting the relationship. This is a First Principle Violation (FPV). "
        "Enforcement OS activates its Integrity track (separate from Performance, which keeps running).", body_style))

    story.append(Paragraph("Enforcement has two parallel tracks. Performance = patience + patterns. Integrity = verified violation = done.", os_callout_style))

    story.append(Paragraph("FPV Confirmed -- The System Responds", heading_style))
    story.append(Paragraph(
        "Investigation confirms disintermediation. Enforcement moves the partner through FPV_FLAGGED then "
        "SUSPENDED. No warning, no second chance. D&amp;A receives INELIGIBLE_ENFORCEMENT -- zero routing. "
        "Exit OS triggers B2 Integrity Termination: skips the 14-day notice period entirely. "
        "S1 -> S3, bypassing S2. Risk overlay R2 (Hostile) -- all grace periods bypassed.", body_style))

    story.append(Paragraph("Exit OS: B2 = no notice, no grace. R2 = immediate restriction + reallocation.", os_callout_style))

    story.append(Paragraph("The Reallocation", heading_style))
    story.append(Paragraph(
        "R2 bypasses the normal 15% batch limit. All 48 connections queued for immediate rerouting. "
        "D&amp;A runs its 4-stage ranking: eligibility, quality, load ratio, tiebreaker. Other Meerut "
        "partners receive these customers. In the OS, Connection Lifecycle keeps each customer's state as "
        "ACTIVE -- only the csp_id changes.", body_style))

    story.append(Paragraph("Connection Lifecycle: state persists through reassignment (CL_CSP_CHANGED).", os_callout_style))
    story.append(Paragraph(
        "<i>Real world note: the OS keeps the connection ACTIVE, but on the ground the new partner must "
        "physically switch wiring/hardware. Customers will face temporary disruption during handover.</i>", os_callout_style))

    story.append(Paragraph("Settlement &amp; Offboarding", heading_style))
    story.append(Paragraph(
        "Partner enters S5 (Offboarding). Asset Custody marks all NetBoxes as RETRIEVAL_PENDING. "
        "Payment in two tranches: Tranche 1 settles earned compensation to exit date. "
        "Tranche 2 (deposit) only after ALL devices reach a terminal state -- RETURNED, DAMAGED, LOST, "
        "or WRITTEN_OFF. Lost = full recovery deducted. S5 cannot close until custody + settlement complete.", body_style))

    story.append(Paragraph("S5 gate: custody confirmed + settlement complete. 4 terminal states: RETURNED, DAMAGED, LOST, WRITTEN_OFF.", os_callout_style))

    story.append(Paragraph("Key Takeaway", takeaway_style))
    story.append(Paragraph(
        "Integrity violations are fundamentally different from performance problems. Performance = patience, "
        "patterns, recovery time. Integrity = one verified violation ends it. No recovery from confirmed FPV. "
        "The two tracks run independently -- if integrity confirms, it overrides everything.", takeaway_body))

    story.append(Paragraph("Wiom OS Story Bank  |  March 2026  |  For standup use", footer_style))
    story.append(PageBreak())

    # ---- STORY 3: The Zone Crisis ---- (CORRECTED)
    story.append(Paragraph("STORY 3: The Zone Crisis", title_style))
    story.append(Paragraph("One partner dominates a zone. Another exits. How does the system prevent a monopoly?", subtitle_style))

    story.append(Paragraph("The Setup", heading_style))
    story.append(Paragraph(
        "Meerut zone, ZC-A (urban). Three partners: A has 35 connections (58%), B has 18 (30%), "
        "C has 7 (12%). Initial cap: 50 (P65). Concentration alert at 60% (P56) -- A is close at 58%. "
        "Zone is REDUNDANT: meets both requirements -- at least 2 eligible CSPs AND no single CSP above 60%.", body_style))

    story.append(Paragraph("REDUNDANT requires BOTH: >=2 eligible CSPs AND no single CSP >60%. Not just a count check.", os_callout_style))

    story.append(Paragraph("Partner B Exits", heading_style))
    story.append(Paragraph(
        "B declares voluntary exit. Exit OS: S0 -> S1 -> S2 (14-day notice). During notice, B continues "
        "serving 18 connections. Capacity OS checks coverage: A headroom 15 (50-35), C headroom 43 (50-7). "
        "Combined 58, well above B's 18. Coverage confirmed.", body_style))

    story.append(Paragraph("Exit OS checks Capacity OS for alternate coverage. This gates S4 execution.", os_callout_style))

    story.append(Paragraph("Reallocation &amp; Concentration Spike", heading_style))
    story.append(Paragraph(
        "Notice expires. B -> S3 -> S4. D&amp;A reroutes B's 18 connections: eligibility, quality rank, "
        "utilization, tiebreaker. Both A and C are COMPLIANT, so utilization decides: C at 12% load gets "
        "priority over A at 70%. After reallocation: A has 42 (65%), C has 18 (35%). "
        "A has crossed the 60% concentration threshold.", body_style))

    story.append(Paragraph("D&amp;A routes by quality then load -- not by relationship. System-led, always.", os_callout_style))

    story.append(Paragraph("The Escalation", heading_style))
    story.append(Paragraph(
        "A at 65% triggers the alert. Zone flips to CONCENTRATED. 3-tier escalation starts (INV-DAO-16). "
        "Tier 1 (3 cycles): ZONE_REDUNDANCY_PRESSURE -- advisory. "
        "Tier 2 (6 cycles): ZONE_REDUNDANCY_CRITICAL -- binding, remediation plan required. "
        "Tier 3 (9 cycles): D&amp;A auto-applies ELIGIBLE_CAPPED to A. No new connections. "
        "Existing 42 untouched, but growth stops.", body_style))

    story.append(Paragraph("3-tier escalation: Advisory -> Binding -> Auto-cap. ZC-A escalates fastest (1x multiplier).", os_callout_style))

    story.append(Paragraph("Resolution", heading_style))
    story.append(Paragraph(
        "System grows alternatives, not punishes the dominant partner. New Partner D onboarded at "
        "ELIGIBLE_BASELINE (30% exposure, P53) for 2 ramp cycles. As D grows and A's share drops below 60%, "
        "the zone can return to REDUNDANT -- but only if both conditions are met again: >=2 eligible CSPs "
        "AND no single CSP >60%. A's ELIGIBLE_CAPPED is lifted only then. Zone ends up healthier.", body_style))

    story.append(Paragraph("ELIGIBLE_CAPPED lifting requires >=2 eligible CSPs in the zone. Not just the dominant partner shrinking.", os_callout_style))

    story.append(Paragraph("Key Takeaway", takeaway_style))
    story.append(Paragraph(
        "No partner owns a territory. The system prevents concentration through escalating pressure -- "
        "advisory, then mandate, then automated cap. When a partner exits, customers don't suffer: "
        "system reroutes by quality and capacity. The zone self-heals.", takeaway_body))

    story.append(Paragraph("Wiom OS Story Bank  |  March 2026  |  For standup use", footer_style))

    doc.build(story)
    print(f"[OK] Written stories: {path}")


# =====================================================================
# RUN ALL
# =====================================================================
if __name__ == '__main__':
    make_cheat_sheet()
    make_visual_stories()
    make_written_stories()
    print("\nAll PDFs generated in:", OUT)

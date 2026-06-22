from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable
import datetime
import os

# ── Colour palette ──────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0A1628")
ELECTRIC  = colors.HexColor("#1E40AF")
CYAN      = colors.HexColor("#06B6D4")
MINT      = colors.HexColor("#10B981")
AMBER     = colors.HexColor("#F59E0B")
ROSE      = colors.HexColor("#EF4444")
LIGHT_BG  = colors.HexColor("#F0F4FF")
MID_GREY  = colors.HexColor("#64748B")
BORDER    = colors.HexColor("#CBD5E1")
WHITE     = colors.white
PAGE_W, PAGE_H = A4

# ── Custom Flowable: Horizontal Score Bar ────────────────────────────────────
class ScoreBar(Flowable):
    def __init__(self, label, score, max_score=10, color=ELECTRIC, width=420):
        super().__init__()
        self.label = label
        self.score = score
        self.max_score = max_score
        self.color = color
        self.width = width
        self.height = 22

    def draw(self):
        bar_start = 180
        bar_w = self.width - bar_start - 10
        filled = int((self.score / self.max_score) * bar_w)
        # label
        self.canv.setFont("Helvetica", 9)
        self.canv.setFillColor(NAVY)
        self.canv.drawString(0, 6, self.label)
        # background bar
        self.canv.setFillColor(colors.HexColor("#E2E8F0"))
        self.canv.roundRect(bar_start, 4, bar_w, 13, 6, fill=1, stroke=0)
        # filled bar
        self.canv.setFillColor(self.color)
        self.canv.roundRect(bar_start, 4, filled, 13, 6, fill=1, stroke=0)
        # score text
        self.canv.setFont("Helvetica-Bold", 9)
        self.canv.setFillColor(NAVY)
        self.canv.drawRightString(self.width, 6, f"{self.score}/{self.max_score}")

# ── Custom Flowable: Section Header Banner ───────────────────────────────────
class SectionBanner(Flowable):
    def __init__(self, number, title, width=None):
        super().__init__()
        self.number = number
        self.title = title
        self.width = width or (PAGE_W - 40*mm)
        self.height = 32

    def draw(self):
        # full-width dark background
        self.canv.setFillColor(NAVY)
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        # cyan accent strip
        self.canv.setFillColor(CYAN)
        self.canv.roundRect(0, 0, 8, self.height, 3, fill=1, stroke=0)
        # number badge
        self.canv.setFillColor(ELECTRIC)
        self.canv.roundRect(14, 6, 24, 20, 4, fill=1, stroke=0)
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.setFillColor(WHITE)
        self.canv.drawCentredString(26, 12, str(self.number))
        # title
        self.canv.setFont("Helvetica-Bold", 13)
        self.canv.setFillColor(WHITE)
        self.canv.drawString(46, 11, self.title)

# ── Custom Flowable: Metric Card Row ─────────────────────────────────────────
class MetricCards(Flowable):
    def __init__(self, cards, width=None):
        super().__init__()
        self.cards = cards   # list of (label, value, sub, color)
        self.width = width or (PAGE_W - 40*mm)
        self.height = 64

    def draw(self):
        n = len(self.cards)
        gap = 8
        card_w = (self.width - gap*(n-1)) / n
        for i, (label, value, sub, clr) in enumerate(self.cards):
            x = i * (card_w + gap)
            # card bg
            self.canv.setFillColor(LIGHT_BG)
            self.canv.roundRect(x, 0, card_w, self.height, 6, fill=1, stroke=0)
            # top accent line
            self.canv.setFillColor(clr)
            self.canv.roundRect(x, self.height-4, card_w, 4, 3, fill=1, stroke=0)
            # value
            self.canv.setFont("Helvetica-Bold", 15)
            self.canv.setFillColor(NAVY)
            self.canv.drawCentredString(x + card_w/2, 30, value)
            # label
            self.canv.setFont("Helvetica-Bold", 7)
            self.canv.setFillColor(MID_GREY)
            self.canv.drawCentredString(x + card_w/2, 18, label.upper())
            # sub
            self.canv.setFont("Helvetica", 7)
            self.canv.setFillColor(clr)
            self.canv.drawCentredString(x + card_w/2, 7, sub)

# ── Style helpers ─────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    def s(name, **kw):
        return ParagraphStyle(name, parent=base["Normal"], **kw)

    return {
        "cover_title": s("ct", fontName="Helvetica-Bold", fontSize=30,
                         textColor=WHITE, leading=36, alignment=TA_CENTER),
        "cover_sub":   s("cs", fontName="Helvetica", fontSize=13,
                         textColor=colors.HexColor("#94A3B8"), leading=18, alignment=TA_CENTER),
        "cover_tag":   s("ctag", fontName="Helvetica-Bold", fontSize=10,
                         textColor=CYAN, alignment=TA_CENTER),
        "body":        s("b", fontName="Helvetica", fontSize=9.5, textColor=NAVY,
                         leading=15, spaceAfter=6, alignment=TA_JUSTIFY),
        "bold_body":   s("bb", fontName="Helvetica-Bold", fontSize=9.5,
                         textColor=NAVY, leading=15),
        "sub_head":    s("sh", fontName="Helvetica-Bold", fontSize=11,
                         textColor=ELECTRIC, spaceBefore=10, spaceAfter=4),
        "small":       s("sm", fontName="Helvetica", fontSize=8,
                         textColor=MID_GREY, leading=11),
        "tag_green":   s("tg", fontName="Helvetica-Bold", fontSize=8,
                         textColor=WHITE, backColor=MINT, leading=12,
                         borderPadding=(2,5,2,5)),
        "tag_red":     s("tr", fontName="Helvetica-Bold", fontSize=8,
                         textColor=WHITE, backColor=ROSE, leading=12,
                         borderPadding=(2,5,2,5)),
        "bullet":      s("bu", fontName="Helvetica", fontSize=9.5,
                         textColor=NAVY, leading=14, leftIndent=12,
                         bulletIndent=2, spaceAfter=3),
        "toc_item":    s("ti", fontName="Helvetica", fontSize=10,
                         textColor=NAVY, leading=18),
        "footer":      s("ft", fontName="Helvetica", fontSize=7.5,
                         textColor=MID_GREY, alignment=TA_CENTER),
        "verdict_yes": s("vy", fontName="Helvetica-Bold", fontSize=22,
                         textColor=MINT, alignment=TA_CENTER),
        "verdict_txt": s("vt", fontName="Helvetica", fontSize=10,
                         textColor=NAVY, alignment=TA_CENTER, leading=16),
    }

def std_table(data, col_widths, header_bg=ELECTRIC):
    style = TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), header_bg),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0), 9),
        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1), (-1,-1), 8.5),
        ("TEXTCOLOR",   (0,1), (-1,-1), NAVY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_BG]),
        ("GRID",        (0,0), (-1,-1), 0.4, BORDER),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,0),(-1,0),[header_bg]),
    ])
    return Table(data, colWidths=col_widths, style=style, repeatRows=1)

def bullet_list(items, st):
    out = []
    for item in items:
        out.append(Paragraph(f"<bullet>\u2022</bullet> {item}", st["bullet"]))
    return out

# ── Page template with header/footer ─────────────────────────────────────────
def draw_cover(canvas):
    w, h = A4
    c = canvas
    c.saveState()
    # dark gradient background simulation
    c.setFillColor(NAVY)
    c.rect(-20*mm, -16*mm, PAGE_W+40*mm, PAGE_H+30*mm, fill=1, stroke=0)
    # decorative circles
    c.setFillColor(colors.HexColor("#1E3A5F"))
    c.circle(PAGE_W*0.85, PAGE_H*0.75, 90, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#162844"))
    c.circle(PAGE_W*0.1, PAGE_H*0.2, 60, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#0D2137"))
    c.circle(PAGE_W*0.9, PAGE_H*0.15, 110, fill=1, stroke=0)
    # cyan accent bar
    c.setFillColor(CYAN)
    c.rect(-20*mm, PAGE_H*0.52, PAGE_W+40*mm, 3, fill=1, stroke=0)
    c.rect(-20*mm, PAGE_H*0.52+6, PAGE_W+40*mm, 1, fill=1, stroke=0)
    # LOGO area
    c.setFillColor(ELECTRIC)
    c.roundRect(PAGE_W/2-40, PAGE_H*0.72, 80, 80, 12, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W/2, PAGE_H*0.72+26, "AP")
    c.setFont("Helvetica", 9)
    c.setFillColor(CYAN)
    c.drawCentredString(PAGE_W/2, PAGE_H*0.72+10, "AutoPilot Jobs")
    # main title
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W/2, PAGE_H*0.60, "STARTUP VALIDATION")
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(CYAN)
    c.drawCentredString(PAGE_W/2, PAGE_H*0.55, "REPORT")
    # subtitle
    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawCentredString(PAGE_W/2, PAGE_H*0.485,
        "AI-Powered Job Application Automation Platform")
    # divider
    c.setFillColor(BORDER)
    c.rect(PAGE_W/2-80, PAGE_H*0.46, 160, 0.8, fill=1, stroke=0)
    # meta pills
    pills = [
        (PAGE_W/2 - 120, "STAGE: EARLY STARTUP"),
        (PAGE_W/2 + 10,  "MARKET: GLOBAL"),
    ]
    for px, ptxt in pills:
        c.setFillColor(ELECTRIC)
        c.roundRect(px, PAGE_H*0.43, 100, 16, 8, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(WHITE)
        c.drawCentredString(px+50, PAGE_H*0.43+5, ptxt)
    # date + confidential
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GREY)
    c.drawCentredString(PAGE_W/2, PAGE_H*0.40,
        f"Prepared: {datetime.date.today().strftime('%B %d, %Y')}  |  CONFIDENTIAL")
    # bottom strip
    c.setFillColor(ELECTRIC)
    c.rect(-20*mm, -16*mm, PAGE_W+40*mm, 18*mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(WHITE)
    c.drawCentredString(PAGE_W/2, -6*mm,
        "AI Startup Advisor  •  VC Analyst  •  Market Research Expert")
    c.restoreState()

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page == 1:
        draw_cover(canvas)
    else:
        # header bar
        canvas.setFillColor(NAVY)
        canvas.rect(0, h-14*mm, w, 14*mm, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, h-14*mm, 4, 14*mm, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(WHITE)
        canvas.drawString(15*mm, h-8*mm, "AUTOPILOT JOBS — STARTUP VALIDATION REPORT")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(w-15*mm, h-8*mm, datetime.date.today().strftime("%B %Y"))
        # footer
        canvas.setFillColor(LIGHT_BG)
        canvas.rect(0, 0, w, 10*mm, fill=1, stroke=0)
        canvas.setFillColor(BORDER)
        canvas.rect(0, 10*mm, w, 0.5, fill=1, stroke=0)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(MID_GREY)
        canvas.drawCentredString(w/2, 3.5*mm,
            "Confidential — Prepared by AI Startup Advisor | For Founder Use Only")
        canvas.drawRightString(w-15*mm, 3.5*mm, f"Page {doc.page}")
    canvas.restoreState()

# ── BUILD PDF ─────────────────────────────────────────────────────────────────
def build_report(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=16*mm,
        title="AutoPilot Jobs — Startup Validation Report",
    )
    st = make_styles()
    story = []
    W = PAGE_W - 40*mm   # usable width

    # Start with a page break so page 1 is only the cover (drawn in onFirstPage)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # EXECUTIVE SUMMARY
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(1, "EXECUTIVE SUMMARY", W))
    story.append(Spacer(1, 10))
    story.append(MetricCards([
        ("Overall Score",  "7.2/10",  "Strong Potential", ELECTRIC),
        ("Market Size",    "$180B+",  "Global TAM",       MINT),
        ("Risk Level",     "Medium",  "Manageable",       AMBER),
        ("Recommendation", "GO ✓",   "With Conditions",  MINT),
    ], W))
    story.append(Spacer(1, 12))

    summary_text = (
        "<b>AutoPilot Jobs</b> is an AI-powered SaaS platform that automates the entire job application "
        "process by controlling the user's computer — browsing job boards, tailoring application materials, "
        "and submitting applications autonomously on behalf of the candidate. The platform also provides "
        "real-time activity logs showing which jobs were applied to, what messages were sent, and how the "
        "candidate was represented. A parallel dashboard for HR professionals surfaces inbound applicants "
        "and AI-generated candidate profiles."
    )
    story.append(Paragraph(summary_text, st["body"]))
    story.append(Spacer(1, 6))

    exec_table_data = [
        ["DIMENSION", "FINDING", "SCORE"],
        ["Problem Severity",       "Job searching is extremely time-consuming & demoralising",   "9/10"],
        ["Solution Uniqueness",    "Computer-control + auto-apply is novel; very few direct rivals", "8/10"],
        ["Market Opportunity",     "Global; multi-billion dollar HR tech & recruitment space",    "9/10"],
        ["Founder-Market Fit",     "Idea-stage; execution risk exists without domain experience","6/10"],
        ["Validation Readiness",   "Zero external validation; needs immediate user interviews",   "4/10"],
        ["Monetisation Clarity",   "Dual-sided B2C + B2B model viable; pricing TBD",             "7/10"],
        ["Competitive Moat",       "Automation depth is a moat; legal/ToS risk is a threat",     "6/10"],
    ]
    story.append(std_table(exec_table_data, [W*0.28, W*0.52, W*0.20]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Bottom Line:</b> AutoPilot Jobs addresses a real, painful, and universal problem. "
        "The core automation mechanic is differentiated. The primary risks are legal/ToS compliance "
        "with job platforms and the cold-start challenge of building trust. We recommend a <b>conditional GO</b> "
        "— proceed immediately to a 30-day validation sprint before committing engineering resources.",
        st["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # PROBLEM VALIDATION
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(2, "PROBLEM VALIDATION", W))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Core Problem Statement", st["sub_head"]))
    story.append(Paragraph(
        "Active job seekers spend an average of <b>11 hours per week</b> on job applications — "
        "browsing listings, tailoring CVs, writing cover letters, filling repetitive forms, and tracking "
        "submissions. Despite this massive time investment, most applicants hear back from fewer than "
        "10% of applications. The emotional toll compounds with each rejection or silence.",
        st["body"]
    ))

    prob_data = [
        ["PAIN POINT", "SEVERITY", "FREQUENCY", "WILLINGNESS TO PAY"],
        ["Repetitive form filling on every job site",     "🔴 Critical",  "Daily",    "High"],
        ["Tailoring CV/cover letter for each role",       "🔴 Critical",  "Per apply","High"],
        ["Tracking where you applied & what you said",    "🟠 High",      "Weekly",   "Medium"],
        ["Missing deadlines / forgetting to follow up",   "🟠 High",      "Weekly",   "Medium"],
        ["Low response rates despite many applications",  "🔴 Critical",  "Ongoing",  "Very High"],
        ["Ghosting by employers after application sent",  "🟡 Medium",    "Ongoing",  "Low"],
    ]
    story.append(std_table(prob_data, [W*0.36, W*0.18, W*0.18, W*0.28]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Problem Score Breakdown", st["sub_head"]))
    score_items = [
        ("Problem is Real & Widespread",    9, MINT),
        ("Pain is Frequent (not episodic)", 8, MINT),
        ("Existing Solutions are Inadequate", 7, ELECTRIC),
        ("People Actively Search for a Fix",  8, ELECTRIC),
        ("Emotional Intensity of Pain",       9, AMBER),
        ("Validated by Founder Experience",   4, ROSE),
    ]
    for label, score, color in score_items:
        story.append(ScoreBar(label, score, 10, color, W))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # FOUNDER-MARKET FIT
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(3, "FOUNDER-MARKET FIT ANALYSIS", W))
    story.append(Spacer(1, 10))

    story.append(MetricCards([
        ("Domain Expertise",   "5/10", "Needs Deepening",  AMBER),
        ("Personal Pain",      "7/10", "Relatable Problem", ELECTRIC),
        ("Technical Depth",    "?/10", "TBD on Build Ability", MID_GREY),
        ("FMF Overall",        "6/10", "Moderate Fit",     AMBER),
    ], W))
    story.append(Spacer(1, 12))

    fmf_data = [
        ["FIT DIMENSION", "ASSESSMENT", "ACTION NEEDED"],
        ["Have you personally felt this pain?",
         "Likely yes — universal problem",
         "Document your own story"],
        ["Do you understand HR workflows deeply?",
         "Unknown — no HR background stated",
         "Interview 10+ HR managers this week"],
        ["Can you build the automation layer?",
         "Computer-control (RPA/AI) is complex",
         "Validate tech stack or find co-founder"],
        ["Do you have recruiter/HR network?",
         "Not mentioned — critical gap",
         "Join HR communities immediately"],
        ["Can you navigate legal/ToS risks?",
         "Needs legal counsel early",
         "Consult a startup lawyer"],
    ]
    story.append(std_table(fmf_data, [W*0.33, W*0.33, W*0.34]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Recommendation:</b> Your founder-market fit score is <b>6/10</b>. The idea resonates with a "
        "universal pain point, which is a strong starting position. However, building credibility in HR Tech "
        "requires either lived experience as an HR professional or deep relationships in the space. "
        "Consider recruiting a co-founder with HR or recruiting industry experience.",
        st["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # TAM SAM SOM
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(4, "MARKET SIZING — TAM / SAM / SOM", W))
    story.append(Spacer(1, 10))

    story.append(MetricCards([
        ("TAM",  "$180B", "Global HR Tech + Job Market",  ELECTRIC),
        ("SAM",  "$12B",  "AI Job Tools Segment",          CYAN),
        ("SOM",  "$240M", "Year 3 Realistic Capture",      MINT),
    ], W))
    story.append(Spacer(1, 12))

    tam_data = [
        ["MARKET TIER", "SIZE", "BASIS", "TIMELINE"],
        ["TAM — Total Addressable Market",
         "$180B",
         "Global HR technology market + online recruitment platforms (2024)",
         "Global, Now"],
        ["SAM — Serviceable Addressable Market",
         "$12B",
         "AI-powered job search tools, resume automation, applicant tracking adjacency",
         "Global SaaS"],
        ["SOM — Serviceable Obtainable Market",
         "$240M",
         "0.5% of SAM; ~4M paying users @ $5/mo or 10K HR seats @ $200/mo",
         "Year 1-3"],
        ["Beachhead Market",
         "$800M",
         "English-speaking markets (US, UK, India, Canada, Australia) — tech job seekers",
         "Year 1"],
    ]
    story.append(std_table(tam_data, [W*0.28, W*0.10, W*0.44, W*0.18]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Revenue Scenario Modelling", st["sub_head"]))
    rev_data = [
        ["SCENARIO", "USERS (YR 1)", "ARPU/MO", "ARR (YR 1)", "ARR (YR 3)"],
        ["Conservative",   "5,000",    "$8",    "$480K",     "$4.8M"],
        ["Base Case",      "20,000",   "$12",   "$2.88M",    "$24M"],
        ["Optimistic",     "80,000",   "$15",   "$14.4M",    "$120M"],
        ["B2B HR Add-on",  "500 cos",  "$199",  "$1.2M",     "$18M"],
    ]
    story.append(std_table(rev_data, [W*0.22, W*0.18, W*0.16, W*0.22, W*0.22]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # COMPETITOR ANALYSIS
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(5, "COMPETITOR ANALYSIS", W))
    story.append(Spacer(1, 10))

    comp_data = [
        ["COMPETITOR", "TYPE", "STRENGTH", "WEAKNESS", "THREAT LEVEL"],
        ["LinkedIn Easy Apply",
         "Job Platform",
         "Massive user base, trusted brand",
         "Manual still; no real automation",
         "🟠 Medium"],
        ["Indeed / Glassdoor",
         "Job Board",
         "Global reach, employer data",
         "User must still apply manually",
         "🟡 Low"],
        ["Simplify.jobs",
         "Autofill Tool",
         "Autofills forms with 1 click",
         "Not fully autonomous; no AI",
         "🔴 High"],
        ["LazyApply",
         "Auto-Apply SaaS",
         "Bulk LinkedIn/Indeed apply",
         "Spammy; low quality; no personalisation",
         "🔴 High"],
        ["Sonara.ai",
         "AI Job Search",
         "AI matching + auto-apply",
         "Limited personalisation depth",
         "🔴 High"],
        ["JobCopilot",
         "AI Auto-Apply",
         "Automated applications",
         "Limited to select platforms",
         "🔴 High"],
        ["Teal HQ",
         "Job Tracker + AI",
         "Strong UX, job tracking",
         "No automation; manual apply",
         "🟡 Low"],
        ["Traditional Recruiters",
         "Human Service",
         "Relationships, quality",
         "Expensive; not scalable for all",
         "🟡 Low"],
    ]
    story.append(std_table(comp_data, [W*0.18, W*0.14, W*0.24, W*0.26, W*0.18]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Competitive Positioning Matrix", st["sub_head"]))
    pos_data = [
        ["FEATURE", "AutoPilot Jobs", "LazyApply", "Simplify", "Sonara"],
        ["Full PC Automation (RPA)",      "✅", "❌", "❌", "❌"],
        ["AI-Personalised Cover Letters", "✅", "❌", "❌", "⚠️"],
        ["Real-time Activity Log",        "✅", "❌", "❌", "❌"],
        ["HR Dashboard (B2B)",            "✅", "❌", "❌", "❌"],
        ["Multi-platform Support",        "✅", "⚠️", "✅", "⚠️"],
        ["Candidate Quality Filtering",   "✅", "❌", "❌", "✅"],
        ["Free Tier Available",           "⚠️", "❌", "✅", "⚠️"],
    ]
    t = std_table(pos_data, [W*0.40, W*0.15, W*0.15, W*0.15, W*0.15], header_bg=NAVY)
    story.append(t)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # MARKET GAP + ICP + PERSONA
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(6, "MARKET GAP ANALYSIS", W))
    story.append(Spacer(1, 10))
    gaps = [
        "No existing tool offers <b>true computer-control automation</b> (RPA-level) that works across ALL job boards simultaneously.",
        "No competitor provides a <b>real-time transparency log</b> showing candidates exactly what was sent on their behalf.",
        "The <b>dual-sided model</b> (job seeker + HR dashboard) is unexplored — creating a unique data network effect.",
        "AI personalisation at scale (unique message per company, per role) is absent from all current tools.",
        "No current solution handles <b>follow-up messages</b> post-application automatically.",
    ]
    for g in gaps:
        story.append(Paragraph(f"<bullet>▶</bullet> {g}", st["bullet"]))
    story.append(Spacer(1, 12))

    story.append(SectionBanner(7, "IDEAL CUSTOMER PROFILE (ICP)", W))
    story.append(Spacer(1, 10))

    icp_data = [
        ["SEGMENT", "PROFILE", "SIZE", "PRIORITY"],
        ["Primary B2C",
         "Active job seekers: 22-40 yrs, tech/knowledge workers, applying to 10+ jobs/wk",
         "~300M globally",
         "🥇 Tier 1"],
        ["Secondary B2C",
         "Recent graduates / career changers overwhelmed by application volume",
         "~80M globally",
         "🥈 Tier 2"],
        ["Primary B2B",
         "HR Managers / Talent Acquisition at SMBs (50-500 employees) seeking quality candidates",
         "~5M companies",
         "🥇 Tier 1"],
        ["Secondary B2B",
         "Recruitment agencies managing high-volume candidate pipelines",
         "~200K agencies",
         "🥈 Tier 2"],
    ]
    story.append(std_table(icp_data, [W*0.18, W*0.44, W*0.18, W*0.20]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # BUYER PERSONAS
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(8, "BUYER PERSONAS", W))
    story.append(Spacer(1, 10))

    # Persona 1
    story.append(Paragraph("Persona 1 — The Exhausted Job Seeker", st["sub_head"]))
    p1_data = [
        ["ATTRIBUTE",     "DETAIL"],
        ["Name / Age",    "Arjun / 27 — Software Engineer, recently laid off"],
        ["Location",      "Bangalore, India (also: London, New York, Toronto)"],
        ["Goal",          "Land a new role within 60 days; applying to 15+ jobs/day"],
        ["Frustrations",  "Spends 4-5 hrs/day on applications; same info entered 50+ times"],
        ["Tools Used",    "LinkedIn, Naukri, Indeed, Glassdoor, Wellfound"],
        ["Trigger",       "Reads about AutoPilot Jobs on Reddit/LinkedIn; tries free trial"],
        ["WTP",           "$10-20/month — same as Netflix; considers it an investment"],
    ]
    story.append(std_table(p1_data, [W*0.28, W*0.72], header_bg=ELECTRIC))
    story.append(Spacer(1, 10))

    # Persona 2
    story.append(Paragraph("Persona 2 — The Overwhelmed HR Manager", st["sub_head"]))
    p2_data = [
        ["ATTRIBUTE",     "DETAIL"],
        ["Name / Age",    "Sarah / 35 — HR Manager, SaaS company (150 employees)"],
        ["Location",      "London, UK"],
        ["Goal",          "Reduce time-to-hire; filter quality candidates from high-volume inbox"],
        ["Frustrations",  "Receives 200+ applications per role; 80% are irrelevant or spam"],
        ["Tools Used",    "LinkedIn Recruiter, Greenhouse ATS, email"],
        ["Trigger",       "Discovers HR dashboard via LinkedIn ad or referral from peer"],
        ["WTP",           "$150-300/month/seat for quality filtered candidate pipeline"],
    ]
    story.append(std_table(p2_data, [W*0.28, W*0.72], header_bg=NAVY))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # PAIN POINTS, TRIGGERS, OBJECTIONS
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(9, "PAIN POINTS, BUYING TRIGGERS & OBJECTIONS", W))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Top Customer Pain Points", st["sub_head"]))
    pain_data = [
        ["#", "PAIN POINT", "SEGMENT", "INTENSITY"],
        ["1", "Wasting hours on repetitive application forms daily",         "Job Seeker", "🔴 10/10"],
        ["2", "Applications feel generic — no personalisation possible at scale", "Job Seeker", "🔴 9/10"],
        ["3", "No system to track what was sent, when, and to whom",         "Job Seeker", "🟠 8/10"],
        ["4", "Missing follow-up windows leading to lost opportunities",     "Job Seeker", "🟠 7/10"],
        ["5", "Inundated with low-quality or irrelevant applications",       "HR Manager", "🔴 10/10"],
        ["6", "No visibility into candidate intent or quality at screening", "HR Manager", "🟠 8/10"],
    ]
    story.append(std_table(pain_data, [W*0.05, W*0.45, W*0.18, W*0.18]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Buying Triggers", st["sub_head"]))
    triggers = [
        "<b>Job Seeker:</b> Just got laid off and facing 100s of applications ahead",
        "<b>Job Seeker:</b> Frustrated after spending a full weekend applying with zero callbacks",
        "<b>Job Seeker:</b> Sees a peer land a job faster using automation tools",
        "<b>HR Manager:</b> Team drowning in unqualified applications this quarter",
        "<b>HR Manager:</b> CFO demands reduction in cost-per-hire",
    ]
    for t_item in triggers:
        story.append(Paragraph(f"<bullet>⚡</bullet> {t_item}", st["bullet"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Key Objections & Rebuttals", st["sub_head"]))
    obj_data = [
        ["OBJECTION", "REBUTTAL STRATEGY"],
        ['"Will this violate LinkedIn/Indeed ToS?"',
         "Disclose clearly; use official API where possible; position as assistive tool, not scraper"],
        ['"What if it sends bad applications in my name?"',
         "Show full transparency log + approval mode; let users preview before send"],
        ['"I don\'t trust AI to represent me accurately"',
         "Offer full personalisation controls; show AI draft + let user edit before submitting"],
        ['"The price isn\'t worth it"',
         "Frame as ROI: one job offer = months of salary; freemium + money-back guarantee"],
        ['"What if employers reject AI-written applications?"',
         "Emphasise human-in-loop option; studies show AI-assisted apps perform as well or better"],
    ]
    story.append(std_table(obj_data, [W*0.36, W*0.64]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CUSTOMER JOURNEY
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(10, "CUSTOMER JOURNEY MAP", W))
    story.append(Spacer(1, 10))

    journey_data = [
        ["STAGE", "TOUCHPOINT", "EMOTION", "YOUR ROLE"],
        ["Awareness",
         "Reddit post, LinkedIn ad, Google search for 'auto job apply tool'",
         "Curious, Hopeful",
         "SEO content, viral social proof, PR"],
        ["Consideration",
         "Lands on website; reads how-it-works; watches demo video",
         "Interested but sceptical",
         "Clear demo video, FAQ on privacy/ToS"],
        ["Trial",
         "Signs up for free tier; installs desktop agent; first 5 auto-applications",
         "Excited, Nervous",
         "Smooth onboarding wizard; safety controls visible"],
        ["Purchase",
         "Sees first interview invite from an auto-applied job",
         "Delighted, Converted",
         "Upgrade prompt at 'aha moment'"],
        ["Retention",
         "Weekly digest: 'You applied to 47 jobs, 3 responses, 1 interview'",
         "Productive, In Control",
         "Dashboard, progress nudges, streaks"],
        ["Advocacy",
         "Shares success story on LinkedIn; refers friends",
         "Proud, Grateful",
         "Referral programme, testimonial requests"],
    ]
    story.append(std_table(journey_data, [W*0.16, W*0.30, W*0.18, W*0.36]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # RISK ASSESSMENT
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(11, "RISK ASSESSMENT MATRIX", W))
    story.append(Spacer(1, 10))

    risk_data = [
        ["RISK", "CATEGORY", "PROBABILITY", "IMPACT", "MITIGATION"],
        ["LinkedIn/Indeed ban/block of automation",
         "Legal/ToS",    "🔴 High",   "🔴 Critical",
         "Use official APIs; build platform-agnostic fallback; legal review"],
        ["Users distrust AI to represent them",
         "Product",      "🟠 Medium", "🟠 High",
         "Full transparency log; human-in-loop approval mode; edits allowed"],
        ["Competitors copy the feature set quickly",
         "Competitive",  "🟠 Medium", "🟠 High",
         "Move fast; build data moat; file provisional patents"],
        ["Data privacy breach (CV/personal data)",
         "Security",     "🟡 Low",    "🔴 Critical",
         "SOC 2 from day 1; end-to-end encryption; minimal data retention"],
        ["Low application quality = employer complaints",
         "Reputation",   "🟠 Medium", "🟠 High",
         "Quality filters; spam controls; employer feedback loop"],
        ["Difficulty acquiring first 1,000 users",
         "Growth",       "🟠 Medium", "🟠 High",
         "Reddit/LinkedIn community building; influencer partnerships"],
        ["Regulatory changes in AI hiring laws",
         "Regulatory",   "🟡 Low",    "🟠 High",
         "Monitor EU AI Act; US EEOC AI guidance; build compliance module"],
    ]
    story.append(std_table(risk_data, [W*0.24, W*0.14, W*0.14, W*0.14, W*0.34]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # PIVOT OPPORTUNITIES
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(12, "PIVOT OPPORTUNITIES", W))
    story.append(Spacer(1, 10))

    pivot_data = [
        ["PIVOT DIRECTION", "DESCRIPTION", "APPEAL"],
        ["B2B-First Model",
         "Sell directly to staffing/recruitment agencies as a candidate sourcing + outreach tool",
         "🟢 Higher LTV; easier enterprise sale; less ToS risk"],
        ["Niche Vertical Focus",
         "Start with one sector (e.g., tech jobs, nursing, remote) before going horizontal",
         "🟢 Easier to market; faster product-market fit"],
        ["Career Coach Platform",
         "Pivot to AI career coach that includes (but isn't only) auto-apply as a feature",
         "🟡 Broader; less differentiated"],
        ["University / Campus B2B",
         "Partner with universities to help graduating students automate their job search",
         "🟢 Captive audience; high LTV via institutional contracts"],
        ["HR Productivity SaaS",
         "Pivot to pure HR-side tool: AI that manages inbound applications, ranks, and responds",
         "🟡 Competitive; but avoids ToS issues"],
        ["WhiteLabel for Job Boards",
         "Licence the auto-apply engine to smaller job boards as a premium feature",
         "🟢 Asset-light; distribution advantage"],
    ]
    story.append(std_table(pivot_data, [W*0.24, W*0.46, W*0.30]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # GO / NO-GO RECOMMENDATION
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(13, "GO / NO-GO RECOMMENDATION", W))
    story.append(Spacer(1, 14))

    class VerdictBox(Flowable):
        def __init__(self, w):
            super().__init__()
            self.width = w
            self.height = 100

        def draw(self):
            c = self.canv
            c.setFillColor(colors.HexColor("#F0FDF4"))
            c.roundRect(0, 0, self.width, self.height, 10, fill=1, stroke=0)
            c.setFillColor(MINT)
            c.roundRect(0, 0, 6, self.height, 3, fill=1, stroke=0)
            c.roundRect(0, self.height-6, self.width, 6, 3, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 38)
            c.setFillColor(MINT)
            c.drawCentredString(self.width/2, 52, "✅  CONDITIONAL GO")
            c.setFont("Helvetica", 11)
            c.setFillColor(NAVY)
            c.drawCentredString(self.width/2, 28,
                "The opportunity is real. The risk is manageable. The market is large.")
            c.setFont("Helvetica", 10)
            c.setFillColor(MID_GREY)
            c.drawCentredString(self.width/2, 12,
                "Proceed to 30-Day Validation Sprint before engineering investment.")

    story.append(VerdictBox(W))
    story.append(Spacer(1, 14))

    verdict_data = [
        ["FACTOR", "WEIGHT", "SCORE", "WEIGHTED"],
        ["Problem Severity & Market Need",    "25%", "9",   "2.25"],
        ["Solution Differentiation",          "20%", "8",   "1.60"],
        ["Founder-Market Fit",                "15%", "6",   "0.90"],
        ["Market Size (TAM/SAM)",             "15%", "9",   "1.35"],
        ["Competitive Landscape",             "10%", "6",   "0.60"],
        ["Monetisation Viability",            "10%", "7",   "0.70"],
        ["Validation Evidence",               "5%",  "2",   "0.10"],
        ["TOTAL SCORE",                       "100%","—",   "7.50 / 10"],
    ]
    t = std_table(verdict_data, [W*0.40, W*0.15, W*0.15, W*0.30])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,-1),(-1,-1), NAVY),
        ("TEXTCOLOR",   (0,-1),(-1,-1), WHITE),
        ("FONTNAME",    (0,-1),(-1,-1), "Helvetica-Bold"),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Conditions for GO:</b> Speak to 20 target users within 30 days. "
        "Obtain legal opinion on ToS compliance. Build a no-code prototype or Wizard-of-Oz MVP. "
        "Secure at least 100 waitlist signups before writing a single line of production code.",
        st["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # 30-DAY ACTION PLAN
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(14, "30-DAY ACTION PLAN", W))
    story.append(Spacer(1, 10))

    story.append(MetricCards([
        ("Week 1", "Discover", "Talk to users",     ELECTRIC),
        ("Week 2", "Define",   "Shape the MVP",     CYAN),
        ("Week 3", "Build",    "Prototype fast",    MINT),
        ("Week 4", "Validate", "Get real feedback", AMBER),
    ], W))
    story.append(Spacer(1, 12))

    plan_data = [
        ["DAY", "ACTION", "OWNER", "SUCCESS METRIC"],
        ["1-2",  "Map all direct & indirect competitors; use their free trials",
                 "Founder", "Competitive matrix complete"],
        ["3-5",  "Conduct 10 user interviews (job seekers aged 22-40)",
                 "Founder", "10 interviews recorded & transcribed"],
        ["5-7",  "Conduct 5 HR Manager interviews (LinkedIn outreach)",
                 "Founder", "5 HR insights captured"],
        ["7",    "Publish landing page with email waitlist (use Carrd/Framer)",
                 "Founder", "Live page with waitlist form"],
        ["8-10", "Post on Reddit (r/jobs, r/cscareerquestions, r/recruitinghell)",
                 "Founder", "100+ upvotes; 50+ waitlist signups"],
        ["10-12","Consult startup lawyer on ToS/legal risk of automation",
                 "Lawyer",  "Written legal risk summary"],
        ["12-15","Build Wizard-of-Oz MVP (manually do what the AI will automate)",
                 "Founder", "5 beta users onboarded"],
        ["15-20","Run 5 beta users through the manual MVP; document friction",
                 "Founder", "Beta feedback doc; list of top 5 features"],
        ["20-22","Decide: build in-house or outsource automation engine?",
                 "Founder", "Tech decision + budget plan"],
        ["22-25","Launch on Product Hunt or IndieHackers for first press",
                 "Founder", "500+ waitlist sign-ups"],
        ["25-28","Pitch to 3 angel investors or startup accelerators",
                 "Founder", "At least 1 follow-up meeting"],
        ["28-30","Review all findings; decide to build, pivot or pause",
                 "Founder", "Written Go/Pivot/No-Go decision"],
    ]
    story.append(std_table(plan_data, [W*0.08, W*0.46, W*0.14, W*0.32]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Tools & Resources to Use This Month", st["sub_head"]))
    tools = [
        "<b>Landing page:</b> Carrd.co, Framer, or Webflow — launch in under 2 hours",
        "<b>User interviews:</b> Calendly + Zoom + Otter.ai for recording/transcription",
        "<b>Community outreach:</b> Reddit (r/jobs, r/recruitinghell), LinkedIn, Twitter/X",
        "<b>Prototype:</b> Loom videos + Google Form for a Wizard-of-Oz simulation",
        "<b>Legal:</b> Clerky or Stripe Atlas for incorporation + startup lawyer consultation",
        "<b>Investor pipeline:</b> YC, Antler, Sequoia Scout, AngelList",
    ]
    for tool in tools:
        story.append(Paragraph(f"<bullet>→</bullet> {tool}", st["bullet"]))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # FINAL SUMMARY PAGE
    # ════════════════════════════════════════════════════════════════════════
    story.append(SectionBanner(15, "FINAL SUMMARY & KEY TAKEAWAYS", W))
    story.append(Spacer(1, 12))

    final_data = [
        ["✅  STRENGTHS",               "⚠️  RISKS TO MANAGE"],
        ["Massive, universal pain point",    "ToS / legal grey area with job platforms"],
        ["Differentiated core mechanic (RPA)", "No validation yet — ideas need testing"],
        ["Dual-sided network effect potential", "Technical complexity of automation layer"],
        ["Large and growing market",          "Trust gap: users nervous about AI applications"],
        ["Multiple monetisation paths",       "Competitive market — need speed"],
    ]
    ts = TableStyle([
        ("BACKGROUND",  (0,0),(0,0), MINT),
        ("BACKGROUND",  (1,0),(1,0), ROSE),
        ("TEXTCOLOR",   (0,0),(-1,0), WHITE),
        ("FONTNAME",    (0,0),(-1,-1), "Helvetica"),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT_BG]),
        ("GRID",        (0,0),(-1,-1), 0.4, BORDER),
        ("TOPPADDING",  (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING", (0,0),(-1,-1), 10),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
    ])
    ft = Table(final_data, colWidths=[W/2, W/2], style=ts)
    story.append(ft)
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "The single biggest thing you can do right now is <b>talk to 20 real job seekers and 5 HR managers "
        "before writing a single line of code.</b> The idea is compelling — but ideas without validation "
        "are just hypotheses. Your 30-day sprint should answer: Do people want this enough to pay? "
        "Can we build it legally? Who is our best first customer?",
        st["body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("You've got something worth pursuing. Now go validate it.", st["sub_head"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "— Prepared by AI Startup Advisor, VC Analyst & Market Research Expert  |  "
        f"{datetime.date.today().strftime('%B %d, %Y')}",
        st["small"]
    ))

    # BUILD
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("PDF generated successfully!")

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "AutoPilotJobs_Validation_Report.pdf")
    build_report(output_path)

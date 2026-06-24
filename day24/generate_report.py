from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Wedge
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable
import math

OUTPUT = "C:\\Users\\VISHAL\\Desktop\\60_days_cluade\\day24\\VisualLearn_India_Strategy_Report.pdf"

# ─── BRAND PALETTE ──────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#0D1117")
NAVY       = colors.HexColor("#0F1F3D")
INDIGO     = colors.HexColor("#1A2E6C")
ACCENT     = colors.HexColor("#4F8EF7")
ACCENT2    = colors.HexColor("#7C5CFC")
TEAL       = colors.HexColor("#00C4B4")
GREEN      = colors.HexColor("#22C55E")
AMBER      = colors.HexColor("#F59E0B")
RED_C      = colors.HexColor("#EF4444")
ORANGE     = colors.HexColor("#F97316")
LIGHT_GRAY = colors.HexColor("#E5E7EB")
MID_GRAY   = colors.HexColor("#9CA3AF")
DARK_GRAY  = colors.HexColor("#374151")
WHITE      = colors.white
CARD_BG    = colors.HexColor("#F8FAFC")
BORDER     = colors.HexColor("#CBD5E1")

PAGE_W, PAGE_H = A4
L_MARGIN = 18*mm
R_MARGIN = 18*mm
BODY_W = PAGE_W - L_MARGIN - R_MARGIN

# ─── STYLES ─────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE_STYLE   = S("RPT_Title",   fontName="Helvetica-Bold",   fontSize=28, leading=34, textColor=WHITE,      alignment=TA_CENTER)
SUB_STYLE     = S("RPT_Sub",     fontName="Helvetica",        fontSize=13, leading=18, textColor=LIGHT_GRAY, alignment=TA_CENTER)
H1            = S("RPT_H1",      fontName="Helvetica-Bold",   fontSize=16, leading=22, textColor=NAVY,       spaceBefore=10, spaceAfter=6)
H2            = S("RPT_H2",      fontName="Helvetica-Bold",   fontSize=13, leading=18, textColor=INDIGO,     spaceBefore=8,  spaceAfter=4)
H3            = S("RPT_H3",      fontName="Helvetica-Bold",   fontSize=11, leading=15, textColor=DARK_GRAY,  spaceBefore=6,  spaceAfter=3)
BODY          = S("RPT_Body",    fontName="Helvetica",        fontSize=9,  leading=14, textColor=DARK_GRAY,  spaceAfter=4, alignment=TA_JUSTIFY)
BODY_SM       = S("RPT_BodySm", fontName="Helvetica",        fontSize=8,  leading=12, textColor=DARK_GRAY)
BULLET        = S("RPT_Bullet",  fontName="Helvetica",        fontSize=9,  leading=13, textColor=DARK_GRAY,  leftIndent=12, spaceAfter=2)
LABEL         = S("RPT_Label",   fontName="Helvetica-Bold",   fontSize=8,  leading=11, textColor=MID_GRAY,   spaceAfter=2)
CAPTION       = S("RPT_Caption", fontName="Helvetica-Oblique",fontSize=8, leading=11, textColor=MID_GRAY,   alignment=TA_CENTER)
TBL_HDR       = S("TBL_Hdr",    fontName="Helvetica-Bold",   fontSize=8,  leading=11, textColor=WHITE,      alignment=TA_CENTER)
TBL_CELL      = S("TBL_Cell",   fontName="Helvetica",        fontSize=8,  leading=12, textColor=DARK_GRAY)
TBL_CELL_B    = S("TBL_CellB",  fontName="Helvetica-Bold",   fontSize=8,  leading=12, textColor=DARK_GRAY)
ACCENT_TXT    = S("AccentTxt",  fontName="Helvetica-Bold",   fontSize=10, leading=14, textColor=ACCENT,     spaceAfter=3)
VERDICT       = S("Verdict",    fontName="Helvetica-Bold",   fontSize=22, leading=28, textColor=AMBER,      alignment=TA_CENTER)
TOC_ITEM      = S("TOC_item",   fontName="Helvetica",        fontSize=10, leading=16, textColor=NAVY)
TOC_ITEM_B    = S("TOC_itemB",  fontName="Helvetica-Bold",   fontSize=10, leading=16, textColor=NAVY)
PITCH_STYLE   = S("Pitch",      fontName="Helvetica-BoldOblique", fontSize=12, leading=18, textColor=DARK_GRAY, alignment=TA_JUSTIFY)
PAGE_NUM      = S("PageNum",    fontName="Helvetica",        fontSize=8,  leading=10, textColor=MID_GRAY,   alignment=TA_RIGHT)

# ─── HELPERS ────────────────────────────────────────────────────────────────
def HR(color=BORDER, thickness=0.5, space_before=4, space_after=8):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=space_before, spaceAfter=space_after)

def sp(n=6):
    return Spacer(1, n)

def bullet(text, color=ACCENT):
    return Paragraph(f'<font color="#{color.hexval()[2:]}">&#x2022;</font> {text}', BULLET)

def tag_badge(text, bg_color, txt_color=WHITE):
    """Returns a small colored inline badge string for Paragraph use."""
    return f'<font color="#{bg_color.hexval()[2:]}" backColor="#{bg_color.hexval()[2:]}"> </font> {text}'

# ─── CUSTOM FLOWABLES ───────────────────────────────────────────────────────
class ColorBar(Flowable):
    """A colored horizontal rule/divider"""
    def __init__(self, width, height=3, color=ACCENT, radius=2):
        super().__init__()
        self.bar_width  = width
        self.bar_height = height
        self.color      = color
        self.radius     = radius

    def wrap(self, *args):
        return (self.bar_width, self.bar_height + 6)

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 3, self.bar_width, self.bar_height, self.radius, fill=1, stroke=0)


class SectionHeader(Flowable):
    """Bold section banner with left accent bar"""
    def __init__(self, number, title, width=BODY_W, bg=NAVY):
        super().__init__()
        self.number = number
        self.title  = title
        self.width  = width
        self.bg     = bg
        self.height = 28

    def wrap(self, *args):
        return (self.width, self.height + 10)

    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(self.bg)
        c.roundRect(0, 4, self.width, self.height, 4, fill=1, stroke=0)
        # Accent bar
        c.setFillColor(ACCENT)
        c.rect(0, 4, 5, self.height, fill=1, stroke=0)
        # Number circle
        c.setFillColor(ACCENT)
        c.circle(20, 4 + self.height/2, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(20, 4 + self.height/2 - 3, self.number)
        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(35, 4 + self.height/2 - 5, self.title)


class ScoreCard(Flowable):
    """Displays a metric with score bar"""
    def __init__(self, label, score, max_score=100, color=ACCENT, width=BODY_W):
        super().__init__()
        self.label  = label
        self.score  = score
        self.max_score = max_score
        self.color  = color
        self.width  = width
        self.height = 22

    def wrap(self, *args):
        return (self.width, self.height + 4)

    def draw(self):
        c = self.canv
        bar_x = 190
        bar_w = self.width - bar_x - 40
        bar_h = 10
        bar_y = 9

        # Label
        c.setFillColor(DARK_GRAY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0, bar_y + 1, self.label)

        # Background track
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(bar_x, bar_y, bar_w, bar_h, 3, fill=1, stroke=0)

        # Fill
        fill_w = bar_w * (self.score / self.max_score)
        c.setFillColor(self.color)
        c.roundRect(bar_x, bar_y, fill_w, bar_h, 3, fill=1, stroke=0)

        # Score text
        c.setFillColor(DARK_GRAY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(bar_x + bar_w + 6, bar_y + 1, f"{self.score}/100")


class TitlePageFlowable(Flowable):
    """Full-page title block"""
    def __init__(self):
        super().__init__()
        self.width  = PAGE_W
        self.height = PAGE_H

    def wrap(self, *args):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        w, h = PAGE_W, PAGE_H

        # Deep navy gradient background
        c.setFillColor(DARK_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Decorative circles
        c.setFillColor(colors.HexColor("#1A2E6C"))
        c.circle(w * 0.85, h * 0.88, 120, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#0F1F3D"))
        c.circle(w * 0.1, h * 0.12, 90, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#4F8EF720"))
        c.circle(w * 0.5, h * 0.5, 200, fill=1, stroke=0)

        # Top accent bar
        c.setFillColor(ACCENT)
        c.rect(0, h - 8, w, 8, fill=1, stroke=0)

        # Bottom accent bar
        c.setFillColor(ACCENT2)
        c.rect(0, 0, w, 6, fill=1, stroke=0)

        # Tag line box
        bx, by, bw, bh = 40, h * 0.72, w - 80, 24
        c.setFillColor(ACCENT)
        c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(w/2, by + 7, "AI CO-FOUNDER BUSINESS STRATEGY REPORT  |  CONFIDENTIAL")

        # Main Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(w/2, h * 0.59, "VisualLearn India")

        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(w/2, h * 0.53, "Interactive Visual E-Learning Platform")

        # Divider
        c.setFillColor(ACCENT)
        c.rect(w/2 - 60, h*0.51, 120, 2, fill=1, stroke=0)

        # Subtitle
        c.setFillColor(LIGHT_GRAY)
        c.setFont("Helvetica", 12)
        c.drawCentredString(w/2, h * 0.465, "Comprehensive Business Strategy & Investment Analysis")

        # Meta row
        meta_y = h * 0.38
        items = [
            ("MARKET", "India — EdTech"),
            ("STAGE", "Pre-Validation"),
            ("DATE", "June 2025"),
            ("VERDICT", "🟡 VALIDATE"),
        ]
        col_w = (w - 80) / len(items)
        for i, (lbl, val) in enumerate(items):
            cx = 40 + col_w * i + col_w/2
            # Card bg
            c.setFillColor(colors.HexColor("#1A2E6C"))
            c.roundRect(cx - col_w/2 + 5, meta_y - 10, col_w - 10, 52, 6, fill=1, stroke=0)
            c.setFillColor(ACCENT)
            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(cx, meta_y + 28, lbl)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(cx, meta_y + 10, val)

        # Prepared by
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(w/2, h * 0.14, "Prepared by: AI Co-Founder  |  Growth Strategist  |  YC Advisor  |  Business Consultant")
        c.drawCentredString(w/2, h * 0.10, "Based on Customer & MVP Blueprint — VisualLearn India, June 2025")

        # Confidence notice
        c.setFillColor(AMBER)
        c.setFont("Helvetica-BoldOblique", 8)
        c.drawCentredString(w/2, h*0.06, "⚠  Zero validation done — all analysis based on stated assumptions. Validate before building.")


class DashboardFlowable(Flowable):
    """One-page visual dashboard"""
    def __init__(self, width=BODY_W):
        super().__init__()
        self._width = width
        self._height = 220*mm

    def wrap(self, *args):
        return (self._width, self._height)

    def draw(self):
        c   = self.canv
        W   = self._width
        H   = self._height
        py  = float(H)  # current y from top (we'll subtract)

        def box(x, y, w, h, bg=CARD_BG, radius=4, stroke_color=BORDER):
            c.setFillColor(bg)
            c.setStrokeColor(stroke_color)
            c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

        def label_txt(x, y, txt, color=MID_GRAY, size=7, bold=False):
            c.setFillColor(color)
            c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
            c.drawString(x, y, txt)

        def centered(x, y, txt, color=DARK_GRAY, size=9, bold=False):
            c.setFillColor(color)
            c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
            c.drawCentredString(x, y, txt)

        # ── Row 1: Title Banner ────────────────────────────────
        c.setFillColor(NAVY)
        c.roundRect(0, H - 22, W, 20, 3, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, H-22, 4, 20, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(10, H - 14, "VisualLearn India — Business Strategy Dashboard")
        c.setFont("Helvetica", 8)
        c.setFillColor(LIGHT_GRAY)
        c.drawRightString(W - 4, H - 14, "Pre-Validation Stage  |  June 2025")

        row_y = H - 26

        # ── Row 2: Score Cards ────────────────────────────────
        scores = [
            ("Business Viability",  58, ACCENT),
            ("Revenue Potential",   65, TEAL),
            ("GTM Strength",        42, AMBER),
            ("Competitive Strength",48, ACCENT2),
            ("Investor Readiness",  35, ORANGE),
        ]
        sc_h   = 28
        sc_w   = W / len(scores) - 4
        sc_top = row_y - sc_h - 4

        for i, (lbl, val, col) in enumerate(scores):
            sx = i * (sc_w + 4)
            box(sx, sc_top, sc_w, sc_h, bg=DARK_BG, stroke_color=col)
            # Label
            c.setFillColor(LIGHT_GRAY)
            c.setFont("Helvetica", 6)
            # Wrap label
            words = lbl.split()
            if len(words) > 2:
                l1 = " ".join(words[:2])
                l2 = " ".join(words[2:])
            else:
                l1 = lbl
                l2 = ""
            c.drawCentredString(sx + sc_w/2, sc_top + sc_h - 10, l1)
            if l2:
                c.drawCentredString(sx + sc_w/2, sc_top + sc_h - 17, l2)
            c.setFillColor(col)
            c.setFont("Helvetica-Bold", 13)
            c.drawCentredString(sx + sc_w/2, sc_top + 4, f"{val}")

        row_y = sc_top - 6

        # ── Row 3: 3 columns ─────────────────────────────────
        col_w3 = (W - 8) / 3
        r3_h   = 54
        r3_top = row_y - r3_h

        # Business Model
        box(0, r3_top, col_w3, r3_h)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(4, r3_top + r3_h - 10, "BUSINESS MODEL")
        items_bm = ["B2B SaaS (Primary)", "B2B2C via EdTech", "Pilot → Subscription", "Per-learner + Flat fee"]
        for j, itm in enumerate(items_bm):
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 7)
            c.drawString(8, r3_top + r3_h - 20 - j*10, f"• {itm}")

        # Revenue Streams
        box(col_w3 + 4, r3_top, col_w3, r3_h)
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(col_w3 + 8, r3_top + r3_h - 10, "REVENUE STREAMS")
        streams = ["Starter: Rs.15-30/learner/mo", "Growth: Rs.40K-1.2L/mo", "Enterprise: Rs.5L-20L/yr", "Free pilot (3 months)"]
        for j, s in enumerate(streams):
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 7)
            c.drawString(col_w3 + 8, r3_top + r3_h - 20 - j*10, f"• {s}")

        # GTM
        box(2*col_w3 + 8, r3_top, col_w3, r3_h)
        c.setFillColor(AMBER)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(2*col_w3 + 12, r3_top + r3_h - 10, "GO-TO-MARKET")
        gtm_items = ["Direct outbound to CPOs", "EdTech conferences", "Inc42 / LinkedIn content", "Referral from pilot partners"]
        for j, g in enumerate(gtm_items):
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 7)
            c.drawString(2*col_w3 + 12, r3_top + r3_h - 20 - j*10, f"• {g}")

        row_y = r3_top - 6

        # ── Row 4: First 100 Users + Key Risks ──────────────
        col2_w = (W - 6) / 2
        r4_h   = 64
        r4_top = row_y - r4_h

        # First 100 users
        box(0, r4_top, col2_w, r4_h)
        c.setFillColor(ACCENT2)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(4, r4_top + r4_h - 10, "FIRST 100 USERS PLAN")
        users_plan = [
            ("0-10",  "Founder's personal network, CPO cold calls"),
            ("11-30", "EdTech WhatsApp/Slack communities"),
            ("31-60", "Inc42 / LinkedIn thought-leadership content"),
            ("61-100","Pilot partner referrals + conference demos"),
        ]
        for j, (rng, desc) in enumerate(users_plan):
            c.setFillColor(ACCENT2)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(6, r4_top + r4_h - 22 - j*13, rng)
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 6.5)
            # wrap if needed
            c.drawString(38, r4_top + r4_h - 22 - j*13, desc[:55])

        # Key Risks
        box(col2_w + 6, r4_top, col2_w, r4_h)
        c.setFillColor(RED_C)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(col2_w + 10, r4_top + r4_h - 10, "KEY RISKS")
        risks = [
            ("HIGH",   "Zero validation — all assumptions"),
            ("HIGH",   "Tech complexity & WebGL cost spiral"),
            ("MED",    "3-9 month B2B sales cycles"),
            ("MED",    "Established global competitors"),
            ("MED-LOW","Bandwidth constraints Tier 2/3"),
        ]
        risk_colors = {
            "HIGH":   RED_C,
            "MED":    AMBER,
            "MED-LOW":GREEN,
        }
        for j, (lvl, desc) in enumerate(risks):
            rc = risk_colors.get(lvl, MID_GRAY)
            c.setFillColor(rc)
            c.setFont("Helvetica-Bold", 6)
            c.drawString(col2_w + 10, r4_top + r4_h - 22 - j*10, f"[{lvl}]")
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 6.5)
            c.drawString(col2_w + 10 + 38, r4_top + r4_h - 22 - j*10, desc)

        row_y = r4_top - 6

        # ── Row 5: Competitive Moat + Verdict ───────────────
        moat_w = W * 0.58
        verd_w = W - moat_w - 6
        r5_h   = 50
        r5_top = row_y - r5_h

        # Moat
        box(0, r5_top, moat_w, r5_h)
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(4, r5_top + r5_h - 10, "COMPETITIVE MOAT (Building Blocks)")
        moat_items = [
            ("Visual IP Library", ACCENT),
            ("SDK Integrations", TEAL),
            ("Engagement Data", ACCENT2),
            ("NPS/Outcome Data", AMBER),
        ]
        mx = 6
        for j, (m, mc) in enumerate(moat_items):
            bx2 = mx + j * (moat_w/4 - 2)
            c.setFillColor(mc)
            c.roundRect(bx2, r5_top + 8, moat_w/4 - 8, 22, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 6)
            # two lines
            words2 = m.split()
            c.drawCentredString(bx2 + (moat_w/4 - 8)/2, r5_top + 22, words2[0])
            if len(words2) > 1:
                c.drawCentredString(bx2 + (moat_w/4 - 8)/2, r5_top + 13, " ".join(words2[1:]))

        # Verdict
        box(moat_w + 6, r5_top, verd_w, r5_h, bg=DARK_BG, stroke_color=AMBER)
        c.setFillColor(AMBER)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(moat_w + 6 + verd_w/2, r5_top + r5_h - 14, "🟡 VERDICT")
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(moat_w + 6 + verd_w/2, r5_top + r5_h - 27, "VALIDATE")
        c.setFillColor(LIGHT_GRAY)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(moat_w + 6 + verd_w/2, r5_top + r5_h - 38, "Strong concept, real market,")
        c.drawCentredString(moat_w + 6 + verd_w/2, r5_top + r5_h - 47, "zero proof. Validate first.")

        # Footer
        c.setFillColor(BORDER)
        c.rect(0, 0, W, 1, fill=1, stroke=0)
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 6)
        c.drawString(0, 3, "VisualLearn India — AI Co-Founder Strategy Report  |  Confidential  |  June 2025")


def draw_title_page(canvas, doc):
    """Draw the full-page title page on the first page."""
    c = canvas
    w, h = A4

    # Deep navy gradient background
    c.setFillColor(DARK_BG)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Decorative circles
    c.setFillColor(colors.HexColor("#1A2E6C"))
    c.circle(w * 0.85, h * 0.88, 120, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#0F1F3D"))
    c.circle(w * 0.1, h * 0.12, 90, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#4F8EF720"))
    c.circle(w * 0.5, h * 0.5, 200, fill=1, stroke=0)

    # Top accent bar
    c.setFillColor(ACCENT)
    c.rect(0, h - 8, w, 8, fill=1, stroke=0)

    # Bottom accent bar
    c.setFillColor(ACCENT2)
    c.rect(0, 0, w, 6, fill=1, stroke=0)

    # Tag line box
    bx, by, bw, bh = 40, h * 0.72, w - 80, 24
    c.setFillColor(ACCENT)
    c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(w/2, by + 7, "AI CO-FOUNDER BUSINESS STRATEGY REPORT  |  CONFIDENTIAL")

    # Main Title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(w/2, h * 0.59, "VisualLearn India")

    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w/2, h * 0.53, "Interactive Visual E-Learning Platform")

    # Divider
    c.setFillColor(ACCENT)
    c.rect(w/2 - 60, h*0.51, 120, 2, fill=1, stroke=0)

    # Subtitle
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 12)
    c.drawCentredString(w/2, h * 0.465, "Comprehensive Business Strategy & Investment Analysis")

    # Meta row
    meta_y = h * 0.38
    items = [
        ("MARKET", "India — EdTech"),
        ("STAGE", "Pre-Validation"),
        ("DATE", "June 2025"),
        ("VERDICT", "🟡 VALIDATE"),
    ]
    col_w = (w - 80) / len(items)
    for i, (lbl, val) in enumerate(items):
        cx = 40 + col_w * i + col_w/2
        c.setFillColor(colors.HexColor("#1A2E6C"))
        c.roundRect(cx - col_w/2 + 5, meta_y - 10, col_w - 10, 52, 6, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(cx, meta_y + 28, lbl)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(cx, meta_y + 10, val)

    # Prepared by
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(w/2, h * 0.14, "Prepared by: AI Co-Founder  |  Growth Strategist  |  YC Advisor  |  Business Consultant")
    c.drawCentredString(w/2, h * 0.10, "Based on Customer & MVP Blueprint — VisualLearn India, June 2025")

    # Confidence notice
    c.setFillColor(AMBER)
    c.setFont("Helvetica-BoldOblique", 8)
    c.drawCentredString(w/2, h*0.06, "⚠  Zero validation done — all analysis based on stated assumptions. Validate before building.")


# ─── DOCUMENT BUILDER ───────────────────────────────────────────────────────
def build_report():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=L_MARGIN,
        rightMargin=R_MARGIN,
        topMargin=18*mm,
        bottomMargin=18*mm,
        title="VisualLearn India — Business Strategy Report",
        author="AI Co-Founder Analysis Engine",
        onFirstPage=draw_title_page,
    )

    story = []

    # ════════════════════════════════════════════════════════
    # PAGE 2: TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("📋", "Table of Contents"))
    story.append(sp(12))

    toc_data = [
        ("SECTION", "TITLE", "PAGE"),
        ("01", "Startup Snapshot — 10-Point Summary", "3"),
        ("02", "Extracted Assumptions", "3"),
        ("03", "Business Reality Check", "4"),
        ("04", "Executive Summary", "4"),
        ("05", "Business Model Canvas", "5"),
        ("06", "Revenue & Pricing Strategy", "6"),
        ("07", "Go-To-Market Strategy", "7"),
        ("08", "Customer Acquisition Strategy", "7"),
        ("09", "First 100 Users Plan", "8"),
        ("10", "Competitive Position & Moat", "8"),
        ("11", "Reverse SWOT Analysis", "9"),
        ("12", "Investment Scorecard", "9"),
        ("13", "Investor One-Liner & 30-Second Pitch", "10"),
        ("14", "Founder Action Sheet — Top 10 Actions", "10"),
        ("15", "Visual Strategy Dashboard", "11"),
        ("16", "Sustainability Verdict", "11"),
    ]
    toc_style = TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,1), (-1,-1), 9),
        ("TEXTCOLOR",    (0,1), (0,-1), ACCENT),
        ("TEXTCOLOR",    (1,1), (1,-1), DARK_GRAY),
        ("TEXTCOLOR",    (2,1), (2,-1), MID_GRAY),
        ("ALIGN",        (0,0), (0,-1), "CENTER"),
        ("ALIGN",        (2,0), (2,-1), "CENTER"),
        ("GRID",         (0,0), (-1,-1), 0.3, BORDER),
        ("ROWHEIGHT",    (0,0), (-1,-1), 16),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ])
    toc_rows = [[Paragraph(str(r[0]), TBL_HDR if i==0 else TBL_CELL_B),
                 Paragraph(str(r[1]), TBL_HDR if i==0 else TBL_CELL),
                 Paragraph(str(r[2]), TBL_HDR if i==0 else TBL_CELL)]
                for i, r in enumerate(toc_data)]
    toc_table = Table(toc_rows, colWidths=[0.12*BODY_W, 0.76*BODY_W, 0.12*BODY_W])
    toc_table.setStyle(toc_style)
    story.append(toc_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 3: SNAPSHOT + ASSUMPTIONS
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("01", "Startup Snapshot — 10-Point Summary"))
    story.append(sp(8))

    snap_points = [
        ("Concept",       "Gamified, interactive visual e-learning platform replacing passive video/PDF learning with animations, simulations & visual storytelling."),
        ("Problem",       "Indian EdTech platforms report 15–30% course completion rates. Static content causes rapid disengagement, especially on mobile."),
        ("Target",        "Primary: B2B EdTech platforms (BYJU'S, Unacademy, regional players). Secondary: Schools, coaching institutes, colleges (B2B2C)."),
        ("Market",        "250M+ online learners in India. Rs.7,500 Cr market growing at 39% CAGR. NEP 2020 provides strong institutional tailwind."),
        ("ICP",           "CPO / Head of Product at Series-A or bootstrapped EdTech startup with 1K–50K learners. Completion rate problem = primary pain."),
        ("MVP",           "Embeddable HTML5/React visual module player with 3–5 interaction types, SDK/iFrame for LMS, and basic analytics dashboard."),
        ("Pricing",       "Free 3-month pilot → Rs.15–30/learner/mo (Starter) → Rs.40K–1.2L/mo (Growth) → Rs.5L–20L/yr (Enterprise)."),
        ("Validation",    "ZERO. No interviews, pilots, revenue, or market signal. Entire blueprint is assumption-based — high risk."),
        ("Blueprint Scores", "Customer Clarity 52/100 | Problem Severity 70/100 | PMF Potential 58/100 | MVP Readiness 35/100."),
        ("Verdict",       "Promising concept in a real, growing market. However, must be stress-tested with 20 customer interviews and a Figma prototype before any code is written."),
    ]
    snap_data = [[Paragraph(f"<b>{k}</b>", TBL_CELL_B), Paragraph(v, TBL_CELL)] for k, v in snap_points]
    snap_table = Table(snap_data, colWidths=[0.22*BODY_W, 0.78*BODY_W])
    snap_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [CARD_BG, WHITE]),
        ("GRID",          (0,0),(-1,-1), 0.3, BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(snap_table)
    story.append(sp(14))

    story.append(SectionHeader("02", "Extracted Assumptions"))
    story.append(sp(8))

    assum_data = [
        [Paragraph("<b>Category</b>", TBL_HDR), Paragraph("<b>Assumption</b>", TBL_HDR), Paragraph("<b>Risk if Wrong</b>", TBL_HDR)],
        [Paragraph("Customer", TBL_CELL_B), Paragraph("CPOs actively want better engagement tools and will trial unknown vendors", TBL_CELL), Paragraph("High — procurement inertia is real", TBL_CELL)],
        [Paragraph("MVP", TBL_CELL_B), Paragraph("An embeddable player alone is sufficient to prove value without authoring tools", TBL_CELL), Paragraph("High — clients may need content creation help", TBL_CELL)],
        [Paragraph("Value Prop", TBL_CELL_B), Paragraph("20%+ completion rate uplift is achievable and attributable to visual interactivity", TBL_CELL), Paragraph("Critical — without this data, pricing collapses", TBL_CELL)],
        [Paragraph("Pricing", TBL_CELL_B), Paragraph("Rs.15–30/learner willingness-to-pay exists at Starter tier", TBL_CELL), Paragraph("Medium — budget cycles and ROI proof required", TBL_CELL)],
        [Paragraph("GTM", TBL_CELL_B), Paragraph("Cold outreach + conference presence will generate 3 pilots in 60 days", TBL_CELL), Paragraph("High — no existing brand or network", TBL_CELL)],
        [Paragraph("Tech", TBL_CELL_B), Paragraph("HTML5/Canvas MVP is fast to build and integrates cleanly into existing LMS", TBL_CELL), Paragraph("Medium — integration complexity varies widely", TBL_CELL)],
        [Paragraph("Revenue", TBL_CELL_B), Paragraph("B2B SaaS model with pilot-to-paid conversion is achievable pre-product-market fit", TBL_CELL), Paragraph("High — 3–9 month sales cycles in EdTech", TBL_CELL)],
    ]
    assum_table = Table(assum_data, colWidths=[0.16*BODY_W, 0.52*BODY_W, 0.32*BODY_W])
    assum_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), INDIGO),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story.append(assum_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 4: BUSINESS REALITY CHECK + EXEC SUMMARY
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("03", "Business Reality Check"))
    story.append(sp(8))

    reality_data = [
        [Paragraph("<b>Question</b>", TBL_HDR), Paragraph("<b>Honest Answer</b>", TBL_HDR), Paragraph("<b>Action Required</b>", TBL_HDR)],
        [Paragraph("Who pays?", TBL_CELL_B),
         Paragraph("EdTech platform CPOs / CTOs — B2B buyers with quarterly budget cycles. Schools/colleges are slower, institutional buyers.", TBL_CELL),
         Paragraph("Target bootstrapped & Series-A startups first — faster decisions.", TBL_CELL)],
        [Paragraph("Why do they pay?", TBL_CELL_B),
         Paragraph("Only if completion rate uplift is proven, integration is frictionless, and cost is lower than in-house animation production.", TBL_CELL),
         Paragraph("Run pilot with measurable baseline. Generate completion rate data immediately.", TBL_CELL)],
        [Paragraph("How will they discover?", TBL_CELL_B),
         Paragraph("Cold email/WhatsApp to CPOs, Inc42/LinkedIn content, EdTech conferences (EduTech India, BETT), word-of-mouth from pilot partners.", TBL_CELL),
         Paragraph("Founder must be face of the brand. 20 cold calls/week minimum until first 3 pilots.", TBL_CELL)],
        [Paragraph("Biggest growth risk?", TBL_CELL_B),
         Paragraph("Long B2B sales cycles (3–9 months) will exhaust runway before revenue. No founder brand = no inbound pipeline.", TBL_CELL),
         Paragraph("Compress the sales cycle: free pilot + zero-integration SDK. Build in public on LinkedIn.", TBL_CELL)],
        [Paragraph("Biggest monetization risk?", TBL_CELL_B),
         Paragraph("Inability to prove ROI. If completion uplift data is weak or not attributable, pricing falls apart entirely.", TBL_CELL),
         Paragraph("Instrument everything from day 1. Time-on-task, completion delta vs platform baseline, NPS.", TBL_CELL)],
        [Paragraph("Weakest assumptions?", TBL_CELL_B),
         Paragraph("(1) That CPOs will try a zero-brand SDK. (2) That 3 pilots can be closed in 60 days. (3) That an embeddable player alone proves the value.", TBL_CELL),
         Paragraph("Validate #1 with 20 interviews. Target #2 with warm intros. Address #3 with a hybrid offer: player + 3 free modules.", TBL_CELL)],
    ]
    reality_table = Table(reality_data, colWidths=[0.18*BODY_W, 0.44*BODY_W, 0.38*BODY_W])
    reality_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story.append(reality_table)
    story.append(sp(14))

    story.append(SectionHeader("04", "Executive Summary"))
    story.append(sp(8))

    exec_text = [
        ("The Opportunity", "India's EdTech market is structurally broken at the content layer. 250M+ learners consume primarily static video and PDF content, resulting in catastrophic 15–30% course completion rates. VisualLearn India proposes to solve this with an embeddable visual interaction layer — a plug-in SDK that EdTech platforms can drop into their existing LMS to deliver physics animations, coding simulations, maths visualisers, and process flows. The timing is strong: NEP 2020 mandates experiential learning, mobile penetration is accelerating, and no Indian-native player owns this category."),
        ("The Business Model", "The core model is B2B SaaS: charge EdTech platforms a per-learner monthly fee or flat monthly subscription for access to the visual module player SDK. A free 3-month pilot removes buying friction. The unit economics are potentially strong — if a platform with 50,000 learners pays Rs.20/learner/month, that is Rs.10L/month ARR from a single customer. However, this math only works if the completion rate uplift is real, measurable, and defensible enough to justify the line item in a CPO's budget."),
        ("The Critical Risk", "Zero validation has been done. Every number, persona, and assumption in this blueprint is theoretical. The single most important action for the founding team is not to write code — it is to conduct 20 customer discovery interviews with EdTech CPOs and students in the next 7 days. Until there is evidence of pain severity, willingness to pilot, and integration feasibility, no resource should be spent on development."),
        ("The Path Forward", "If interviews confirm the pain and 3 pilot partners express interest, the recommended path is: build a Figma prototype → get validation → build a minimal HTML5 player → go live with one pilot in 30 days → collect completion rate data → use that data to close paid contracts and raise a pre-seed round. This is a fundable idea with the right evidence. Without it, it is a hypothesis."),
    ]
    for title, text in exec_text:
        story.append(Paragraph(f"<b>{title}</b>", H3))
        story.append(Paragraph(text, BODY))
        story.append(sp(4))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 5: BUSINESS MODEL CANVAS
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("05", "Business Model Canvas"))
    story.append(sp(8))
    story.append(Paragraph("The canvas below reflects the hypothesized model based on the blueprint. All cells marked ⚠ require validation.", BODY))
    story.append(sp(8))

    canvas_data = [
        [Paragraph("<b>KEY PARTNERS</b>", TBL_HDR),
         Paragraph("<b>KEY ACTIVITIES</b>", TBL_HDR),
         Paragraph("<b>VALUE PROPOSITIONS</b>", TBL_HDR),
         Paragraph("<b>CUSTOMER RELATIONSHIPS</b>", TBL_HDR),
         Paragraph("<b>CUSTOMER SEGMENTS</b>", TBL_HDR)],
        [Paragraph("• LMS providers\n• EdTech conference organisers\n• EdTech accelerators (Surge, Antler)\n• Content design freelancers\n• NEP 2020 bodies ⚠", TBL_CELL),
         Paragraph("• Visual module development\n• SDK/API maintenance\n• Customer onboarding\n• Analytics & reporting\n• B2B sales outreach ⚠", TBL_CELL),
         Paragraph("• 20%+ completion rate uplift ⚠\n• Plug-and-play SDK (<1 day integration)\n• Mobile-first, low-bandwidth design\n• 5× cheaper than custom animation\n• Measurable ROI dashboard ⚠", TBL_CELL),
         Paragraph("• White-glove onboarding\n• Dedicated pilot success manager\n• Monthly engagement reports\n• Community of EdTech PMs\n• NPS tracking loop ⚠", TBL_CELL),
         Paragraph("PRIMARY: EdTech platforms (B2B)\n• 10–500 employees\n• Rs.1Cr–50Cr ARR\n• Series A / bootstrapped\n\nSECONDARY: Schools & coaching institutes (B2B2C) ⚠", TBL_CELL)],
        [Paragraph("<b>KEY RESOURCES</b>", TBL_HDR),
         Paragraph("", TBL_HDR),
         Paragraph("<b>CHANNELS</b>", TBL_HDR),
         Paragraph("", TBL_HDR),
         Paragraph("", TBL_HDR)],
        [Paragraph("• Founder/tech team\n• Visual interaction library (IP)\n• Analytics platform\n• SDK codebase\n• Pilot engagement data ⚠", TBL_CELL),
         Paragraph("", TBL_CELL),
         Paragraph("• Direct outbound (LinkedIn, email)\n• EdTech conferences & demos\n• Inc42 / EdSurge content\n• Partner referral program\n• Product Hunt launch ⚠", TBL_CELL),
         Paragraph("", TBL_CELL),
         Paragraph("", TBL_CELL)],
        [Paragraph("<b>COST STRUCTURE</b>", TBL_HDR),
         Paragraph("", TBL_HDR),
         Paragraph("", TBL_HDR),
         Paragraph("<b>REVENUE STREAMS</b>", TBL_HDR),
         Paragraph("", TBL_HDR)],
        [Paragraph("Tech development (HTML5/React/Canvas) | Content creation costs | B2B sales & marketing | Infrastructure & hosting | Team salaries", TBL_CELL),
         Paragraph("", TBL_CELL),
         Paragraph("", TBL_CELL),
         Paragraph("Free pilot (3 months) → Per-learner SaaS (Rs.15–30/mo) → Flat monthly (Rs.40K–1.2L/mo) → Enterprise annual licence (Rs.5L–20L/yr)", TBL_CELL),
         Paragraph("", TBL_CELL)],
    ]
    canvas_col_w = BODY_W / 5
    canvas_table = Table(canvas_data, colWidths=[canvas_col_w]*5,
                         rowHeights=[16, 80, 16, 60, 16, 40])
    canvas_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(4,0), NAVY),
        ("BACKGROUND",   (0,2),(4,2), INDIGO),
        ("BACKGROUND",   (0,4),(4,4), INDIGO),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("TEXTCOLOR",    (0,2),(-1,2), WHITE),
        ("TEXTCOLOR",    (0,4),(-1,4), WHITE),
        ("ROWBACKGROUNDS",(0,1),(4,1),[CARD_BG]*5),
        ("ROWBACKGROUNDS",(0,3),(4,3),[WHITE]*5),
        ("ROWBACKGROUNDS",(0,5),(4,5),[CARD_BG]*5),
        ("GRID",         (0,0),(-1,-1), 0.5, BORDER),
        ("SPAN",         (2,2),(4,2)),
        ("SPAN",         (3,2),(4,2)),
        ("SPAN",         (1,3),(2,3)),
        ("SPAN",         (3,3),(4,3)),
        ("SPAN",         (1,5),(2,5)),
        ("SPAN",         (3,5),(4,5)),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("FONTSIZE",     (0,0),(-1,-1), 7.5),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
    ]))
    story.append(canvas_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 6: REVENUE + GTM
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("06", "Revenue & Pricing Strategy"))
    story.append(sp(8))

    story.append(Paragraph("<b>Pricing Architecture</b>", H3))
    story.append(sp(4))

    price_data = [
        [Paragraph("<b>Tier</b>", TBL_HDR), Paragraph("<b>Model</b>", TBL_HDR), Paragraph("<b>Price</b>", TBL_HDR), Paragraph("<b>Target</b>", TBL_HDR), Paragraph("<b>ARR Potential</b>", TBL_HDR)],
        [Paragraph("Pilot", TBL_CELL_B), Paragraph("Free / Rev-share", TBL_CELL), Paragraph("Rs.0 (3 months)", TBL_CELL), Paragraph("First 3 EdTech partners", TBL_CELL), Paragraph("Rs.0 (validation phase)", TBL_CELL)],
        [Paragraph("Starter", TBL_CELL_B), Paragraph("SaaS — Per learner/month", TBL_CELL), Paragraph("Rs.15–30/learner", TBL_CELL), Paragraph("Platforms <10K learners", TBL_CELL), Paragraph("Rs.18L–36L/yr @ 10K learners", TBL_CELL)],
        [Paragraph("Growth", TBL_CELL_B), Paragraph("SaaS — Flat monthly", TBL_CELL), Paragraph("Rs.40K–1.2L/month", TBL_CELL), Paragraph("Platforms 10K–1L learners", TBL_CELL), Paragraph("Rs.4.8L–14.4L/yr per account", TBL_CELL)],
        [Paragraph("Enterprise", TBL_CELL_B), Paragraph("Annual licence + setup", TBL_CELL), Paragraph("Rs.5L–20L/year", TBL_CELL), Paragraph("Large EdTech / institutions", TBL_CELL), Paragraph("Rs.5L–20L/yr per account", TBL_CELL)],
    ]
    price_table = Table(price_data, colWidths=[0.12*BODY_W, 0.20*BODY_W, 0.18*BODY_W, 0.24*BODY_W, 0.26*BODY_W])
    price_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE, CARD_BG, WHITE]),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(price_table)
    story.append(sp(8))

    story.append(Paragraph("<b>Revenue Milestones & Targets</b>", H3))
    story.append(sp(4))
    rev_points = [
        ("Month 1–3", "Rs.0", "3 free pilots live. Data collection begins. Zero revenue, 100% validation."),
        ("Month 4–6", "Rs.2L–5L", "1–2 pilots convert to paid Starter/Growth. First real ARR signal."),
        ("Month 7–12", "Rs.15L–40L ARR", "5–8 paying clients. Enterprise pipeline developing. Fundable milestone."),
        ("Year 2",     "Rs.1Cr–3Cr ARR", "10–20 accounts. 1–2 enterprise deals. Series A territory if NRR > 110%."),
    ]
    rev_data = [[Paragraph("<b>Milestone</b>", TBL_HDR), Paragraph("<b>Target Revenue</b>", TBL_HDR), Paragraph("<b>Key Action</b>", TBL_HDR)]] + \
               [[Paragraph(m, TBL_CELL_B), Paragraph(r, TBL_CELL), Paragraph(a, TBL_CELL)] for m, r, a in rev_points]
    rev_table = Table(rev_data, colWidths=[0.16*BODY_W, 0.20*BODY_W, 0.64*BODY_W])
    rev_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), INDIGO),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE, CARD_BG, WHITE]),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(rev_table)
    story.append(sp(10))

    story.append(SectionHeader("07", "Go-To-Market Strategy"))
    story.append(sp(8))

    gtm_phases = [
        ("Phase 1\nDays 1–30\nValidate & Signal", ACCENT,
         ["20 CPO/student interviews — document pain severity", "Build Figma prototype of 1 visual module", "LinkedIn daily posts: 'Building VisualLearn in public'", "Set up landing page with waitlist (target: 100 signups)", "Identify 3 warm EdTech contacts for pilot conversation"]),
        ("Phase 2\nDays 31–60\nLaunch & Learn", TEAL,
         ["Go live with first pilot partner", "Track completion rate delta vs baseline in real-time", "Collect 50+ student NPS scores", "Submit to Product Hunt (EdTech category)", "Begin Inc42 / EdSurge contributed article pipeline"]),
        ("Phase 3\nDays 61–90\nConvert & Scale", AMBER,
         ["Convert 1–2 pilots to paid (use data as lever)", "Close 2 additional paid pilots via referral", "Apply to Surge / Antler India / 100X.VC", "Build partner referral incentive programme", "Prepare Series Pre-Seed deck with real metrics"]),
    ]
    gtm_data = [[Paragraph(f"<b>{p}</b>", TBL_HDR) for p, _, _ in gtm_phases]]
    max_items = max(len(items) for _, _, items in gtm_phases)
    for i in range(max_items):
        row = []
        for _, col, items in gtm_phases:
            if i < len(items):
                row.append(Paragraph(f"• {items[i]}", TBL_CELL))
            else:
                row.append(Paragraph("", TBL_CELL))
        gtm_data.append(row)

    gtm_table = Table(gtm_data, colWidths=[BODY_W/3]*3)
    gtm_colors = [ACCENT, TEAL, AMBER]
    gtm_ts = TableStyle([
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]*10),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
    ])
    for i, c in enumerate(gtm_colors):
        gtm_ts.add("BACKGROUND", (i,0), (i,0), c)
        gtm_ts.add("TEXTCOLOR",  (i,0), (i,0), WHITE if c != AMBER else DARK_GRAY)
    gtm_table.setStyle(gtm_ts)
    story.append(gtm_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 7: CUSTOMER ACQUISITION + FIRST 100
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("08", "Customer Acquisition Strategy"))
    story.append(sp(8))

    acq_data = [
        [Paragraph("<b>Channel</b>", TBL_HDR), Paragraph("<b>Tactic</b>", TBL_HDR), Paragraph("<b>Target</b>", TBL_HDR), Paragraph("<b>Cost</b>", TBL_HDR), Paragraph("<b>Priority</b>", TBL_HDR)],
        [Paragraph("Founder Outbound", TBL_CELL_B), Paragraph("Direct WhatsApp/LinkedIn cold outreach to CPOs at 50 EdTech startups", TBL_CELL), Paragraph("3 pilot partners in 30 days", TBL_CELL), Paragraph("Rs.0 (time)", TBL_CELL), Paragraph("🔴 P0", TBL_CELL)],
        [Paragraph("Community Presence", TBL_CELL_B), Paragraph("Active participation in EdTech India Slack/LinkedIn/WhatsApp groups", TBL_CELL), Paragraph("10 warm leads", TBL_CELL), Paragraph("Rs.0", TBL_CELL), Paragraph("🔴 P0", TBL_CELL)],
        [Paragraph("Content Marketing", TBL_CELL_B), Paragraph("Weekly LinkedIn posts on 'India EdTech engagement data'. Guest posts on Inc42.", TBL_CELL), Paragraph("Brand awareness + inbound", TBL_CELL), Paragraph("Rs.0 (time)", TBL_CELL), Paragraph("🟡 P1", TBL_CELL)],
        [Paragraph("Conference/Events", TBL_CELL_B), Paragraph("EduTech India, BETT Asia, EdTech Roadshow. Demo the prototype live.", TBL_CELL), Paragraph("2–5 warm prospects per event", TBL_CELL), Paragraph("Rs.10K–30K/event", TBL_CELL), Paragraph("🟡 P1", TBL_CELL)],
        [Paragraph("Partner Referrals", TBL_CELL_B), Paragraph("Incentivise pilot partners to refer peers with a revenue share or extended free access", TBL_CELL), Paragraph("2× referral per happy pilot", TBL_CELL), Paragraph("Rev-share", TBL_CELL), Paragraph("🟢 P2", TBL_CELL)],
        [Paragraph("Accelerator Network", TBL_CELL_B), Paragraph("Apply to Surge, Antler India, 100X.VC — mentors introduce to EdTech portfolio", TBL_CELL), Paragraph("Warm intros to 20+ EdTechs", TBL_CELL), Paragraph("Equity", TBL_CELL), Paragraph("🟢 P2", TBL_CELL)],
    ]
    acq_table = Table(acq_data, colWidths=[0.20*BODY_W, 0.36*BODY_W, 0.20*BODY_W, 0.12*BODY_W, 0.12*BODY_W])
    acq_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]*6),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story.append(acq_table)
    story.append(sp(14))

    story.append(SectionHeader("09", "First 100 Users Plan"))
    story.append(sp(8))

    fu_data = [
        [Paragraph("<b>Users</b>", TBL_HDR), Paragraph("<b>Source</b>", TBL_HDR), Paragraph("<b>Method</b>", TBL_HDR), Paragraph("<b>Timeline</b>", TBL_HDR)],
        [Paragraph("1–10", TBL_CELL_B), Paragraph("Founder's personal EdTech network", TBL_CELL), Paragraph("Direct ask: 'Be my first pilot CPO contact'", TBL_CELL), Paragraph("Week 1", TBL_CELL)],
        [Paragraph("11–30", TBL_CELL_B), Paragraph("EdTech WhatsApp & Slack groups", TBL_CELL), Paragraph("Provide value (data, insights) before pitching", TBL_CELL), Paragraph("Week 2–3", TBL_CELL)],
        [Paragraph("31–50", TBL_CELL_B), Paragraph("LinkedIn content virality", TBL_CELL), Paragraph("Post 'India EdTech completion rate study' — collect emails from engaged commenters", TBL_CELL), Paragraph("Week 3–5", TBL_CELL)],
        [Paragraph("51–75", TBL_CELL_B), Paragraph("Waitlist landing page + Product Hunt teaser", TBL_CELL), Paragraph("Carrd.co page with 1 GIF demo, email capture. Target 100 signups.", TBL_CELL), Paragraph("Week 4–6", TBL_CELL)],
        [Paragraph("76–100", TBL_CELL_B), Paragraph("Pilot partner referrals & accelerator network", TBL_CELL), Paragraph("Ask each happy pilot partner to refer 2 peers. Leverage Surge/Antler mentor network.", TBL_CELL), Paragraph("Week 6–8", TBL_CELL)],
    ]
    fu_table = Table(fu_data, colWidths=[0.10*BODY_W, 0.24*BODY_W, 0.44*BODY_W, 0.22*BODY_W])
    fu_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), INDIGO),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]*5),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story.append(fu_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 8: COMPETITIVE POSITION + REVERSE SWOT
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("10", "Competitive Position & Moat"))
    story.append(sp(8))

    comp_data = [
        [Paragraph("<b>Competitor</b>", TBL_HDR), Paragraph("<b>Strength</b>", TBL_HDR), Paragraph("<b>Weakness vs VisualLearn</b>", TBL_HDR), Paragraph("<b>Threat Level</b>", TBL_HDR)],
        [Paragraph("Kahoot!", TBL_CELL_B), Paragraph("Global brand, gamification, large user base", TBL_CELL), Paragraph("Quiz-focused, not concept visualisation. Not LMS-embeddable SDK.", TBL_CELL), Paragraph("🟡 Medium", TBL_CELL)],
        [Paragraph("Genially", TBL_CELL_B), Paragraph("Rich interactive content, EU market leader", TBL_CELL), Paragraph("Desktop-first, not mobile-optimised for India. High bandwidth requirement.", TBL_CELL), Paragraph("🟡 Medium", TBL_CELL)],
        [Paragraph("Articulate 360", TBL_CELL_B), Paragraph("Enterprise standard for eLearning authoring", TBL_CELL), Paragraph("Authoring tool, not embeddable player. Very expensive for Indian market.", TBL_CELL), Paragraph("🟢 Low-Medium", TBL_CELL)],
        [Paragraph("iSpring / Instancy", TBL_CELL_B), Paragraph("LMS integration capability", TBL_CELL), Paragraph("No India-specific visual content. Generic, not subject-specific.", TBL_CELL), Paragraph("🟢 Low-Medium", TBL_CELL)],
        [Paragraph("BYJU'S in-house", TBL_CELL_B), Paragraph("Proprietary animations, strong brand", TBL_CELL), Paragraph("Not licensable to competitors — actually creates demand for an external solution.", TBL_CELL), Paragraph("🟢 Low", TBL_CELL)],
        [Paragraph("New India entrant", TBL_CELL_B), Paragraph("Local market knowledge, low cost", TBL_CELL), Paragraph("Unknown — primary risk. Must win on speed and data quality.", TBL_CELL), Paragraph("🔴 High", TBL_CELL)],
    ]
    comp_table = Table(comp_data, colWidths=[0.18*BODY_W, 0.28*BODY_W, 0.38*BODY_W, 0.16*BODY_W])
    comp_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]*6),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story.append(comp_table)
    story.append(sp(8))

    story.append(Paragraph("<b>Moat-Building Strategy</b>", H3))
    story.append(sp(4))
    moat_items = [
        ("Visual IP Library", "Each module produced becomes proprietary content. Over time, the breadth and quality of the library becomes a switching cost. Competitors cannot easily replicate 500+ interactive modules."),
        ("SDK Integration Depth", "The deeper the integration with a client's LMS, the harder it is to rip out. Focus on making integrations richer over time — analytics hooks, personalisation APIs."),
        ("Engagement & Outcome Data", "Aggregate anonymised completion rate data across clients creates a benchmarking dataset no competitor has. 'Your platform completes at 28% — the VisualLearn average is 47%' is a powerful sales tool."),
        ("India-Specific Content Design", "Optimise modules for low bandwidth (2G/3G fallback), vernacular language support, and Indian curriculum (CBSE/ICSE/JEE). This creates a deep local moat that global players cannot match cheaply."),
    ]
    for title, text in moat_items:
        story.append(bullet(f"<b>{title}:</b> {text}"))
    story.append(sp(14))

    story.append(SectionHeader("11", "Reverse SWOT Analysis"))
    story.append(sp(6))
    story.append(Paragraph("Reverse SWOT flips the lens: instead of listing assets, it surfaces the worst-case scenario for each quadrant to expose hidden assumptions.", BODY))
    story.append(sp(6))

    rswot_data = [
        [Paragraph("<b>If STRENGTHS are actually weaknesses...</b>", TBL_HDR), Paragraph("<b>If OPPORTUNITIES become threats...</b>", TBL_HDR)],
        [Paragraph(
            "• 'Plug-and-play SDK' assumes LMS standardisation that doesn't exist — most Indian EdTechs use custom-built, incompatible infrastructure.\n"
            "• 'No-code embeddable' may be technically naive — actual integration may require 2–4 weeks of developer time per client, killing the 'easy onboarding' pitch.\n"
            "• 'Visual learning superiority' is not proven for all subjects — some topics (rote learning, language) may show no engagement delta.", TBL_CELL),
         Paragraph(
            "• NEP 2020 tailwind could attract well-funded government-backed competitors who lock up institutional contracts.\n"
            "• The 39% CAGR EdTech market growth may be decelerating post-COVID boom — BYJU'S collapse is a warning sign.\n"
            "• Rising interest in AI tutors (ChatGPT, Khanmigo) could make visual modules obsolete faster than expected.", TBL_CELL)],
        [Paragraph("<b>If WEAKNESSES prove fatal...</b>", TBL_HDR), Paragraph("<b>If THREATS materialise immediately...</b>", TBL_HDR)],
        [Paragraph(
            "• Zero validation means the entire ICP and pain hypothesis could be wrong — CPOs may not actually be the buyer; procurement could go through IT or Academic Heads.\n"
            "• Cash runway exhausted before first paid deal closes (3–9 month B2B sales cycle is brutal at pre-revenue stage).\n"
            "• Technical complexity underestimated — WebGL/Canvas interactive content at scale is expensive and fragile.", TBL_CELL),
         Paragraph(
            "• A well-capitalised competitor (or BYJU'S relaunching) copies the SDK concept and gives it away free to lock the market.\n"
            "• India's 4G data cost spike causes EdTech platforms to deprioritise data-heavy interactive content.\n"
            "• A global player (Coursera, Duolingo) acquires a competitor and bundles visual modules into their India offering.", TBL_CELL)],
    ]
    rswot_table = Table(rswot_data, colWidths=[BODY_W/2, BODY_W/2])
    rswot_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0), colors.HexColor("#1A4731")),
        ("BACKGROUND",   (1,0),(1,0), colors.HexColor("#1A3A5C")),
        ("BACKGROUND",   (0,2),(0,2), colors.HexColor("#4A1A1A")),
        ("BACKGROUND",   (1,2),(1,2), colors.HexColor("#4A3800")),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("TEXTCOLOR",    (0,2),(-1,2), WHITE),
        ("ROWBACKGROUNDS",(0,1),(1,1), [colors.HexColor("#F0FFF4"), colors.HexColor("#EFF6FF")]),
        ("ROWBACKGROUNDS",(0,3),(1,3), [colors.HexColor("#FFF5F5"), colors.HexColor("#FFFBEB")]),
        ("GRID",         (0,0),(-1,-1), 0.5, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 7.5),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story.append(rswot_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 9: INVESTMENT SCORECARD + PITCH
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("12", "Investment Scorecard"))
    story.append(sp(8))

    score_items = [
        ("Business Viability",   58, ACCENT,  "Real pain, real market, real timing with NEP 2020. However, zero validated revenue signal brings this down significantly. Model is sound if assumptions hold."),
        ("Revenue Potential",    65, TEAL,    "Rs.1,500 Cr+ TAM within reach. Per-learner SaaS model scales well. Enterprise contracts (Rs.5L–20L/yr) provide strong ACV. Risk: long sales cycles and price sensitivity."),
        ("GTM Strength",         42, AMBER,   "GTM plan is founder-dependent with no existing network, brand, or distribution. Cold outbound to EdTech CPOs is hard without social proof. Needs thought-leadership and warm intros urgently."),
        ("Competitive Strength", 48, ACCENT2, "No clear moat today. The visual IP library and engagement data are the future moat, but require 12–24 months to build. Global competitors are better-funded."),
        ("Investor Readiness",   35, ORANGE,  "Pre-validation, pre-revenue, pre-prototype. Not yet investable for institutional capital. Could attract a small friends-and-family or angel round after 3 pilots and completion rate data."),
    ]

    for label, score, color, reasoning in score_items:
        story.append(ScoreCard(label, score, color=color, width=BODY_W))
        story.append(Paragraph(reasoning, BODY_SM))
        story.append(sp(4))

    story.append(sp(6))
    story.append(ColorBar(BODY_W, color=BORDER))
    story.append(sp(6))

    # Overall
    overall_score = round(sum(s for _, s, _, _ in score_items) / len(score_items))
    overall_data = [[Paragraph("<b>OVERALL INVESTMENT READINESS SCORE</b>", TBL_HDR), Paragraph(f"<b>{overall_score} / 100</b>", TBL_HDR)]]
    ov_table = Table(overall_data, colWidths=[0.75*BODY_W, 0.25*BODY_W])
    ov_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,-1), WHITE),
        ("FONTSIZE",     (0,0),(-1,-1), 11),
        ("ALIGN",        (1,0),(1,0), "CENTER"),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
    ]))
    story.append(ov_table)
    story.append(sp(14))

    story.append(SectionHeader("13", "Investor One-Liner & 30-Second Pitch"))
    story.append(sp(8))

    # One-liner box
    liner_data = [[Paragraph(
        '<b>Investor One-Liner:</b> VisualLearn India is a B2B SaaS visual interaction layer for India\'s 250M+ learners — '
        'an embeddable SDK that plugs into any EdTech platform and converts passive video content into interactive animations, '
        'simulations and drag-to-learn modules, targeting the 70%+ course drop-off crisis and commanding a per-learner '
        'subscription model in a Rs.7,500 Cr market growing at 39% CAGR.',
        PITCH_STYLE)]]
    liner_table = Table(liner_data, colWidths=[BODY_W])
    liner_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), CARD_BG),
        ("LEFTBORDER",   (0,0),(0,-1), 4),
        ("LINEAFTER",    (0,0),(0,0), 4, ACCENT),
        ("BOX",        (0,0),(-1,-1), 0.5, ACCENT),
        ("LEFTPADDING",(0,0),(-1,-1), 16),
        ("TOPPADDING", (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
    ]))
    story.append(liner_table)
    story.append(sp(10))

    story.append(Paragraph("<b>30-Second Founder Pitch</b>", H3))
    story.append(sp(4))
    pitch_text = (
        '"India has 250 million online learners — and 70% of them drop out before finishing a single course. '
        'Not because the content is bad, but because static video and PDFs cannot explain Physics, Maths, or Coding at the level students actually need. '
        'We built VisualLearn India: a plug-and-play SDK that any EdTech platform can drop into their existing app in under a day. '
        'It converts lecture content into interactive animations, drag-to-learn simulations, and visual concept flows. '
        'In our first pilot, we saw completion rates improve from 24% to 47% — on the same course. '
        'We charge Rs.20 per learner per month. A platform with 50,000 learners pays Rs.10 lakh a month. '
        'There are 200+ such platforms in India today, and none of them have this. '
        'We are raising Rs.1.5 crore to sign 10 paying customers and hit Rs.1 crore ARR in 12 months."'
    )
    pitch_data = [[Paragraph(pitch_text, PITCH_STYLE)]]
    pitch_table = Table(pitch_data, colWidths=[BODY_W])
    pitch_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), DARK_BG),
        ("BOX",         (0,0),(-1,-1), 0.5, ACCENT),
        ("LEFTPADDING", (0,0),(-1,-1), 16),
        ("TOPPADDING",  (0,0),(-1,-1), 12),
        ("BOTTOMPADDING",(0,0),(-1,-1), 12),
        ("TEXTCOLOR",   (0,0),(-1,-1), WHITE),
    ]))
    story.append(pitch_table)
    story.append(Paragraph("⚠  Note: Pitch references pilot data for illustrative purposes. Replace with real numbers once validation is complete.", CAPTION))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 10: FOUNDER ACTION SHEET
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("14", "Founder Action Sheet — Top 10 Actions"))
    story.append(sp(8))

    actions = [
        ("01", "🔴 IMMEDIATE", "Do 20 Customer Discovery Interviews This Week",
         "Call or WhatsApp 20 EdTech CPOs and 10 students. Do not pitch. Ask: What is your course completion rate? What have you tried? What would you pay to fix it? Document verbatim responses. This is the most important action in the entire plan."),
        ("02", "🔴 IMMEDIATE", "Build a Figma Prototype — Not Code",
         "Create 1 visual module on a real topic (JEE Physics, coding loops, or Biology cell division). Show it to 10 contacts. Measure their reaction: 'Would your platform use this?' If yes, proceed. If no, understand why."),
        ("03", "🔴 IMMEDIATE", "Define Your 1 Differentiator in One Sentence",
         "Not 'interactive learning' — be surgical. Example: 'A mobile-first visual concept player that proves 20% completion uplift in 30 days or the pilot is free.' This sentence will close deals."),
        ("04", "🟡 WEEK 1", "Join 5 EdTech Communities and Listen First",
         "EdTech India on LinkedIn, Slack (Inc42 community, EdSurge), WhatsApp groups. Do not pitch. Share insights, data points, useful research. Build trust before you ask for anything."),
        ("05", "🟡 WEEK 1", "Set Up a Landing Page With Waitlist",
         "Use Carrd.co or Webflow. 1 headline, 1 demo GIF, email capture form. Target: 100 email signups in 30 days. This is your early social proof."),
        ("06", "🟡 WEEK 2", "Identify and Approach 3 Pilot Partners",
         "Target small bootstrapped EdTechs (1K–50K learners) — they decide faster. Offer a free 3-month pilot with completion rate benchmarking included. Use your interviews to shortlist the 3 warmest leads."),
        ("07", "🟡 WEEK 2", "Research All Competitors Deeply",
         "Spend 2 days on Kahoot!, Genially, Articulate, iSpring, Instancy. Know their pricing, gaps, India presence, and LMS compatibility. Your sales pitch must reference them specifically."),
        ("08", "🟢 WEEK 2–3", "Decide Tech Stack and Stick to It",
         "React + HTML5 Canvas/SVG for MVP. Do not use Unity, WebGL, or native apps until you have 3 paying customers. Complexity kills pre-revenue startups. Simple scales first."),
        ("09", "🟢 WEEK 3", "Apply to EdTech Accelerators",
         "Apply simultaneously to: Surge (Peak XV Partners), Antler India, 100X.VC, Google for Startups India. The network value alone justifies the equity cost. Accelerators also open EdTech client doors directly."),
        ("10", "🟢 ONGOING", "Track 3 Core Weekly Metrics — Review Every Friday",
         "Number of customer conversations completed | Number of prototype demo views | Number of pilot interest confirmations. Nothing else matters until these numbers move."),
    ]

    action_data = [[Paragraph("<b>#</b>", TBL_HDR), Paragraph("<b>Priority</b>", TBL_HDR), Paragraph("<b>Action</b>", TBL_HDR), Paragraph("<b>Detail</b>", TBL_HDR)]]
    priority_colors = {"🔴 IMMEDIATE": RED_C, "🟡 WEEK 1": AMBER, "🟡 WEEK 2": AMBER, "🟢 WEEK 2–3": GREEN, "🟢 WEEK 3": GREEN, "🟢 ONGOING": GREEN}
    for num, priority, title, detail in actions:
        action_data.append([
            Paragraph(f"<b>{num}</b>", TBL_CELL_B),
            Paragraph(priority, TBL_CELL),
            Paragraph(f"<b>{title}</b>", TBL_CELL_B),
            Paragraph(detail, TBL_CELL),
        ])

    action_table = Table(action_data, colWidths=[0.06*BODY_W, 0.13*BODY_W, 0.27*BODY_W, 0.54*BODY_W])
    action_ts = TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[CARD_BG, WHITE]*10),
        ("GRID",         (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",     (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("ALIGN",        (0,0),(0,-1), "CENTER"),
    ])
    # Color priority cells
    for i, (_, priority, _, _) in enumerate(actions, 1):
        col = priority_colors.get(priority, MID_GRAY)
        action_ts.add("TEXTCOLOR", (1,i), (1,i), col)
        action_ts.add("FONTNAME",  (1,i), (1,i), "Helvetica-Bold")
    action_table.setStyle(action_ts)
    story.append(action_table)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # PAGE 11: VISUAL DASHBOARD
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("15", "Visual Strategy Dashboard"))
    story.append(sp(8))
    story.append(DashboardFlowable(width=BODY_W))
    story.append(sp(10))

    # ════════════════════════════════════════════════════════
    # PAGE 12: SUSTAINABILITY VERDICT
    # ════════════════════════════════════════════════════════
    story.append(SectionHeader("16", "Sustainability Verdict"))
    story.append(sp(10))

    verdict_data = [[Paragraph("🟡  VALIDATE — DO NOT BUILD YET", VERDICT)]]
    verdict_table = Table(verdict_data, colWidths=[BODY_W])
    verdict_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), DARK_BG),
        ("BOX",         (0,0),(-1,-1), 2, AMBER),
        ("TOPPADDING",  (0,0),(-1,-1), 14),
        ("BOTTOMPADDING",(0,0),(-1,-1), 14),
    ]))
    story.append(verdict_table)
    story.append(sp(12))

    verdict_body = [
        "VisualLearn India addresses a genuine, structurally persistent problem in a large, fast-growing market with strong government tailwind — the case for a visual interaction layer in Indian EdTech is credible, and the B2B SaaS model is the right vehicle to monetise it at scale. However, the entire blueprint is built on zero validated evidence: no interviews, no prototype tests, no market signal, and no revenue. At this stage, the startup is a hypothesis, not a business — and the gap between a compelling hypothesis and a sustainable company is measured in customer conversations, not lines of code.",
        "The path to sustainability is clear and achievable in 90 days: conduct 20 customer discovery interviews to validate the pain and ICP, build a Figma prototype to test the value proposition, secure 3 pilot partners to generate completion rate data, and use that data to close the first paid contracts and open an investor conversation. If those milestones are hit with strong data (>20% completion uplift, NPS > 40, integration time < 1 day), this becomes a fundable, scalable B2B SaaS business with a defensible moat in India's EdTech infrastructure layer.",
        "The sustainability risk is not the idea — it is execution velocity and the founder's ability to sell before building. Every day spent on code without customer evidence is a day of runway wasted. The market will not wait: validate aggressively, build minimally, and let real customer data — not this blueprint — drive every product and pricing decision from here.",
    ]
    for para in verdict_body:
        story.append(Paragraph(para, BODY))
        story.append(sp(6))

    story.append(sp(8))
    story.append(ColorBar(BODY_W, height=2, color=ACCENT2))
    story.append(sp(8))

    footer_data = [[
        Paragraph("VisualLearn India", TBL_CELL_B),
        Paragraph("AI Co-Founder Strategy Report", TBL_CELL),
        Paragraph("June 2025  |  Confidential", TBL_CELL),
        Paragraph("Overall Score: 49/100", TBL_CELL_B),
    ]]
    footer_table = Table(footer_data, colWidths=[0.25*BODY_W]*4)
    footer_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), CARD_BG),
        ("BOX",         (0,0),(-1,-1), 0.3, BORDER),
        ("GRID",        (0,0),(-1,-1), 0.3, BORDER),
        ("FONTSIZE",    (0,0),(-1,-1), 8),
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("TOPPADDING",  (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("TEXTCOLOR",   (3,0),(3,0), AMBER),
    ]))
    story.append(footer_table)

    doc.build(story)
    print(f"PDF generated: {OUTPUT}")

build_report()

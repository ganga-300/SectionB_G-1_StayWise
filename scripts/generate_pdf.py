from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.pdfgen import canvas as rl_canvas

OUTPUT_PATH = "/Users/SarMish/Desktop/SectionB_G-1_StayWise/reports/StayWise_Final_Report.pdf"

# ── Colors ──────────────────────────────────────────────────────────────────
DARK_BLUE  = colors.HexColor("#0D2B4E")
MID_BLUE   = colors.HexColor("#1A5276")
ACCENT_RED = colors.HexColor("#C0392B")
LIGHT_GRAY = colors.HexColor("#F2F4F6")
MED_GRAY   = colors.HexColor("#BDC3C7")
TEXT_DARK  = colors.HexColor("#1C2833")
WHITE      = colors.white

W, H = A4

# ── Page numbering ───────────────────────────────────────────────────────────
class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        page_num = self._saved_page_states.index(dict(self.__dict__)) if dict(self.__dict__) in self._saved_page_states else 0
        # Footer line
        self.setStrokeColor(MID_BLUE)
        self.setLineWidth(0.5)
        self.line(2*cm, 1.8*cm, W - 2*cm, 1.8*cm)
        self.setFont("Helvetica", 8)
        self.setFillColor(MID_BLUE)
        self.drawString(2*cm, 1.2*cm, "StayWise | Hotel Booking Analytics | Newton School of Technology")
        self.drawRightString(W - 2*cm, 1.2*cm, f"Page {self._pageNumber} of {page_count}")

# ── Doc Setup ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.8*cm,
    title="StayWise: Hotel Booking Analytics",
    author="Section B, G-1 | Newton School of Technology"
)

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=base[parent], **kw)
    return s

S = {
    "cover_title": style("cover_title", "Title",
        fontSize=28, textColor=WHITE, spaceAfter=8, leading=34,
        fontName="Helvetica-Bold", alignment=TA_LEFT),
    "cover_sub": style("cover_sub", "Normal",
        fontSize=13, textColor=colors.HexColor("#AED6F1"), spaceAfter=4,
        fontName="Helvetica", alignment=TA_LEFT),
    "cover_label": style("cover_label", "Normal",
        fontSize=9, textColor=MED_GRAY, fontName="Helvetica",
        spaceAfter=2, alignment=TA_LEFT),
    "cover_value": style("cover_value", "Normal",
        fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
        spaceAfter=6, alignment=TA_LEFT),
    "h1": style("h1", "Heading1",
        fontSize=16, textColor=DARK_BLUE, fontName="Helvetica-Bold",
        spaceBefore=18, spaceAfter=6, leading=20),
    "h2": style("h2", "Heading2",
        fontSize=12, textColor=MID_BLUE, fontName="Helvetica-Bold",
        spaceBefore=12, spaceAfter=4, leading=15),
    "body": style("body", "Normal",
        fontSize=10, textColor=TEXT_DARK, fontName="Helvetica",
        leading=15, spaceAfter=7, alignment=TA_JUSTIFY),
    "body_b": style("body_b", "Normal",
        fontSize=10, textColor=TEXT_DARK, fontName="Helvetica-Bold",
        leading=15, spaceAfter=5),
    "bullet": style("bullet", "Normal",
        fontSize=10, textColor=TEXT_DARK, fontName="Helvetica",
        leading=14, spaceAfter=4, leftIndent=14, firstLineIndent=-10,
        alignment=TA_JUSTIFY),
    "caption": style("caption", "Normal",
        fontSize=8.5, textColor=colors.HexColor("#7F8C8D"),
        fontName="Helvetica-Oblique", spaceAfter=6, alignment=TA_CENTER),
    "small": style("small", "Normal",
        fontSize=8.5, textColor=TEXT_DARK, fontName="Helvetica",
        leading=12, spaceAfter=3),
    "tag": style("tag", "Normal",
        fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
        leading=11, spaceAfter=2),
}

def bullet_item(txt):
    return Paragraph(f"&#8226;&nbsp;&nbsp;{txt}", S["bullet"])

def h1(txt, num=""):
    prefix = f"{num}.&nbsp;&nbsp;" if num else ""
    return Paragraph(f"{prefix}{txt}", S["h1"])

def h2(txt):
    return Paragraph(txt, S["h2"])

def body(txt):
    return Paragraph(txt, S["body"])

def sp(h=6):
    return Spacer(1, h)

def hr(color=MID_BLUE, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=2)

# ────────────────────────────────────────────────────────────────────────────
# COVER PAGE
# ────────────────────────────────────────────────────────────────────────────
def cover_page():
    elements = []

    # Blue banner drawn via a table
    cover_data = [[""]]
    cover_table = Table(cover_data, colWidths=[W - 5*cm], rowHeights=[7*cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("BOX", (0,0), (-1,-1), 0, DARK_BLUE),
    ]))

    # We'll use a blue background block via a nested approach
    # Top accent bar
    accent = Table([[""]], colWidths=[W - 5*cm], rowHeights=[0.4*cm])
    accent.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), ACCENT_RED)]))
    elements.append(accent)
    elements.append(sp(4))

    # Institute badge
    badge_data = [["NEWTON SCHOOL OF TECHNOLOGY  |  DATA VISUALIZATION & ANALYTICS"]]
    badge = Table(badge_data, colWidths=[W - 5*cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,-1), WHITE),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    elements.append(badge)
    elements.append(sp(30))

    # Big title block
    title_content = [
        [Paragraph("StayWise", S["cover_title"])],
        [Paragraph("Hotel Booking Analytics for Revenue &amp; Cancellation Optimization", S["cover_sub"])],
        [Paragraph("DVA Capstone 2 — Final Project Report", ParagraphStyle("ct2", parent=S["cover_sub"],
            fontSize=10, textColor=MED_GRAY, spaceAfter=2))],
    ]
    title_tbl = Table(title_content, colWidths=[W - 5*cm])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
        ("TOPPADDING", (0,0), (0,0), 22),
        ("BOTTOMPADDING", (0,-1), (-1,-1), 22),
    ]))
    elements.append(title_tbl)
    elements.append(sp(28))

    # Info grid
    def info_row(label, value):
        return [
            Paragraph(label.upper(), ParagraphStyle("lbl", parent=S["small"],
                textColor=colors.HexColor("#7F8C8D"), fontName="Helvetica-Bold", fontSize=8)),
            Paragraph(value, ParagraphStyle("val", parent=S["small"],
                fontName="Helvetica-Bold", fontSize=10, textColor=TEXT_DARK))
        ]

    info_data = [
        info_row("Sector", "Hospitality / Travel"),
        info_row("Team ID", "Section B, Group G-1"),
        info_row("Institute", "Newton School of Technology"),
        info_row("GitHub", "github.com/ganga-300/SectionB_G-1_StayWise"),
        info_row("Tableau", "public.tableau.com — Dashboard 1 &amp; Dashboard 2"),
    ]
    info_tbl = Table(info_data, colWidths=[4*cm, W - 5*cm - 4*cm - 0.5*cm])
    info_tbl.setStyle(TableStyle([
        ("LINEBELOW", (0,0), (-1,-2), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elements.append(info_tbl)
    elements.append(sp(20))

    # Team members table
    members = [
        ("Sarthak Mishra", "Project Lead"),
        ("Ganga Raghuwanshi", "Data Lead"),
        ("Musthyala Sadhvik", "ETL Lead"),
        ("Kunal Dev Sahu", "Analysis Lead"),
        ("Soumen Dass", "Visualization Lead"),
        ("Deepak Mishra", "Strategy Lead"),
        ("Lakshay Yadav", "PPT &amp; Quality Lead"),
    ]
    header = [[
        Paragraph("TEAM MEMBER", ParagraphStyle("th", parent=S["small"], fontName="Helvetica-Bold",
            fontSize=8, textColor=WHITE)),
        Paragraph("ROLE", ParagraphStyle("th2", parent=S["small"], fontName="Helvetica-Bold",
            fontSize=8, textColor=WHITE)),
    ]]
    rows = [[Paragraph(n, S["small"]), Paragraph(r, S["small"])] for n, r in members]
    team_data = header + rows
    team_tbl = Table(team_data, colWidths=[8*cm, W - 5*cm - 8*cm - 0.5*cm])
    team_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("BACKGROUND", (0,1), (-1,-1), LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    elements.append(team_tbl)
    elements.append(PageBreak())
    return elements

# ────────────────────────────────────────────────────────────────────────────
# SECTION HELPERS
# ────────────────────────────────────────────────────────────────────────────
def section_header(num, title):
    data = [[Paragraph(f"{num}", ParagraphStyle("sn", parent=S["tag"], fontSize=11)),
             Paragraph(title, ParagraphStyle("st", parent=S["h1"], textColor=WHITE, spaceBefore=0, spaceAfter=0, fontSize=15))]]
    tbl = Table(data, colWidths=[1.1*cm, W - 5*cm - 1.5*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("LEFTPADDING", (0,0), (0,-1), 10),
        ("LEFTPADDING", (1,0), (1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    return [tbl, sp(10)]

def callout_box(title, items, color=MID_BLUE):
    rows = [[Paragraph(f"&#10003;&nbsp;&nbsp;{i}", S["small"])] for i in items]
    inner = Table(rows, colWidths=[W - 5*cm - 2.4*cm])
    inner.setStyle(TableStyle([
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
    ]))
    header_row = [[Paragraph(title, ParagraphStyle("bh", parent=S["body_b"], textColor=WHITE, spaceAfter=0))]]
    full_data = header_row + [[inner]]
    box = Table(full_data, colWidths=[W - 5*cm - 2*cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), color),
        ("BACKGROUND", (0,1), (-1,-1), LIGHT_GRAY),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("BOX", (0,0), (-1,-1), 0.5, color),
    ]))
    return [box, sp(8)]

def kpi_row(kpis):
    """kpis = list of (value, label) tuples, max 4"""
    cells = []
    for val, lbl in kpis:
        cell = Table([
            [Paragraph(val, ParagraphStyle("kv", parent=S["h1"], textColor=DARK_BLUE, fontSize=22, spaceAfter=2, spaceBefore=0))],
            [Paragraph(lbl, ParagraphStyle("kl", parent=S["small"], textColor=colors.HexColor("#5D6D7E"), fontSize=8.5))],
        ], colWidths=[(W - 5*cm) / len(kpis) - 0.4*cm])
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), LIGHT_GRAY),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("BOX", (0,0), (-1,-1), 0.5, MED_GRAY),
        ]))
        cells.append(cell)
    row_data = [cells]
    tbl = Table(row_data, colWidths=[(W - 5*cm) / len(kpis)] * len(kpis), hAlign="LEFT")
    tbl.setStyle(TableStyle([("LEFTPADDING", (0,0), (-1,-1), 2), ("RIGHTPADDING", (0,0), (-1,-1), 2)]))
    return [tbl, sp(10)]

# ────────────────────────────────────────────────────────────────────────────
# CONTENT
# ────────────────────────────────────────────────────────────────────────────
def build_story():
    e = []
    e += cover_page()

    # ── 2. Executive Summary ─────────────────────────────────────────────
    e += section_header("2", "Executive Summary")
    e.append(body(
        "The global hospitality industry faces persistent revenue pressure from two intertwined challenges: "
        "high booking cancellation rates and suboptimal distribution-channel strategies. StayWise is a "
        "data-driven analytics initiative developed by Newton School of Technology's Section B, Group G-1, "
        "designed to convert raw booking transaction data into actionable intelligence for hotel revenue "
        "managers. This report presents findings derived from a robust Python-based ETL pipeline and an "
        "interactive Tableau dashboard, enabling decision-makers to understand, anticipate, and mitigate "
        "cancellation-driven revenue loss."
    ))
    e.append(h2("Business Challenge"))
    e.append(body(
        "Hotel operators routinely encounter booking cancellations that leave rooms vacant with little "
        "time to fill them, eroding RevPAR (Revenue Per Available Room) and disrupting staffing plans. "
        "The problem is compounded by heavy dependence on Online Travel Agencies (OTAs), which facilitate "
        "flexible—and frequently exercised—cancellation policies that benefit consumers but penalize "
        "properties. Without data-driven visibility into cancellation risk factors, hotels rely on reactive "
        "overbooking strategies that damage guest experience and brand reputation."
    ))
    e.append(h2("Analytical Approach"))
    e.append(body(
        "The team sourced a publicly available Hotel Booking Demand dataset covering 119,209 reservations "
        "across two hotel types (City and Resort) for the period 2015–2017. A Python ETL pipeline "
        "standardised and enriched the data, reducing it to 87,219 analytically valid records across "
        "29 curated columns. Exploratory and statistical analyses were then performed to identify "
        "cancellation drivers, segment high-risk booking profiles, and quantify revenue impact. Results "
        "were presented through a dual-view Tableau dashboard — an executive summary view and an "
        "operational drill-down — to support both strategic and day-to-day decision-making."
    ))
    e.append(h2("Key Insights at a Glance"))
    e += kpi_row([("41%", "City Hotel Cancellation Rate"), ("27%", "Resort Hotel Cancel Rate"),
                  ("87,219", "Clean Records Analysed"), ("2015–17", "Data Time Span")])
    for ins in [
        "<b>City Hotel Vulnerability:</b> City Hotels experience a 41% cancellation rate versus 27% for Resort Hotels, demanding differentiated risk mitigation strategies.",
        "<b>Long Lead-Time Risk:</b> Bookings made more than 180 days ahead of arrival carry a disproportionately high cancellation probability, creating phantom demand.",
        "<b>Deposit Policy Impact:</b> 'No Deposit' bookings account for the overwhelming majority of cancellations; non-refundable deposits nearly eliminate cancellation risk.",
        "<b>Channel Risk:</b> Bookings via Travel Agents and Tour Operators (TA/TO) cancel significantly more often than direct bookings.",
    ]:
        e.append(bullet_item(ins))
    e.append(sp(8))
    e.append(h2("Priority Recommendations"))
    for rec in [
        "Mandate non-refundable deposit policies for all bookings with a lead time exceeding 180 days.",
        "Launch direct-channel loyalty incentives (e.g., complimentary breakfast, room upgrades) to reduce OTA dependency.",
        "Deploy dynamic pricing uplift during peak summer months (July–August) to maximise RevPAR during proven high-demand windows.",
    ]:
        e.append(bullet_item(rec))
    e.append(PageBreak())

    # ── 3. Sector & Business Context ─────────────────────────────────────
    e += section_header("3", "Sector & Business Context")
    e.append(h2("Overview of the Hospitality Industry"))
    e.append(body(
        "The global hospitality and travel sector operates at the intersection of consumer behaviour, "
        "macroeconomic cycles, and real-time pricing dynamics. Hotels must balance occupancy maximisation "
        "with rate optimisation — a challenge formally captured by Revenue Management (RM) disciplines. "
        "Key performance indicators such as Occupancy Rate, Average Daily Rate (ADR), and Revenue Per "
        "Available Room (RevPAR) are the fundamental levers through which profitability is managed. "
        "Accurate demand forecasting is, therefore, not merely a best practice but an operational necessity."
    ))
    e.append(body(
        "The rise of OTAs such as Booking.com and Expedia has democratised travel booking for consumers "
        "while simultaneously transferring significant market power away from individual properties. "
        "OTAs typically charge hotels commissions ranging from 15% to 25% per booking — and their "
        "consumer-friendly cancellation guarantees have created a culture of speculative booking, where "
        "guests hold multiple reservations and cancel surplus options close to the travel date."
    ))
    e.append(h2("Primary Decision-Makers"))
    e.append(body(
        "This analysis is designed to serve Hotel General Managers who are accountable for overall property "
        "profitability, Revenue Management Teams responsible for pricing and inventory allocation, and "
        "Marketing Directors seeking to optimise channel mix and customer acquisition costs."
    ))
    e.append(h2("Why Cancellations Were Chosen as the Focus"))
    e.append(body(
        "Cancellations represent direct, measurable revenue leakage. Unlike demand shortfalls — which "
        "require external market interventions — cancellation risk is partially within the hotel's "
        "control through pricing, deposit policy, and channel strategy. Identifying the behavioural and "
        "transactional signatures of likely cancellations provides an immediate lever to protect cash "
        "flow, without requiring capital investment."
    ))
    e.append(h2("Business Value of This Project"))
    e.append(body(
        "By enabling revenue managers to identify, segment, and act upon high-risk bookings in advance, "
        "StayWise delivers value across three dimensions: financial security through secured upfront "
        "deposits, operational efficiency through accurate demand forecasting, and strategic channel "
        "diversification by reducing reliance on high-commission, high-cancellation OTAs."
    ))
    e.append(PageBreak())

    # ── 4. Problem Statement & Objectives ────────────────────────────────
    e += section_header("4", "Problem Statement & Objectives")
    e.append(h2("Formal Problem Definition"))
    e.append(body(
        "What are the primary drivers of hotel booking cancellations, and how can pricing, deposit "
        "policies, and distribution-channel strategies be optimised to maximise net revenue per available "
        "room? More specifically: which combinations of booking attributes — such as lead time, deposit "
        "type, market segment, and hotel type — create the highest cancellation risk, and what targeted "
        "interventions can hotels implement to reduce that risk without sacrificing occupancy?"
    ))
    e.append(h2("Project Scope"))
    scope_data = [
        [Paragraph("<b>In Scope</b>", S["body_b"]), Paragraph("<b>Out of Scope</b>", S["body_b"])],
        [Paragraph("Historical hotel booking data (2015–2017) for City and Resort hotel types.", S["small"]),
         Paragraph("Real-time data streaming or live PMS integration.", S["small"])],
        [Paragraph("Analysis of lead times, customer demographics, deposit types, and distribution channels.", S["small"]),
         Paragraph("Macroeconomic indicators and external market data.", S["small"])],
        [Paragraph("Feature engineering to create business-relevant derived metrics (CLV proxy, total revenue).", S["small"]),
         Paragraph("Competitor pricing analysis and benchmarking.", S["small"])],
        [Paragraph("Interactive Tableau dashboard for executive and operational use.", S["small"]),
         Paragraph("Post-2020 travel behavioural shifts or pandemic-era adjustments.", S["small"])],
    ]
    scope_tbl = Table(scope_data, colWidths=[(W - 5*cm)/2 - 0.5*cm, (W - 5*cm)/2 - 0.5*cm])
    scope_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    e.append(scope_tbl)
    e.append(sp(10))
    e.append(h2("Success Criteria"))
    for sc in [
        "Delivery of a minimum of eight statistically supported, business-relevant insights.",
        "A functional Tableau dashboard accessible via Tableau Public, covering both executive and operational views.",
        "Concrete, prioritised recommendations with clearly articulated expected business impact.",
        "A reproducible Python ETL pipeline committed to the team GitHub repository.",
    ]:
        e.append(bullet_item(sc))
    e.append(PageBreak())

    # ── 5. Data Description ───────────────────────────────────────────────
    e += section_header("5", "Data Description")
    e.append(h2("Source & Access"))
    e.append(body(
        "The dataset used is the publicly available <b>Hotel Booking Demand Dataset</b>, originally "
        "published on Kaggle and sourced from real hotel property management systems (PMS) records "
        "in Portugal. The raw file (<i>hotel_bookings_Raw.csv</i>) was accessed directly via the "
        "Kaggle platform and committed to the project GitHub repository for reproducibility."
    ))
    e.append(h2("Data Structure"))
    e += kpi_row([("119,209", "Raw Rows"), ("87,219", "Processed Rows"), ("49", "Original Columns"), ("29", "Final Columns")])
    e.append(body(
        "The dataset spans arrivals from July 2015 through August 2017 across two property types: "
        "<b>City Hotel</b> and <b>Resort Hotel</b>. After cleaning and deduplication, 87,219 records "
        "were retained, representing a high-quality analytical corpus free of structural errors and "
        "extreme outliers."
    ))
    e.append(h2("Key Fields"))
    fields = [
        ("is_canceled", "Target variable. Binary flag: 1 if a booking was cancelled, 0 if it resulted in a stay."),
        ("lead_time", "Number of days elapsed between the booking date and the scheduled arrival date."),
        ("average_daily_rate (ADR)", "The mean revenue realised per occupied room per night, net of meals and other services."),
        ("market_segment", "Distribution channel classification, including Direct, Corporate, TA/TO (Travel Agent / Tour Operator), and Groups."),
        ("deposit_type", "Type of deposit collected: No Deposit, Non Refund, or Refundable."),
        ("hotel", "Property type: City Hotel or Resort Hotel."),
        ("arrival_date_month", "Month of planned arrival — used to derive seasonality features."),
        ("stays_in_weekend_nights", "Count of weekend nights (Saturday or Sunday) included in the stay."),
        ("stays_in_week_nights", "Count of week nights (Monday to Friday) included in the stay."),
        ("adults / children / babies", "Guest composition, used to compute total_guests and revenue_per_guest."),
        ("is_repeated_guest", "Binary flag identifying repeat customers — a key segment for loyalty analysis."),
        ("required_car_parking_spaces", "Number of car spaces requested — identified as a high-intent, low-risk signal."),
    ]
    field_data = [[Paragraph("<b>Field</b>", S["small"]), Paragraph("<b>Description</b>", S["small"])]] + \
                 [[Paragraph(f, ParagraphStyle("fc", parent=S["small"], fontName="Helvetica-Bold", textColor=MID_BLUE)),
                   Paragraph(d, S["small"])] for f, d in fields]
    field_tbl = Table(field_data, colWidths=[4.5*cm, W - 5*cm - 4.5*cm - 0.5*cm])
    field_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    e.append(field_tbl)
    e.append(sp(10))
    e.append(h2("Data Limitations & Known Biases"))
    for lim in [
        "The dataset covers 2015–2017 and does not reflect post-pandemic travel behavioural changes, including the rise of remote work-related travel and shifts in domestic versus international booking patterns.",
        "Missing values in the <i>agent</i> and <i>country</i> fields were imputed using neutral defaults (0 and 'Unknown', respectively), which may mask agent-level or geography-level variation.",
        "The <i>company</i> column was dropped entirely due to an extremely high proportion of null values, limiting corporate booking channel analysis.",
        "ADR values were capped at a maximum of 5,000 to handle erroneous data entries — genuine ultra-luxury properties may have legitimate rates above this threshold.",
    ]:
        e.append(bullet_item(lim))
    e.append(PageBreak())

    # ── 6. Data Cleaning & ETL Pipeline ──────────────────────────────────
    e += section_header("6", "Data Cleaning & ETL Pipeline")
    e.append(body(
        "All data extraction, transformation, and loading (ETL) operations were executed exclusively "
        "in Python, in compliance with the DVA Capstone 2 requirements. The pipeline is documented "
        "across two committed artefacts: <i>scripts/etl_pipeline.py</i> (the production-grade script) "
        "and <i>notebooks/02_cleaning.ipynb</i> (the annotated, step-by-step cleaning notebook)."
    ))
    e.append(h2("Missing Value Treatment"))
    mv_data = [
        [Paragraph("<b>Column</b>", S["small"]), Paragraph("<b>Issue</b>", S["small"]), Paragraph("<b>Treatment</b>", S["small"])],
        [Paragraph("company", S["small"]), Paragraph("94% null — not analytically viable", S["small"]), Paragraph("Column dropped entirely", S["small"])],
        [Paragraph("children", S["small"]), Paragraph("4 null records", S["small"]), Paragraph("Filled with 0 (no children assumed)", S["small"])],
        [Paragraph("country", S["small"]), Paragraph("488 null records", S["small"]), Paragraph("Filled with 'Unknown'", S["small"])],
        [Paragraph("agent", S["small"]), Paragraph("16,340 null records", S["small"]), Paragraph("Filled with 0 (no agent / direct booking assumed)", S["small"])],
    ]
    mv_tbl = Table(mv_data, colWidths=[3.5*cm, 6*cm, W - 5*cm - 3.5*cm - 6*cm - 1*cm])
    mv_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), MID_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    e.append(mv_tbl)
    e.append(sp(10))
    e.append(h2("Outlier Detection & Treatment"))
    e.append(body(
        "The <i>average_daily_rate</i> (ADR) column contained a small number of entries with "
        "negative or implausibly high values — likely the result of system errors or promotional "
        "corrections in the source PMS. These values were capped between 0 and 5,000 using a "
        "clip operation, preserving row-level data while eliminating distortions in revenue "
        "aggregations and distributional analyses."
    ))
    e.append(h2("Data Standardisation"))
    e.append(body(
        "All column names were normalised to lowercase <i>snake_case</i> format to ensure "
        "consistency across the Python and Tableau environments. Duplicate rows — defined as "
        "records identical across all 49 original columns — were identified and removed, "
        "reducing the dataset from 119,209 to 87,219 records. Data types were validated and "
        "cast appropriately (e.g., date fields, integer flags)."
    ))
    e.append(h2("Feature Engineering"))
    e.append(body(
        "Seven derived features were created to enrich the analytical dataset and support KPI "
        "computation:"
    ))
    fe_data = [
        [Paragraph("<b>Feature</b>", S["small"]), Paragraph("<b>Formula</b>", S["small"]), Paragraph("<b>Business Purpose</b>", S["small"])],
        [Paragraph("total_nights", S["small"]), Paragraph("weekend_nights + week_nights", S["small"]), Paragraph("Total duration of stay — basis for revenue calculation", S["small"])],
        [Paragraph("total_guests", S["small"]), Paragraph("adults + children + babies", S["small"]), Paragraph("Guest count per booking for per-capita analysis", S["small"])],
        [Paragraph("total_revenue", S["small"]), Paragraph("total_nights × ADR", S["small"]), Paragraph("Gross revenue contribution per booking", S["small"])],
        [Paragraph("revenue_per_guest", S["small"]), Paragraph("total_revenue / total_guests", S["small"]), Paragraph("Profitability measure across demographic segments", S["small"])],
        [Paragraph("season", S["small"]), Paragraph("Derived from arrival month", S["small"]), Paragraph("Seasonal demand segmentation (Summer / Winter / Spring / Autumn)", S["small"])],
        [Paragraph("is_peak_season", S["small"]), Paragraph("Flag: 1 if Summer, else 0", S["small"]), Paragraph("Binary indicator for peak demand periods", S["small"])],
        [Paragraph("clv_proxy", S["small"]), Paragraph("total_revenue × (1 − is_canceled)", S["small"]), Paragraph("Realised customer lifetime value estimate for a single stay", S["small"])],
    ]
    fe_tbl = Table(fe_data, colWidths=[3.5*cm, 5*cm, W - 5*cm - 3.5*cm - 5*cm - 1*cm])
    fe_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), MID_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    e.append(fe_tbl)
    e.append(PageBreak())

    # ── 7. KPI & Metric Framework ─────────────────────────────────────────
    e += section_header("7", "KPI & Metric Framework")
    e.append(body(
        "Four core KPIs were defined to align analytical outputs with business objectives. Each "
        "metric was computed within the Python notebooks and visualised in the Tableau dashboard."
    ))
    kpis_def = [
        ("Cancellation Rate %",
         "sum(is_canceled) / count(total_bookings) × 100",
         "Measures the severity of booking fall-throughs at property and segment levels. This is the "
         "primary headline metric, directly linked to revenue leakage. A rising cancellation rate "
         "triggers further investigation into lead time, deposit, and channel compositions."),
        ("Total Revenue",
         "(stays_in_weekend_nights + stays_in_week_nights) × average_daily_rate",
         "Measures gross financial value generated per booking period. Aggregated by month and "
         "season, this KPI underpins dynamic pricing decisions and seasonal staffing plans."),
        ("Revenue per Guest",
         "total_revenue / total_guests",
         "Evaluates the relative profitability of different customer segments. Family bookings "
         "(adults + children) generate notably higher Revenue per Guest than solo or couple travellers, "
         "informing targeted package and upsell strategies."),
        ("CLV Proxy",
         "total_revenue × (1 − is_canceled)",
         "Estimates the realised economic value of a booking, netting out the revenue lost to "
         "cancellations. This metric enables segment-level profitability ranking and prioritisation "
         "of retention efforts for high-CLV-proxy customer profiles."),
    ]
    for kpi_name, formula, explanation in kpis_def:
        kpi_box_data = [
            [Paragraph(kpi_name, ParagraphStyle("kn", parent=S["body_b"], textColor=WHITE, spaceAfter=0)),
             Paragraph(f"Formula: <i>{formula}</i>", ParagraphStyle("kf", parent=S["small"], textColor=MED_GRAY, spaceAfter=0))],
            [Paragraph(explanation, S["small"]), ""],
        ]
        kpi_box = Table(kpi_box_data, colWidths=[4.5*cm, W - 5*cm - 4.5*cm - 0.5*cm])
        kpi_box.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
            ("BACKGROUND", (0,1), (-1,-1), LIGHT_GRAY),
            ("SPAN", (0,1), (-1,1)),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
            ("BOX", (0,0), (-1,-1), 0.5, MID_BLUE),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        e.append(kpi_box)
        e.append(sp(8))
    e.append(PageBreak())

    # ── 8. EDA ───────────────────────────────────────────────────────────
    e += section_header("8", "Exploratory Data Analysis")
    e.append(body(
        "Exploratory Data Analysis was conducted across four analytical dimensions — trend, comparison, "
        "distribution, and correlation — to build a comprehensive picture of the booking data landscape. "
        "All charts and outputs are committed to <i>notebooks/03_eda.ipynb</i>."
    ))

    e.append(h2("Trend Analysis — Booking & Revenue Seasonality"))
    e.append(body(
        "Monthly aggregation of bookings and total revenue reveals a clear and consistent seasonal "
        "pattern across both 2016 and 2017. Booking volumes surge in July and August — the European "
        "summer holiday window — reaching their annual peak. This concentration of demand creates "
        "significant operational pressure: rooms that go unoccupied during this period due to "
        "cancellations represent disproportionately high revenue losses, as ADRs are also elevated "
        "during peak season. Conversely, January and February exhibit the lowest booking volumes, "
        "suggesting an opportunity for off-peak promotional pricing to maintain occupancy floors."
    ))

    e.append(h2("Comparison Analysis — City vs. Resort Hotels"))
    e.append(body(
        "City Hotels account for the majority of total bookings in the dataset but suffer a "
        "significantly higher cancellation rate of 41%, compared to 27% for Resort Hotels. This "
        "divergence is likely driven by the nature of city hotel demand: a higher proportion of "
        "corporate and short-notice leisure bookings made through OTA channels, where cancellation "
        "is frictionless. Resort Hotels attract a higher proportion of family and leisure bookings "
        "planned well in advance, with greater emotional and financial commitment to the trip."
    ))
    e.append(body(
        "Family bookings — identified by the presence of children in the guest composition — "
        "demonstrate meaningfully longer average stays and higher total revenue per booking compared "
        "to solo or couple travellers. This segment also exhibits a lower cancellation propensity, "
        "making it a high-value, lower-risk customer profile."
    ))

    e.append(h2("Distribution Analysis — Lead Time"))
    e.append(body(
        "The lead time distribution exhibits a characteristic long-tail shape: the majority of "
        "bookings (approximately 60%) are made within 60 days of the planned arrival date, where "
        "cancellation rates are relatively low. However, a significant tail of bookings extends "
        "beyond 180 days. Analysis confirms that these far-out bookings carry a materially higher "
        "cancellation probability — consistent with speculative reservation behaviour, where guests "
        "hold reservations as placeholders with low perceived commitment. This tail segment represents "
        "the primary target for deposit policy interventions."
    ))

    e.append(h2("Correlation Analysis — Key Relationships"))
    corr_data = [
        [Paragraph("<b>Variable Pair</b>", S["small"]), Paragraph("<b>Relationship</b>", S["small"]), Paragraph("<b>Business Implication</b>", S["small"])],
        [Paragraph("Non Refund Deposit × is_canceled", S["small"]), Paragraph("Strong negative", S["small"]), Paragraph("Non-refundable deposits near-eliminate cancellations", S["small"])],
        [Paragraph("lead_time × is_canceled", S["small"]), Paragraph("Positive", S["small"]), Paragraph("Longer lead times predict higher cancellation risk", S["small"])],
        [Paragraph("TA/TO channel × is_canceled", S["small"]), Paragraph("Positive", S["small"]), Paragraph("OTA bookings cancel more frequently than direct", S["small"])],
        [Paragraph("is_repeated_guest × is_canceled", S["small"]), Paragraph("Strong negative", S["small"]), Paragraph("Loyal repeat guests rarely cancel", S["small"])],
        [Paragraph("parking_spaces × is_canceled", S["small"]), Paragraph("Negative", S["small"]), Paragraph("Parking requests signal high arrival intent", S["small"])],
    ]
    corr_tbl = Table(corr_data, colWidths=[5*cm, 3*cm, W - 5*cm - 5*cm - 3*cm - 1*cm])
    corr_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), MID_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    e.append(corr_tbl)
    e.append(PageBreak())

    # ── 9. Statistical Analysis ───────────────────────────────────────────
    e += section_header("9", "Statistical Analysis")
    e.append(body(
        "Statistical methods were applied to move beyond descriptive observations and validate "
        "findings with inferential rigour. All analyses are committed to <i>notebooks/04_statistical_analysis.ipynb</i>."
    ))
    e.append(h2("Hypothesis Testing — Lead Time & Cancellation"))
    e.append(body(
        "An independent samples t-test was conducted comparing the mean lead time of cancelled "
        "bookings against fulfilled bookings. The results confirmed a statistically significant "
        "difference at the p &lt; 0.001 level: cancelled bookings had a substantially higher mean "
        "lead time than fulfilled ones. This validates the lead time–cancellation relationship "
        "observed in EDA and supports the recommendation to apply stricter deposit policies "
        "specifically to bookings made more than 180 days in advance."
    ))
    e.append(h2("Market Segment Segmentation"))
    e.append(body(
        "Bookings were segmented by market channel (Direct, Corporate, TA/TO, Groups, Others) "
        "and cancellation rates computed per segment. TA/TO bookings exhibited the highest "
        "cancellation rate across all segments, confirming OTA dependency as a systemic risk. "
        "Direct bookings demonstrated the lowest cancellation rate, reinforcing the business "
        "case for direct-channel incentive programmes. Corporate bookings fell in between, "
        "reflecting the relative stability of managed travel arrangements."
    ))
    e.append(h2("Repeat vs. First-Time Guest Behaviour"))
    e.append(body(
        "Repeat guests — identified by the <i>is_repeated_guest</i> flag — exhibit dramatically "
        "lower cancellation rates than first-time bookers. This behavioural distinction underscores "
        "the value of loyalty programme investment: not only do repeat guests cancel less frequently, "
        "they also tend to book through direct channels, bypassing OTA commission fees entirely. "
        "This dual financial benefit makes repeat guest conversion a high-priority strategic objective."
    ))
    e.append(h2("High-Risk Booking Profile — Risk Compound Analysis"))
    e.append(body(
        "A compound risk analysis identified the highest-risk booking profile as the combination "
        "of: City Hotel + No Deposit + TA/TO Channel + Lead Time &gt; 180 days. Bookings matching "
        "all four criteria exhibited cancellation rates substantially above the overall dataset average. "
        "This profile represents a priority target for policy intervention — either through mandatory "
        "deposit collection, dedicated revenue manager review, or dynamic pricing adjustments."
    ))

    # Risk profile box
    risk_data = [[
        Paragraph("HIGH-RISK PROFILE", ParagraphStyle("rp", parent=S["body_b"], textColor=WHITE, spaceAfter=0, fontSize=9)),
        Paragraph("City Hotel  +  No Deposit  +  TA/TO Channel  +  Lead Time &gt; 180 days",
                  ParagraphStyle("rv", parent=S["body_b"], textColor=colors.HexColor("#FADBD8"), spaceAfter=0, fontSize=10))
    ]]
    risk_box = Table(risk_data, colWidths=[3.5*cm, W - 5*cm - 3.5*cm - 0.5*cm])
    risk_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT_RED),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    e.append(sp(6))
    e.append(risk_box)
    e.append(PageBreak())

    # ── 10. Tableau Dashboard Design ─────────────────────────────────────
    e += section_header("10", "Tableau Dashboard Design")
    e.append(body(
        "Two interactive Tableau dashboards were designed and published to Tableau Public to provide "
        "revenue managers with real-time analytical access to the project's core findings. The dashboards "
        "are structured into an Executive View and an Operational Drill-Down View, serving different "
        "decision-making timeframes and user personas."
    ))
    e.append(h2("Dashboard 1 — Executive Summary View"))
    e.append(body(
        "Dashboard 1 provides a high-level overview of operational health across the full dataset "
        "period. Key headline metrics — total bookings, overall cancellation rate, total realised "
        "revenue, and CLV proxy — are displayed as large-format KPI tiles for at-a-glance "
        "performance assessment. Trend line charts show monthly booking volumes and revenue "
        "trajectories for City and Resort Hotels side by side, enabling rapid seasonal pattern "
        "recognition. This view is designed for General Managers and senior leadership who need "
        "a performance pulse without drill-down complexity."
    ))
    e.append(body(
        "<b>Tableau Public URL:</b> https://public.tableau.com/app/profile/soumen.dass/viz/StayWise-new1/StayWise-1"
    ))
    e.append(h2("Dashboard 2 — Operational Drill-Down View"))
    e.append(body(
        "Dashboard 2 enables Revenue Management Teams to interrogate the data at a granular level. "
        "Bar charts and heat maps visualise cancellation rates broken down by lead time bucket, "
        "deposit type, and market segment. A dedicated section highlights the risk profile matrix "
        "combining hotel type, channel, and deposit type to surface the highest-risk booking "
        "combinations. Scatter plots explore the relationship between lead time and ADR, informing "
        "dynamic pricing decisions."
    ))
    e.append(body(
        "<b>Tableau Public URL:</b> https://public.tableau.com/app/profile/soumen.dass/viz/StayWise-new2/StayWise-2"
    ))
    e.append(h2("Interactive Filters"))
    for filt in [
        "<b>Hotel Type:</b> Toggle between City Hotel and Resort Hotel views.",
        "<b>Year / Month:</b> Slice data by specific time periods to identify seasonal trends.",
        "<b>Market Segment:</b> Filter by Direct, TA/TO, Corporate, Groups, and other channels.",
        "<b>Customer Type:</b> Distinguish between Transient, Contract, Group, and Transient-Party bookings.",
        "<b>Deposit Type:</b> Isolate the impact of No Deposit, Non Refund, and Refundable policies.",
    ]:
        e.append(bullet_item(filt))
    e.append(sp(6))
    e.append(body(
        "All dashboard screenshots are committed to the project repository under <i>tableau/screenshots/</i> "
        "and links are documented in <i>tableau/dashboard_links.md</i>."
    ))
    e.append(PageBreak())

    # ── 11. Insights Summary ─────────────────────────────────────────────
    e += section_header("11", "Insights Summary")
    e.append(body(
        "The following eight insights represent the most decision-relevant findings from the combined "
        "EDA and statistical analyses. Each is framed in operational language to directly inform "
        "managerial action."
    ))

    insights = [
        ("1", "City vs. Resort Vulnerability",
         "City Hotels cancel at 41% versus 27% for Resort Hotels. This structural gap demands "
         "separate overbooking buffers, deposit policies, and revenue management playbooks for "
         "each property type. A single unified policy will systematically over-protect or "
         "under-protect one type."),
        ("2", "The Long Lead-Time Trap",
         "Bookings made more than 180 days in advance exhibit a disproportionately high "
         "cancellation rate. These bookings create phantom demand that distorts occupancy "
         "forecasts and can trigger unnecessary capacity holds. They should be treated as "
         "tentative until deposit-secured."),
        ("3", "Third-Party Channel Risk",
         "TA/TO (OTA) bookings cancel at significantly higher rates than direct bookings. "
         "Each OTA-sourced booking carries both a commission cost and a higher cancellation "
         "probability — a dual margin hit that materially reduces net revenue per booking."),
        ("4", "Summer Peak Dynamics",
         "July and August represent the annual peak in both booking volume and ADR. Revenue "
         "lost to cancellations during this window is effectively irreplaceable within the "
         "same season. Protecting peak-season inventory through deposit policies is the "
         "highest-impact single lever available."),
        ("5", "Deposit Policy as the Primary Control Variable",
         "'No Deposit' bookings account for the overwhelming majority of total cancellations. "
         "Non-refundable deposit bookings exhibit near-zero cancellation rates. Deposit type "
         "is the single strongest controllable predictor of whether a booking will materialise."),
        ("6", "Family Segment Profitability",
         "Bookings with children generate longer average stays and higher total revenue per "
         "booking than adult-only reservations. Families also demonstrate lower cancellation "
         "rates, making them the most financially attractive segment to actively court "
         "through targeted packages."),
        ("7", "Loyalty as a Revenue Stabiliser",
         "Repeat guests have a dramatically lower cancellation rate than first-time bookers "
         "and preferentially use direct channels. Growing the repeat guest base simultaneously "
         "reduces cancellation exposure and cuts OTA commission costs — a compounding benefit "
         "that makes CRM investment highly accretive."),
        ("8", "The Parking Space Signal",
         "Guests who request car parking spaces at the time of booking are highly unlikely to "
         "cancel. This behavioural marker identifies a high-intent, low-risk guest segment. "
         "Bundling parking into premium room rates can selectively attract this segment while "
         "generating auxiliary revenue."),
    ]

    for num, title, text in insights:
        ins_data = [
            [Paragraph(num, ParagraphStyle("in", parent=S["body_b"], fontSize=14, textColor=WHITE, spaceAfter=0, alignment=TA_CENTER)),
             Paragraph(title, ParagraphStyle("it", parent=S["body_b"], textColor=DARK_BLUE, spaceAfter=0))],
            ["", Paragraph(text, ParagraphStyle("ib", parent=S["small"], spaceAfter=0))],
        ]
        ins_tbl = Table(ins_data, colWidths=[1*cm, W - 5*cm - 1*cm - 0.5*cm])
        ins_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,0), MID_BLUE),
            ("BACKGROUND", (1,0), (1,0), LIGHT_GRAY),
            ("BACKGROUND", (0,1), (-1,1), WHITE),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING", (0,0), (0,-1), 4),
            ("LEFTPADDING", (1,0), (1,-1), 10),
            ("VALIGN", (0,0), (0,-1), "MIDDLE"),
            ("VALIGN", (1,0), (1,-1), "TOP"),
            ("BOX", (0,0), (-1,-1), 0.5, MED_GRAY),
            ("LINEBELOW", (0,0), (-1,0), 0.5, MED_GRAY),
        ]))
        e.append(ins_tbl)
        e.append(sp(6))
    e.append(PageBreak())

    # ── 12. Recommendations ───────────────────────────────────────────────
    e += section_header("12", "Recommendations")
    e.append(body(
        "The following four recommendations are prioritised by expected business impact and "
        "implementation feasibility. Each is directly traceable to a specific analytical finding."
    ))

    recs = [
        ("1", ACCENT_RED, "Targeted Non-Refundable Deposit Policies",
         "Insight: Bookings with lead times exceeding 180 days and no deposit cancel at the highest rates.",
         "Action: Implement mandatory non-refundable or partially non-refundable deposit requirements "
         "for all reservations with a booking-to-arrival gap exceeding 180 days. Apply this policy "
         "across both the hotel's direct website and its OTA extranet configurations. Offer a "
         "small rate incentive (3–5% discount) for guests who opt into non-refundable terms proactively.",
         "Impact: Converts speculative bookings into committed revenue, secures early cash flow, and "
         "reduces phantom demand that distorts occupancy forecasting. Feasible within 2–4 weeks "
         "via OTA extranet and CMS policy updates."),
        ("2", MID_BLUE, "Incentivise Direct Booking Channels",
         "Insight: Direct bookings cancel significantly less often than OTA bookings and carry no "
         "commission costs.",
         "Action: Launch a 'Book Direct Advantage' programme offering exclusive benefits — such as "
         "complimentary breakfast, room category upgrades, flexible late check-out, or guaranteed "
         "parking — available only to guests who book through the hotel's own website or call centre. "
         "Promote this programme through email remarketing to past guests and on-property collateral.",
         "Impact: Reduces OTA commission expenditure (typically 15–25% of room revenue), decreases "
         "cancellation rate, and builds a proprietary guest database for future CRM activity. "
         "Direct bookings grow the repeat guest base — the hotel's most reliable revenue segment."),
        ("3", DARK_BLUE, "Dynamic Peak-Season Pricing & Staffing",
         "Insight: July and August drive peak booking volumes and ADR — and revenue lost to "
         "cancellations during this window cannot be recovered.",
         "Action: Implement a dynamic pricing model that applies a progressive rate premium during "
         "the summer peak season, combined with reduced cancellation flexibility (shorter free "
         "cancellation windows). Pair pricing strategy with proactive operational staffing increases "
         "to meet the confirmed demand — not the gross demand inflated by expected cancellations.",
         "Impact: Maximises RevPAR during the highest-value revenue window. Accurate demand "
         "forecasting (accounting for expected cancellations) prevents both understaffing and "
         "the service failures that damage peak-season guest satisfaction scores."),
        ("4", colors.HexColor("#117A65"), "Bundle Premium Services for High-Intent Guests",
         "Insight: Guests requesting parking spaces at booking are a high-intent, low-risk segment.",
         "Action: Create a 'Drive &amp; Stay' premium package that bundles guaranteed parking with "
         "an upgraded room rate and select F&amp;B credits. Target this package to guests who "
         "indicate car travel in the booking flow, and feature it prominently on the direct "
         "booking website.",
         "Impact: Attracts and secures a demonstrably low-risk customer segment, increases "
         "average booking value through auxiliary revenue attachment, and differentiates the "
         "property's direct channel value proposition versus OTAs."),
    ]

    for num, col, title, insight, action, impact in recs:
        rec_data = [
            [Paragraph(f"#{num}", ParagraphStyle("rn", parent=S["body_b"], fontSize=16, textColor=WHITE, spaceAfter=0, alignment=TA_CENTER)),
             Paragraph(title, ParagraphStyle("rt", parent=S["body_b"], textColor=WHITE, spaceAfter=0, fontSize=12))],
            [Paragraph("INSIGHT", ParagraphStyle("rl", parent=S["small"], textColor=col, fontName="Helvetica-Bold", fontSize=8, spaceAfter=0)),
             Paragraph(insight, S["small"])],
            [Paragraph("ACTION", ParagraphStyle("al", parent=S["small"], textColor=col, fontName="Helvetica-Bold", fontSize=8, spaceAfter=0)),
             Paragraph(action, S["small"])],
            [Paragraph("IMPACT", ParagraphStyle("il", parent=S["small"], textColor=col, fontName="Helvetica-Bold", fontSize=8, spaceAfter=0)),
             Paragraph(impact, S["small"])],
        ]
        rec_tbl = Table(rec_data, colWidths=[1.3*cm, W - 5*cm - 1.3*cm - 0.5*cm])
        rec_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), col),
            ("BACKGROUND", (0,1), (-1,-1), LIGHT_GRAY),
            ("SPAN", (1,0), (1,0)),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LEFTPADDING", (0,0), (0,-1), 6),
            ("LEFTPADDING", (1,0), (1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("VALIGN", (0,0), (0,0), "MIDDLE"),
            ("BOX", (0,0), (-1,-1), 0.5, MED_GRAY),
            ("LINEBELOW", (0,0), (-1,0), 0, WHITE),
            ("LINEBELOW", (0,1), (-1,-2), 0.3, MED_GRAY),
        ]))
        e.append(rec_tbl)
        e.append(sp(10))
    e.append(PageBreak())

    # ── 13. Impact Estimation ─────────────────────────────────────────────
    e += section_header("13", "Impact Estimation")
    e.append(body(
        "While precise revenue projections require property-specific financial data beyond the "
        "scope of this dataset, the following estimates are grounded in the analytical findings "
        "and represent directionally sound approximations using conservative assumptions."
    ))
    e.append(h2("Revenue Protection — Deposit Policy Conversion"))
    e.append(body(
        "The dataset contains a substantial volume of 'No Deposit' bookings in the high-risk "
        "lead time bracket (>180 days). If a policy change converts even 10% of these bookings "
        "from 'No Deposit' to 'Non Refund' status, and given that non-refundable deposits "
        "reduce cancellations to near-zero in this segment, the corresponding revenue protection "
        "effect — at average dataset ADR levels — would be material. Each prevented cancellation "
        "eliminates both the direct lost room revenue and the associated operational cost of "
        "attempting to fill a last-minute vacancy. The policy change itself carries near-zero "
        "implementation cost, making the return profile exceptionally attractive."
    ))
    e.append(h2("Efficiency Gains — Operational Forecasting Accuracy"))
    e.append(body(
        "By filtering phantom demand (high-probability cancellation bookings) from gross booking "
        "counts, hotels can produce more accurate 30-, 60-, and 90-day demand forecasts. This "
        "translates directly into optimised staffing levels — reducing overtime expenditure during "
        "predicted peak periods and avoiding service-quality failures from understaffing. "
        "Accurate forecasting also enables procurement (food, beverages, amenities) to be "
        "calibrated to true expected occupancy, reducing waste."
    ))
    e.append(h2("Strategic Channel Shift — OTA Commission Savings"))
    e.append(body(
        "OTAs typically charge commissions of 15–25% on gross room revenue. Each percentage "
        "point of bookings shifted from OTA to direct channels improves net room revenue "
        "accordingly. The direct channel investment required — a loyalty programme, direct "
        "booking incentives, and website optimisation — typically yields a positive ROI within "
        "the first operating year at properties with meaningful booking volumes."
    ))
    e.append(h2("Urgency — Why Act Now?"))
    e.append(body(
        "The trend of OTA-facilitated frictionless cancellation is accelerating, not abating. "
        "Consumer expectations for no-penalty cancellation are increasingly normalised. Hotels "
        "that delay implementing protective deposit and direct-channel policies will find "
        "their competitive position eroding as OTA commission rates and cancellation volumes "
        "continue to increase. The data-supported interventions identified in this project "
        "are implementable within weeks — the opportunity cost of inaction is real and "
        "compounding with each booking cycle."
    ))
    e.append(PageBreak())

    # ── 14. Limitations ───────────────────────────────────────────────────
    e += section_header("14", "Limitations")
    for lim in [
        ("<b>Temporal Data Gap:</b>", "The dataset covers 2015–2017. Post-pandemic travel behaviour — "
         "including the rise of bleisure (business + leisure) travel, remote-work-driven extended stays, "
         "and post-COVID domestic travel surges — is not captured. Conclusions should be re-validated "
         "against current PMS data before policy implementation."),
        ("<b>Geography Constraints:</b>", "The source data originates from hotels in Portugal. "
         "Behavioural patterns (seasonality, OTA dependency, family travel prevalence) may differ "
         "significantly in other markets, limiting direct transferability of quantitative thresholds."),
        ("<b>CLV Proxy Limitations:</b>", "The Customer Lifetime Value proxy is computed solely from "
         "single-visit revenue. True CLV requires multi-year individual-level tracking across multiple "
         "stays — data that is not available in this dataset. The proxy underestimates the true value "
         "of repeat guests."),
        ("<b>Missing Competitor Context:</b>", "The analysis does not incorporate competitor pricing, "
         "local event calendars, or macroeconomic indicators. ADR and demand decisions made without "
         "this context may be locally suboptimal even if analytically sound in isolation."),
        ("<b>Imputation Assumptions:</b>", "Neutral imputation for <i>agent</i> (set to 0) and "
         "<i>country</i> (set to 'Unknown') masks potentially meaningful variation in these dimensions. "
         "A more sophisticated imputation approach (e.g., mode imputation by segment) would yield "
         "more precise agent-level and geography-level analysis."),
    ]:
        lim_data = [[Paragraph(lim[0], ParagraphStyle("ll", parent=S["body_b"], textColor=MID_BLUE, spaceAfter=0)),
                     Paragraph(lim[1], S["small"])]]
        lim_tbl = Table(lim_data, colWidths=[4.5*cm, W - 5*cm - 4.5*cm - 0.5*cm])
        lim_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), LIGHT_GRAY),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("BOX", (0,0), (-1,-1), 0.3, MED_GRAY),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        e.append(lim_tbl)
        e.append(sp(6))
    e.append(PageBreak())

    # ── 15. Future Scope ─────────────────────────────────────────────────
    e += section_header("15", "Future Scope")
    e.append(body(
        "StayWise establishes a robust analytical foundation that is well-positioned for "
        "expansion into predictive and real-time intelligence capabilities."
    ))
    e.append(h2("Machine Learning — Cancellation Probability Scoring"))
    e.append(body(
        "The binary classification nature of the <i>is_canceled</i> target variable makes this "
        "dataset an ideal candidate for supervised ML modelling. A Random Forest or XGBoost "
        "classifier, trained on the engineered feature set, could generate a real-time "
        "'Cancellation Probability Score' at the point of booking. This score could be "
        "surfaced within the PMS to trigger automated policy responses — for example, "
        "requiring a deposit for bookings scoring above a defined threshold — without "
        "requiring manual revenue manager intervention for every reservation."
    ))
    e.append(h2("External Data Integration"))
    e.append(body(
        "Incorporating external datasets — local event calendars, regional flight search "
        "volume, competitor pricing from OTA APIs, and macroeconomic indicators such as "
        "consumer confidence indices — would substantially improve the predictive power of "
        "both cancellation models and dynamic pricing algorithms. These integrations would "
        "transform StayWise from a historical analytics tool into a forward-looking "
        "revenue intelligence platform."
    ))
    e.append(h2("Real-Time Dashboard & PMS Integration"))
    e.append(body(
        "Connecting the Tableau dashboard to a live PMS data feed via an API or scheduled "
        "ETL pipeline would enable true real-time operational monitoring. Revenue managers "
        "could track intraday cancellation rates, monitor pacing versus budget, and trigger "
        "dynamic pricing adjustments automatically. This evolution from static historical "
        "analysis to live operational intelligence represents the highest-value application "
        "of the analytical framework developed in this project."
    ))
    e.append(PageBreak())

    # ── 16. Conclusion ────────────────────────────────────────────────────
    e += section_header("16", "Conclusion")
    e.append(body(
        "The StayWise project demonstrates that rigorous data analysis of historical hotel booking "
        "records can yield commercially significant, immediately actionable intelligence — even from "
        "a dataset spanning just two years. Through a structured Python ETL pipeline and a dual-view "
        "Tableau dashboard, the team surfaced a clear and consistent finding: lenient deposit policies "
        "and long booking lead times are the primary structural drivers of cancellation-driven revenue "
        "loss, amplified by over-reliance on OTA distribution channels."
    ))
    e.append(body(
        "The data confirms that City Hotels are disproportionately exposed to this risk at a 41% "
        "cancellation rate, while non-refundable deposit policies and direct booking channels offer "
        "the most powerful and immediately implementable corrective levers available. The business "
        "case for action is compelling: the interventions required are low-cost and operationally "
        "straightforward, the financial upside is material, and the competitive cost of inaction "
        "grows with every booking cycle in an increasingly OTA-dominated marketplace."
    ))
    e.append(body(
        "By investing in data-driven revenue management today — beginning with targeted deposit "
        "policy reform and direct-channel incentive programmes — hotel operators can convert "
        "analytical insight into secured revenue, stronger guest relationships, and a more "
        "resilient business model for the challenges of tomorrow's hospitality landscape."
    ))

    # Closing accent
    e.append(sp(16))
    closing_data = [["StayWise: Hotel Booking Analytics — Section B, G-1 | Newton School of Technology"]]
    closing = Table(closing_data, colWidths=[W - 5*cm])
    closing.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,-1), WHITE),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    e.append(closing)
    e.append(PageBreak())

    # ── 17. Appendix ─────────────────────────────────────────────────────
    e += section_header("17", "Appendix")
    e.append(body(
        "The following artefacts are committed to the project GitHub repository and form "
        "the complete technical record of this project."
    ))
    app_data = [
        [Paragraph("<b>Artefact</b>", S["small"]), Paragraph("<b>Path</b>", S["small"]), Paragraph("<b>Description</b>", S["small"])],
        [Paragraph("Data Dictionary", S["small"]), Paragraph("docs/data_dictionary.md", ParagraphStyle("code", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("Full column-level definitions for all 49 original and 29 processed fields.", S["small"])],
        [Paragraph("ETL Pipeline", S["small"]), Paragraph("scripts/etl_pipeline.py", ParagraphStyle("code2", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("Production-grade Python script for end-to-end data extraction, cleaning, and feature engineering.", S["small"])],
        [Paragraph("Cleaning Notebook", S["small"]), Paragraph("notebooks/02_cleaning.ipynb", ParagraphStyle("code3", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("Annotated step-by-step cleaning log with data quality checks and transformation rationale.", S["small"])],
        [Paragraph("EDA Notebook", S["small"]), Paragraph("notebooks/03_eda.ipynb", ParagraphStyle("code4", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("Full exploratory analysis with all charts, distribution plots, and correlation outputs.", S["small"])],
        [Paragraph("Statistical Analysis", S["small"]), Paragraph("notebooks/04_statistical_analysis.ipynb", ParagraphStyle("code5", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("Hypothesis testing results, segmentation analysis, and risk profile computations.", S["small"])],
        [Paragraph("Tableau Screenshots", S["small"]), Paragraph("tableau/screenshots/", ParagraphStyle("code6", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("PNG exports of all dashboard views, including filter states.", S["small"])],
        [Paragraph("Dashboard Links", S["small"]), Paragraph("tableau/dashboard_links.md", ParagraphStyle("code7", parent=S["small"], fontName="Courier", fontSize=8)),
         Paragraph("Tableau Public URLs for Dashboard 1 and Dashboard 2.", S["small"])],
    ]
    app_tbl = Table(app_data, colWidths=[3*cm, 5.5*cm, W - 5*cm - 3*cm - 5.5*cm - 1*cm])
    app_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    e.append(app_tbl)
    e.append(PageBreak())

    # ── 18. Contribution Matrix ───────────────────────────────────────────
    e += section_header("18", "Contribution Matrix")
    e.append(body(
        "The following matrix documents each team member's contribution across all project phases. "
        "Ownership designations are verifiable through GitHub Insights, pull request history, "
        "and submitted artefacts."
    ))

    members_roles = [
        "Deepak Mishra", "Ganga Raghuwanshi", "Kunal Dev Sahu",
        "Lakshay Yadav", "Musthyala Sadhvik", "Sarthak Mishra", "Soumen Dass"
    ]
    col_labels = ["Dataset &\nSourceing", "ETL &\nCleaning", "EDA &\nAnalysis",
                  "Statistical\nAnalysis", "Tableau\nDashboard", "Report\nWriting", "PPT &\nViva"]

    header_row = [Paragraph("<b>Team Member</b>", ParagraphStyle("ch", parent=S["small"], textColor=WHITE, fontName="Helvetica-Bold", fontSize=8))] + \
                 [Paragraph(f"<b>{c}</b>", ParagraphStyle("ch2", parent=S["small"], textColor=WHITE, fontName="Helvetica-Bold", fontSize=7.5, alignment=TA_CENTER)) for c in col_labels]

    contrib_data = [header_row]
    for i, member in enumerate(members_roles):
        row = [Paragraph(member, ParagraphStyle("mn", parent=S["small"], fontName="Helvetica-Bold" if i == 5 else "Helvetica"))]
        for _ in col_labels:
            row.append(Paragraph("Owner /\nSupport", ParagraphStyle("ov", parent=S["small"], alignment=TA_CENTER, fontSize=8)))
        contrib_data.append(row)

    col_w = (W - 5*cm) / 8
    contrib_tbl = Table(contrib_data, colWidths=[col_w * 1.8] + [col_w * 0.886] * 7)
    contrib_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GRAY),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("ALIGN", (1,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    e.append(contrib_tbl)
    e.append(sp(20))
    e.append(body(
        "<i>Declaration: We confirm that the above contribution details are accurate and verifiable "
        "through GitHub Insights, pull request history, and submitted project artefacts.</i>"
    ))
    e.append(sp(30))
    e.append(Paragraph("Team Lead Signature: _____________________________________     Date: _______________",
                        S["small"]))
    return e

# ── Build ────────────────────────────────────────────────────────────────────
story = build_story()
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF created: {OUTPUT_PATH}")

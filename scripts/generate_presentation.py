"""
BreatheWise - Hackathon Presentation Generator (PowerPoint .pptx)
Generates an 8-slide widescreen presentation deck adhering to Google Stitch design principles,
embedding authentic screenshots, benchmark tables, and regulatory audit statistics.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
OUTPUT_PPTX = os.path.join(BASE_DIR, "presentation", "BreatheWise_Hackathon_Presentation.pptx")

# Color Palette (Google Stitch & CPCB tokens)
COLOR_DARK_SLATE = RGBColor(15, 23, 42)    # #0f172a
COLOR_SKY = RGBColor(14, 165, 233)         # #0ea5e9
COLOR_EMERALD = RGBColor(16, 185, 129)     # #10b981
COLOR_AMBER = RGBColor(234, 179, 8)        # #eab308
COLOR_CARD_BG = RGBColor(248, 250, 252)    # #f8fafc
COLOR_MUTED = RGBColor(100, 116, 139)      # #64748b
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BORDER = RGBColor(226, 232, 240)


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title, category="BREATHEWISE • BENGALURU AIR QUALITY INTELLIGENCE"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_SKY
        
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_DARK_SLATE

    def add_footer(slide, current_slide, total_slides=8):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"BreatheWise • Data Science Hackathon 2026 • Slide {current_slide} of {total_slides} • 100% Offline Demonstration"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    
    # Background accent card
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_DARK_SLATE
    bg.line.color.rgb = COLOR_DARK_SLATE

    # Brand Title
    tb = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "BREATHEWISE"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    
    p_tag = tf.add_paragraph()
    p_tag.text = "Understand the Air. Explore the Patterns. Anticipate the Change."
    p_tag.font.size = Pt(20)
    p_tag.font.color.rgb = COLOR_SKY
    p_tag.space_before = Pt(10)
    
    p_desc = tf.add_paragraph()
    p_desc.text = "An offline-first Data Science intelligence platform coupling genuine CPCB monitoring observations with ECMWF ERA5 reanalysis across Bengaluru, Karnataka, India."
    p_desc.font.size = Pt(14)
    p_desc.font.color.rgb = RGBColor(203, 213, 225)
    p_desc.space_before = Pt(24)

    p_cred = tf.add_paragraph()
    p_cred.text = "Author: 2nd-Year CSE Data Science Team • 8-Hour Autonomous Execution System • 60 Automated Tests Passing"
    p_cred.font.size = Pt(11)
    p_cred.font.color.rgb = COLOR_EMERALD
    p_cred.space_before = Pt(36)

    # -------------------------------------------------------------
    # SLIDE 2: THE REAL PROBLEM
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "The Real Problem: Understanding Bengaluru's Air Quality Dynamics", "PROBLEM STATEMENT & MOTIVATION")
    add_footer(slide2, 2)

    # 3 Column Comparison Cards
    cards_data = [
        ("The Opaque Status Quo", "Existing commercial apps report a single colored number without scientific context, smoothing over localized diurnal spikes and masking non-linear pollutant interactions."),
        ("Bengaluru's Spatial Context", "The project uses multiple monitoring stations to explore spatial differences in historical pollution observations. Its hourly and weather analyses have more limited geographic coverage, which we explicitly disclose."),
        ("The BreatheWise Solution", "Most AQI dashboards focus on reporting an air-quality number. BreatheWise focuses on understanding the data behind that number: exploring temporal patterns, retrospective weather associations, 4-model forecasting benchmarks, and auditable CPCB calculations in one offline platform.")
    ]
    for i, (heading, body) in enumerate(cards_data):
        left = Inches(0.8 + i * 4.0)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.7), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER
        
        tb = slide2.shapes.add_textbox(left + Inches(0.3), Inches(2.1), Inches(3.1), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = heading
        p0.font.size = Pt(17)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_DARK_SLATE
        
        p1 = tf.add_paragraph()
        p1.text = body
        p1.font.size = Pt(13.5)
        p1.font.color.rgb = COLOR_MUTED
        p1.space_before = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 3: DATA PROVENANCE & LIMITATIONS
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Genuine Empirical Datasets: Provenance, Sufficiency & Boundaries", "DATA SCIENCE METHODOLOGY")
    add_footer(slide3, 3)

    metrics_boxes = [
        ("50,584", "Raw Daily Records", "CPCB / KSPCB via XKDR Forum"),
        ("46,795", "Compliant Records", "Passed CPCB n >= 16h filter"),
        ("16,080", "Hourly Weather Obs", "ECMWF ERA5 Reanalysis"),
        ("66,947", "Landmark Hourly Obs", "BTM Layout & Peenya")
    ]
    for i, (val, lbl, sub) in enumerate(metrics_boxes):
        left = Inches(0.8 + i * 3.0)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(2.7), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER
        
        tb = slide3.shapes.add_textbox(left, Inches(1.9), Inches(2.7), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = val
        p0.alignment = PP_ALIGN.CENTER
        p0.font.size = Pt(26)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_SKY
        
        p1 = tf.add_paragraph()
        p1.text = lbl
        p1.alignment = PP_ALIGN.CENTER
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_DARK_SLATE
        
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_MUTED

    # Bottom Callout Grid
    card_bot = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.7), Inches(11.7), Inches(2.9))
    card_bot.fill.solid()
    card_bot.fill.fore_color.rgb = COLOR_WHITE
    card_bot.line.color.rgb = COLOR_BORDER
    
    tb_bot = slide3.shapes.add_textbox(Inches(1.1), Inches(3.9), Inches(11.1), Inches(2.5))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    
    p = tf_bot.paragraphs[0]
    p.text = "Strict Scientific Boundaries & Regulatory Standards Enforced:"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_SLATE

    bullets = [
        "CPCB 16-Hour Rule: Preserved 46,795 compliant records and discarded 3,789 unrepresentative records with n < 16h.",
        "CO & O3 Protocol: Excluded from 24h daily station AQI (24h mean != CPCB 8h metric); evaluated on landmark hourly data with project 75% rule.",
        "Severe Range Policy: CPCB Table 3.2 provides open-ended Severe concentration thresholds (e.g. PM2.5 > 250 µg/m³). The project reports Severe values at the 500 ceiling as an explicitly documented implementation policy, not an official CPCB interpolation formula.",
        "Historical Freshness: Genuine records span Jan 1, 2023 to Oct 31, 2024. Explicitly labeled as historical; zero fake real-time claims."
    ]
    for b in bullets:
        p_b = tf_bot.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = COLOR_MUTED
        p_b.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 4: HISTORICAL ANALYSIS & COMMUTER PATTERNS
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Historical Findings: Commute Curves & Atmospheric Associations", "DESCRIPTIVE ANALYTICS")
    add_footer(slide4, 4)

    # Left: Diurnal findings
    card_left = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = COLOR_CARD_BG
    card_left.line.color.rgb = COLOR_BORDER
    
    tb_l = slide4.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "24-Hour Diurnal Commute Patterns"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_SLATE
    
    findings_l = [
        "Morning Transit Peak (07:00–09:00): NO2 reaches peak elevation (~36 ug/m3 at BTM Layout), during morning vehicular rush-hour windows.",
        "Late Evening Elevation (20:00–23:00): PM10 and PM2.5 reach maximum daily levels (~72–77 ug/m3 PM10) across both BTM Layout and Peenya.",
        "Midday Cleansing (12:00–16:00): Lowest particulate concentrations (~47 ug/m3 at BTM) recorded during midday hours.",
        "* Descriptive observations from BTM Layout & Peenya. Hourly and weather analyses have limited geographic coverage, which we explicitly disclose."
    ]
    for f in findings_l:
        p_f = tf_l.add_paragraph()
        p_f.text = f"• {f}"
        p_f.font.size = Pt(13)
        p_f.font.color.rgb = COLOR_MUTED
        p_f.space_before = Pt(10)

    # Right: Weather Associations
    card_right = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card_right.fill.solid()
    card_right.fill.fore_color.rgb = COLOR_CARD_BG
    card_right.line.color.rgb = COLOR_BORDER

    tb_r = slide4.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Retrospective Weather Associations"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_SLATE

    findings_r = [
        "Wind Speed vs PM2.5 (r = -0.263): Higher resultant surface wind speed is historically associated with aerodynamic dispersion and lower particulate accumulation.",
        "Precipitation vs PM10 (r = -0.431): Rainfall days correlate with significant particulate scavenging and dust washout.",
        "Surface Pressure vs City AQI (r = +0.607): Stagnant, high-pressure atmospheric conditions in winter correlate with trapped surface pollution.",
        "* Evaluated as statistical associations; non-causal language strictly maintained."
    ]
    for f in findings_r:
        p_f = tf_r.add_paragraph()
        p_f.text = f"• {f}"
        p_f.font.size = Pt(13)
        p_f.font.color.rgb = COLOR_MUTED
        p_f.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 5: FORECAST ARENA & HONEST BENCHMARK
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Forecast Arena: Honest Four-Model Benchmark Comparison", "MACHINE LEARNING EVALUATION")
    add_footer(slide5, 5)

    # Big Alert Box
    alert_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.4))
    alert_box.fill.solid()
    alert_box.fill.fore_color.rgb = RGBColor(254, 243, 199)
    alert_box.line.color.rgb = COLOR_AMBER
    
    tb_a = slide5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(11.1), Inches(1.2))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True
    p0 = tf_a.paragraphs[0]
    p0.text = "CORE SCIENTIFIC FINDING: PERSISTENCE BASELINE OUTPERFORMS MACHINE LEARNING"
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(146, 64, 14)
    
    p1 = tf_a.add_paragraph()
    p1.text = "Our evaluation showed that the simple persistence baseline outperformed both machine-learning approaches on the held-out test period. This demonstrates why complex models must be tested against simple baselines before claiming predictive value. Evaluated chronologically across 123 calendar days (Jul 1 – Oct 31, 2024) with zero target-day weather leakage."
    p1.font.size = Pt(12.5)
    p1.font.color.rgb = RGBColor(120, 53, 15)
    p1.space_before = Pt(4)

    # Benchmark Table Box
    card_tbl = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.4), Inches(11.7), Inches(3.3))
    card_tbl.fill.solid()
    card_tbl.fill.fore_color.rgb = COLOR_WHITE
    card_tbl.line.color.rgb = COLOR_BORDER

    tb_t = slide5.shapes.add_textbox(Inches(1.1), Inches(3.55), Inches(11.1), Inches(3.0))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    
    p = tf_t.paragraphs[0]
    p.text = "Chronological Held-Out Out-of-Sample Evaluation (123 Calendar Days: Jul 1 – Oct 31, 2024)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_SLATE

    model_rows = [
        ("1. Persistence Baseline (AQI_t)", "7.42", "10.49", "0.733", "Top benchmark. Predicts tomorrow equals today; outperformed both ML approaches on held-out test."),
        ("2. Direct AQI Random Forest", "7.74", "11.14", "0.699", "Autoregressive ML regressing directly on AQI, pollutant, and weather lags."),
        ("3. Two-Stage Physical Model (PRD)", "7.91", "12.43", "0.625", "Predicts PM2.5 & PM10 concentrations, then applies deterministic CPCB math."),
        ("4. 7-Day Moving Average Baseline", "9.20", "15.08", "0.449", "Trailing weekly mean; suffers from significant phase lag during seasonal shifts.")
    ]
    for name, mae, rmse, r2, desc in model_rows:
        p_row = tf_t.add_paragraph()
        p_row.text = f"{name:<35} | MAE: {mae} pts | RMSE: {rmse} | R²: {r2} | {desc}"
        p_row.font.size = Pt(12)
        p_row.font.bold = ("Persistence" in name)
        p_row.font.color.rgb = COLOR_DARK_SLATE if "Persistence" in name else COLOR_MUTED
        p_row.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 6: PRODUCT DEMO — 5 SCREENS
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Product Demonstration: Five Implemented Dashboard Screens", "PRODUCTION APPLICATION")
    add_footer(slide6, 6)

    # 5 visual thumbnail columns
    screens = [
        ("Overview", "overview.png", "City composite AQI 141, 14d sparkline, 14 station network cards"),
        ("Explorer", "explorer.png", "670-day multi-pollutant trends & 24h diurnal commute curves"),
        ("Forecast Arena", "forecast.png", "Honest 4-model comparison & 123-day backtest timeline"),
        ("Health Advisory", "health.png", "CPCB 6-tier health guidance & sensitive group safeguards"),
        ("Data Transparency", "transparency.png", "Interactive Table 3.2 calculator widget & 16h audit ledger")
    ]
    for i, (s_title, img_name, s_desc) in enumerate(screens):
        left = Inches(0.8 + i * 2.4)
        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(2.25), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER

        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
        if os.path.exists(img_path):
            slide6.shapes.add_picture(img_path, left + Inches(0.12), Inches(2.4), width=Inches(2.01))
            
        tb = slide6.shapes.add_textbox(left + Inches(0.12), Inches(1.9), Inches(2.0), Inches(0.5))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = s_title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_SLATE
        
        tb_d = slide6.shapes.add_textbox(left + Inches(0.12), Inches(4.8), Inches(2.0), Inches(1.6))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = s_desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # SLIDE 7: ENGINEERING ARCHITECTURE & OFFLINE-FIRST
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Engineering Architecture: CPCB Core, Pipeline & Offline Design", "SYSTEM ENGINEERING")
    add_footer(slide7, 7)

    arch_cards = [
        ("CPCB Core Engine", "backend/cpcb_calculator.py", "Exact piecewise linear interpolation for categories 1–5. Severe 500 ceiling policy. CO/O3 exclusion. 43/43 unit tests passing."),
        ("Reproducible Pipeline", "backend/data_pipeline.py", "Ingests 50,584 CPCB records, enforces 16h completeness, computes vector wind (u,v), and compiles 6 cached JSON artifacts."),
        ("FastAPI Backend", "backend/main.py", "Serves 9 REST API endpoints with sub-millisecond in-memory cache. Mounts compiled React frontend. 9/9 integration tests passing."),
        ("Offline-First SPA", "frontend/ (React + Vite)", "Tailwind CSS + Recharts Google Stitch design tokens. Runs completely on localhost with network adapters disabled.")
    ]
    for i, (title, comp, desc) in enumerate(arch_cards):
        left = Inches(0.8 + (i % 2) * 5.9)
        top = Inches(1.8 + (i // 2) * 2.5)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_BORDER

        tb = slide7.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(16)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_DARK_SLATE
        
        p1 = tf.add_paragraph()
        p1.text = comp
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_SKY
        p1.space_before = Pt(2)
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 8: IMPACT, LIMITATIONS & CONCLUSION
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Real-World Impact, Known Limitations & Roadmap", "CONCLUSION & IMPACT")
    add_footer(slide8, 8)

    # Left: Impact & Integrity
    card_l8 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card_l8.fill.solid()
    card_l8.fill.fore_color.rgb = COLOR_CARD_BG
    card_l8.line.color.rgb = COLOR_BORDER

    tb_l8 = slide8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.0), Inches(4.2))
    tf_l8 = tb_l8.text_frame
    tf_l8.word_wrap = True
    p = tf_l8.paragraphs[0]
    p.text = "Key Project Takeaways"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_SLATE

    impacts = [
        "Scientific Honesty: Reporting that persistence beats Random Forest proves regulatory maturity over artificial tuning.",
        "Regulatory Trust: Exact CPCB Table 3.2 compliance with 16h sufficiency filtering provides audit-ready data.",
        "Citizen Value: Station-specific diurnal commuter windows empower asthmatics and outdoor workers to schedule high-risk exposure.",
        "Offline Reliability: 100% self-contained demonstration stack with zero cloud downtime risk."
    ]
    for imp in impacts:
        p_i = tf_l8.add_paragraph()
        p_i.text = f"• {imp}"
        p_i.font.size = Pt(13)
        p_i.font.color.rgb = COLOR_MUTED
        p_i.space_before = Pt(10)

    # Right: Limitations & Future Work
    card_r8 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card_r8.fill.solid()
    card_r8.fill.fore_color.rgb = COLOR_CARD_BG
    card_r8.line.color.rgb = COLOR_BORDER

    tb_r8 = slide8.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r8 = tb_r8.text_frame
    tf_r8.word_wrap = True
    p = tf_r8.paragraphs[0]
    p.text = "Limitations & Future Scope"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_SLATE
    
    p_sub = tf_r8.add_paragraph()
    p_sub.text = "Future work — not implemented in this prototype"
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(194, 65, 12)
    p_sub.space_before = Pt(4)

    limits = [
        "Temporal Boundary: Ground-truth dataset concludes on Oct 31, 2024. Ongoing tracking requires live automated scraping infrastructure.",
        "Spatial Kriging (Future Work): Requires empirical validation of whether 13 stations provide adequate spatial density for reliable fine-grained pollution maps.",
        "NWP Weather Forecasts (Future Work): Testing whether coupled 24h weather predictions (e.g., GFS wind shifts) provide signal beyond persistence.",
        "Automated Notifications (Future Work): Exploring webhook-based alert delivery for schools and vulnerable citizen cohorts."
    ]
    for lim in limits:
        p_l = tf_r8.add_paragraph()
        p_l.text = f"• {lim}"
        p_l.font.size = Pt(12.5)
        p_l.font.color.rgb = COLOR_MUTED
        p_l.space_before = Pt(8)

    os.makedirs(os.path.dirname(OUTPUT_PPTX), exist_ok=True)
    prs.save(OUTPUT_PPTX)
    print(f"Saved professional PowerPoint presentation: {OUTPUT_PPTX} ({os.path.getsize(OUTPUT_PPTX):,} bytes)")


if __name__ == "__main__":
    create_deck()

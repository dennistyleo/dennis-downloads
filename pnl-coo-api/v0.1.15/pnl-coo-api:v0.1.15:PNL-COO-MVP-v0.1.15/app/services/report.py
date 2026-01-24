from __future__ import annotations

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


def _ensure_fonts() -> dict[str, str]:
    """Return {lang: fontName} and register fonts as needed."""
    # English uses built-in Helvetica
    zh_font = "STSong-Light"
    try:
        pdfmetrics.getFont(zh_font)
    except KeyError:
        pdfmetrics.registerFont(UnicodeCIDFont(zh_font))
    return {"en": "Helvetica", "zh": zh_font}


def _t(lang: str, key: str) -> str:
    en = {
        # Cover / meta
        "title": "PNL-COO Board Pack",
        "tagline": "Board-level governance pack (evidence-driven, causality-aware)",
        "period": "Reporting Period",
        "generated": "Generated",
        "governance_intent": "Governance Intent",
        "lang": "Language",
        "theme": "Theme",
        "theme_dark": "Dark (Projector)",
        "theme_light": "Light (Print)",

        # Fixed A版 structure (12–15 pages)
        "ch0": "0 Cover",
        "ch1": "1 Summary",
        "ch2": "2 Executive Summary",
        "ch3": "3 Performance vs Plan",
        "ch4": "4 Financial Scoreboard",
        "ch5": "5 Working Capital & CCC",
        "ch6": "6 Customer Priority & Counterparty Risk",
        "ch7": "7 Product Priority & Portfolio Model",
        "ch8": "8 Causality & Governance Radar",
        "ch9": "9 Solution Taskforce Matrix",
        "ch10": "10 Board Q&A",
        "ch11": "11 Appendix",

        # Common labels
        "kpi": "KPI",
        "value": "Value",
        "delta": "Δ",
        "note": "Note",
        "placeholder": "Placeholder: section template is locked; data & narratives will be filled based on evidence mapping.",
        "no_data": "No corresponding data found in the uploaded workbook.",
        "answer_seed": "Answer Seed",
        "evidence_ref": "Evidence Reference",
        "action_id": "Action-ID",
        "owner": "Owner",
        "kpi_window": "KPI / Window",
    }
    zh = {
        # Cover / meta
        "title": "PNL-COO 董事會 Board Pack",
        "tagline": "董事會級治理報告（以證據驅動、以因果對齊）",
        "period": "報告期間",
        "generated": "產生時間",
        "governance_intent": "治理意圖",
        "lang": "語文",
        "theme": "版式",
        "theme_dark": "黑底（投影）",
        "theme_light": "白底（列印）",

        # Fixed A版 structure (12–15 pages)
        "ch0": "0 封面",
        "ch1": "1 摘要",
        "ch2": "2 執行摘要",
        "ch3": "3 對計畫績效（vs Plan）",
        "ch4": "4 財務配分板",
        "ch5": "5 營運資金與 CCC",
        "ch6": "6 客戶優先與對手方風險",
        "ch7": "7 產品優先與組合模型",
        "ch8": "8 因果與治理雷達",
        "ch9": "9 解決方案任務矩陣",
        "ch10": "10 董事會 Q&A",
        "ch11": "11 附錄",

        # Common labels
        "kpi": "指標",
        "value": "數值",
        "delta": "變動",
        "note": "備註",
        "placeholder": "佔位：章節模板已鎖定；將依證據映射填入數據與敘事。",
        "no_data": "在上傳的試算表中找不到對應資料。",
        "answer_seed": "埋答案（Answer Seed）",
        "evidence_ref": "證據引用",
        "action_id": "Action-ID",
        "owner": "Owner",
        "kpi_window": "KPI / 時窗",
    }
    return (zh if lang == "zh" else en).get(key, key)


def _fmt_num(x: Any) -> str:
    if x is None:
        return "(unmapped)"
    try:
        return f"{float(x):,.0f}"
    except Exception:
        return str(x)


def _fmt_pct(p: Any) -> str:
    if p is None:
        return "(n/a)"
    try:
        p = float(p) * 100
        sign = "+" if p >= 0 else ""
        return f"{sign}{p:.2f}%"
    except Exception:
        return str(p)


def _fmt_days(x: Any) -> str:
    if x is None:
        return "(unmapped)"
    try:
        return f"{float(x):.1f}"
    except Exception:
        return str(x)


def generate_board_pack_pdf(analysis: dict[str, Any], lang: str = "en", theme: str = "dark") -> bytes:
    """Generate Board Pack (A版) PDF.

    This function focuses on **layout-system stability** (no overlap / safe margins / fixed chapters).
    Content will be progressively filled from evidence mapping without changing the locked structure.
    """
    lang = "zh" if str(lang).lower().startswith("zh") else "en"
    theme = (theme or "dark").lower()
    if theme not in ("dark", "light"):
        theme = "dark"

    fonts = _ensure_fonts()
    font = fonts[lang]

    # Palette (Mo-Gold, restrained)
    gold = colors.HexColor("#b8892f")
    if theme == "dark":
        bg = colors.HexColor("#0b0b0d")
        text = colors.HexColor("#f2f2f2")
        subtext = colors.HexColor("#c9c9c9")
        hairline = colors.HexColor("#5a4a2a")
        panel = colors.HexColor("#121217")
    else:
        bg = colors.white
        text = colors.HexColor("#111111")
        subtext = colors.HexColor("#444444")
        hairline = colors.HexColor("#d5c49b")
        panel = colors.HexColor("#fbfbfb")

    # Safe margins (print & projector friendly)
    left = 18 * mm
    right = 18 * mm
    top = 16 * mm
    bottom = 16 * mm

    styles = getSampleStyleSheet()
    base = ParagraphStyle(
        "base",
        parent=styles["Normal"],
        fontName=font,
        fontSize=10,
        leading=14,
        textColor=text,
    )
    h1 = ParagraphStyle(
        "h1",
        parent=base,
        fontSize=22,
        leading=28,
        spaceAfter=10,
        alignment=1,
        textColor=text,
    )
    h2 = ParagraphStyle(
        "h2",
        parent=base,
        fontSize=14,
        leading=18,
        spaceBefore=0,
        spaceAfter=10,
        textColor=text,
    )
    meta = ParagraphStyle(
        "meta",
        parent=base,
        fontSize=9,
        leading=12,
        textColor=subtext,
    )
    small = ParagraphStyle(
        "small",
        parent=base,
        fontSize=9,
        leading=12,
        textColor=text,
    )
    pill = ParagraphStyle(
        "pill",
        parent=base,
        fontSize=9,
        leading=12,
        textColor=text,
    )

    period = analysis.get("period") or "(unmapped)"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    intent = analysis.get("governance_intent") or {}
    cycle = intent.get("cycle") or "quarterly"
    terms = intent.get("terms") or "net-70"
    mode = intent.get("mode") or "evidence-first"
    hold = intent.get("hold") or "unknown"

    buf = io.BytesIO()

    def _on_page(canv, doc):
        # Background
        canv.saveState()
        w, h = A4
        canv.setFillColor(bg)
        canv.rect(0, 0, w, h, stroke=0, fill=1)

        # Header line + title
        canv.setStrokeColor(gold)
        canv.setLineWidth(0.8)
        canv.line(left, h - top + 6, w - right, h - top + 6)

        canv.setFont(font, 9)
        canv.setFillColor(subtext)
        header = f"PNL-COO | {period}"
        canv.drawString(left, h - top + 10, header)

        # Footer
        canv.setStrokeColor(hairline)
        canv.setLineWidth(0.5)
        canv.line(left, bottom - 6, w - right, bottom - 6)
        canv.setFont(font, 9)
        canv.setFillColor(subtext)
        canv.drawRightString(w - right, bottom - 18, f"{doc.page}")
        canv.restoreState()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=left,
        rightMargin=right,
        topMargin=top,
        bottomMargin=bottom,
        title=_t(lang, "title"),
        author="PNL-COO",
    )

    def _chapter(title_key: str, extra: str | None = None, answer_seed: str | None = None):
        story.append(Paragraph(_t(lang, title_key), h2))
        story.append(Paragraph(_t(lang, "placeholder"), meta))
        if extra:
            story.append(Spacer(1, 8))
            story.append(Paragraph(extra, base))
        if answer_seed:
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"<b>{_t(lang,'answer_seed')}</b>: {answer_seed}", small))

    story: list[Any] = []

    # 0 Cover
    story.append(Spacer(1, 40))
    story.append(Paragraph(_t(lang, "title"), h1))
    story.append(Paragraph(_t(lang, "tagline"), meta))
    story.append(Spacer(1, 18))

    gi_lines = (
        f"{_t(lang,'period')}: <b>{period}</b><br/>"
        f"{_t(lang,'generated')}: {ts}<br/>"
        f"{_t(lang,'governance_intent')}: "
        f"Cycle={cycle}; Terms={terms}; Mode={mode}; Hold={hold}<br/>"
        f"{_t(lang,'lang')}: {lang.upper()} &nbsp;&nbsp; { _t(lang,'theme') }: { _t(lang, 'theme_dark' if theme=='dark' else 'theme_light') }"
    )
    story.append(Paragraph(gi_lines, base))

    # Chapter pages (fixed structure)
    story.append(PageBreak()); _chapter("ch1")
    story.append(PageBreak()); _chapter("ch2")
    story.append(PageBreak()); _chapter("ch3")
    story.append(PageBreak()); _chapter("ch4", answer_seed="EV-001 / Action-A01 / Owner: CFO / KPI: Revenue+GM / Window: 30-60d")
    story.append(PageBreak()); _chapter("ch5", answer_seed="EV-002 / Action-W01 / Owner: AR Lead / KPI: DSO/CCC / Window: 14-45d")
    story.append(PageBreak()); _chapter("ch6")
    story.append(PageBreak()); _chapter("ch7")
    story.append(PageBreak()); _chapter("ch8")
    story.append(PageBreak()); _chapter("ch9")

    # 10 Board Q&A (fixed questions)
    story.append(PageBreak())
    story.append(Paragraph(_t(lang, "ch10"), h2))
    if lang == "en":
        q = [
            "Why did revenue differ from expectation, and what is the evidence?",
            "How do we pull revenue: short / mid / long term (with evidence & owners)?",
            "How do we cost-down without breaking growth (with evidence & owners)?",
        ]
    else:
        q = [
            "营收为何与预期不同？证据是什么？",
            "如何拉营收：短/中/长期（含证据与责任归属）？",
            "如何 cost down 而不伤增长（含证据与责任归属）？",
        ]
    story.append(Paragraph("<br/>".join([f"• {x}" for x in q]), base))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"<b>{_t(lang,'evidence_ref')}</b>: EV-xxx  &nbsp; <b>{_t(lang,'action_id')}</b>: Action-xx  &nbsp; <b>{_t(lang,'owner')}</b>: Org/Role  &nbsp; <b>{_t(lang,'kpi_window')}</b>: KPI / Window",
        meta,
    ))

    # 11 Appendix
    story.append(PageBreak())
    story.append(Paragraph(_t(lang, "ch11"), h2))
    fx_note = (
        "FX rule: Output currency = USD; preserve original currency as evidence; FX source & timestamp recorded in appendix."
        if lang == "en"
        else "匯率規則：輸出幣別統一 USD；保留原幣別證據；於附錄記錄匯率來源與時間戳。"
    )
    story.append(Paragraph(fx_note, base))
    story.append(Spacer(1, 10))
    story.append(Paragraph(_t(lang, "placeholder"), meta))

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buf.getvalue()

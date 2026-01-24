from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from app.services.analyze import analyze_file_cached


@dataclass
class ChatResult:
    reply: str
    analysis: dict[str, Any]


FORBIDDEN_PHRASES_ZH = [
    "資料不足",
    "请贴",
    "請貼",
    "貼卡",
    "卡片內容",
]


def _contains_forbidden(text: str) -> bool:
    t = (text or "").lower()
    for p in FORBIDDEN_PHRASES_ZH:
        if p.lower() in t:
            return True
    return False


def _status_block(analysis: dict[str, Any], lang: str) -> str:
    status = analysis.get("status") or "UNKNOWN"
    period = analysis.get("period") or "—"
    sys_ = analysis.get("system") or {}
    sheets = sys_.get("sheets") or []
    filters = analysis.get("filters") or {}
    backlog = analysis.get("mapping_backlog") or []
    gaps = [b for b in backlog if b.get("type") in ("MAPPING_GAP", "SYSTEM_ERROR")]

    lens_parts = []
    for k in ("cycle", "terms", "mode", "hold"):
        v = filters.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            lens_parts.append(f"{k}:{s}")
    lens_txt = " | ".join(lens_parts) if lens_parts else "—"

    if lang == "zh":
        lines = [
            f"系統狀態: {status}",
            f"期間: {period}",
            f"輸出條件: {lens_txt}",
            f"已辨識工作表: {len(sheets)}",
        ]
        if gaps:
            top = ", ".join([str(g.get("code") or "—") for g in gaps[:5]])
            lines.append(f"缺口: {len(gaps)} (例: {top})")
            lines.append("下一步: 補齊 term mapping（spec/v0.4.6/PNL-COO-IMH-Term-Mapping-EN-ZH-v0.4.6.csv），再重跑 Analyze/Charts。")
        else:
            lines.append("缺口: 0")
        return "\n".join(lines)

    # EN
    lines = [
        f"System status: {status}",
        f"Period: {period}",
        f"Lens (output conditions): {lens_txt}",
        f"Sheets detected: {len(sheets)}",
    ]
    if gaps:
        top = ", ".join([str(g.get("code") or "—") for g in gaps[:5]])
        lines.append(f"Gaps: {len(gaps)} (e.g., {top})")
        lines.append("Next action: fill term mapping at spec/v0.4.6/PNL-COO-IMH-Term-Mapping-EN-ZH-v0.4.6.csv, then re-run Analyze/Charts.")
    else:
        lines.append("Gaps: 0")
    return "\n".join(lines)


def _summary_block(analysis: dict[str, Any], lang: str) -> str:
    kpis = analysis.get("kpis") or []
    cash = analysis.get("cash_cycle") or {}
    dso, dio, dpo, ccc = cash.get("dso"), cash.get("dio"), cash.get("dpo"), cash.get("ccc")

    def _fmt_delta(dp: Any) -> str:
        if not isinstance(dp, (int, float)):
            return ""
        sign = "+" if dp > 0 else ""
        return f" {sign}{dp*100:.1f}%"

    if lang == "zh":
        lines = []
        for k in kpis[:5]:
            lbl = k.get("label") or "—"
            val = k.get("value")
            unit = k.get("unit") or ""
            dp = _fmt_delta(k.get("delta_pct"))
            vtxt = "—" if val is None else str(val)
            lines.append(f"- {lbl}: {vtxt}{unit}{dp}")
        lines.append(f"- CCC: {('—' if ccc is None else f'{float(ccc):.1f}')}; DSO/DIO/DPO: {('—' if dso is None else f'{float(dso):.1f}')}/{('—' if dio is None else f'{float(dio):.1f}')}/{('—' if dpo is None else f'{float(dpo):.1f}')}")
        return "\n".join(lines)

    # EN
    lines = []
    for k in kpis[:5]:
        lbl = k.get("label") or "—"
        val = k.get("value")
        unit = k.get("unit") or ""
        dp = _fmt_delta(k.get("delta_pct"))
        vtxt = "—" if val is None else str(val)
        lines.append(f"- {lbl}: {vtxt}{unit}{dp}")
    lines.append(f"- CCC: {('—' if ccc is None else f'{float(ccc):.1f}')}; DSO/DIO/DPO: {('—' if dso is None else f'{float(dso):.1f}')}/{('—' if dio is None else f'{float(dio):.1f}')}/{('—' if dpo is None else f'{float(dpo):.1f}')}")
    return "\n".join(lines)


def chat_reply(
    message: str,
    file_path: Optional[Path],
    lang: str = "en",
    use_openai: bool = False,
    lens: Optional[dict[str, Any]] = None,
) -> ChatResult:
    """Evidence-first chat.

    VLD-AI-001: if file_id exists (file_path provided), never ask the user to paste
    card contents; always return status + reason + next steps.
    """
    message = (message or "").strip()
    if lang not in ("en", "zh"):
        lang = "en"

    if not file_path:
        # No file context.
        if lang == "zh":
            return ChatResult(reply="請先上傳財務報表（XLSX）。", analysis={"status": "NO_FILE"})
        return ChatResult(reply="Please upload a finance report (XLSX) first.", analysis={"status": "NO_FILE"})

    # Always run deterministic analysis; never raise.
    flt = lens or {}
    analysis = analyze_file_cached(
        file_path,
        lang=lang,
        prompt="",
        cycle=str(flt.get("cycle") or "MOM"),
        terms=str(flt.get("terms") or "AUTO"),
        mode=str(flt.get("mode") or "AUTO"),
        hold=str(flt.get("hold") or "OFF"),
    )

    status = _status_block(analysis, lang=lang)
    summary = _summary_block(analysis, lang=lang)

    # Simple intent handling (deterministic). Real-AI path can be added later.
    if lang == "zh":
        body = [status, "", "摘要：", summary]
        if message:
            body.append("")
            body.append(f"針對你的問題（{message}）：")
            body.append("我會以目前已解析的 KPI / CCC / Radar 訊號來回覆；若存在 mapping 缺口，已記錄於 Evidence Pull 的 backlog，修補後即可提升完整性。")
        reply = "\n".join(body).strip()
    else:
        body = [status, "", "Summary:", summary]
        if message:
            body.append("")
            body.append(f"Regarding your question ({message}):")
            body.append("I will answer using the extracted KPIs / CCC / radar signals. If term mapping gaps exist, they are logged in Evidence Pull and closing them will improve completeness.")
        reply = "\n".join(body).strip()

    # Safety: never violate VLD-AI-001 by emitting forbidden phrases.
    if _contains_forbidden(reply):
        # Replace with neutral status wording.
        reply = reply.replace("資料不足", "系統尚在補齊 mapping")
        reply = reply.replace("請貼", "請參考 Evidence Pull")

    return ChatResult(reply=reply, analysis=analysis)

from __future__ import annotations

from datetime import datetime
import uuid
import traceback
from pathlib import Path
import os
from typing import Any

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from app.services.quota import attach_daily_quota_middleware

from app.services.ingest import save_upload_and_preview
from app.services.analyze import (
    analyze_file_cached,
    scoreboard_chart_png,
    radar_chart_png,
    causality_link_map_png,
    revenue_bridge_chart_png,
    gross_margin_bridge_chart_png,
    opex_mix_chart_png,
    working_capital_pulse_chart_png,
    bcg_customers_chart_png,
    empty_state_chart_png,
)
from app.services.report import generate_board_pack_pdf
from app.services.chat import chat_reply

APP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = APP_ROOT.parent
DATA_DIR = REPO_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _load_dotenv_if_present() -> None:
    """Load key=value pairs from REPO_ROOT/.env if present.

    We keep this dependency-free so the MVP runs out-of-the-box.
    It only sets variables that are NOT already present in the environment.
    """

    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return

    try:
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v
    except Exception:
        # If .env is malformed, don't crash the server.
        return

_load_dotenv_if_present()

app = FastAPI(title="PNL-COO MVP", version="0.1.13")

# Daily quota limiter (demo safety). Uses Asia/Taipei day boundary.
attach_daily_quota_middleware(app)

app.mount("/static", StaticFiles(directory=str(APP_ROOT / "static")), name="static")
INDEX_FILE = APP_ROOT / "templates" / "index.html"
BUILD_UTC = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _find_file_path(file_id: str) -> Path:
    matches = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="File not found")
    return matches[0]


def _client_ip(request: Request) -> str:
    # Prefer proxy-forwarded IP (Render / Cloud Run / Nginx)
    xff = request.headers.get("x-forwarded-for") or request.headers.get("X-Forwarded-For")
    if xff:
        # First IP is the original client
        return xff.split(",")[0].strip()
    return getattr(request.client, "host", "unknown")


def _demo_token_ok(request: Request) -> bool:
    """Return True if real-AI is allowed for this request.

    Behavior:
      - If DEMO_TOKEN is NOT set: allow real AI (local dev compatibility).
      - If DEMO_TOKEN is set: require header X-DEMO-TOKEN to match.
    """
    expected = (os.getenv("DEMO_TOKEN") or "").strip()
    if not expected:
        return True
    provided = (request.headers.get("x-demo-token") or request.headers.get("X-DEMO-TOKEN") or "").strip()
    return bool(provided) and provided == expected


def _lens(cycle: str | None, terms: str | None, mode: str | None, hold: str | None) -> dict[str, str | None]:
    """Normalize governance filter inputs.

    Spec: these 4 filters are output conditions. They must never crash the pipeline.
    """
    def _n(v: str | None) -> str | None:
        if v is None:
            return None
        s = str(v).strip()
        return s if s else None

    return {
        "cycle": _n(cycle),
        "terms": _n(terms),
        "mode": _n(mode),
        "hold": _n(hold),
    }


@app.get("/", response_class=HTMLResponse)
def index(trace: int | None = None):
    """Serve the dashboard shell as a plain HTML file.

    If anything goes wrong (missing file, permission, encoding), return a
    diagnostic HTML so the user sees the real error instead of a blank 500.
    Add ?trace=1 to include a Python stack trace.
    """
    try:
        return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        tb = traceback.format_exc() if trace else ""
        body = f"""<!doctype html>
<html><head><meta charset='utf-8'>
<title>PNL-COO: Startup diagnostic</title>
<style>body{{font-family:ui-monospace,Menlo,monospace;padding:20px;}}pre{{white-space:pre-wrap;}}</style>
</head><body>
<h2>PNL-COO dashboard failed to load</h2>
<p><b>Error:</b> {type(e).__name__}: {e}</p>
<p><b>INDEX_FILE:</b> {INDEX_FILE}</p>
<p><b>Exists:</b> {INDEX_FILE.exists()}</p>
<p><b>App version:</b> {app.version} <b>Build:</b> {BUILD_UTC}</p>
<p>Try: <a href='/api/health'>/api/health</a> (should return JSON)</p>
<p>For stack trace: append <code>?trace=1</code> to the URL.</p>
<pre>{tb}</pre>
</body></html>"""
        return HTMLResponse(body, status_code=200)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "version": app.version, "build": BUILD_UTC}


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)) -> dict[str, Any]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename")

    file_id = str(uuid.uuid4())
    result = await save_upload_and_preview(file=file, upload_dir=UPLOAD_DIR, file_id=file_id)
    return {"file_id": file_id, **result}


@app.post("/api/analyze")
async def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    file_id = payload.get("file_id")
    if not file_id:
        raise HTTPException(status_code=400, detail="Missing file_id")

    lang = (payload.get("lang") or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"

    file_path = _find_file_path(str(file_id))

    try:
        lens = _lens(
            cycle=payload.get("cycle"),
            terms=payload.get("terms"),
            mode=payload.get("mode"),
            hold=payload.get("hold"),
        )
        analysis = analyze_file_cached(
            file_path,
            lang=lang,
            prompt=str(payload.get("prompt") or ""),
            cycle=lens["cycle"],
            terms=lens["terms"],
            mode=lens["mode"],
            hold=lens["hold"],
        )
        return analysis
    except Exception as e:
        # Never 500 the UI: return a stable, demo-safe analysis object.
        # (Charts remain available via 200/png fallback endpoints.)
        return {
            "ok": True,
            "status": "DEGRADED",
            "error": f"{type(e).__name__}: {e}",
            "ai_brief": "Analysis is running in safe fallback mode (recoverable issue detected). Charts remain available.",
            "kpis": [],
            "scoreboard_narrative": "",
            "cards": {
                "cash_cycle": {"html": ""},
                "evidence_pull": {"html": ""},
                "solution_task_force": {"html": ""},
                "causality_radar": {"legend_html": ""},
            },
            "filters": _lens(payload.get("cycle"), payload.get("terms"), payload.get("mode"), payload.get("hold")),
            "meta": {"build": BUILD_UTC, "version": app.version},
        }


def _safe_png(fn, *args, **kwargs) -> bytes:
    try:
        out = fn(*args, **kwargs)
        if isinstance(out, (bytes, bytearray)) and len(out) > 8:
            return bytes(out)
    except Exception:
        pass
    # Always return a valid PNG to satisfy VLD-CHART-001.
    return empty_state_chart_png(lang=str(kwargs.get("lang") or "en"), title="Chart unavailable")


@app.get("/api/chart/scoreboard")
def chart_scoreboard(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(scoreboard_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/radar")
def chart_radar(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(radar_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/linkmap")
def chart_linkmap(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(causality_link_map_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/rev_bridge")
def chart_rev_bridge(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(revenue_bridge_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/gm_bridge")
def chart_gm_bridge(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(gross_margin_bridge_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/opex_mix")
def chart_opex_mix(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(opex_mix_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/wc_pulse")
def chart_wc_pulse(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(working_capital_pulse_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/chart/bcg_customers")
def chart_bcg_customers(
    file_id: str,
    lang: str = "en",
    cycle: str | None = None,
    terms: str | None = None,
    mode: str | None = None,
    hold: str | None = None,
) -> Response:
    file_path = _find_file_path(file_id)
    lang = (lang or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"
    lens = _lens(cycle, terms, mode, hold)
    png_bytes = _safe_png(bcg_customers_chart_png, file_path, lang=lang, lens=lens)
    return Response(content=png_bytes, media_type="image/png")


@app.post("/api/report/boardpack")
async def report_boardpack(payload: dict[str, Any]) -> Response:
    file_id = payload.get("file_id")
    if not file_id:
        raise HTTPException(status_code=400, detail="Missing file_id")

    lang = (payload.get("lang") or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"

    theme = (payload.get("theme") or "dark").lower()
    if theme not in ("dark", "light"):
        theme = "dark"

    file_path = _find_file_path(str(file_id))
    analysis = analyze_file_cached(
        file_path,
        lang=lang,
        prompt=str(payload.get('prompt') or ''),
        cycle=str(payload.get('cycle') or None) if payload.get('cycle') is not None else None,
        terms=str(payload.get('terms') or None) if payload.get('terms') is not None else None,
        mode=str(payload.get('mode') or None) if payload.get('mode') is not None else None,
        hold=str(payload.get('hold') or None) if payload.get('hold') is not None else None,
    )
    # Attach theme for PDF styling
    analysis.setdefault('governance_intent', {})
    analysis['governance_intent']['theme'] = theme

    pdf_bytes = generate_board_pack_pdf(analysis=analysis, lang=lang, theme=theme)

    period = analysis.get("period") or "period"
    fname = f"PNL-COO_BoardPack_{period}_{lang}_{theme}.pdf".replace("/", "-")

    headers = {
        "Content-Disposition": f'attachment; filename="{fname}"'
    }
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)


@app.post("/api/chat")
async def chat(payload: dict[str, Any], request: Request) -> dict[str, Any]:
    message = str(payload.get("message") or "").strip()
    lang = (payload.get("lang") or "en").lower()
    if lang not in ("en", "zh"):
        lang = "en"

    file_id = payload.get("file_id")
    file_path = None
    if file_id:
        try:
            file_path = _find_file_path(str(file_id))
        except Exception:
            file_path = None

    # Demo rule: default Mock. Only enable real AI if access code matches.
    use_real_ai = _demo_token_ok(request)
    lens = _lens(
        cycle=payload.get("cycle"),
        terms=payload.get("terms"),
        mode=payload.get("mode"),
        hold=payload.get("hold"),
    )
    result = chat_reply(
        message=message,
        file_path=file_path,
        lang=lang,
        use_openai=use_real_ai,
        lens=lens,
    )
    return {
        "ok": True,
        "reply": result.reply,
        "analysis": result.analysis,
        "meta": {
            "mode": "real" if use_real_ai else "mock",
            "ip": _client_ip(request),
        },
    }

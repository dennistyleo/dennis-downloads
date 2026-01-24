#!/usr/bin/env python3
"""PNL-COO MVP Validator Gate Runner

Runs the ship-stopper gates defined in:
  spec/v0.4.6/PNL-COO-VALIDATOR-v0.4.6.md

Designed to be deterministic and offline: uses FastAPI TestClient.

Usage:
  python tools/validator_gate.py --sample /path/to.xlsx --lang en

Exit codes:
  0 = PASS
  2 = FAIL
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fastapi.testclient import TestClient

# Ensure project root is on sys.path even when running from tools/
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


FORBIDDEN_AI_PHRASES = [
    "資料不足",
    "请贴",
    "請貼",
    "貼卡",
    "卡片內容",
]


@dataclass
class CheckResult:
    check_id: str
    status: str  # PASS/FAIL
    detail: str


def _load_app() -> Any:
    # Import the FastAPI app from app.main
    from app.main import app  # type: ignore

    return app


def _assert(cond: bool, check_id: str, detail: str) -> CheckResult:
    return CheckResult(check_id=check_id, status="PASS" if cond else "FAIL", detail=detail)


def _is_png(resp) -> bool:
    ct = (resp.headers.get("content-type") or "").lower()
    if "image/png" not in ct:
        return False
    return len(resp.content or b"") > 200  # small but non-empty


def _nontrivial_png(resp, min_bytes: int = 5000) -> bool:
    """Heuristic to reject broken/blank chart images.

    Spec intent (VLD-EMPTY-001): after upload, cards must not be blank or broken.
    We enforce a conservative size threshold to catch 1x1/empty renders.
    """
    return _is_png(resp) and len(resp.content or b"") >= int(min_bytes)


def run(sample: Path, lang: str = "en") -> Tuple[List[CheckResult], Dict[str, Any]]:
    app = _load_app()
    client = TestClient(app)

    # 1) Upload
    with sample.open("rb") as f:
        files = {"file": (sample.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        r = client.post("/api/upload", files=files)
    ok = r.status_code == 200 and r.json().get("ok") is True and r.json().get("file_id")
    res: List[CheckResult] = [_assert(ok, "VLD-UPLOAD-001", f"upload status={r.status_code}")]
    file_id = r.json().get("file_id") if r.status_code == 200 else None

    meta: Dict[str, Any] = {"file_id": file_id, "sample": str(sample)}

    if not file_id:
        return res, meta

    # 2) Analyze
    payload = {
        "file_id": file_id,
        "lang": lang,
        "cycle": "MOM",
        "terms": "AUTO",
        "mode": "AUTO",
        "hold": "OFF",
    }
    ra = client.post("/api/analyze", json=payload)
    ok = ra.status_code == 200 and ra.json().get("ok") is True
    res.append(_assert(ok, "VLD-ANALYZE-001", f"analyze status={ra.status_code}"))

    analysis = ra.json() if ra.status_code == 200 else {}
    meta["analysis_status"] = analysis.get("status")

    # 3) Chart endpoints must be 200 + png (VLD-CHART-001)
    chart_paths = [
        "/api/chart/scoreboard",
        "/api/chart/radar",
        "/api/chart/linkmap",
        "/api/chart/rev_bridge",
        "/api/chart/gm_bridge",
        "/api/chart/opex_mix",
        "/api/chart/wc_pulse",
        "/api/chart/bcg_customers",
    ]

    for p in chart_paths:
        rc = client.get(p, params={"file_id": file_id, "lang": lang, "cycle": "MOM", "terms": "AUTO", "mode": "AUTO", "hold": "OFF"})
        ok = rc.status_code == 200 and _is_png(rc)
        res.append(_assert(ok, "VLD-CHART-001", f"{p} status={rc.status_code} ct={rc.headers.get('content-type')}") )

        # VLD-EMPTY-001: no blank/broken images (at least for key demo cards)
        if p in ("/api/chart/scoreboard", "/api/chart/radar", "/api/chart/linkmap"):
            ok2 = rc.status_code == 200 and _nontrivial_png(rc)
            res.append(_assert(ok2, "VLD-EMPTY-001", f"{p} bytes={len(rc.content or b'')}") )

    # 4) AI behavior (VLD-AI-001)
    rq = client.post(
        "/api/chat",
        json={
            "file_id": file_id,
            "lang": lang,
            "message": "Why are the charts empty?",
            "cycle": "MOM",
            "terms": "AUTO",
            "mode": "AUTO",
            "hold": "OFF",
        },
    )
    ok = rq.status_code == 200 and rq.json().get("ok") is True
    res.append(_assert(ok, "VLD-CHAT-000", f"chat status={rq.status_code}"))

    reply = (rq.json().get("reply") or "") if rq.status_code == 200 else ""
    forbidden = any(x.lower() in reply.lower() for x in FORBIDDEN_AI_PHRASES)
    has_status = ("System status" in reply) or ("系統狀態" in reply)
    res.append(_assert((not forbidden) and has_status, "VLD-AI-001", "reply must include system status and no forbidden phrases"))

    # 5) Language gate (light check): when EN, main text should not contain Chinese chars
    if lang == "en":
        ai_brief = (analysis.get("ai_brief") or "")
        # evidence_pull may contain ZH; ai_brief should not.
        contains_zh = bool(re.search(r"[\u4e00-\u9fff]", ai_brief))
        res.append(_assert(not contains_zh, "VLD-LANG-001", "ai_brief should not contain CJK when lang=en"))

    # Aggregate pass/fail
    meta["pass"] = all(r.status == "PASS" for r in res)
    return res, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", required=True, help="Sample XLSX to upload")
    ap.add_argument("--lang", default="en", choices=["en", "zh"])
    ap.add_argument("--out", default="validator_results.json")
    args = ap.parse_args()

    sample = Path(args.sample).resolve()
    if not sample.exists():
        raise SystemExit(f"sample not found: {sample}")

    results, meta = run(sample=sample, lang=args.lang)

    payload = {
        "meta": meta,
        "results": [r.__dict__ for r in results],
    }
    Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Print a compact summary
    width = max(len(r.check_id) for r in results) if results else 10
    for r in results:
        print(f"{r.status:<4} {r.check_id:<{width}}  {r.detail}")

    passed = all(r.status == "PASS" for r in results)
    print("\nOVERALL:", "PASS" if passed else "FAIL")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())

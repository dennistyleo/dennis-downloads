from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Tuple

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


@dataclass
class QuotaConfig:
    chat: int
    analyze: int
    report: int
    tz: str = "Asia/Taipei"


def _get_cfg() -> QuotaConfig:
    def _i(name: str, default: int) -> int:
        try:
            v = int(str(os.getenv(name, str(default))).strip())
            return v if v > 0 else default
        except Exception:
            return default

    return QuotaConfig(
        chat=_i("DAILY_QUOTA_CHAT", 200),
        analyze=_i("DAILY_QUOTA_ANALYZE", 50),
        report=_i("DAILY_QUOTA_REPORT", 20),
        tz=os.getenv("DEMO_TZ", "Asia/Taipei"),
    )


def _today_key(tz_name: str) -> str:
    # Daily quota resets at 00:00 in Asia/Taipei by default.
    if ZoneInfo:
        return datetime.now(ZoneInfo(tz_name)).date().isoformat()
    # Fallback: local time
    return datetime.now().date().isoformat()


def _client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for") or request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return getattr(request.client, "host", "unknown")


# In-memory counters for demo. Key: (day, ip, bucket)
_COUNTS: Dict[Tuple[str, str, str], int] = {}


def attach_daily_quota_middleware(app: FastAPI) -> None:
    cfg = _get_cfg()

    @app.middleware("http")
    async def _quota_mw(request: Request, call_next):
        path = request.url.path or ""
        bucket = None
        limit = None
        if path.startswith("/api/chat"):
            bucket, limit = "chat", cfg.chat
        elif path.startswith("/api/analyze"):
            bucket, limit = "analyze", cfg.analyze
        elif path.startswith("/api/report"):
            bucket, limit = "report", cfg.report

        # Only rate-limit the costful APIs
        if bucket and limit:
            day = _today_key(cfg.tz)
            ip = _client_ip(request)
            key = (day, ip, bucket)
            cur = _COUNTS.get(key, 0)
            if cur >= limit:
                headers = {
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset-Day": day,
                }
                return JSONResponse(
                    status_code=429,
                    content={
                        "ok": False,
                        "error": "Daily quota exceeded",
                        "bucket": bucket,
                        "limit": limit,
                        "day": day,
                        "ip": ip,
                    },
                    headers=headers,
                )
            _COUNTS[key] = cur + 1

        resp = await call_next(request)
        # add informative headers for these endpoints
        if bucket and limit:
            day = _today_key(cfg.tz)
            ip = _client_ip(request)
            key = (day, ip, bucket)
            used = _COUNTS.get(key, 0)
            resp.headers["X-RateLimit-Limit"] = str(limit)
            resp.headers["X-RateLimit-Remaining"] = str(max(0, limit - used))
            resp.headers["X-RateLimit-Reset-Day"] = day
        return resp

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import UploadFile


def _sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()


async def save_upload_and_preview(file: UploadFile, upload_dir: Path, file_id: str) -> dict[str, Any]:
    upload_dir.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    if not content:
        return {"ok": False, "error": "Empty file"}

    suffix = Path(file.filename).suffix.lower() or ".bin"
    saved_path = upload_dir / f"{file_id}{suffix}"
    saved_path.write_bytes(content)

    preview = extract_preview(saved_path)
    return {
        "ok": True,
        "filename": file.filename,
        "saved_as": saved_path.name,
        "sha256": _sha256_bytes(content),
        "preview": preview,
    }


def extract_preview(path: Path) -> dict[str, Any]:
    """Best-effort preview extraction.

    Supports:
    - .csv
    - .xlsx / .xls

    Other formats are accepted but return stub preview.
    """

    ext = path.suffix.lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(path)
            return {
                "type": "table",
                "format": "csv",
                "rows": int(df.shape[0]),
                "cols": int(df.shape[1]),
                "columns": list(map(str, df.columns.tolist()))[:60],
                "head": df.head(10).fillna("").astype(str).to_dict(orient="records"),
            }

        if ext in {".xlsx", ".xls"}:
            xl = pd.ExcelFile(path)
            sheets = []
            for name in xl.sheet_names[:12]:
                df = xl.parse(name)
                sheets.append(
                    {
                        "sheet": str(name),
                        "rows": int(df.shape[0]),
                        "cols": int(df.shape[1]),
                        "columns": list(map(str, df.columns.tolist()))[:60],
                        "head": df.head(8).fillna("").astype(str).to_dict(orient="records"),
                    }
                )
            return {"type": "workbook", "format": "xlsx", "sheets": sheets}

    except Exception as e:
        return {"type": "error", "message": f"Preview parse failed: {e}"}

    # Stub for PDF/image/other
    return {
        "type": "binary",
        "format": ext.lstrip(".") or "bin",
        "message": "Preview not supported for this format yet (OCR/PDF pipeline stub).",
    }

# DoubleClick DEV.COMMAND (macOS)


# PNL-COO MVP v0.1.12

## v0.1.12 focus
- **JS hard-fix:** removed fatal null dereference; rewrote UI init/bind to eliminate silent front-end failure
- **AI cockpit lock:** removed extra/unused output box; single large scrollable conversation log + compact input
- **Premium chart fill (demo-ready):** ships with `PNL-COO-CHART-PACK-EBN-2017-08-V5` and auto-detects the demo XLSX to show premium static charts immediately
- **Focus View upgraded:** Scoreboard focus shows 4 executive charts in demo mode; Radar focus includes Drift Flow + Event→Org linkmap
- **Scrollbars made visible:** cards + cockpit use thin high-contrast scrollbars (no “hover to appear” surprises)

# SPEC LOCK (v0.4.6 Patch + Validator)

- **Patch (唯一真相):** `spec/v0.4.6/PNL-COO-SPEC-PATCH-v0.4.6.md`
- **Validator (Ship-stopper):** `spec/v0.4.6/PNL-COO-VALIDATOR-v0.4.6.md`

## Validator Gate (必跑)

Run against any XLSX (example sample file):

```bash
python tools/validator_gate.py --sample "NEW-201708_monthly review_financial_Causality.xlsx" --lang en
```

Expected: **PASS** on `VLD-CHART-001 / VLD-AI-001 / VLD-EMPTY-001` and the v0.4.6 core gates.

---


1) Download & unzip this project folder.
2) Double-click **dev.command** at the project root.
3) Your browser should open automatically at port **8001**.

If macOS blocks `dev.command` (Permission denied / “can’t be opened”):

- Finder: right‑click `dev.command` → **Open** (not double‑click) → Open anyway.
- Or Terminal:

```bash
cd "<YOUR_PROJECT_FOLDER>"
chmod +x dev.command
xattr -dr com.apple.quarantine dev.command
./dev.command
```

## .env (recommended)

Keep your secrets locally (do NOT paste keys into chat).

This MVP auto-detects and links a central env file if it exists at:

- `~/Documents/PNL COO/.env`

It then reads variables like:

- `OPENAI_API_KEY=...` (optional; enables Real AI if you implement ai_real.py)
- `OPENAI_MODEL=gpt-5.2` (optional)

You can also set `ENV_PATH` before running to point to any `.env` file.

Quick sanity check: open /api/health and confirm you see the version/build JSON.
If you ever see "Internal Server Error" on the homepage, open /?trace=1 to display the real error details.

---

## What this MVP scaffold includes
- FastAPI backend + single-page dashboard UI (no build step)
- **AI-left + 5-card-right** layout
- Custom **Upload Finance Report** button (hidden native input)
- Upload → basic parsing preview (CSV/XLSX supported; others stubbed)
- Deterministic analysis (no invented numbers) + **COO governance report** generator (Board Pack PDF)
- Radar chart image endpoint (>=8 axes) + **Event → Org Link Map** endpoint
- Bilingual labels (EN/ZH) for headers and chart titles
- **Functional governance filters**: CYCLE / TERMS / MODE / HOLD (v0.4.6 topology)


## v0.4.6 spec patch + validator (embedded)

- Patch doc: `spec/v0.4.6/PNL-COO-SPEC-PATCH-v0.4.6.md`
- Validator: `spec/v0.4.6/PNL-COO-VALIDATOR-v0.4.6.md`

These are shipped with the MVP to prevent spec drift.

## Quick start (manual)

### 1) Python version
This repo expects Python **3.11.9** (pyenv recommended).

```bash
pyenv local 3.11.9
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run server
```bash
uvicorn app.main:app --reload --port 8001
```

Open http://127.0.0.1:8001

---

## Demo (no local Python/dev environment)

If the demo user machine does **not** have a Python dev setup, run the MVP via **Docker**:

1) Install Docker Desktop.
2) In this project folder, create a `.env` file (or rely on your existing env path rules).
3) Run:

```bash
docker compose up --build
```

Open http://127.0.0.1:8000

## Notes / next build steps
- **Real public-company data**: this scaffold does not ship any numbers. Use upload to bring your real files.
- **OCR / PDF**: endpoints are stub-ready; optional dependencies may be needed (tesseract, poppler) depending on file types.
- **ERP protocol connector**: placeholder endpoint exists; we can extend to your connector spec.

## Folder layout
- app/main.py              FastAPI app + routes
- app/services/ingest.py   File ingestion + preview extraction
- app/services/analyze.py  Metric extraction + chart generation
- app/services/report.py   COO governance report generator
- app/templates/index.html UI shell
- app/static/styles.css    Black+Gold+Neon styling
- app/static/app.js        Front-end logic (upload/analyze/render)
- app/config/mappings.yml  Term mapping / topology hints (internal)
- data/uploads/            Uploaded files (local)

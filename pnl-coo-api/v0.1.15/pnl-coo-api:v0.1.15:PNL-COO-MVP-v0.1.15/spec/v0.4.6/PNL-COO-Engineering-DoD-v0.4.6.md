# PNL-COO v0.4.6 — Engineering DoD (Definition of Done)

## Ship Criteria
- All Validator gates PASS.
- XLSX ingestion demo succeeds and populates 5 cards.
- Evidence ledger supports all key outputs.
- No fabricated numbers; missing disclosures handled as Not disclosed.

## Work Plan (Agent-Driven Order)
### P0 — UI & Interaction Gates
- Remove left 'ERP uploaded' block.
- Remove 'Data Preview' block.
- Remove Causality input field.
- Remove Refresh buttons.
- Add fixed 'Back to 5 Cards' in all detail views.
- Normalize banner buttons using v0.4.6 button spec.
- Wire pills CYCLE/TERMS/MODE/HOLD to state + output pipeline.

### P0 — Chart Policy Gates (Bar-only)
- Replace any line chart with bar/stacked bar/waterfall/bullet.
- Implement Scoreboard Primary 5 charts.
- Implement conditional Backup 5 charts.

### P0 — Causality Gates
- Implement 8-axis radar (v0.4.6 library).
- Implement Link Map (Event→Org) with evidence pointers.
- Implement 0–10 drift score pipeline (baseline/delta/confidence).

### P1 — Portfolio & Variance
- Add BCG sub-view.
- Add Budget vs Actual variance when Plan exists; else Not disclosed.

### P1 — EN Gate
- Display alias layer for EN.
- Regex validation: fail build if EN UI contains CJK outside Evidence Pull raw reference.

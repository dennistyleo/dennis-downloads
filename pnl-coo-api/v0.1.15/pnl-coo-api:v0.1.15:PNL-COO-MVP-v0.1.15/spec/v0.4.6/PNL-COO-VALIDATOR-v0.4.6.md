# PNL-COO Validator — v0.4.6 (Ship-Stopper Gates)

Fail any gate → NOT shippable.

## UI Gates
1) 5-card architecture exists; card names unchanged.
2) Each card has its own internal scrollbar.
3) Left-zone "ERP data uploaded" block is removed.
4) Left-zone "Data Preview" block is removed.
5) Causality Radar card has no text input field.
6) No Refresh button exists inside cards.
7) Any expanded card detail view shows fixed **Back to 5 Cards** (same label, placement, style).
8) Banner buttons follow fixed spec (28px height, 64px min width, 14px radius); EN pill must not become a circle.
9) Left-zone pills CYCLE/TERMS/MODE/HOLD are functional and change output behavior.

## Data & Evidence Gates
10) No fabricated numbers. Missing disclosures → Not disclosed + evidence request.
11) Evidence Pull outputs Evidence Ledger: file, sheet, anchor (cell/row/col), value, unit/scale, canonical_metric_id, governance relevance.
12) IMH term mapping works: EN/ZH synonyms, unit scaling, sign conventions.

## Chart Policy Gates
13) No line chart (line+marker) anywhere.
14) Scoreboard outputs Primary 5; Backup 5 is conditional and policy-compliant.

### Hard Gates (MVP v0.1.9 additions)
15) **VLD-CHART-001**: After upload, all chart endpoints must return **HTTP 200 + image/png** (no 500).
    - Applies: /api/chart/scoreboard, /api/chart/radar, /api/chart/linkmap, /api/chart/rev_bridge, /api/chart/gm_bridge, /api/chart/opex_mix, /api/chart/wc_pulse, /api/chart/bcg_customers.
16) **VLD-EMPTY-001**: If analysis is partial or missing data, UI must show an empty-state or fallback chart (no broken image / blank card).
17) **VLD-AI-001**: When file_id exists, built-in AI must not respond with “資料不足/請貼卡片內容”. It must return **system status + reason + next actions**, and log gaps into Evidence Pull backlog.

## Causality Gates
18) Radar has ≥8 axes; axes match v0.4.6 library.
19) Causality includes both: Simple Radar + Link Map (Event→Org), each edge has evidence pointer.

## Language Gate (EN)
20) When Language=EN, UI main text contains no Chinese characters outside Evidence Pull raw reference.

# PNL-COO Spec Patch — v0.4.6 (Additive Hardening, No Layout Regression)

> Additive patch on top of **PNL-COO-SPEC v0.4.5**.  
> **Hard Constraints remain unchanged.**

## 1) UI Hardening (Must Fix)
### 1.1 Remove Non-functional UI Blocks (Left Zone)
- Remove the non-functional "ERP data has been uploaded..." block (entire container).
- Remove the entire "Data Preview" block (entire container and any entry points).

### 1.2 Causality Card Hygiene (Right Zone)
- Remove the text input field inside **Causality Radar** card (no in-card typing).
- Remove all **Refresh** buttons inside cards.

### 1.3 Detail View Navigation
- When any card is expanded to fill the right 5-card zone, a fixed button MUST appear:
  - **Back to 5 Cards**
- Same label, same location, same styling across all cards.

### 1.4 Banner Buttons Consistency (EN should not become a circle)
Default button spec (global):
- height: 28px
- min-width: 64px
- padding: 0 12px
- border-radius: 14px
- font-size: 12px
- line-height: 28px
- border: 1px (Mo-Gold)

## 2) Governance Filters (Left Zone Pills MUST be functional)
Four pills are mandatory and must affect outputs:
- **CYCLE**: Monthly / Quarterly / Yearly → baseline selection (MoM / QoQ / YoY) + chart comparisons
- **TERMS**: Net-30 / Net-70 / Custom → AR/credit/overdue thresholds + narrative
- **MODE**: Evidence-first / Executive-first → ordering + “Need Evidence” list behavior
- **HOLD**: Unknown / Hold-Yes / Hold-No → hypothesis labeling rules

## 3) Charts Policy Update (Bar-only)
- Line charts (line+marker) are disallowed.
- Allowed: bar, stacked bar, waterfall/bridge, bullet, heatmap (optional).

## 4) Causality Radar v0.4.6 (8-Axis Locked + Two Views)
### 4.1 8-Axis Library (Locked)
1. Revenue Drift
2. Customer Concentration & Retention Drift
3. Margin Drift
4. Cost Structure Drift
5. Inventory Health Drift
6. AR Quality & Credit Drift
7. Cash Cycle & Liquidity Drift (DSO/DIO/DPO/CCC directionality)
8. Execution Volatility Drift (rush vs planned orders, forecast variance, terms-behavior shifts)

### 4.2 Two Required Visualizations
- A) Simple 8-axis Radar
- B) Causality Link Map (Event → Org)
  - Left: Events (drift symptoms)
  - Right: Orgs (owners/teams)
  - Every edge MUST carry an evidence pointer (worksheet + cell/row/col anchor).

### 4.3 Score Semantics
- Radar numbers are **0–10 drift/risk scores**, NOT raw finance values.
- Each axis must output: score, baseline, delta, confidence, evidence_anchors
- Missing disclosures → "Not disclosed" (never fabricate).

## 5) Executive Scoreboard (Primary 5 + Backup 5, Bar-only)
Primary 5 (must output):
1) Revenue Bridge (waterfall)
2) Gross Margin Bridge (waterfall)
3) Opex Mix (stacked bar)
4) Profit Snapshot (bars)
5) Working Capital Pulse (4 bars: DSO/DIO/DPO/CCC)

Backup 5 (conditional):
6) Customer Concentration (Top1/Top3/Top5)
7) AR Aging (0–30/31–60/61–90/90+)
8) Inventory Aging (0–30/31–60/61–90/90+)
9) Budget vs Actual Variance (bridge) — only if plan exists; else Not disclosed
10) One-off Items (bars)

## 6) BCG Portfolio Lens (Customer or Product)
- Add as a sub-view inside **Executive Scoreboard detail view**, and used to drive Task Force suggestions.
- Internal-proxy BCG (no external market data required):
  - X: Growth (MoM/QoQ/YoY per CYCLE)
  - Y: Contribution proxy (Revenue share OR GP share; default Revenue share)
- If insufficient periods → mark "Single-period" and do not force quadrant decisions.

## 7) Budget vs Actual Variance
- If workbook provides Plan/Budget values → must compute variance views.
- If not disclosed → show Not disclosed and list required evidence fields.

## 8) Language (EN must not copy Chinese UI text)
- When UI Language=EN:
  - card contents, chart labels, tooltips, captions MUST be in English display aliases
  - Chinese allowed only inside Evidence Pull "raw reference" field, paired with English explanation.

# PNL‑COO MVP QA Report (v0.1.11)

This report is based on your screenshots + the MP4 style targets you described. Goal: **investor‑grade demo credibility** (not GTM).

## A. UI / Visual Spec Issues (Before) → Fix (v0.1.11)

1) **Banner composition wrong**
- **Issue:** Logo/title/buttons crowded in center; left/right empty; gradient start not pure black; logo not “popping”.
- **Fix:** Banner is now a 3‑column grid: **Logo far-left**, **Title+subtitle centered**, **4 buttons right**. Gradient starts at **#000** and gradually brightens to the right.

2) **Buttons not premium / inconsistent sizing**
- **Issue:** AI/version/lang controls didn’t look like real buttons; sizes inconsistent.
- **Fix:** All four are equal-height “engraved LED” pills (neon-green glow + inset shadow) for a higher-end feel.

3) **AI cockpit had an unused mini control**
- **Issue:** Small “+” square in chatbar provides no value and distracts.
- **Fix:** Removed the “+” mini button; input bar is cleaner.

## B. Data Credibility Issues (Before) → Fix (v0.1.11)

4) **Executive Scoreboard numbers impossible**
- **Symptom:** Gross Profit shows a small ratio (e.g., 0.11…) and other KPI rows missing.
- **Root cause:** Row matching could accidentally pick “Gross Profit Margin / 毛利率” rows when extracting “Gross Profit”.
- **Fix:** KPI row search now:
  - prefers exact/startswith matches,
  - penalizes forbidden tokens (margin / % / 率),
  - outputs **Revenue / Gross Profit / Net Profit / OPEX** (more board-friendly than “Operating Income”).

## C. Causality Link Map Readability (Before) → Fix (v0.1.11)

5) **Link map tangled / unreadable**
- **Issue:** Dense lines make it hard to demo causality.
- **Fix:** Link map endpoint returns **premium static map** (EN/ZH) for demo clarity; if missing, it falls back to generated.

## D. Recommended Demo Flow (Investor expectation)

### 1) Two-minute “what you get”
- Upload report → Generate → show **Scoreboard** (4 KPIs) + **CCC drivers**.
- One click: open **Evidence Pull** and show that each KPI can be traced to sheet/anchor.

### 2) Two-minute “why it’s credible”
- Explain: “No invented numbers. When a KPI is missing, it is logged as a mapping gap.”
- Show **Causality Radar** (risk signals) → then **Link Map** (cause→org ownership).

### 3) One-minute “why it’s fundable”
- Close with “evidence-chain governance” + “repeatable ingestion” + “board pack export”.

## E. What’s intentionally Mock (for demo stability)
- AI stays **AI: Mock** in v0.1.11 to keep outcomes deterministic and avoid live-model drift during fundraising demos.

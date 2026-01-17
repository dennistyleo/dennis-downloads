<!-- =========================
     Dennis Leo - Downloads Hub
     index.md (FULL REPLACE)
     ========================= -->

<style>
  :root{
    --bg0:#07080a;
    --bg1:#0b0f12;
    --card: rgba(12,14,16,.62);
    --gold: rgba(180,140,60,.75);
    --gold2: rgba(180,140,60,.35);
    --white: rgba(255,255,255,.92);
    --muted: rgba(255,255,255,.68);
    --muted2: rgba(255,255,255,.52);
    --green: rgba(80,255,120,.92);
    --green2: rgba(80,255,120,.20);
    --shadow: 0 18px 44px rgba(0,0,0,.35);
  }

  /* Page */
  body{
    background: radial-gradient(1200px 700px at 20% 0%, rgba(0,140,70,.18), transparent 55%),
                radial-gradient(900px 600px at 80% 10%, rgba(200,140,40,.14), transparent 58%),
                linear-gradient(180deg, var(--bg0), var(--bg1));
    color: var(--white);
  }

  .dl-wrap{
    max-width: 980px;
    margin: 28px auto 64px;
    padding: 0 18px;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,"PingFang TC","Noto Sans TC",sans-serif;
  }

  /* Top bar */
  .dl-topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    margin-bottom: 18px;
  }
  .dl-brand{
    display:flex;
    align-items:center;
    gap:10px;
    font-weight:900;
    letter-spacing:.2px;
  }
  .dl-brand .dl-sub{
    display:block;
    font-size:12px;
    font-weight:700;
    color: var(--muted2);
    margin-top:2px;
  }
  .dl-actions{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
  }
  .dl-pill{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    padding: 9px 12px;
    border-radius: 999px;
    border: 1px solid var(--gold2);
    background: rgba(0,0,0,.22);
    text-decoration:none;
    color: var(--white);
    font-weight:800;
    font-size:12px;
    box-shadow: 0 0 0 2px rgba(180,140,60,.10) inset;
  }
  .dl-pill:hover{
    transform: translateY(-1px);
    border-color: var(--gold);
    box-shadow: 0 0 0 2px rgba(180,140,60,.16) inset;
  }
  .dl-pill.green{
    border-color: rgba(80,255,120,.55);
    box-shadow: 0 0 0 2px rgba(80,255,120,.10) inset;
  }
  .dl-pill.green:hover{
    border-color: rgba(80,255,120,.9);
    box-shadow: 0 0 0 2px rgba(80,255,120,.18) inset;
  }

  /* Hero */
  .dl-hero{
    border: 1px solid var(--gold2);
    border-radius: 18px;
    background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
    box-shadow: var(--shadow);
    padding: 22px 22px;
    margin: 16px 0 18px;
  }
  .dl-hero h1{
    margin:0 0 8px;
    font-size: 32px;
    line-height:1.08;
    letter-spacing:.2px;
  }
  .dl-hero p{
    margin:0;
    color: var(--muted);
    font-weight:650;
    font-size: 14px;
  }

  /* Section card */
  .dl-card{
    border: 1px solid var(--gold2);
    border-radius: 18px;
    background: var(--card);
    box-shadow: var(--shadow);
    padding: 18px 18px;
    margin-top: 14px;
  }
  .dl-card h2{
    margin: 4px 0 10px;
    font-size: 18px;
    letter-spacing:.2px;
  }
  .dl-note{
    margin: 0 0 12px;
    color: var(--muted2);
    font-size: 13px;
    line-height: 1.45;
  }
  .dl-divider{
    height:1px;
    background: rgba(180,140,60,.22);
    margin: 14px 0;
  }

  /* Download items */
  .dl-item{
    margin: 12px 0 14px;
    padding: 14px 14px;
    border: 1px solid rgba(180,140,60,.22);
    border-radius: 14px;
    background: rgba(0,0,0,.18);
  }
  .dl-name{
    font-weight: 900;
    font-size: 15px;
    color: var(--white);
    margin: 0 0 6px;
  }
  .dl-meta{
    font-weight: 750;
    font-size: 12px;
    color: var(--muted2);
  }
  .dl-label{
    margin-top: 10px;
    font-size: 11px;
    font-weight: 900;
    color: var(--muted2);
    text-transform: uppercase;
    letter-spacing: .55px;
  }
  .dl-btn{
    margin-top: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid rgba(80,255,120,.70);
    background: rgba(0,0,0,.20);
    color: var(--white);
    text-decoration: none;
    font-weight: 950;
    box-shadow: 0 0 0 2px rgba(80,255,120,.10) inset;
    cursor: pointer;
    user-select: none;
    gap: 10px;
  }
  .dl-btn:hover{
    transform: translateY(-1px);
    border-color: rgba(80,255,120,.95);
    box-shadow: 0 0 0 2px rgba(80,255,120,.18) inset;
    background: rgba(0,0,0,.28);
  }
  .dl-fn{
    display:block;
    margin-top: 8px;
    font-size: 12px;
    color: var(--muted2);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
    word-break: break-all;
  }

  /* Footer */
  .dl-footer{
    margin-top: 16px;
    color: var(--muted2);
    font-size: 12px;
    line-height: 1.5;
  }
</style>

<div class="dl-wrap">

  <div class="dl-topbar">
    <div class="dl-brand">
      <div>
        Dennis Leo
        <span class="dl-sub">Official Downloads Hub</span>
      </div>
    </div>

    <div class="dl-actions">
      <a class="dl-pill" href="https://dennisleo.com/watchers-over-the-frontiers-of-innovation" target="_blank" rel="noopener">Main Site</a>
      <a class="dl-pill green" href="mailto:dennis@dennisleo.com">Contact</a>
    </div>
  </div>

  <div class="dl-hero">
    <h1>Documents & Media</h1>
    <p>Significant materials for download — whitepapers, specs, and private demo videos. Support / Contact: dennis@dennisleo.com</p>
  </div>

  <!-- =========================
       Featured Documents
       ========================= -->
  <div class="dl-card">
    <h2>Featured Documents</h2>
    <p class="dl-note">
      Everything below is intentionally “Download-first” so visitors don’t have to guess what is clickable.
    </p>

    <div class="dl-item">
      <div class="dl-name">XR Governance — Uptime (Whitepaper) <span class="dl-meta">(PDF · 20260116 · v01)</span></div>

      <div class="dl-label">Download</div>

      <a class="dl-btn"
         href="https://downloads.dennisleo.com/assets/docs/dlhub-xr-wp-governance-uptime-pdf-20260116-v01.pdf"
         download>
        Download PDF
      </a>

      <span class="dl-fn">dlhub-xr-wp-governance-uptime-pdf-20260116-v01.pdf</span>
    </div>

  </div>

  <!-- =========================
       Investor Demos
       ========================= -->
  <div class="dl-card">
    <h2>Investor Demos</h2>
    <p class="dl-note">
      Videos may still open in-browser on some devices; the button uses the <code>download</code> hint to encourage saving.
      If a browser insists on playing, visitors can still use the viewer’s download icon.
    </p>

    <div class="dl-item">
      <div class="dl-name">XRSHOW EP01 — Full Demo <span class="dl-meta">(MP4 · 20260116 · v02)</span></div>

      <div class="dl-label">Download</div>

      <a class="dl-btn"
         href="https://downloads.dennisleo.com/assets/media/dlhub-xr-demo-investor-xrshow-ep01-full-20260116-v02.mp4"
         download>
        Download MP4
      </a>

      <span class="dl-fn">dlhub-xr-demo-investor-xrshow-ep01-full-20260116-v02.mp4</span>
    </div>

    <div class="dl-item">
      <div class="dl-name">Product Traction — 90s <span class="dl-meta">(MP4 · 20260115 · v01)</span></div>

      <div class="dl-label">Download</div>

      <a class="dl-btn"
         href="https://downloads.dennisleo.com/assets/media/dlhub-xr-demo-investor-product-traction-90s-20260115-v01.mp4"
         download>
        Download MP4
      </a>

      <span class="dl-fn">dlhub-xr-demo-investor-product-traction-90s-20260115-v01.mp4</span>
    </div>

    <div class="dl-item">
      <div class="dl-name">Team Intro — 60s <span class="dl-meta">(MP4 · 20260115 · v01)</span></div>

      <div class="dl-label">Download</div>

      <a class="dl-btn"
         href="https://downloads.dennisleo.com/assets/media/dlhub-xr-demo-investor-team-intro-60s-20260115-v01.mp4"
         download>
        Download MP4
      </a>

      <span class="dl-fn">dlhub-xr-demo-investor-team-intro-60s-20260115-v01.mp4</span>
    </div>

  </div>

  <!-- =========================
       XR Ecosystem Library
       ========================= -->
  <div class="dl-card">
    <h2>XR Ecosystem Library (Specs / Architecture)</h2>
    <p class="dl-note">
      Coming soon (links will appear after files are uploaded; naming already locked).
    </p>

    <div class="dl-item">
      <div class="dl-name">XR Ecosystem — Overview <span class="dl-meta">(PDF · 20260115 · v01)</span></div>
      <div class="dl-label">Status</div>
      <span class="dl-fn">dlhub-xr-wp-ecosystem-overview-pdf-20260115-v01.pdf</span>
    </div>

    <div class="dl-item">
      <div class="dl-name">XR Roadmap — Vision <span class="dl-meta">(PDF · 20260115 · v01)</span></div>
      <div class="dl-label">Status</div>
      <span class="dl-fn">dlhub-xr-wp-roadmap-vision-pdf-20260115-v01.pdf</span>
    </div>

  </div>

  <div class="dl-footer">
    © Dennis Leo · Downloads Hub<br/>
    For access issues or missing links, contact: <a href="mailto:dennis@dennisleo.com" style="color: rgba(80,255,120,.92); text-decoration:none; font-weight:900;">dennis@dennisleo.com</a>
  </div>

</div>

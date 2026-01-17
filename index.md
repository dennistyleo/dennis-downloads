<style>
  :root{
    --bg0:#07080a;
    --bg1:#0b0f12;
    --card:rgba(12,14,16,.62);

    --gold:rgba(180,140,60,.78);
    --gold2:rgba(180,140,60,.35);
    --line:rgba(180,140,60,.22);

    --white:rgba(255,255,255,.92);
    --muted:rgba(255,255,255,.62);

    --green:rgba(80,255,120,.92);
    --shadow:0 18px 44px rgba(0,0,0,.35);
  }

  body{
    margin:0;
    color:var(--white);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,"PingFang TC","Noto Sans TC",sans-serif;
    background:
      radial-gradient(1100px 760px at 18% 8%, rgba(40,170,70,.20), transparent 58%),
      radial-gradient(980px 660px at 82% 12%, rgba(200,140,40,.18), transparent 60%),
      linear-gradient(180deg,var(--bg0),var(--bg1));
  }

  .dl-wrap{max-width:960px;margin:26px auto 64px;padding:0 18px;}

  /* TOP BAR (ONLY ONCE) */
  .dl-topbar{
    display:flex;align-items:center;justify-content:space-between;
    gap:16px;margin-bottom:14px;
  }
  .dl-brand{display:flex;align-items:center;gap:10px;}
  .dl-mark{
    width:30px;height:30px;border-radius:999px;
    display:flex;align-items:center;justify-content:center;
    border:1px solid var(--gold2);
    background:rgba(0,0,0,.22);
    color:var(--gold);
    font-weight:900;
    box-shadow:0 0 0 2px rgba(180,140,60,.10) inset;
  }
  .dl-brand-text{line-height:1.15;}
  .dl-brand-title{font-weight:800;font-size:14px;letter-spacing:.2px;margin:0;}
  .dl-brand-sub{font-size:12px;color:var(--muted);margin:2px 0 0;}

  .dl-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;}
  .dl-pill{
    display:inline-flex;align-items:center;justify-content:center;
    padding:9px 14px;border-radius:999px;
    border:1px solid var(--gold2);
    background:rgba(0,0,0,.22);
    color:var(--white);
    text-decoration:none;
    font-weight:850;font-size:12px;
    box-shadow:0 0 0 2px rgba(180,140,60,.10) inset;
    transition:transform .12s ease, border-color .12s ease, box-shadow .12s ease;
  }
  .dl-pill:hover{transform:translateY(-1px);border-color:var(--gold);}
  .dl-pill-green{
    border-color:rgba(80,255,120,.88);
    background:linear-gradient(180deg, rgba(80,255,120,.30), rgba(80,255,120,.10));
    box-shadow:
      0 0 0 2px rgba(80,255,120,.18) inset,
      0 0 18px rgba(80,255,120,.12);
  }
  .dl-pill-green:hover{
    border-color:rgba(80,255,120,1);
    box-shadow:
      0 0 0 2px rgba(80,255,120,.20) inset,
      0 0 22px rgba(80,255,120,.16);
  }

  /* CARDS */
  .dl-card{
    border:1px solid var(--gold2);
    border-radius:18px;
    background:var(--card);
    box-shadow:var(--shadow);
    padding:22px 22px;
    margin:14px 0;
  }

  /* HEADER AREA */
  .dl-hero h1{
    margin:0 0 10px;
    font-size:34px;
    letter-spacing:.2px;
  }

  /* Instruction box (TOP, meaningful) */
  .dl-instruct{
    border:1px solid var(--line);
    border-radius:16px;
    background:rgba(0,0,0,.18);
    padding:14px 16px;
  }
  .dl-instruct p{
    margin:6px 0;
    color:var(--muted);
    font-size:13px;
    line-height:1.55;
  }
  .dl-instruct b{color:var(--white);}

  .dl-label{
    margin:0 0 10px;
    color:var(--muted);
    font-size:12px;
    font-weight:900;
    letter-spacing:.55px;
    text-transform:uppercase;
  }
  .dl-divider{height:1px;background:var(--line);margin:12px 0 0;}

  /* Download rows */
  .dl-item{
    display:flex;align-items:center;justify-content:space-between;
    gap:14px;
    padding:14px 14px;
    border:1px solid var(--line);
    border-radius:14px;
    background:rgba(0,0,0,.18);
    margin:12px 0;
  }
  .dl-left{min-width:0;}
  .dl-name{
    margin:0;
    font-weight:900;
    font-size:13px;
    letter-spacing:.15px;
  }
  .dl-meta{
    margin-top:6px;
    color:var(--muted);
    font-size:12px;
  }

  /* Buttons */
  .dl-btn{
    display:inline-flex;align-items:center;justify-content:center;
    padding:10px 16px;border-radius:12px;
    text-decoration:none;
    font-weight:950;font-size:12px;
    border:1px solid rgba(80,255,120,.90);
    color:var(--white);
    background:linear-gradient(180deg, rgba(80,255,120,.30), rgba(80,255,120,.08));
    box-shadow:
      0 0 0 2px rgba(80,255,120,.14) inset,
      0 0 18px rgba(80,255,120,.10);
    cursor:pointer;
    white-space:nowrap;
    transition:transform .12s ease, box-shadow .12s ease, border-color .12s ease;
  }
  .dl-btn:hover{
    transform:translateY(-1px);
    border-color:rgba(80,255,120,1);
    box-shadow:
      0 0 0 2px rgba(80,255,120,.18) inset,
      0 0 22px rgba(80,255,120,.14);
  }

  .dl-btn-disabled{
    border:1px solid rgba(255,255,255,.16);
    color:rgba(255,255,255,.55);
    background:rgba(255,255,255,.06);
    box-shadow:none;
    cursor:not-allowed;
    pointer-events:none;
  }

  .dl-footer{
    text-align:center;
    color:var(--muted);
    font-size:12px;
    margin-top:18px;
  }

  @media (max-width:720px){
    .dl-hero h1{font-size:28px;}
    .dl-item{flex-direction:column;align-items:stretch;}
    .dl-btn,.dl-btn-disabled{width:100%;}
    .dl-actions{justify-content:flex-start;}
  }
</style>

<div class="dl-wrap">
  <!-- TOP BAR (ONLY ONCE) -->
  <div class="dl-topbar">
    <div class="dl-brand">
      <div class="dl-mark">D</div>
      <div class="dl-brand-text">
        <p class="dl-brand-title">Dennis Leo</p>
        <p class="dl-brand-sub">Official Downloads Hub</p>
      </div>
    </div>

    <div class="dl-actions">
      <a class="dl-pill" href="https://dennisleo.com/watchers-over-the-frontiers-of-innovation" target="_blank" rel="noopener">Main Site</a>
      <a class="dl-pill dl-pill-green" href="mailto:dennis@dennisleo.com">Contact</a>
    </div>
  </div>

  <!-- HEADER + INSTRUCTION (MEANINGFUL BOX) -->
  <div class="dl-card dl-hero">
    <h1>Downloads</h1>

    <div class="dl-instruct">
      <p><b>Significant materials for download</b> — whitepapers, specs, and private demo videos.</p>
      <p>Support / Contact: <b>dennis@dennisleo.com</b></p>
      <p><b>Download tip:</b> Click the <b>Download</b> button. If the file opens in the browser, use the viewer download icon (⬇︎) to save.  
      To force save: right-click the <b>Download</b> button → <b>Save Link As…</b></p>
    </div>
  </div>

  <!-- LIST -->
  <div class="dl-card">
    <div class="dl-label">Featured</div>

    <div class="dl-item">
      <div class="dl-left">
        <p class="dl-name">XR Governance — Uptime (Whitepaper)</p>
        <div class="dl-meta">PDF · 20260116 · v01</div>
      </div>
      <a class="dl-btn" href="/assets/docs/dlhub-xr-wp-governance-uptime-pdf-20260116-v01.pdf" target="_blank" rel="noopener">Download</a>
    </div>

    <div class="dl-divider"></div>

    <div class="dl-label" style="margin-top:16px;">XR Ecosystem Library (Specs / Architecture)</div>

    <div class="dl-item">
      <div class="dl-left">
        <p class="dl-name">XR Ecosystem — Overview</p>
        <div class="dl-meta">PDF · 20260115 · v01</div>
      </div>
      <span class="dl-btn dl-btn-disabled">Coming soon</span>
    </div>

    <div class="dl-item">
      <div class="dl-left">
        <p class="dl-name">XR Roadmap — Vision</p>
        <div class="dl-meta">PDF · 20260115 · v01</div>
      </div>
      <span class="dl-btn dl-btn-disabled">Coming soon</span>
    </div>
  </div>

  <div class="dl-footer">© 2026 Dennis Leo · downloads.dennisleo.com</div>
</div>

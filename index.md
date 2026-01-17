---
layout: null
---

<style>
:root{
  --bg0:#07080a;
  --bg1:#0b0f12;
  --card:rgba(12,14,16,.65);
  --gold:rgba(180,140,60,.85);
  --gold2:rgba(180,140,60,.28);
  --white:rgba(255,255,255,.95);
  --muted:rgba(255,255,255,.72);
  --shadow:0 18px 44px rgba(0,0,0,.35);
  --green:rgba(73,255,106,1);
}

html,body{height:100%;}
body{
  margin:0;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,"PingFang TC","Noto Sans TC",sans-serif;
  color:var(--white);
  background:
    radial-gradient(1200px 720px at 15% 12%, rgba(0,255,128,.10), transparent 55%),
    radial-gradient(900px 560px at 92% 18%, rgba(255,170,0,.12), transparent 55%),
    linear-gradient(180deg,var(--bg0),var(--bg1));
}

a{color:inherit;}
.wrap{max-width:980px;margin:22px auto 40px;padding:0 18px;}

.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:16px;
}
.brand{display:flex;align-items:center;gap:10px;}
.mark{
  width:34px;height:34px;border-radius:10px;
  border:1px solid var(--gold2);
  display:grid;place-items:center;
  background:rgba(0,0,0,.25);
  box-shadow:0 0 0 2px rgba(180,140,60,.06) inset;
}
.mark span{font-weight:900;letter-spacing:.5px;color:rgba(180,140,60,.95);}
.brandname{line-height:1.1;}
.brandname .t{font-weight:800;font-size:14px;}
.brandname .s{font-size:12px;color:var(--muted);margin-top:2px;}

.actions{display:flex;gap:10px;flex-wrap:wrap;}
.pill{
  display:inline-flex;align-items:center;justify-content:center;
  padding:9px 12px;border-radius:999px;
  border:1px solid var(--gold2);
  background:rgba(0,0,0,.22);
  text-decoration:none;
  font-weight:800;font-size:12px;letter-spacing:.25px;
  box-shadow:0 0 0 2px rgba(180,140,60,.06) inset;
  user-select:none;
}
.pill:hover{transform:translateY(-1px);border-color:var(--gold);}

.pill-green{
  border:1px solid rgba(73,255,106,.55);
  background:linear-gradient(180deg, rgba(73,255,106,.22), rgba(0,0,0,.18));
  box-shadow:
    0 0 0 2px rgba(73,255,106,.10) inset,
    0 6px 16px rgba(0,0,0,.22);
}
.pill-green:hover{border-color:rgba(73,255,106,.95);}

.card{
  border:1px solid var(--gold2);
  border-radius:18px;
  background:var(--card);
  box-shadow:var(--shadow);
  padding:22px 22px;
  margin:14px 0;
}

.title{font-size:34px;font-weight:850;letter-spacing:.2px;margin:0 0 8px;}
.sub{color:var(--muted);font-size:13px;line-height:1.6;margin:0;}
.sub strong{color:var(--white);}

.instruction{
  margin-top:12px;
  padding:12px 14px;
  border-radius:14px;
  border:1px solid rgba(180,140,60,.18);
  background:rgba(0,0,0,.18);
  color:var(--muted);
  font-size:12px;
  line-height:1.6;
}

.section{margin-top:18px;}
.section h2{
  margin:0 0 10px;
  font-size:12px;
  letter-spacing:1.2px;
  color:rgba(255,255,255,.78);
  text-transform:uppercase;
}

.list{
  border:1px solid rgba(180,140,60,.16);
  border-radius:16px;
  overflow:hidden;
  background:rgba(0,0,0,.12);
}

.item{
  display:flex;
  gap:14px;
  align-items:center;
  justify-content:space-between;
  padding:14px 14px;
  border-top:1px solid rgba(180,140,60,.12);
}
.item:first-child{border-top:none;}

.left{min-width:0;}
.name{font-weight:850;font-size:13px;margin:0 0 4px;}
.meta{font-size:12px;color:var(--muted);margin:0;}
.path{margin-top:8px;font-size:12px;color:rgba(255,255,255,.60);}
.path code{
  font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;
  font-size:11px;
  background:rgba(0,0,0,.22);
  border:1px solid rgba(180,140,60,.12);
  padding:2px 6px;
  border-radius:9px;
}

.btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  padding:10px 14px;
  border-radius:12px;
  border:1px solid rgba(73,255,106,.55);
  background:linear-gradient(180deg, rgba(73,255,106,.25), rgba(0,0,0,.18));
  box-shadow:
    0 0 0 2px rgba(73,255,106,.08) inset,
    0 6px 16px rgba(0,0,0,.25);
  text-decoration:none;
  font-weight:900;
  font-size:12px;
  letter-spacing:.3px;
  white-space:nowrap;
  cursor:pointer;
  user-select:none;
}
.btn:hover{
  transform:translateY(-1px);
  border-color:rgba(73,255,106,.95);
  box-shadow:
    0 0 0 2px rgba(73,255,106,.14) inset,
    0 10px 22px rgba(0,0,0,.30);
}
.btn-disabled{
  opacity:.55;
  border-color:rgba(180,140,60,.22);
  background:rgba(0,0,0,.18);
  box-shadow:none;
  cursor:not-allowed;
  pointer-events:none;
}

.footer{margin-top:16px;text-align:center;color:rgba(255,255,255,.60);font-size:12px;}

@media (max-width:640px){
  .title{font-size:26px;}
  .item{flex-direction:column;align-items:flex-start;}
}
</style>

<div class="wrap">
  <!-- SINGLE topbar (only one logo + one set of buttons) -->
  <div class="topbar">
    <div class="brand">
      <div class="mark" aria-hidden="true"><span>D</span></div>
      <div class="brandname">
        <div class="t">Dennis Leo</div>
        <div class="s">Official Downloads Hub</div>
      </div>
    </div>
    <div class="actions">
      <a class="pill" href="https://dennisleo.com/watchers-over-the-frontiers-of-innovation" target="_blank" rel="noopener">Main Site</a>
      <a class="pill pill-green" href="mailto:dennis@dennisleo.com">Contact</a>
    </div>
  </div>

  <div class="card">
    <h1 class="title">Downloads</h1>
    <p class="sub">Significant materials for download — whitepapers, specs, and private demo videos.</p>
    <p class="sub"><strong>Support / Contact:</strong> <a href="mailto:dennis@dennisleo.com">dennis@dennisleo.com</a></p>

    <div class="instruction">
      <strong>Download instruction:</strong> Click the <strong>Download</strong> button.
      If a PDF/MP4 opens in the browser, use the viewer’s download icon (⬇︎).
      To force save: right-click the <strong>Download</strong> button → <strong>Save Link As…</strong>
    </div>

    <div class="section">
      <h2>Featured</h2>
      <div class="list">
        <div class="item">
          <div class="left">
            <div class="name">XR Governance — Uptime (Whitepaper)</div>
            <div class="meta">PDF • 20260116 • v01</div>
            <div class="path"><code>/assets/docs/dlhub-xr-wp-governance-uptime-pdf-20260116-v01.pdf</code></div>
          </div>
          <a class="btn" href="/assets/docs/dlhub-xr-wp-governance-uptime-pdf-20260116-v01.pdf" download>Download</a>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>XR Ecosystem Library (Specs / Architecture)</h2>
      <div class="list">
        <div class="item">
          <div class="left">
            <div class="name">XR Ecosystem — Overview</div>
            <div class="meta">PDF • 20260115 • v01</div>
            <div class="path"><code>dlhub-xr-wp-ecosystem-overview-pdf-20260115-v01.pdf</code></div>
          </div>
          <span class="btn btn-disabled">Coming soon</span>
        </div>

        <div class="item">
          <div class="left">
            <div class="name">XR Roadmap — Vision</div>
            <div class="meta">PDF • 20260115 • v01</div>
            <div class="path"><code>dlhub-xr-wp-roadmap-vision-pdf-20260115-v01.pdf</code></div>
          </div>
          <span class="btn btn-disabled">Coming soon</span>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">© 2026 Dennis Leo • downloads.dennisleo.com</div>
</div>

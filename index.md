---
layout: null
---

<style>
:root{
  --bg0:#07080a;
  --bg1:#0b0f12;
  --card:rgba(12,14,16,.62);
  --gold:rgba(180,140,60,.75);
  --gold2:rgba(180,140,60,.35);
  --white:rgba(255,255,255,.92);
  --muted:rgba(255,255,255,.62);
  --shadow:0 18px 44px rgba(0,0,0,.35);
  --green:rgba(80,255,120,.70);
  --green2:rgba(80,255,120,.20);
}

html,body{height:100%}
body{
  margin:0;
  background:
    radial-gradient(1200px 700px at 20% 0%, rgba(0,140,70,.18), transparent 55%),
    radial-gradient(900px 600px at 80% 10%, rgba(200,140,40,.14), transparent 60%),
    linear-gradient(180deg,var(--bg0),var(--bg1));
  color:var(--white);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,"PingFang TC","Noto Sans TC",sans-serif;
}

a{color:inherit; text-decoration:none}
a:hover{opacity:.95}

.dl-wrap{
  max-width:980px;
  margin:28px auto 64px;
  padding:0 18px;
}

.dl-topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  margin-bottom:18px;
}

.dl-brand{
  display:flex;
  align-items:center;
  gap:10px;
}

.dl-logo{
  width:34px;height:34px;
  border-radius:10px;
  border:1px solid var(--gold2);
  box-shadow:0 0 0 2px rgba(180,140,60,.10) inset;
  display:grid;
  place-items:center;
  font-weight:900;
  color:rgba(180,140,60,.95);
  background:rgba(0,0,0,.22);
}

.dl-brand-name{
  font-weight:800;
  letter-spacing:.3px;
  font-size:13px;
  line-height:1.1;
}
.dl-brand-sub{
  font-size:12px;
  color:var(--muted);
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
  padding:8px 12px;
  border-radius:999px;
  border:1px solid var(--gold2);
  background:rgba(0,0,0,.22);
  font-weight:800;
  font-size:12px;
  color:var(--white);
  box-shadow:0 0 0 2px rgba(180,140,60,.10) inset;
}

.dl-pill:hover{
  transform:translateY(-1px);
  border-color:var(--gold);
}

.dl-pill-green{
  border-color:rgba(80,255,120,.55);
  box-shadow:0 0 0 2px rgba(80,255,120,.18) inset;
}
.dl-pill-green:hover{
  border-color:rgba(80,255,120,.90);
}

.dl-hero{
  border:1px solid var(--gold2);
  border-radius:18px;
  background:linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
  box-shadow:var(--shadow);
  padding:22px 22px;
  margin:16px 0 14px;
}

.dl-hero h1{
  margin:0 0 6px;
  font-size:32px;
  letter-spacing:.2px;
}

.dl-hero p{
  margin:0;
  color:var(--muted);
  font-size:13px;
  line-height:1.55;
}

.dl-support{
  margin-top:10px !important;
  color:var(--muted);
}
.dl-support a{
  color:var(--white);
  text-decoration:underline;
  text-underline-offset:3px;
}

.dl-card{
  border:1px solid var(--gold2);
  border-radius:18px;
  background:var(--card);
  box-shadow:var(--shadow);
  padding:18px 18px;
  margin-top:14px;
}

.dl-label{
  margin:0 0 10px;
  color:var(--muted);
  font-size:12px;
  font-weight:900;
  letter-spacing:.55px;
  text-transform:uppercase;
}

.dl-divider{
  height:1px;
  background:rgba(180,140,60,.22);
  margin:12px 0;
}

.dl-note{
  color:var(--muted);
  font-size:12px;
  line-height:1.55;
}

.dl-item{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding:12px 12px;
  border-radius:14px;
  border:1px solid rgba(180,140,60,.22);
  background:rgba(0,0,0,.18);
  margin-top:10px;
}

.dl-item:hover{
  border-color:rgba(180,140,60,.55);
  background:rgba(0,0,0,.24);
}

.dl-item-left{
  min-width:0;
}

.dl-title{
  font-weight:900;
  font-size:13px;
  letter-spacing:.2px;
  margin:0 0 4px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.dl-meta{
  font-size:12px;
  color:var(--muted);
}

.dl-btn{
  display:inl

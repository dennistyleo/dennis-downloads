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
    background: rgba

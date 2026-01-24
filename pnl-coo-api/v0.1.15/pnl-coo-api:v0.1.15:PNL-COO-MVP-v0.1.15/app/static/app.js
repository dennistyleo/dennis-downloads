/* PNL-COO MVP (demo-ready)
 * UI LOCK:
 * - Banner: left logo on black, center title/subtitle, right 3 equal buttons
 * - Layout: left AI cockpit (single large log + upload + generate + compact input)
 *           right 5 cards (top 1 + bottom 4), each card has header + internal scroll
 */

const STATE = {
  lang: "en",
  file_id: null,
  filename: null,
  // "AI Mock" switch (banner): when true, the UI can render the premium demo pack
  // even before an XLSX is uploaded.
  demoCharts: true,
  lens: { cycle: "MOM", terms: "AUTO", mode: "AUTO", hold: "OFF" },
};

function setAiMock(on){
  STATE.demoCharts = !!on;
  localStorage.setItem("pnlcoo.demoCharts", STATE.demoCharts ? "1" : "0");
  const btn = $("btnAiMock");
  if (btn){
    btn.setAttribute("aria-pressed", STATE.demoCharts ? "true" : "false");
    btn.classList.toggle("is-off", !STATE.demoCharts);
  }
  // Re-render charts in-place (do not destroy chat history)
  renderCharts();
}

const I18N = {
  en: {
    uploadOk: (f) => `ERP export uploaded: ${f}`,
    uploadFail: "Upload failed. Please try again.",
    analyzeStart: "Generating governance brief…",
    analyzeOk: "Updated. You can click any card to open Focus View.",
    analyzeFail: "Generate failed. Please check DevTools Console (Errors) and try again.",
    needFile: "Upload an ERP export (XLSX) to start the demo.",
    promptHead: "PROMPT INPUT: ASK A COO QUESTION / GIVE AN INSTRUCTION",
    cards: {
      score: "Executive Scoreboard",
      radar: "Causality Radar",
      cash: "Cash Cycle Drivers",
      evidence: "Evidence Pull",
      task: "Solution Taskforce Matrix",
      radarA: "A) 8-axis Radar",
      radarB: "B) Event → Org Link Map",
    },
  },
  zh: {
    uploadOk: (f) => `已上傳 ERP 匯出：${f}`,
    uploadFail: "上傳失敗，請重試。",
    analyzeStart: "正在產出治理摘要…",
    analyzeOk: "已更新。點選任何卡片可進入 Focus View。",
    analyzeFail: "Generate 失敗。請查看 DevTools Console (Errors) 後重試。",
    needFile: "請先上傳 ERP 匯出檔 (XLSX) 以開始 Demo。",
    promptHead: "PROMPT INPUT: ASK A COO QUESTION / GIVE AN INSTRUCTION",
    cards: {
      score: "Executive Scoreboard",
      radar: "Causality Radar",
      cash: "Cash Cycle Drivers",
      evidence: "Evidence Pull",
      task: "Solution Taskforce Matrix",
      radarA: "A) 8 軸 Radar",
      radarB: "B) 事件 → 組織 關聯圖",
    },
  },
};

function $(id){ return document.getElementById(id); }

function safeText(s){ return (s==null) ? "" : String(s); }

function setStatus(text){
  $("statusLine").textContent = safeText(text);
}

function addLog(role, text){
  const el = document.createElement("div");
  el.className = `msg ${role}`;
  const tag = role === "ai" ? "AI" : (role === "user" ? "YOU" : "SYSTEM");
  el.innerHTML = `<span class="tag">${tag}</span>${escapeHtml(text).replace(/\n/g,"<br>")}`;
  $("cockpitLog").appendChild(el);
  $("cockpitLog").scrollTop = $("cockpitLog").scrollHeight;
}

function escapeHtml(str){
  return safeText(str)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

function detectDemoCharts(filename){
  const f = (filename || "").toLowerCase();
  // Heuristic for the provided demo file: NEW-201708_monthly review_financial_Causality.xlsx
  return f.includes("201708") || (f.includes("2017") && f.includes("monthly")) || f.includes("causality");
}

function chartSrc(kind){
  const q = new URLSearchParams({
    file_id: STATE.file_id || "",
    lang: STATE.lang,
    cycle: STATE.lens.cycle,
    terms: STATE.lens.terms,
    mode: STATE.lens.mode,
    hold: STATE.lens.hold,
  });

  if (STATE.demoCharts){
    const base = "/static/charts/ebn_2017_08/";
    const map = {
      score_main: "02_executive_profitability_grouped.png",
      score_rev: "01_executive_revenue_bar.png",
      score_cash: "03_executive_earnings_vs_cash.png",
      score_opex: "04_executive_opex_bar.png",
      cash: "05_cash_cycle_drivers_grouped.png",
      radar: "11_causality_radar.png",
      // linkmap uses a premium static pack to avoid tangled lines
      linkmap: null,
      evidence: "13_evidence_ledger_example.png",
      task: "15_solution_task_force_matrix.png",
      drift: "12_causality_drift_flow.png",
    };
    if (kind === "linkmap"){
      return `/static/linkmap_premium_${STATE.lang}.png`;
    }
    if (map[kind]) return base + map[kind];
  }

  const apiMap = {
    score_main: "/api/chart/scoreboard",
    radar: "/api/chart/radar",
    linkmap: "/api/chart/linkmap",
    cash: "/api/chart/wc_pulse",
    evidence: "/api/chart/rev_bridge",
    task: "/api/chart/bcg_customers",
  };
  const path = apiMap[kind];
  if (!path) return "";
  // Avoid calling backend with an empty file_id (prevents noisy errors in demo flows).
  if (!STATE.file_id) return "";
  return `${path}?${q.toString()}`;
}

function setLang(lang){
  STATE.lang = (lang === "zh") ? "zh" : "en";
  $("btnLangEn").setAttribute("aria-pressed", STATE.lang === "en" ? "true" : "false");
  $("btnLangZh").setAttribute("aria-pressed", STATE.lang === "zh" ? "true" : "false");

  const t = I18N[STATE.lang];
  $("promptHead").textContent = t.promptHead;
  $("scoreHd").textContent = t.cards.score;
  $("radarHd").textContent = t.cards.radar;
  $("cashHd").textContent = t.cards.cash;
  $("evidenceHd").textContent = t.cards.evidence;
  $("taskHd").textContent = t.cards.task;
  $("radarCapA").textContent = t.cards.radarA;
  $("radarCapB").textContent = t.cards.radarB;

  // Re-render in demo mode OR after file loaded.
  if (STATE.file_id || STATE.demoCharts){
    renderCharts();
  }
}

function setLens(partial){
  STATE.lens = { ...STATE.lens, ...partial };
  $("btnCycle").textContent = `CYCLE: ${STATE.lens.cycle}`;
  $("btnTerms").textContent = `TERMS: ${STATE.lens.terms}`;
  $("btnMode").textContent = `MODE: ${STATE.lens.mode}`;
  $("btnHold").textContent = `HOLD: ${STATE.lens.hold}`;
  if (STATE.file_id || STATE.demoCharts){ renderCharts(); }
}

function renderKpis(kpis){
  const row = $("kpiRow");
  row.innerHTML = "";
  (kpis || []).slice(0,6).forEach(k => {
    const div = document.createElement("div");
    div.className = "kpi";
    div.innerHTML = `
      <div class="kpi-lbl">${escapeHtml(k.label || k.k || "")}</div>
      <div class="kpi-val">${escapeHtml(k.value || k.v || "")}</div>
      <div class="kpi-dlt">${escapeHtml(k.delta || k.d || "")}</div>
    `;
    row.appendChild(div);
  });
}

function defaultCardNotes(){
  if (STATE.lang === "en"){
    return {
      score: "Chart-first KPIs + AI brief to preserve insight and challenge outdated assumptions.",
      radar: "Signals are symptoms. Evidence confirms root causes. Ownership maps execution.",
      cash: "Finance → operational levers. DSO / DIO / DPO drive CCC.",
      evidence: "No evidence, no decision. Pull audit-ready traces before declaring RCA.",
      task: "Route causality into accountable execution: Action | Owner | Due.",
    };
  }
  return {
    score: "以圖表為主的 KPI + 私人 AI brief，保留洞察、挑戰過期假設。",
    radar: "Signal 是症狀，Evidence 才能定因；Ownership 才能落地。",
    cash: "財務 → 營運槓桿。DSO / DIO / DPO 共同決定 CCC。",
    evidence: "沒有證據就不下結論。先 Pull 可稽核的 trace，再談 RCA。",
    task: "把因果路由成可問責的行動：Action | Owner | Due。",
  };
}

function renderCharts(){
  // Scoreboard
  $("scoreChartMain").src = chartSrc("score_main");

  // Radar + linkmap
  $("radarChart").src = chartSrc("radar");
  $("linkMapChart").src = chartSrc("linkmap");

  // Other cards
  $("cashChart").src = chartSrc("cash");
  $("evidenceChart").src = chartSrc("evidence");
  $("taskChart").src = chartSrc("task");
}

async function upload(file){
  const t = I18N[STATE.lang];
  try{
    const fd = new FormData();
    fd.append("file", file);
    const r = await fetch("/api/upload", { method:"POST", body: fd });
    const j = await r.json().catch(()=> ({}));
    if (!r.ok || !j.ok){ throw new Error(j.error || `HTTP ${r.status}`); }

    STATE.file_id = j.file_id;
    STATE.filename = j.filename || file.name;
    STATE.demoCharts = detectDemoCharts(STATE.filename);

    localStorage.setItem("pnlcoo.file_id", STATE.file_id);
    localStorage.setItem("pnlcoo.filename", STATE.filename);

    addLog("system", t.uploadOk(STATE.filename));
    setStatus(`file_id=${STATE.file_id} | ${STATE.filename}`);

    // Update images immediately (pre-generate, to avoid blank cards in demo)
    renderCharts();

    return true;
  }catch(e){
    console.error(e);
    addLog("system", t.uploadFail);
    setStatus(`upload error: ${e}`);
    return false;
  }
}

async function analyze(){
  const t = I18N[STATE.lang];
  if (!STATE.file_id){
    addLog("system", t.needFile);
    return;
  }

  setStatus(t.analyzeStart);

  const prompt = $("chatInput").value.trim();
  if (prompt){ addLog("user", prompt); }

  const payload = {
    file_id: STATE.file_id,
    lang: STATE.lang,
    cycle: STATE.lens.cycle,
    terms: STATE.lens.terms,
    mode: STATE.lens.mode,
    hold: STATE.lens.hold,
    prompt: prompt || "Generate governance brief and populate all cards.",
  };

  try{
    const r = await fetch("/api/analyze", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload),
    });
    const j = await r.json().catch(()=> ({}));
    if (!r.ok || !j.ok){ throw new Error(j.error || `HTTP ${r.status}`); }

    // KPIs
    renderKpis(j.kpis || j.scoreboard_kpis || []);

    // Notes / narratives
    const notes = defaultCardNotes();
    $("scoreNarrative").textContent = safeText(j.ai_brief || j.executive_summary || notes.score);
    $("radarLegend").textContent = safeText(j.radar_legend || notes.radar);
    $("cashNote").textContent = safeText(j.cash_note || notes.cash);
    $("evidenceNote").textContent = safeText(j.evidence_note || notes.evidence);
    $("taskNote").textContent = safeText(j.task_note || notes.task);

    // Ensure charts always point to something non-empty
    renderCharts();

    // Add AI brief to cockpit log
    addLog("ai", safeText(j.ai_brief || notes.score));

    $("chatInput").value = "";
    setStatus(t.analyzeOk);
  }catch(e){
    console.error(e);
    addLog("system", t.analyzeFail);
    setStatus(`analyze error: ${e}`);
  }
}

async function chat(){
  const text = $("chatInput").value.trim();
  if (!text){ return; }
  if (!STATE.file_id){
    addLog("system", I18N[STATE.lang].needFile);
    return;
  }
  addLog("user", text);
  $("chatInput").value = "";

  try{
    const r = await fetch("/api/chat", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({
        file_id: STATE.file_id,
        lang: STATE.lang,
        message: text,
        cycle: STATE.lens.cycle,
        terms: STATE.lens.terms,
        mode: STATE.lens.mode,
        hold: STATE.lens.hold,
      }),
    });
    const j = await r.json().catch(()=> ({}));
    if (!r.ok || !j.ok){ throw new Error(j.error || `HTTP ${r.status}`); }
    addLog("ai", safeText(j.reply || ""));
  }catch(e){
    console.error(e);
    addLog("system", `Chat error: ${e}`);
  }
}

function openFocus(kind){
  const focus = $("focus");
  document.body.classList.add("focus-mode");
  focus.setAttribute("aria-hidden", "false");

  const titles = {
    score: STATE.lang === "zh" ? "Executive Scoreboard（Focus）" : "Executive Scoreboard (Focus)",
    radar: STATE.lang === "zh" ? "Causality Radar（Focus）" : "Causality Radar (Focus)",
    cash: STATE.lang === "zh" ? "Cash Cycle Drivers（Focus）" : "Cash Cycle Drivers (Focus)",
    evidence: STATE.lang === "zh" ? "Evidence Pull（Focus）" : "Evidence Pull (Focus)",
    task: STATE.lang === "zh" ? "Solution Taskforce Matrix（Focus）" : "Solution Taskforce Matrix (Focus)",
  };
  $("focusTitle").textContent = titles[kind] || "Focus";

  // Focus content: larger chart(s) + a compact explanation
  let html = "";

  if (kind === "score"){
    const imgs = STATE.demoCharts
      ? [
          ["Profitability", chartSrc("score_main")],
          ["Revenue", chartSrc("score_rev")],
          ["Earnings vs Cash", chartSrc("score_cash")],
          ["OPEX", chartSrc("score_opex")],
        ]
      : [["Scoreboard", chartSrc("score_main")]];

    html += `<div class="focus-stack">`;
    imgs.forEach(([cap, src]) => {
      html += `<div><div style="font-weight:950;margin:6px 0">${escapeHtml(cap)}</div><img class="chart" style="display:block;max-height:360px" src="${src}" alt="${escapeHtml(cap)}"></div>`;
    });
    html += `</div>`;
  }

  if (kind === "radar"){
    html += `
      <div class="focus-stack">
        <div style="font-weight:950;margin:6px 0">Radar</div>
        <img class="chart" style="display:block;max-height:360px" src="${chartSrc("radar")}" alt="Radar">
        <div style="font-weight:950;margin:16px 0 6px 0">Event → Org Link Map</div>
        <img class="chart" style="display:block;max-height:360px" src="${chartSrc("linkmap")}" alt="Link Map">
        ${STATE.demoCharts ? `<div style="font-weight:950;margin:16px 0 6px 0">Drift Flow</div>
        <img class="chart" style="display:block;max-height:360px" src="${chartSrc("drift")}" alt="Drift Flow">` : ""}
      </div>
    `;
  }

  if (kind === "cash"){
    html += `<div class="focus-stack"><img class="chart" style="display:block;max-height:520px" src="${chartSrc("cash")}" alt="Cash"></div>`;
  }

  if (kind === "evidence"){
    html += `<div class="focus-stack"><img class="chart" style="display:block;max-height:520px" src="${chartSrc("evidence")}" alt="Evidence"></div>`;
  }

  if (kind === "task"){
    html += `<div class="focus-stack"><img class="chart" style="display:block;max-height:520px" src="${chartSrc("task")}" alt="Task"></div>`;
  }

  $("focusBody").innerHTML = html || "—";
}

function closeFocus(){
  document.body.classList.remove("focus-mode");
  $("focus").setAttribute("aria-hidden", "true");
}

function bind(){
  // Banner: AI Mock switch
  $("btnAiMock").addEventListener("click", () => setAiMock(!STATE.demoCharts));

  // Lang
  $("btnLangEn").addEventListener("click", () => setLang("en"));
  $("btnLangZh").addEventListener("click", () => setLang("zh"));

  // File upload
  $("btnUpload").addEventListener("click", () => $("fileInput").click());
  $("fileInput").addEventListener("change", async (e) => {
    const f = (e.target.files || [])[0];
    if (f) await upload(f);
  });

  // Generate
  $("btnGenerate").addEventListener("click", analyze);

  // Chat
  $("btnSend").addEventListener("click", chat);
  $("chatInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") chat();
  });

  // Focus handlers
  $("card-score").addEventListener("click", () => openFocus("score"));
  $("card-radar").addEventListener("click", () => openFocus("radar"));
  $("card-cash").addEventListener("click", () => openFocus("cash"));
  $("card-evidence").addEventListener("click", () => openFocus("evidence"));
  $("card-task").addEventListener("click", () => openFocus("task"));
  $("btnBack").addEventListener("click", closeFocus);

  // Lens toggles (simple cycling, deterministic)
  const cycle = ["MOM", "QOQ", "YOY", "ROLLING3", "ROLLING6"];
  const terms = ["AUTO", "NET70", "GM", "OPEX", "CCC"];
  const mode = ["AUTO", "EVIDENCE_FIRST", "ACTION_FIRST"];
  const hold = ["OFF", "ON"];

  $("btnCycle").addEventListener("click", () => {
    const i = cycle.indexOf(STATE.lens.cycle);
    setLens({ cycle: cycle[(i+1) % cycle.length] });
  });
  $("btnTerms").addEventListener("click", () => {
    const i = terms.indexOf(STATE.lens.terms);
    setLens({ terms: terms[(i+1) % terms.length] });
  });
  $("btnMode").addEventListener("click", () => {
    const i = mode.indexOf(STATE.lens.mode);
    setLens({ mode: mode[(i+1) % mode.length] });
  });
  $("btnHold").addEventListener("click", () => {
    const i = hold.indexOf(STATE.lens.hold);
    setLens({ hold: hold[(i+1) % hold.length] });
  });
}

function restore(){
  // Restore AI Mock switch first
  const demoPref = localStorage.getItem("pnlcoo.demoCharts");
  if (demoPref !== null){
    STATE.demoCharts = (demoPref === "1");
  }
  setAiMock(STATE.demoCharts);

  const fid = localStorage.getItem("pnlcoo.file_id");
  const fname = localStorage.getItem("pnlcoo.filename");
  if (fid){
    STATE.file_id = fid;
    STATE.filename = fname || null;
    // If user didn't explicitly pin AI Mock, auto-detect demo dataset from filename
    if (demoPref === null){
      STATE.demoCharts = detectDemoCharts(STATE.filename);
      setAiMock(STATE.demoCharts);
    }
    setStatus(`file_id=${STATE.file_id}${STATE.filename ? " | " + STATE.filename : ""}`);
    addLog("system", `Restored session. file_id=${STATE.file_id}`);
    renderCharts();
  } else {
    // Demo pack can render without upload
    if (STATE.demoCharts){
      addLog("system", "AI Mock is ON — rendering demo charts without upload.");
      renderCharts();
    } else {
      addLog("system", I18N[STATE.lang].needFile);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  bind();
  restore();
  // Apply UI defaults after restore (avoids flicker when AI Mock is OFF)
  setLang(STATE.lang || "en");
  setLens({});
});

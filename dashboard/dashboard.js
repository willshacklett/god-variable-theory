// dashboard.js (updated)
// Adds support for SAFE_REFUSAL + gv_state + goodness_ratio if present

const CSV_CANDIDATES = [
  "../data/longitudinal/summary_history_binned.csv",
  "../data/longitudinal/summary_history.csv",
];

const $ = (id) => document.getElementById(id);

const state = {
  timer: null,
  csvPath: null,
  rows: [],
  headers: [],
};

function setStatus(msg) {
  $("status").textContent = msg;
}

function fmt(x, digits = 4) {
  const n = Number(x);
  if (!Number.isFinite(n)) return String(x ?? "");
  return n.toFixed(digits);
}

function labelForRow(r) {
  const action = (r.safety_action || "").toUpperCase();
  if (action === "SAFE_REFUSAL") return "SAFE";
  // Prefer explicit gv_state if present
  const gvState = (r.gv_state || "").toUpperCase();
  if (gvState === "GOOD") return "GOOD";
  if (gvState === "BAD") return "BAD";
  return ""; // fall back to heuristic
}

function clsForRow(r) {
  const action = (r.safety_action || "").toUpperCase();
  if (action === "SAFE_REFUSAL") return "good"; // SAFE is good behavior

  const gvState = (r.gv_state || "").toUpperCase();
  if (gvState === "GOOD") return "good";
  if (gvState === "BAD") return "bad";

  // heuristic mapping (fallback if gv_state not present)
  const rec = Number(r.final_recoverability ?? r.recoverability);
  const dgv = Number(r.final_cum_abs_dgv ?? r.cum_abs_dgv ?? r.final_cum_dgv);
  const peak = Number(r.peak_abs_ds_dt ?? r.peak_ds_dt ?? r.peak_abs_dsdt);

  if (Number.isFinite(rec)) {
    if (rec < 0.35) return "bad";
    if (rec < 0.60) return "warn";
  }
  if (Number.isFinite(dgv)) {
    if (dgv > 0.9) return "bad";
    if (dgv > 0.4) return "warn";
  }
  if (Number.isFinite(peak)) {
    if (peak > 0.005) return "warn";
  }
  return "good";
}

function parseCSV(text) {
  const lines = text.replace(/\r/g, "").split("\n").filter(Boolean);
  if (!lines.length) return { headers: [], rows: [] };

  const parseLine = (line) => {
    const out = [];
    let cur = "";
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (ch === "," && !inQuotes) {
        out.push(cur);
        cur = "";
      } else {
        cur += ch;
      }
    }
    out.push(cur);
    return out.map((s) => s.trim());
  };

  const headers = parseLine(lines[0]);
  const rows = lines.slice(1).map((ln) => {
    const vals = parseLine(ln);
    const r = {};
    headers.forEach((h, idx) => (r[h] = vals[idx] ?? ""));
    return r;
  });

  return { headers, rows };
}

function pickLatestPerScenario(rows) {
  const score = (r) => {
    const t = r.run_created_utc || r.run_created || r.created_utc || "";
    const n = Number(r.run_number);
    return [t, Number.isFinite(n) ? n : -1];
  };

  const byScenario = new Map();
  for (const r of rows) {
    const scen = r.scenario || r.case || "unknown";
    if (!byScenario.has(scen)) {
      byScenario.set(scen, r);
      continue;
    }
    const cur = byScenario.get(scen);
    const [t1, n1] = score(cur);
    const [t2, n2] = score(r);
    if ((t2 && t2 > t1) || (t2 === t1 && n2 > n1)) {
      byScenario.set(scen, r);
    }
  }

  return Array.from(byScenario.entries())
    .map(([scenario, row]) => ({ scenario, row }))
    .sort((a, b) => a.scenario.localeCompare(b.scenario));
}

function sortNewestFirst(rows) {
  const pickTime = (r) => r.run_created_utc || r.run_created || r.created_utc || "";
  const pickRun = (r) => {
    const n = Number(r.run_number);
    return Number.isFinite(n) ? n : -1;
  };

  return [...rows].sort((a, b) => {
    const ta = pickTime(a), tb = pickTime(b);
    if (tb !== ta) return tb.localeCompare(ta);
    return pickRun(b) - pickRun(a);
  });
}

function renderTiles(latest) {
  const tiles = $("tiles");
  tiles.innerHTML = "";

  for (const { scenario, row } of latest) {
    const riskClass = clsForRow(row);
    const label = labelForRow(row) || riskClass.toUpperCase();

    const rec = row.final_recoverability ?? row.recoverability ?? "";
    const dgv = row.final_cum_abs_dgv ?? row.cum_abs_dgv ?? "";
    const peak = row.peak_abs_ds_dt ?? row.peak_ds_dt ?? "";

    const action = row.safety_action ?? "";
    const reason = row.interlock_reason ?? "";
    const ratio = row.goodness_ratio ?? "";

    const run = row.run_number ?? "";
    const sha = (row.git_sha ?? "").slice(0, 10);
    const when = row.run_created_utc ?? "";

    const el = document.createElement("div");
    el.className = "tile";
    el.innerHTML = `
      <div class="k">
        <div class="name">${scenario}</div>
        <div class="pill ${riskClass}">${label}</div>
      </div>

      <div class="metric">
        <div class="box">
          <div class="label">final_recoverability</div>
          <div class="val">${fmt(rec, 4)}</div>
        </div>
        <div class="box">
          <div class="label">final_cum_abs_dgv</div>
          <div class="val">${fmt(dgv, 4)}</div>
        </div>
      </div>

      <div class="hr"></div>

      <div class="small">
        peak_abs_ds_dt: <span class="${riskClass}">${fmt(peak, 6)}</span><br/>
        safety_action: <code>${action || "—"}</code> ${reason ? `(${reason})` : ""}<br/>
        goodness_ratio: <code>${ratio || "—"}</code><br/>
        run: <code>${run}</code> &nbsp; sha: <code>${sha || "—"}</code><br/>
        <span class="muted">${when || ""}</span>
      </div>
    `;
    tiles.appendChild(el);
  }
}

function renderTable(tableId, headers, rows, limit) {
  const table = $(tableId);
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  thead.innerHTML = "";
  tbody.innerHTML = "";

  const showRows = limit ? rows.slice(0, limit) : rows;
  const trh = document.createElement("tr");
  for (const h of headers) {
    const th = document.createElement("th");
    th.textContent = h;
    trh.appendChild(th);
  }
  thead.appendChild(trh);

  for (const r of showRows) {
    const tr = document.createElement("tr");
    for (const h of headers) {
      const td = document.createElement("td");
      td.textContent = r[h] ?? "";
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
}

async function fetchFirstAvailableCSV() {
  for (const p of CSV_CANDIDATES) {
    try {
      const url = `${p}?_=${Date.now()}`;
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) continue;
      const text = await res.text();
      if (!text.trim()) continue;
      return { path: p, text };
    } catch (e) {}
  }
  throw new Error("No CSV found. Expected data/longitudinal/*.csv in repo.");
}

async function loadAndRender() {
  const started = Date.now();
  setStatus("Loading CSV…");

  const { path, text } = await fetchFirstAvailableCSV();
  state.csvPath = path;

  const parsed = parseCSV(text);
  state.headers = parsed.headers;
  state.rows = parsed.rows;

  if (!state.headers.length || !state.rows.length) {
    setStatus("CSV loaded but empty.");
    return;
  }

  const newest = sortNewestFirst(state.rows);
  const latestPerScenario = pickLatestPerScenario(newest);

  renderTiles(latestPerScenario);

  const preferred = [
    "scenario",
    "safety_action",
    "interlock_reason",
    "gv_state",
    "goodness_ratio",
    "final_recoverability",
    "final_cum_abs_dgv",
    "peak_abs_ds_dt",
    "peak_s_total",
    "monitor_alpha",
    "monitor_beta",
    "monitor_gamma",
    "run_number",
    "run_created_utc",
    "git_sha",
  ];
  const latestHeaders = preferred.filter((h) => state.headers.includes(h));
  const useLatestHeaders = latestHeaders.length ? latestHeaders : state.headers;

  const latestRows = latestPerScenario.map((x) => x.row);
  renderTable("latestTable", useLatestHeaders, latestRows);

  renderTable("tailTable", useLatestHeaders, newest, 50);

  $("meta").textContent = `rows: ${state.rows.length} • scenarios: ${latestPerScenario.length}`;
  $("csvPathLabel").textContent = path;

  const ms = Date.now() - started;
  setStatus(`Updated • ${ms}ms`);
}

function startAutoRefresh() {
  stopAutoRefresh();
  state.timer = setInterval(() => {
    if ($("autoRefresh").checked) {
      loadAndRender().catch((e) => setStatus(`Error: ${e.message}`));
    }
  }, 60_000);
}

function stopAutoRefresh() {
  if (state.timer) clearInterval(state.timer);
  state.timer = null;
}

function wireUI() {
  $("btnReload").addEventListener("click", () => {
    loadAndRender().catch((e) => setStatus(`Error: ${e.message}`));
  });

  $("autoRefresh").addEventListener("change", () => {
    if ($("autoRefresh").checked) startAutoRefresh();
    else stopAutoRefresh();
  });
}

(async function init(){
  wireUI();
  try {
    await loadAndRender();
  } catch (e) {
    setStatus(`Error: ${e.message}`);
  }
  startAutoRefresh();
})();

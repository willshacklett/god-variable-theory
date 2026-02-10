// Dashboard reads repo CSV and renders:
// 1) tiles per scenario (latest row)
// 2) a "latest rows" table
// 3) a "tail rows" table (last 50 rows)
//
// CSV path choice:
// - First tries the binned file (recommended)
// - Falls back to summary_history.csv if binned doesn't exist
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

function clsForRisk(r) {
  // heuristic mapping:
  // - if recoverability is low => bad
  // - if cum_abs_dgv or peak_dsdt is high => warn/bad
  const rec = Number(r.final_recoverability);
  const dgv = Number(r.final_cum_abs_dgv);
  const peak = Number(r.peak_abs_ds_dt);

  // Some binned files may rename columns; try alternates
  const rec2 = Number(r.recoverability ?? r.final_recoverability);
  const dgv2 = Number(r.cum_abs_dgv ?? r.final_cum_abs_dgv ?? r.final_cum_dgv);
  const peak2 = Number(r.peak_ds_dt ?? r.peak_abs_ds_dt ?? r.peak_abs_dsdt);

  const R = Number.isFinite(rec) ? rec : rec2;
  const D = Number.isFinite(dgv) ? dgv : dgv2;
  const P = Number.isFinite(peak) ? peak : peak2;

  if (Number.isFinite(R)) {
    if (R < 0.35) return "bad";
    if (R < 0.60) return "warn";
  }
  if (Number.isFinite(D)) {
    if (D > 0.9) return "bad";
    if (D > 0.4) return "warn";
  }
  if (Number.isFinite(P)) {
    if (P > 0.005) return "warn";
  }
  return "good";
}

function parseCSV(text) {
  // Minimal CSV parser that handles commas + quotes.
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
  // Prefer ordering by run_created_utc, else by run_number, else by appearance order.
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

    // Compare time first (ISO string sorts), then run_number
    if ((t2 && t2 > t1) || (t2 === t1 && n2 > n1)) {
      byScenario.set(scen, r);
    }
  }

  return Array.from(byScenario.entries())
    .map(([scenario, row]) => ({ scenario, row }))
    .sort((a, b) => a.scenario.localeCompare(b.scenario));
}

function renderTiles(latest) {
  const tiles = $("tiles");
  tiles.innerHTML = "";

  for (const { scenario, row } of latest) {
    const riskClass = clsForRisk(row);

    const rec = row.final_recoverability ?? row.recoverability ?? "";
    const dgv = row.final_cum_abs_dgv ?? row.cum_abs_dgv ?? "";
    const peak = row.peak_abs_ds_dt ?? row.peak_ds_dt ?? "";
    const run = row.run_number ?? "";
    const sha = (row.git_sha ?? "").slice(0, 10);
    const when = row.run_created_utc ?? "";

    const el = document.createElement("div");
    el.className = "tile";
    el.innerHTML = `
      <div class="k">
        <div class="name">${scenario}</div>
        <div class="pill ${riskClass}">${riskClass.toUpperCase()}</div>
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
      const url = `${p}?_=${Date.now()}`; // cache-buster
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) continue;
      const text = await res.text();
      if (!text.trim()) continue;
      return { path: p, text };
    } catch (e) {
      // try next
    }
  }
  throw new Error("No CSV found. Expected data/longitudinal/*.csv in repo.");
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

  // Sort newest first for tables
  const newest = sortNewestFirst(state.rows);

  // Pick latest per scenario for tiles + latest table
  const latestPerScenario = pickLatestPerScenario(newest);
  renderTiles(latestPerScenario);

  // Latest table headers: pick a useful subset first, else fallback to all
  const preferred = [
    "scenario",
    "final_recoverability",
    "final_cum_abs_dgv",
    "peak_abs_ds_dt",
    "peak_s_total",
    "monitor_alpha",
    "monitor_beta",
    "monitor_gamma",
    "monitor_threshold",
    "run_number",
    "run_created_utc",
    "git_sha",
  ];
  const latestHeaders = preferred.filter((h) => state.headers.includes(h));
  const useLatestHeaders = latestHeaders.length ? latestHeaders : state.headers;

  const latestRows = latestPerScenario.map((x) => x.row);
  renderTable("latestTable", useLatestHeaders, latestRows);

  // Tail table: show last 50 rows, newest first
  const tailHeaders = useLatestHeaders; // keep consistent
  renderTable("tailTable", tailHeaders, newest, 50);

  // Meta + footer
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

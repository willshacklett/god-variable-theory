// Dashboard reads repo CSV via raw.githubusercontent.com
// Update OWNER/REPO if you fork/rename.
const OWNER = "willshacklett";
const REPO = "god-variable-theory";
const BRANCH = "main";
const CSV_PATH = "data/longitudinal/summary_history.csv";

const srcEl = document.getElementById("src");
const statusEl = document.getElementById("status");
const refreshEl = document.getElementById("refresh");
const scenarioEl = document.getElementById("scenario");
const sortEl = document.getElementById("sort");
const reloadBtn = document.getElementById("reload");
const kpisEl = document.getElementById("kpis");
const theadEl = document.getElementById("thead");
const tbodyEl = document.getElementById("tbody");

let timer = null;
let lastRows = [];

function rawUrl() {
  // cache-bust with timestamp so we always see newest
  const t = Date.now();
  return `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}/${CSV_PATH}?t=${t}`;
}

function setStatus(text, ok = true) {
  statusEl.textContent = text;
  statusEl.style.borderColor = ok ? "rgba(52,211,153,0.25)" : "rgba(248,113,113,0.25)";
  statusEl.style.color = ok ? "#34d399" : "#f87171";
}

function parseCSV(text) {
  // Minimal CSV parser (handles commas + quotes)
  const rows = [];
  let i = 0, field = "", row = [], inQuotes = false;

  while (i < text.length) {
    const c = text[i];

    if (c === '"') {
      if (inQuotes && text[i + 1] === '"') { field += '"'; i += 2; continue; }
      inQuotes = !inQuotes; i++; continue;
    }

    if (!inQuotes && (c === "," || c === "\n" || c === "\r")) {
      if (c === "\r") { i++; continue; }
      row.push(field);
      field = "";
      if (c === "\n") { rows.push(row); row = []; }
      i++;
      continue;
    }

    field += c;
    i++;
  }

  // flush last field
  if (field.length || row.length) { row.push(field); rows.push(row); }

  const header = rows.shift();
  if (!header) return [];

  return rows
    .filter(r => r.length && r.some(x => (x || "").trim() !== ""))
    .map(r => {
      const obj = {};
      header.forEach((h, idx) => obj[h] = (r[idx] ?? "").trim());
      return obj;
    });
}

function num(x, fallback = NaN) {
  const v = Number(x);
  return Number.isFinite(v) ? v : fallback;
}

function unique(arr) {
  return Array.from(new Set(arr));
}

function renderScenarioOptions(rows) {
  const scenarios = unique(rows.map(r => r.scenario).filter(Boolean)).sort();
  const current = scenarioEl.value;
  scenarioEl.innerHTML = `<option value="">All</option>` + scenarios.map(s => `<option value="${s}">${s}</option>`).join("");
  if (scenarios.includes(current)) scenarioEl.value = current;
}

function applyFilters(rows) {
  const scenario = scenarioEl.value;
  let out = rows.slice();
  if (scenario) out = out.filter(r => r.scenario === scenario);

  const [key, dir] = sortEl.value.split(":");
  out.sort((a, b) => {
    const av = (key.includes("utc") || key.includes("sha") || key.includes("run_") || key === "scenario")
      ? (a[key] || "")
      : num(a[key], -Infinity);

    const bv = (key.includes("utc") || key.includes("sha") || key.includes("run_") || key === "scenario")
      ? (b[key] || "")
      : num(b[key], -Infinity);

    if (typeof av === "number" && typeof bv === "number") return dir === "asc" ? av - bv : bv - av;
    return dir === "asc" ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
  });

  return out;
}

function badgeRecoverability(r) {
  const v = num(r.final_recoverability, NaN);
  if (!Number.isFinite(v)) return `<span class="badge">n/a</span>`;
  if (v < 0.4) return `<span class="badge bad">${v.toFixed(3)}</span>`;
  return `<span class="badge good">${v.toFixed(3)}</span>`;
}

function renderKPIs(rows) {
  if (!rows.length) {
    kpisEl.innerHTML = `<div class="kpi"><div class="label">No data</div><div class="val">—</div></div>`;
    return;
  }

  // newest row by run_created_utc (string ISO sorts fine)
  const newest = rows.slice().sort((a,b) => String(b.run_created_utc).localeCompare(String(a.run_created_utc)))[0];

  const scenarios = unique(rows.map(r => r.scenario).filter(Boolean));
  const runs = unique(rows.map(r => r.run_id).filter(Boolean));

  kpisEl.innerHTML = `
    <div class="kpi">
      <div class="label">Rows tracked</div>
      <div class="val">${rows.length}</div>
      <div class="tiny">${runs.length} runs • ${scenarios.length} scenarios</div>
    </div>
    <div class="kpi">
      <div class="label">Latest run</div>
      <div class="val">${newest.run_number || "—"}</div>
      <div class="tiny">${newest.run_created_utc || "—"}</div>
    </div>
    <div class="kpi">
      <div class="label">Latest scenario</div>
      <div class="val">${newest.scenario || "—"}</div>
      <div class="tiny">Recoverability: ${badgeRecoverability(newest)}</div>
    </div>
  `;
}

function renderTable(rows) {
  if (!rows.length) {
    theadEl.innerHTML = "";
    tbodyEl.innerHTML = `<tr><td>No rows to display.</td></tr>`;
    return;
  }

  // show a curated set first; keep the rest if you want later
  const cols = [
    "run_number",
    "scenario",
    "final_recoverability",
    "final_cum_abs_dgv",
    "peak_abs_ds_dt",
    "monitor_threshold",
    "monitor_gamma",
    "run_created_utc",
    "git_sha"
  ];

  theadEl.innerHTML = `<tr>${cols.map(c => `<th>${c}</th>`).join("")}</tr>`;

  tbodyEl.innerHTML = rows.map(r => {
    const rec = badgeRecoverability(r);
    const cum = Number.isFinite(num(r.final_cum_abs_dgv)) ? num(r.final_cum_abs_dgv).toFixed(3) : "n/a";
    const peak = Number.isFinite(num(r.peak_abs_ds_dt)) ? num(r.peak_abs_ds_dt).toFixed(6) : "n/a";
    const thr = r.monitor_threshold || "n/a";
    const gam = r.monitor_gamma || "n/a";
    const sha = (r.git_sha || "").slice(0, 7);

    return `
      <tr>
        <td>${r.run_number || ""}</td>
        <td>${r.scenario || ""}</td>
        <td>${rec}</td>
        <td>${cum}</td>
        <td>${peak}</td>
        <td>${thr}</td>
        <td>${gam}</td>
        <td>${(r.run_created_utc || "").replace("T", " ").slice(0, 19)}</td>
        <td title="${r.git_sha || ""}">${sha}</td>
      </tr>
    `;
  }).join("");
}

async function load() {
  const url = rawUrl();
  srcEl.textContent = url;

  setStatus("loading…", true);
  try {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const text = await res.text();
    lastRows = parseCSV(text);

    setStatus(`ok • ${lastRows.length} rows`, true);
    renderScenarioOptions(lastRows);

    const filtered = applyFilters(lastRows);
    renderKPIs(lastRows);
    renderTable(filtered);
  } catch (e) {
    console.error(e);
    setStatus(`error • ${String(e.message || e)}`, false);
  }
}

function setTimer() {
  if (timer) clearInterval(timer);
  timer = null;

  const sec = Number(refreshEl.value);
  if (sec > 0) {
    timer = setInterval(load, sec * 1000);
  }
}

reloadBtn.addEventListener("click", load);
refreshEl.addEventListener("change", setTimer);
scenarioEl.addEventListener("change", () => renderTable(applyFilters(lastRows)));
sortEl.addEventListener("change", () => renderTable(applyFilters(lastRows)));

setTimer();
load();

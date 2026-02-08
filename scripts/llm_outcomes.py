from __future__ import annotations

import csv
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


SUMMARY_CSV = "data/longitudinal/summary_history.csv"
OUT_DIR = "data/longitudinal"
OUT_CSV = os.path.join(OUT_DIR, "llm_outcomes.csv")
OUT_MD = os.path.join(OUT_DIR, "llm_outcomes_latest.md")


@dataclass
class Verdict:
  provider: str
  model: str
  risk_label: str
  rationale: str


def read_latest_rows(path: str, max_rows: int = 3) -> List[Dict[str, str]]:
  with open(path, "r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
  # take latest by run_created_utc (ISO string sorts)
  rows.sort(key=lambda r: (r.get("run_created_utc") or ""), reverse=True)
  return rows[:max_rows]


def build_payload(rows: List[Dict[str, str]]) -> Dict[str, Any]:
  # Only share minimal metrics (no code, no repo content)
  keep = [
    "scenario",
    "final_recoverability",
    "final_cum_abs_dgv",
    "peak_abs_ds_dt",
    "peak_s_total",
    "monitor_alpha",
    "monitor_beta",
    "monitor_gamma",
    "monitor_threshold",
    "run_created_utc",
    "run_number",
    "git_sha",
  ]
  trimmed = [{k: r.get(k, "") for k in keep} for r in rows]
  return {
    "project": "god-variable-theory",
    "purpose": "Assess stability and risk from longitudinal GV metrics. Output a simple risk label and a brief rationale.",
    "rows": trimmed,
  }


def parse_verdict(text: str, provider: str, model: str) -> Verdict:
  """
  Expect the model to respond with:
  RISK: <LOW|MEDIUM|HIGH>
  WHY: <one paragraph>
  """
  risk = "UNKNOWN"
  why = text.strip()

  for line in text.splitlines():
    if line.strip().upper().startswith("RISK:"):
      risk = line.split(":", 1)[1].strip().upper()
    if line.strip().upper().startswith("WHY:"):
      why = line.split(":", 1)[1].strip()
      # grab remainder too
      rest = "\n".join(text.splitlines()[text.splitlines().index(line)+1:]).strip()
      if rest:
        why = (why + "\n" + rest).strip()
      break

  # normalize
  if risk not in {"LOW", "MEDIUM", "HIGH"}:
    risk = "UNKNOWN"

  return Verdict(provider=provider, model=model, risk_label=risk, rationale=why[:1200])


def call_openai(api_key: str, payload: Dict[str, Any]) -> Optional[Verdict]:
  # Uses OpenAI Responses API style payload (simple, robust)
  # If your account requires a specific model name, change OPENAI_MODEL env var.
  model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
  url = "https://api.openai.com/v1/responses"

  prompt = f"""
You are an external evaluator. You will be given JSON metrics from automated simulations.
Return EXACTLY:

RISK: LOW|MEDIUM|HIGH
WHY: <short rationale referencing the metrics and scenarios>

JSON:
{json.dumps(payload, indent=2)}
""".strip()

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
  }
  data = {
    "model": model,
    "input": prompt,
  }

  r = requests.post(url, headers=headers, json=data, timeout=60)
  if r.status_code >= 300:
    print("OpenAI error:", r.status_code, r.text[:500])
    return None

  out = r.json()
  # Responses API can return in several shapes; easiest is to pull "output_text"
  text = out.get("output_text")
  if not text:
    # fallback: try to stitch from output blocks
    try:
      blocks = out["output"][0]["content"]
      text = "\n".join([b.get("text", "") for b in blocks if b.get("type") == "output_text"]).strip()
    except Exception:
      text = ""
  if not text:
    return None

  return parse_verdict(text, provider="openai", model=model)


def call_xai(api_key: str, payload: Dict[str, Any]) -> Optional[Verdict]:
  # xAI API endpoint may differ depending on your plan/product.
  # Set XAI_BASE_URL if needed.
  base = os.getenv("XAI_BASE_URL", "https://api.x.ai")
  model = os.getenv("XAI_MODEL", "grok-2-latest")
  url = f"{base}/v1/chat/completions"

  prompt = f"""
You are an external evaluator. You will be given JSON metrics from automated simulations.
Return EXACTLY:

RISK: LOW|MEDIUM|HIGH
WHY: <short rationale referencing the metrics and scenarios>

JSON:
{json.dumps(payload, indent=2)}
""".strip()

  headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
  }
  data = {
    "model": model,
    "messages": [
      {"role": "system", "content": "You are a rigorous safety evaluator."},
      {"role": "user", "content": prompt},
    ],
    "temperature": 0.2,
  }

  r = requests.post(url, headers=headers, json=data, timeout=60)
  if r.status_code >= 300:
    print("xAI error:", r.status_code, r.text[:500])
    return None

  out = r.json()
  text = out.get("choices", [{}])[0].get("message", {}).get("content", "")
  if not text:
    return None

  return parse_verdict(text, provider="xai", model=model)


def ensure_header(path: str, fieldnames: List[str]) -> None:
  if os.path.exists(path) and os.path.getsize(path) > 0:
    return
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()


def append_outcome(out_path: str, row: Dict[str, Any]) -> None:
  fieldnames = list(row.keys())
  ensure_header(out_path, fieldnames)
  with open(out_path, "a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writerow(row)


def write_latest_md(md_path: str, payload: Dict[str, Any], verdicts: List[Verdict]) -> None:
  now = datetime.now(timezone.utc).isoformat()
  lines = []
  lines.append("# LLM Outcomes (latest)\n")
  lines.append(f"- updated_utc: `{now}`\n")
  lines.append("## Input rows\n")
  lines.append("```json\n" + json.dumps(payload, indent=2) + "\n```\n")
  lines.append("## Verdicts\n")
  for v in verdicts:
    lines.append(f"### {v.provider} / {v.model}\n")
    lines.append(f"- **RISK:** `{v.risk_label}`\n")
    lines.append(f"- **WHY:** {v.rationale}\n")
  os.makedirs(os.path.dirname(md_path), exist_ok=True)
  with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines).strip() + "\n")


def main() -> None:
  if not os.path.exists(SUMMARY_CSV):
    raise SystemExit(f"Missing {SUMMARY_CSV}. Run metrics collection first.")

  latest = read_latest_rows(SUMMARY_CSV, max_rows=3)
  payload = build_payload(latest)

  verdicts: List[Verdict] = []

  openai_key = os.getenv("OPENAI_API_KEY", "").strip()
  if openai_key:
    v = call_openai(openai_key, payload)
    if v:
      verdicts.append(v)

  xai_key = os.getenv("XAI_API_KEY", "").strip()
  if xai_key:
    v = call_xai(xai_key, payload)
    if v:
      verdicts.append(v)

  if not verdicts:
    print("No LLM keys set (OPENAI_API_KEY / XAI_API_KEY). Skipping outcomes.")
    return

  # Save outcomes
  now = datetime.now(timezone.utc).isoformat()
  # Store one row per provider for the same snapshot
  for v in verdicts:
    row = {
      "recorded_utc": now,
      "provider": v.provider,
      "model": v.model,
      "risk_label": v.risk_label,
      "rationale": v.rationale.replace("\n", " ").strip(),
      # Include an anchor to the newest run id/sha for traceability
      "latest_run_number": latest[0].get("run_number", ""),
      "latest_run_id": latest[0].get("run_id", ""),
      "latest_git_sha": (latest[0].get("git_sha", "") or "")[:12],
      "scenario": latest[0].get("scenario", ""),
    }
    append_outcome(OUT_CSV, row)

  write_latest_md(OUT_MD, payload, verdicts)
  print(f"Wrote: {OUT_CSV}")
  print(f"Wrote: {OUT_MD}")


if __name__ == "__main__":
  main()

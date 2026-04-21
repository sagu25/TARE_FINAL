# TARE — Setup & Run Guide
### Trusted Access Response Engine · Energy & Utilities Security Platform
*POC Demo — Internal Use Only*

---

## What This Is

TARE is a post-grant identity security platform for autonomous AI agents
operating on critical infrastructure. It detects and responds to behavioural
anomalies in real time — even when the agent's credentials are completely valid.

**12-agent architecture across 4 zones:**

| Zone | Name | Agents | Role |
|------|------|--------|------|
| Z3 — Reef | Observe & Recommend | KORAL · MAREA · TASYA · NEREUS | Telemetry, drift analysis, context, recommendation |
| Z2 — Shelf | Diagnose & Prepare | ECHO · SIMAR · NAVIS · RISKADOR | Diagnostics, simulation, planning, risk scoring |
| Z1 — Trench | Execute with Safety | TRITON · AEGIS · TEMPEST · LEVIER | Execution, safety validation, tempo, rollback |
| Z4 | Policy Enforcement | BARRIER | Sole ALLOW/DENY gateway authority |

**Four attack scenarios demonstrated:**

| # | Name | Type | Key Agents |
|---|---|---|---|
| 1 | 🕒 OUT-OF-HOURS | High-impact action outside approved window | TASYA · BARRIER |
| 2 | 🔁 REPEATED FAILURES | Unsafe persistence — retrying a blocked action | TEMPEST · BARRIER |
| 3 | 🔄 RUNAWAY LOOP | Automation bug — valid command at machine speed | TEMPEST · BARRIER |
| 4 | 🚫 READ-ONLY BREACH | Identity policy violation — write from read-only role | KORAL · BARRIER |

---

## Requirements

```
python --version    ✅ Need Python 3.10+
```

Node.js only needed if editing and rebuilding the frontend. Not required to run the demo.

---

## Step 1 — Get Your Groq API Key

All six scenario buttons require a free Groq API key.

1. Go to **console.groq.com**
2. Sign up (free) → Create an API key → Copy it

---

## Step 2 — Install Backend Dependencies (First Time Only)

```
cd aegis-poc\backend
pip install -r requirements.txt
```

If pip fails due to firewall:
```
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

## Step 3 — Set the Groq API Key (Optional — for Ask TARE chat only)

Scenarios run without a Groq key. The key is only needed for the **Ask TARE** chat interface.

Create `backend/.env` containing:
```
GROQ_API_KEY=your_actual_key_here
```

Without a key, Ask TARE returns a plain session summary instead of an LLM-written answer.

---

## Step 4 — Train the ML Model (First Time Only)

```
cd aegis-poc\ml
python generate_grid_data.py
python train_model.py
```

Creates `ml/model.pkl`. Only needed once.

---

## Step 5 — Start the Server

From the `aegis-poc` folder:

```
cd aegis-poc
python run.py
```

Expected output:
```
═══════════════════════════════════════════
  TARE - Trusted Access Response Engine
═══════════════════════════════════════════

  Starting server on port 8050...
  Browser will open at:  http://localhost:8050

  Press Ctrl+C to stop.
```

The server auto-finds a free port between 8050–8100 and opens your browser automatically.

Leave this window open throughout the demo.

---

## Step 6 — Open the App

The browser opens automatically. If it doesn't:
```
http://localhost:8050
```

The **animated landing page** loads first.

---

## Step 7 — Landing Page

The landing page displays:
- **Maturity Journey** — Manual → Automated → Autonomous
- **What TARE Monitors** — 6 parameters in plain English
- **▶ Play Narration** — starts voice walkthrough on demand (browser Text-to-Speech, no install needed)
- **Launch Demo →** — fades into the main dashboard

**Narrated presentation flow:**
1. Click **▶ Play Narration** to start the voice walkthrough
2. Click **Launch Demo →** when ready — narration continues seamlessly on dashboard
3. Use the **narration controls** in the Live Event Monitor (right panel) to pause/mute/resume at any time

**Manual presentation:**
1. Walk through landing page yourself
2. Click **Launch Demo →** to enter dashboard

---

## Step 8 — Run the Scenarios

All four scenarios are in the **▶ Scenarios ▼** dropdown on the right panel. Each scenario shows a **briefing card** before running — read it, then click **▶ Run Scenario**.

| Scenario | What to watch | Supervisor action |
|---|---|---|
| 🕒 OUT-OF-HOURS | Reads allowed → OPEN_BREAKER blocked at 02:30 → TASYA + BARRIER speak → ServiceNow P2 raised | **Approve 15-min Emergency Window** (executes the one command under BARRIER oversight) — or leave blocked. Then Reset. |
| 🔁 REPEATED FAILURES | BARRIER denies 4× → on 3rd retry TEMPEST fires → FREEZE + siren | No button — P1 incident raised automatically. Click Reset. |
| 🔄 RUNAWAY LOOP | 8 identical commands in <3s → TEMPEST detects loop on 5th → SAFETY HOLD (no approval needed) | No button — TARE acts autonomously. P1 auto-raised. Click Reset. |
| 🚫 READ-ONLY BREACH | 2 reads allowed → write attempt blocked → KORAL logs → BARRIER enforces READ_ONLY_DOWNGRADE | No button — DOWNGRADE applied, P2 raised. Click Reset. |

**Always click ↺ Reset between scenarios.**

---

## What You Will See

### Agent Voices
Each of the 12 agents + BARRIER speaks aloud during scenarios using the browser's built-in Text-to-Speech. Every agent has a distinct voice (pitch, rate, accent) so you can tell them apart. Use the **🔊 On / 🔇 Muted** button in the left panel Agents tab to toggle agent voices independently of narration.

### Narration Controls (Live Event Monitor — right panel)
- **▶ Start / ⏸ Pause** — play or pause narration
- **■ Stop** — end narration
- **🔊 / 🔇** — mute toggle

### Narrative Banner (top scrolling ticker)
Plain-English description of what is happening.
Shows TARE lifecycle: NORMAL → FREEZE → DOWNGRADE → TIME-BOX → SAFE

### Zone Observatory (centre)
Live SVG grid map. Click any zone to open the **Zone Info Modal**:
- **Left:** live Leaflet GIS map (real London geography, power line overlays)
- **Centre:** zone type, fault alert, description + **Active Agents** (2-per-row chips, hover for role details)
- **Right:** asset cards (BRK + FDR) with live state badges

### Left Panel (4 tabs)
- **⬡ Agents** *(default tab)* — live status of all 12 agents across 3 zones + BARRIER. Agents pulse when active. Shows zone groupings (Reef/Shelf/Trench), per-agent stats, activity log, and pipeline output
- **👤 Operator Agent** — identity, role, clearance, RBAC zones, last command
- **⚡ TARE Response** — mode ladder, anomaly score, deviation signals. Auto-switches here when anomaly fires
- **🎫 Incident** — ServiceNow incident auto-created on TARE fire with P1/P2/P3 priority badge. Auto-switches here when incident is created

### Right Panel
- **Live Event Monitor** — 6 source chips, stats, latest event
- **▶ Scenarios** dropdown — all six scenarios
- **↺ Reset** — resets everything to clean state

### Bottom Tabs
- **🛡 Command Gateway** — every command with ALLOW/DENY, policy, zone, asset
- **💬 Ask TARE** — LLM-written supervisor briefing + Approve/Deny buttons + chat interface
- **📋 Activity** — real-time feed with local timestamps

### Ask TARE — Chat Interface
Type any question about session activity or historical data:

| Question type | Example | Source |
|---|---|---|
| Current session | "Any rogue agents?" | Live engine snapshot |
| Current session | "Show session summary" | Live engine snapshot |
| Current session | "Any freeze events?" | Live engine snapshot |
| Historical | "How many rogue agents in the past 30 days?" | 30-day audit data |
| Historical | "Any scope creep last month?" | 30-day audit data |
| Historical | "Identity mismatches recently?" | 30-day audit data |
| Historical | "ML anomalies this week?" | 30-day audit data |

**Keywords that trigger historical mode:** *past, last, days, weeks, months, history, recently, till now, so far*

---

## ServiceNow Priority Classification

| Priority | Badge | Triggered by |
|---|---|---|
| 🔴 P1 — Critical | Red | BURST_RATE, repeated unsafe retries, runaway loop |
| 🟠 P2 — High | Orange | OUT_OF_HOURS, identity policy violation |

Scenario mapping:
- **P1:** Repeated Failures, Runaway Loop
- **P2:** Out-of-Hours, Read-Only Breach

---

## Supervisor Decision Buttons

Appear in the **Ask TARE** tab when a scenario requires human approval:

| Button | Scenario | What happens |
|---|---|---|
| **✓ Approve 15-min Emergency Window** | OUT-OF-HOURS | AEGIS validates safety → TRITON executes the single blocked command → BARRIER monitors for 15 minutes. Window expires automatically. |
| **✕ Deny / Escalate** | OUT-OF-HOURS | Command stays blocked. Incident remains open. DOWNGRADE holds. |

Repeated Failures, Runaway Loop, and Read-Only Breach do **not** show an Approve button — TARE acts autonomously on those.

---

## Port Conflict (Windows)

`run.py` automatically finds a free port between 8050–8100. If all ports in that range are taken:
```
cd aegis-poc\backend
python -m uvicorn main:app --port 8200 --host 0.0.0.0
```

---

## Rebuilding the Frontend (Only If You Edit Source)

```
cd aegis-poc\frontend
npm install        (first time only)
npm run build
cp -r dist/. ../backend/static/
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| **● OFFLINE in header** | Backend not running. Run `python run.py` again. |
| **Blank page** | Check the port printed in the terminal (e.g. `http://localhost:8050`). |
| **Port already in use** | `run.py` auto-selects next free port — check terminal output for actual URL. |
| **Scenarios do nothing** | Check server is running (`● LIVE` in header). Scenarios don't require Groq key. |
| **Ask TARE returns plain summary** | Groq key missing or invalid. Check `backend/.env`. |
| **Agent halted: 429** | Groq rate limit on Ask TARE chat. Wait 30 seconds. |
| **No voice narration** | Click anywhere on page first (browser requires a user gesture), then click ▶ Play Narration. |
| **Agents not speaking** | Check 🔊 On button in left panel Agents tab — may be muted. |
| **pip install fails** | Add `--trusted-host pypi.org` flag. |

---

## Quick Reference

```
FIRST TIME SETUP
────────────────
cd aegis-poc\ml
python generate_grid_data.py && python train_model.py

cd ..\backend
pip install -r requirements.txt
Create .env → GROQ_API_KEY=your_key

EVERY TIME YOU DEMO
────────────────────
cd aegis-poc
python run.py
Browser opens automatically → Landing page → Launch Demo →
Confirm ● LIVE in header

DEMO ORDER
──────────
↺ Reset → 🕒 OUT-OF-HOURS      → Approve 15-min  (time-context enforcement)
↺ Reset → 🔁 REPEATED FAILURES                    (unsafe retry persistence)
↺ Reset → 🔄 RUNAWAY LOOP                         (autonomous SAFETY HOLD)
↺ Reset → 🚫 READ-ONLY BREACH                     (identity policy)
```

---

## BlueVerse MCP Integration (Optional)

Exposes all 13 TARE agents as tools in BlueVerse Foundry via MCP Remote - HTTP.

### Prerequisites
- ngrok installed (download single `.exe` from ngrok.com — no install needed)
- Free ngrok account + authtoken configured
- BlueVerse Foundry access (Creator role)

### Step 1 — Start the AEGIS server
```
cd aegis-poc\backend
python -m uvicorn main:app --port 8052 --host 0.0.0.0
```

### Step 2 — Start ngrok
```
ngrok.exe http 8052
```
Copy the forwarding URL e.g. `https://xxxx.ngrok-free.dev`

### Step 3 — Register in BlueVerse
```
Agents → Tools & MCP Server Hub → Register MCP Server

Name         : AEGIS_TARE
Description  : TARE multi-agent identity security system for energy grid
Server Type  : MCP Remote - HTTP
URL          : https://xxxx.ngrok-free.dev/mcp
Headers      : (leave empty)
Base Unit    : your unit
```

### Step 4 — Create a BlueVerse Agent
```
Agents → Agent Hub → Create Agent
→ Add AEGIS_TARE MCP server as tool source
```

BlueVerse auto-discovers all 16 tools:

| Tool | Agent(s) | What it does |
|---|---|---|
| `tare_evaluate_command` | KORAL→MAREA→TASYA→NEREUS→BARRIER | Full pipeline eval |
| `tare_get_status` | TARE | System mode, stats, zones |
| `tare_get_audit_log` | TARE | Gateway command history |
| `barrier_get_policy` | BARRIER | Current enforcement mode |
| `koral_get_session` | KORAL | Raw telemetry session log |
| `marea_get_signals` | MAREA | All drift signals detected |
| `nereus_get_recommendation` | NEREUS | Latest freeze recommendation |
| `echo_diagnose` | ECHO | Zone/asset diagnostics |
| `simar_simulate` | SIMAR | What-if simulation |
| `navis_build_plan` | NAVIS | NERC CIP execution plan |
| `riskador_score_plan` | RISKADOR | Risk score (0–100) |
| `triton_get_status` | TRITON | Execution status |
| `tare_get_all_agents_status` | All 13 | Live status of every agent |
| `tare_approve_timebox` | TARE+BARRIER | Approve 3-min window |
| `tare_deny_timebox` | TARE+BARRIER | Deny, keep FREEZE |
| `tare_reset` | TARE | Reset full session |

### Troubleshooting

| Problem | Fix |
|---|---|
| **502 Bad Gateway in ngrok** | AEGIS server not running. Run Step 1 again. |
| **405 Method Not Allowed** | Old code without MCP. Pull latest from repo. |
| **Error in BlueVerse on register** | Server not reachable. Check ngrok URL matches server port. |
| **ngrok URL changed** | Re-register in BlueVerse with new URL each ngrok restart. |

---

*TARE AEGIS-ID — Setup & Run Guide*
*Energy & Utilities Security Platform — Internal Use Only*
*Version: POC v4.0 — April 2026*

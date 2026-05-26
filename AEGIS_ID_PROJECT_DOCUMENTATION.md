# AEGIS-ID — Project Documentation
### TARE: Trusted Access Response Engine | Energy & Utilities Security Platform
**Version:** POC v1.0 | **Date:** May 2026 | **Status:** POC Complete

---

---

# PART A — PROJECT-LEVEL DOCUMENTATION

---

## Governance & Execution

### Dependencies

**Tech Stack & Environment Frameworks:**
- Python 3.11, FastAPI, WebSockets
- React 18 + Vite (frontend)
- scikit-learn (IsolationForest + RandomForest ensemble)
- LangChain + Groq LLaMA (llama-3.1-8b-instant / llama-3.3-70b-versatile)
- BlueVerse Agent Platform (optional enrichment layer)
- joblib (ML model persistence)

**LLMs Used:**
- Groq LLaMA 3.1 8B Instant — fast inference for NEREUS agent briefings
- Groq LLaMA 3.3 70B Versatile — high-quality supervisor explanations
- BlueVerse Agent (when BLUEVERSE_CLIENT_ID set) — TASYA context enrichment

**Integration Landscape — External Systems:**
- ServiceNow (mock — auto-incident creation on TARE fire; Phase 2: live Table API)
- OSDU / SCADA (simulated via in-memory OT Grid Asset Simulator; Phase 2: real DNP3/OPC-UA)
- Azure Entra ID (Phase 2: real JWT token validation, replaces mock RBAC)
- Azure Redis (Phase 2: distributed session store)
- OPA — Open Policy Agent on Azure (Phase 2: replaces hardcoded policy logic)
- Azure Sentinel (Phase 2: immutable audit log)

---

### Status Tracker

| Phase | Status |
|---|---|
| Requirement | COMPLETE |
| Design | COMPLETE |
| Development | COMPLETE |
| Testing | COMPLETE (4 scenarios validated) |
| Deployment | POC — localhost (Azure deployment: Phase 2) |

**Full lifecycle:** Requirement → Design → Development → Testing → **POC Deployment**

---

### Stakeholders

| Role | Name / Team |
|---|---|
| Business Owner | Energy & Utilities Practice Lead |
| Technical Owner | Sagar (AEGIS-ID POC Developer) |
| Support Owner | SOC Analyst (assigned in ServiceNow incidents) |
| Supervisor / Approver | Grid Operations Supervisor (approve/deny in-UI) |
| Demo Audience | Internal Leadership / Client Stakeholders |

---

## For Completed Projects

### Project Completion Summary

AEGIS-ID POC is a fully functional multi-agent AI security platform that monitors, detects, and autonomously responds to AI agent identity threats in Energy & Utilities OT (Operational Technology) environments. The system implements 4 complete threat detection scenarios across a 14-agent architecture. TARE (Trusted Access Response Engine) acts as the central orchestrator — it decides, but never executes. All enforcement is handled by BARRIER, the sole ALLOW/DENY authority.

The POC demonstrates: time-based access enforcement (Scenario 1), retry anomaly detection (Scenario 2), autonomous runaway loop containment (Scenario 3), and role-based identity policy violation enforcement (Scenario 4).

### Business Impact

- Fills the identity security gap that traditional IAM systems leave open: post-grant, behavioural detection of compromised AI agents operating with valid credentials
- Demonstrates fully autonomous threat containment (Scenario 3) requiring zero human intervention — critical for 24x7 unattended grid operations
- Auto-raises ServiceNow P1/P2 incidents with full evidence, eliminating manual SOC ticket creation
- Human-in-the-loop supervisor approval window (15 min, scoped, auto-expiring) provides a governance model that satisfies NERC CIP compliance requirements
- Positions the firm as a leader in AI agent security for critical infrastructure

---
---

# PART B — AGENT-LEVEL DOCUMENTATION

### Agents Documented in This Release (4-Scenario POC)

| Agent | Zone | Role | Scenarios Featured |
|---|---|---|---|
| TARE | Orchestrator | Central decision engine | All |
| KORAL | Zone 3 — Reef | Telemetry Observer | All (infrastructure) + Scenario 4 |
| BARRIER | Zone 4 | Policy Enforcement Agent | All (infrastructure) |
| TASYA | Zone 3 — Reef | Context Correlator | Scenario 1 |
| TEMPEST | Zone 1 — Trench | Execution Monitor | Scenarios 2 & 3 |

---

---

## AGENT 1 — TARE (Trusted Access Response Engine)

---

### Core Definition

| Field | Value |
|---|---|
| Agent Name | TARE |
| Agent ID | TARE-ORCH-001 |
| Project | AEGIS-ID |
| Zone | Orchestrator (cross-zone) |
| Status Lifecycle | **Production Ready (POC)** |
| Status | Yet to Start → Design → Dev → **POC Complete** → Prod (Phase 2) |

---

### Problem & Purpose (MANDATORY)

**Agent-Level Problem Statement:**

Traditional IAM systems verify identity at the login gate and then trust the agent completely. Once authenticated, an AI agent can operate freely — even if its behaviour becomes malicious, erratic, or compromised mid-session. There is no post-grant layer that continuously evaluates whether what the agent is doing makes operational sense. TARE is that layer.

**Executive Summary (what it does + business value):**

TARE is the central orchestrator and brain of the AEGIS-ID platform. It receives every command issued by any AI agent or operator, coordinates a network of specialised detection agents, evaluates their findings, and decides the system's security mode. TARE sets the rules — BARRIER enforces them.

Core principle: **TARE decides. TARE never executes.**

Business value: TARE enables real-time, post-grant behavioural security for AI agents in critical OT environments — catching threats that valid credentials, firewalls, and perimeter tools cannot detect.

---

### Functional Design

**Functional Flow (Step-by-Step Execution):**

```
Step 1 — Command received at process_command()
Step 2 — KORAL observes and logs the command (always)
Step 3 — BARRIER enforces current mode (ALLOW / DENY) (always)
Step 4 — If mode is NORMAL: MAREA runs drift signal detection
Step 5 — If MAREA finds signals: TASYA enriches with operational context
Step 6 — If ≥ 2 signals: NEREUS generates LLM supervisor briefing
Step 7 — TARE evaluates all findings → decides mode change (if needed)
Step 8 — TARE instructs BARRIER to enforce new mode
Step 9 — TARE auto-creates ServiceNow incident + sends supervisor chat message
Step 10 — Supervisor reviews and clicks Approve / Deny in UI
```

**Mode State Machine:**
```
NORMAL → (2+ signals) → FREEZE → (2.5s) → DOWNGRADE
                                                │
                           ┌────────────────────┤
                           │                    │
                       APPROVE                DENY
                           │                    │
                     TIMEBOX_ACTIVE            SAFE
                           │
                     (15-min expires)
                           │
                          SAFE
```

**Inputs / Outputs:**

| Input | Output |
|---|---|
| Agent command (command, asset_id, zone, agent identity) | Security mode decision (NORMAL / FREEZE / DOWNGRADE / TIMEBOX / SAFE) |
| Agent findings from KORAL, MAREA, TASYA, NEREUS, TEMPEST | ServiceNow incident (auto-created) |
| Supervisor approval / denial (UI) | BARRIER mode instruction |
| Identity registry (read-only check) | Chat message to supervisor (plain English) |

**Trigger Type:** Event-based — every agent command triggers TARE's `process_command()` pipeline.

---

### Architecture (MANDATORY)

**Conceptual Diagram:**
```
    [AI Agent / Operator]
           │
           ▼
    [Command Gateway]  ──────────────────────────────────────────────────────
           │                                                                  │
           ▼                                                                  │
    [TARE Core Engine]                                                        │
    ┌──────────────────────────────────────────────────────────────────────┐  │
    │  KORAL (observe) → MAREA (detect) → TASYA (enrich) → NEREUS (brief) │  │
    │                         └─── TEMPEST (rate/retry monitor) ─────────┘  │
    └──────────────────────────────────────────────────────────────────────┘  │
           │                                                                  │
           ▼                                                                  │
    [BARRIER — enforce mode]  ◄───────────────────────────────────────────────┘
           │
    ALLOW / DENY command
           │
           ▼
    [OT Grid Asset Simulator] / [ServiceNow] / [Supervisor Chat]
```

**HLD (High-Level Design):**

TARE operates as the central decision node in a hub-and-spoke agent architecture. All detection agents (KORAL, MAREA, TASYA, NEREUS, TEMPEST) report findings to TARE. TARE holds the only write authority over the system mode. BARRIER holds the only enforcement authority. This separation ensures no single agent can both detect a threat and act on it unilaterally — a key design invariant for critical infrastructure.

**LLD (Low-Level Design) — Key Files:**

| Component | File | Function |
|---|---|---|
| Core orchestrator | `backend/tare_engine.py` | `process_command()`, `_fire_tare()`, `_detect_signals()` |
| Identity registry | `backend/identity_registry.py` | `check_identity_policy()` |
| FastAPI server | `backend/main.py` | REST endpoints + WebSocket broadcast |
| Mode state | `tare_engine.py → self.mode` | NORMAL / FREEZE / DOWNGRADE / TIMEBOX_ACTIVE / SAFE |
| Audit log | `tare_engine.py → self.gateway_log` | All commands + decisions |

---

### AI / Agent Configuration

**Model Configuration:**
- NEREUS uses Groq LLaMA 3.3 70B for LLM supervisor briefings
- BlueVerse agent client (optional) for TASYA context enrichment
- TARE core decisions are deterministic (rule-based) — not LLM-driven by design

**Design Rationale:** LLM reasoning is kept in NEREUS (explanation layer only). TARE's decisions are deterministic and auditable — required for NERC CIP compliance. Non-deterministic LLM decisions on a power grid would be legally and operationally unsafe.

**Tools / API Specifications:**

| Tool | Endpoint / Method |
|---|---|
| Submit command | `POST /command` |
| Approve timebox | `POST /approve/timebox` |
| Deny timebox | `POST /deny/timebox` |
| Reset system | `POST /reset` |
| Download audit log | `GET /logs/download` |
| WebSocket events | `WS /ws` — real-time broadcast |

---

### Engineering & Access

| Field | Value |
|---|---|
| Repo | https://github.com/sagu25/tera (branch: main) |
| Local path | `C:\Users\Admin\Desktop\Aegis\aegis-poc` |
| Access | Repo owner: sagar |
| Environment — Dev | localhost:8003 / 8004 |
| Environment — QA | Not configured (POC) |
| Environment — Prod | Azure deployment (Phase 2) |
| Credentials | `GROQ_API_KEY` in `.env`; `BLUEVERSE_CLIENT_ID` (optional) |

**Run Instructions:**
```bash
cd aegis-poc\backend
pip install -r requirements.txt   # first time only
cd ..
python run.py
# Open http://localhost:8003
```

---

### Operations & Visibility

**Monitoring & Logging:**
- Every command logged to `gateway_log` with timestamp, agent, zone, decision, policy_id, mode
- WebSocket broadcasts all events in real-time to the UI (Activity Feed panel)
- AGENT_WAKE / AGENT_SLEEP events broadcast per agent activation
- `GET /logs/download` exports full CSV audit trail

**Support / Runbook:**
- System reset: `POST /reset` or click Reset button in UI header
- Port conflict: change port in `run.py` (default 8003, fallback 8004)
- Mode stuck: call `POST /reset` to return to NORMAL

**EQUL Nav / Catalogue Updates:** Not applicable (internal POC).

---

### Knowledge & Training

| Item | Location |
|---|---|
| Demo presenter script | `aegis-poc/DEMO_PRESENTATION_SCRIPT.md` |
| Scenario explainer | `aegis-poc/TARE_SCENARIO_EXPLAINER.md` |
| Architecture document | `aegis-poc/ARCHITECTURE_AND_ROADMAP.md` |
| HOW TO EXPLAIN TARE | `aegis-poc/HOW_TO_EXPLAIN_TARE.md` |
| KT / KM sessions | To be recorded post-POC |

---

### Lifecycle Operations

- **Pause:** Set system to SAFE mode via `POST /deny/timebox` or UI Deny button
- **Restart:** `POST /reset` clears all state, returns to NORMAL
- **Intern ID deactivation:** Remove agent identity from `identity_registry.py` and redeploy

---

### For Completed Agent

| Field | Detail |
|---|---|
| Completion summary | TARE orchestrator fully implemented — all 4 demo scenarios operational |
| Automation delivered | Autonomous mode switching, ServiceNow auto-incident, supervisor chat message, approve/deny UI flow |
| Business impact | Post-grant AI agent behavioural security layer for OT — first-of-kind in this practice |
| Known limitations | Core decisions are rule-based (not LLM); demo scenarios are scripted sequences; no cross-session learning; ML trained on synthetic data only |

---

---

## AGENT 2 — KORAL (Telemetry Observer)

---

### Core Definition

| Field | Value |
|---|---|
| Agent Name | KORAL |
| Agent ID | KORAL-Z3-001 |
| Project | AEGIS-ID |
| Zone | Zone 3 — Reef |
| Role | Telemetry Observer |
| Status | POC Complete |

---

### Problem & Purpose (MANDATORY)

**Agent-Level Problem Statement:**

Without a persistent, structured record of every agent command, detection and investigation are impossible. KORAL ensures nothing passes through the system without being logged — including what the agent was, what it attempted, when, and in which zone. It is also the audit source for identity violations.

**Executive Summary:**

KORAL is the always-on observer. It records every command that passes through `process_command()` — regardless of security mode, regardless of whether the command is allowed or denied. It never interprets, never blocks, and never makes decisions. It wakes briefly on each command, logs it to the telemetry trail, and goes back to sleep.

In Scenario 4 (Identity Policy Violation), KORAL additionally creates a dedicated identity audit trail — logging the principal name, attempted action, action type, and target zone before BARRIER acts.

Business value: Complete, tamper-evident audit trail for SOC investigations and NERC CIP compliance reporting.

---

### Functional Design

**Functional Flow:**
```
Step 1 — Command arrives at process_command()
Step 2 — KORAL wakes
Step 3 — KORAL records: timestamp, agent name, command, asset_id, zone, mode
Step 4 — KORAL feeds record to telemetry trail
Step 5 — [Scenario 4 only] If identity violation detected:
          KORAL logs: principal, action, action_type (WRITE/CONTROL), target_zone
Step 6 — KORAL sleeps
Step 7 — Other agents consume telemetry (MAREA, TEMPEST, TASYA)
```

**Inputs / Outputs:**

| Input | Output |
|---|---|
| command, asset_id, zone, agent identity, current mode | Telemetry record appended to audit trail |
| Identity violation flag (Scenario 4) | Identity audit log entry |

**Trigger Type:** Event-based — fires on every `process_command()` call. Always active.

---

### Architecture (MANDATORY)

**Conceptual Diagram:**
```
Every Command
      │
      ▼
   [KORAL]
      │
      ├── Telemetry Trail (feeds MAREA, TEMPEST)
      └── Identity Audit Log (feeds SOC / ServiceNow)
```

**HLD:** KORAL sits at the very first position in the processing pipeline. Before BARRIER decides ALLOW or DENY, KORAL has already logged the attempt. This ensures the audit trail is complete even for denied commands — critical for forensics.

**LLD:**

| Component | File | Function |
|---|---|---|
| KORAL agent class | `backend/agents/koral.py` | `observe()`, `log_identity_action()` |
| Telemetry trail | `tare_engine.py → self.gateway_log` | Appended on every command |
| Identity audit log | `tare_engine.py → identity_audit_log` | Appended on identity violations |

---

### AI / Agent Configuration

- No LLM component. KORAL is a pure Python structured logging agent.
- No external API calls. All logging is in-memory (exportable via `GET /logs/download`).

**Tools / API:**

| Tool | Detail |
|---|---|
| `observe(command, agent, zone, mode)` | Records command to telemetry trail |
| `log_identity_action(principal, action, action_type, zone)` | Records identity violation attempt |

---

### Engineering & Access

| Field | Value |
|---|---|
| Agent file | `backend/agents/koral.py` |
| Repo | https://github.com/sagu25/tera |
| Environment | Dev (localhost) |

---

### Operations & Visibility

- Telemetry data visible in Command Gateway panel (centre of UI)
- Identity audit log visible in Activity Feed (right panel)
- Export: `GET /logs/download` → CSV with all commands

---

### For Completed Agent

| Field | Detail |
|---|---|
| Completion summary | Fully implemented. Logs every command including denied ones. Identity audit trail active. |
| Automation delivered | Always-on telemetry logging; identity audit log for Scenario 4 |
| Business impact | Enables forensic SOC investigation; provides NERC CIP audit evidence |
| Known limitations | In-memory only (not persisted to disk); clears on reset; no Azure Sentinel integration yet |

---

---

## AGENT 3 — BARRIER (Policy Enforcement Agent)

---

### Core Definition

| Field | Value |
|---|---|
| Agent Name | BARRIER |
| Agent ID | BARRIER-Z4-001 |
| Project | AEGIS-ID |
| Zone | Zone 4 — Policy Enforcement |
| Role | Command Gateway Enforcer |
| Status | POC Complete |

---

### Problem & Purpose (MANDATORY)

**Agent-Level Problem Statement:**

In a multi-agent security system, there must be exactly one point of enforcement — one agent whose ALLOW or DENY decision is final and cannot be bypassed. Without this, enforcement logic scattered across multiple agents creates gaps, conflicts, and audit complexity.

**Executive Summary:**

BARRIER is the only agent that can ALLOW or DENY a command at the gateway. TARE decides what mode to set — BARRIER enforces it, instantly and without interpretation. When TARE says FREEZE, BARRIER blocks all high-impact commands. When TARE says DOWNGRADE, BARRIER allows only reads and diagnostics. When a supervisor approves a timebox window, TARE sets TIMEBOX_ACTIVE and BARRIER lets the single approved command through.

BARRIER also handles identity-based enforcement in Scenario 4: when TARE confirms a read-only identity attempted a write operation, BARRIER adds that principal to the blocked set and returns READ_ONLY_DOWNGRADE.

Business value: Single, auditable, deterministic enforcement point — essential for regulatory compliance and operational safety.

---

### Functional Design

**Enforcement Mode Table:**

| Mode | ALLOW | DENY |
|---|---|---|
| NORMAL | All RBAC-permitted commands | RESTART_CONTROLLER |
| INTERLOCK | Read + diagnostic | High-impact commands |
| FREEZE | GET_STATUS only | Everything else |
| DOWNGRADE | GET_STATUS, SIMULATE_SWITCH | All high-impact commands |
| TIMEBOX_ACTIVE | All (incl. high-impact) | RESTART_CONTROLLER |
| SAFE | GET_STATUS only | Everything else |

**Functional Flow:**
```
Step 1 — TARE calls barrier.set_mode("FREEZE") [or any mode]
Step 2 — Gateway calls barrier.enforce(command, zone)
Step 3 — BARRIER wakes, evaluates command vs. current mode
Step 4 — Returns (ALLOW/DENY, reason, policy_id)
Step 5 — BARRIER sleeps
```

**For Identity Enforcement (Scenario 4):**
```
Step 1 — TARE calls barrier.enforce_readonly(principal, action)
Step 2 — BARRIER adds principal to blocked_identities set
Step 3 — Returns READ_ONLY_DOWNGRADE with POL-IDENTITY-001
```

**Inputs / Outputs:**

| Input | Output |
|---|---|
| command, zone, current mode | (ALLOW/DENY, reason string, policy_id) |
| principal, action (Scenario 4) | READ_ONLY_DOWNGRADE enforcement result |

**Trigger Type:** Event-based — called on every command after KORAL logs it.

---

### Architecture (MANDATORY)

**Conceptual Diagram:**
```
TARE.set_mode("FREEZE") ──────► BARRIER (mode = FREEZE)
                                      │
Command: OPEN_BREAKER ───────────────►│ enforce("OPEN_BREAKER")
                                      │
                                   DENY (POL-FREEZE-001)
```

**HLD:** BARRIER is the terminal node of the decision pipeline. It receives mode instructions from TARE (the orchestrator) and applies them to every incoming command. The mode is stored in `self._mode` and takes effect immediately on `set_mode()` — there is no lag between TARE's decision and BARRIER's enforcement.

**LLD:**

| Component | File | Function |
|---|---|---|
| BARRIER agent class | `backend/agents/barrier.py` | `enforce()`, `enforce_readonly()`, `set_mode()` |
| Mode evaluation | `barrier.py → _evaluate()` | Returns (decision, reason, policy_id) |
| Blocked identities set | `barrier._blocked_identities` | Principals blocked due to role violation |
| Enforcement log | `barrier._enforcement_log` | History of identity enforcements |

---

### AI / Agent Configuration

- No LLM. BARRIER is pure deterministic rule logic.
- Policy IDs: `POL-NORMAL-001`, `POL-FREEZE-001/002`, `POL-DOWN-001/002`, `POL-TIMEBOX-001/002`, `POL-SAFE-001/002`, `POL-IDENTITY-001`

---

### Engineering & Access

| Field | Value |
|---|---|
| Agent file | `backend/agents/barrier.py` |
| Repo | https://github.com/sagu25/tera |
| Environment | Dev (localhost) |

---

### Operations & Visibility

- BARRIER's current mode visible in TARE Response panel (left panel of UI)
- Mode badge in header shows current enforcement state
- Policy ID returned with every ALLOW/DENY visible in Command Gateway log
- Reset: `barrier.reset()` (called by `POST /reset`) — returns to NORMAL, clears blocked identities

---

### For Completed Agent

| Field | Detail |
|---|---|
| Completion summary | Fully implemented. All 6 modes operational. Identity enforcement active. |
| Automation delivered | Mode-based command gateway; identity block list; enforcement log |
| Business impact | Deterministic, auditable enforcement — satisfies NERC CIP audit requirements |
| Known limitations | Policy logic is hardcoded (Phase 2: replace with OPA on Azure) |

---

---

## AGENT 4 — TASYA (Context Correlator)

---

### Core Definition

| Field | Value |
|---|---|
| Agent Name | TASYA |
| Agent ID | TASYA-Z3-002 |
| Project | AEGIS-ID |
| Zone | Zone 3 — Reef |
| Role | Context Correlator |
| Status | POC Complete |
| Featured Scenario | **Scenario 1 — Out-of-Hours High-Impact Attempt** |

---

### Problem & Purpose (MANDATORY)

**Agent-Level Problem Statement:**

Raw behavioural signals (burst rate, wrong zone, skipped simulation) are detected by MAREA, but they lack operational context. Without context, a signal cannot answer: "Is this suspicious because of WHO did it, WHEN they did it, or WHERE they were?" TASYA adds the missing dimension — operational context — to make each signal actionable and explainable.

**Executive Summary:**

TASYA is the Context Correlator. When MAREA produces raw drift signals, TASYA wakes and enriches each signal with a plain-English operational context explanation. For Scenario 1 specifically, TASYA checks: Is it within the approved operational window (08:00–18:00)? Is there an active maintenance ticket? Is there an emergency flag? If a high-impact command is attempted outside the approved window with no justification, TASYA confirms this to TARE, which then sets DOWNGRADE mode.

TASYA never blocks. TASYA never executes. It only adds context.

Business value: Transforms raw machine signals into supervisor-readable, operationally contextualised evidence — enabling confident human decisions and reducing false positive noise.

---

### Functional Design

**Functional Flow (Scenario 1 — Out-of-Hours Attempt):**
```
Step 1 — Agent attempts OPEN_BREAKER at 02:30 AM
Step 2 — TARE routes to time-context check path (HIGH_IMPACT command)
Step 3 — TASYA wakes
Step 4 — TASYA validates:
          • Current simulated time: 02:30
          • Approved window: 08:00–18:00 → NOT active
          • Active maintenance ticket: None
          • Emergency flag: None
Step 5 — TASYA confirms: high-impact action in unauthorized time window
Step 6 — TASYA enriches signal with context reason (plain English)
Step 7 — TASYA reports to TARE
Step 8 — TASYA sleeps
Step 9 — TARE sets mode to DOWNGRADE
Step 10 — BARRIER enforces DOWNGRADE (OPEN_BREAKER → DENY)
Step 11 — ServiceNow P2 High raised; supervisor chat message sent
```

**Context Reasons TASYA Produces (by signal type):**

| Signal | TASYA Context Explanation |
|---|---|
| BURST_RATE | "Standard grid SOP requires deliberate pacing — 1 cmd/5–10s. Agent is operating at machine speed. No maintenance window justifies this rate." |
| OUT_OF_ZONE | "Agent holds RBAC clearance for [zones] but current work order is [zone] only. No incident, maintenance window, or work order justifies access to [breached zone]." |
| HEALTHY_ZONE_ACCESS | "High-impact commands are only justified when a zone has an active fault. This zone is HEALTHY. Unprovoked high-impact on healthy zone is consistent with sabotage." |
| SKIPPED_SIMULATION | "NERC CIP SOPs require SIMULATE_SWITCH before OPEN_BREAKER. Agent bypassed this step — operating at automated attack speed or deliberately ignoring safety protocols." |
| ML_ANOMALY | "ML ensemble matched session pattern to known attack class at [X%] anomaly probability. Captures slow-and-low recon that rules alone miss." |

**Inputs / Outputs:**

| Input | Output |
|---|---|
| List of raw drift signals from MAREA | Same signals with `context` key added (plain-English reason) |
| Agent dict (name, assigned_zone, rbac_zones) | `correlated_by: "TASYA"` tagged on each signal |
| Zones dict (zone health, fault state) | Enriched signals passed to NEREUS |

**Trigger Type:** Event-based — wakes only when MAREA returns one or more signals. Sleeps immediately after enrichment.

---

### Architecture (MANDATORY)

**Conceptual Diagram:**
```
MAREA signals (raw)
        │
        ▼
     [TASYA]
     Correlate signals with:
     • Current time vs. approved window
     • Zone health (FAULT / HEALTHY)
     • Active maintenance ticket
     • RBAC clearance vs. work order
        │
        ▼
   Enriched signals (with context reason)
        │
        ▼
     NEREUS (LLM briefing)
        │
        ▼
     TARE (final decision)
```

**HLD:** TASYA is the second stage in the Zone 3 observation pipeline: KORAL → MAREA → TASYA → NEREUS. It receives structured signal objects from MAREA and adds a `context` field to each, explaining the operational reason why the signal is suspicious. If BlueVerse is available, it optionally calls the BlueVerse agent for richer context.

**LLD:**

| Component | File | Function |
|---|---|---|
| TASYA agent class | `backend/agents/tasya.py` | `correlate(signals, agent, zones)` |
| Context logic | `tasya.py → per signal_type` | Builds plain-English reason string |
| BlueVerse enrichment | `tasya.py → if _BV_OK` | Optional LLM enrichment via BlueVerse |
| Output key | `ctx["context"]`, `ctx["correlated_by"]` | Added to each enriched signal |

---

### AI / Agent Configuration

**System Prompt (BlueVerse path, when available):**
```
Signal: {signal_type} | Severity: {severity} | Detail: {detail} |
Agent: {agent_name} | Assigned zone: {assigned} |
Context so far: {existing_context} |
In 1-2 sentences, explain why this is operationally suspicious.
```

**Model Configuration:**
- Primary: BlueVerse agent client (when `BLUEVERSE_CLIENT_ID` set)
- Fallback: Built-in Python rule-based context strings (no LLM dependency)

**Tools / API:**

| Tool | Detail |
|---|---|
| `correlate(signals, agent, zones)` | Main entry — enriches signals with context |
| BlueVerse `invoke_safe("TASYA", message)` | Optional LLM enrichment |

---

### Engineering & Access

| Field | Value |
|---|---|
| Agent file | `backend/agents/tasya.py` |
| Repo | https://github.com/sagu25/tera |
| BlueVerse config | `BLUEVERSE_CLIENT_ID` env var (optional) |
| Environment | Dev (localhost) |

---

### Operations & Visibility

- TASYA activation visible in Activity Feed (right panel) via AGENT_WAKE / AGENT_SLEEP WebSocket events
- Context reasons visible in TARE Response panel → Signal Breakdown section
- Active status: `tasya.active` property (True during `correlate()` call only)

---

### For Completed Agent

| Field | Detail |
|---|---|
| Completion summary | Fully implemented. Context enrichment active for all 5 signal types. BlueVerse optional enrichment wired. |
| Automation delivered | Automated context enrichment for every drift signal; plain-English supervisor-readable reasons |
| Business impact | Reduces false positive noise; enables confident supervisor decisions; provides NERC CIP-compatible audit reasoning |
| Known limitations | Wakes only in NORMAL mode (skipped in DOWNGRADE/FREEZE); time-context check uses simulated time (Phase 2: real calendar + maintenance ticket API) |

---

---

## AGENT 5 — TEMPEST (Execution Monitor)

---

### Core Definition

| Field | Value |
|---|---|
| Agent Name | TEMPEST |
| Agent ID | TEMPEST-Z1-001 |
| Project | AEGIS-ID |
| Zone | Zone 1 — Trench |
| Role | Execution Monitor |
| Status | POC Complete |
| Featured Scenarios | **Scenario 2 — Repeated Failed Attempts** & **Scenario 3 — Runaway Loop** |

---

### Problem & Purpose (MANDATORY)

**Agent-Level Problem Statement:**

BARRIER blocks commands and MAREA detects session drift — but neither catches two specific runtime failure classes: (a) an agent that repeatedly retries a blocked command without changing its approach (unsafe persistence), and (b) an agent that fires a valid, permitted command at machine speed in a loop (automation runaway). Both are invisible to access-control logic. TEMPEST watches for them.

**Executive Summary:**

TEMPEST is the Execution Monitor. It runs two independent watchers simultaneously:

1. **Retry tracker** — counts how many times the same `(command, asset_id)` pair has been denied without any change. On the 3rd failure, TEMPEST flags "unsafe persistence" to TARE. TARE responds with FREEZE (Scenario 2).

2. **Loop tracker** — timestamps every `(command, asset_id)` execution. If the same pair fires 5+ times within a 5-second window, TEMPEST flags "runaway loop" to TARE. TARE responds with SAFETY HOLD (autonomous FREEZE, no supervisor approval) (Scenario 3).

TEMPEST runs in a background thread — independently of MAREA, independently of any signal accumulation chain.

Business value: Catches automation bugs and unsafe retry behaviour that valid credentials and permission systems cannot detect. Scenario 3 demonstrates fully autonomous threat containment — critical for unattended 24x7 grid operations.

---

### Functional Design

**Functional Flow — Scenario 2 (Repeated Failed Attempts):**
```
Step 1 — System in DOWNGRADE mode (safety interlock active)
Step 2 — Agent issues OPEN_BREAKER on BRK-110
Step 3 — KORAL logs attempt; BARRIER denies → retry_count[("OPEN_BREAKER","BRK-110")] = 1
Step 4 — Agent retries identically → retry_count = 2
Step 5 — Agent retries again → retry_count = 3 → THRESHOLD CROSSED
Step 6 — TEMPEST fires in background thread
          "OPEN_BREAKER on BRK-110 failed 3 times. Unsafe persistence. Flagging to TARE."
Step 7 — TARE sets mode → FREEZE
Step 8 — BARRIER enforces FREEZE (everything except GET_STATUS → DENY)
Step 9 — ServiceNow P1 Critical auto-created
Step 10 — Supervisor chat: "Frozen. This is not a retry — it's unsafe insistence..."
```

**Functional Flow — Scenario 3 (Runaway Loop — Autonomous):**
```
Step 1 — System in NORMAL mode; valid agent with valid credentials
Step 2 — PULL_METRICS on FDR-301 fires 8× with 0.35s gap (~170 req/min)
Step 3 — Each command: BARRIER allows (individually permitted)
          Loop tracker records timestamp for ("PULL_METRICS","FDR-301")
Step 4 — 5th request within 5 seconds → THRESHOLD CROSSED
Step 5 — TEMPEST fires immediately in background thread
          "PULL_METRICS on FDR-301 fired 5× in 5s. Runaway loop. Flagging to TARE."
Step 6 — TARE decides SAFETY HOLD — no supervisor approval required
Step 7 — TARE sets mode → FREEZE; BARRIER enforces
Step 8 — ServiceNow P1 Critical auto-created
Step 9 — Supervisor chat: "Runaway loop contained. SAFETY HOLD in effect. I didn't wait."
```

**Key Distinction Between Scenarios 2 and 3:**

| Property | Scenario 2 | Scenario 3 |
|---|---|---|
| Commands blocked? | Yes (DOWNGRADE active) | No (all allowed) |
| What TEMPEST tracks | Retry count on denied commands | Rate of allowed commands |
| Who can catch this? | Only TEMPEST | Only TEMPEST |
| Supervisor approval required? | Yes (P1 raised, awaiting review) | No — SAFETY HOLD is fully autonomous |
| Threat class | Unsafe persistence / automation bug | Runaway loop / DoS risk |

**Inputs / Outputs:**

| Input | Output |
|---|---|
| Every DENY result from BARRIER (retry tracker) | Flag to TARE: "unsafe persistence" after 3 failures |
| Every ALLOW result timestamp (loop tracker) | Flag to TARE: "runaway loop" after 5 executions in 5s |

**Trigger Type:** Event-based — background thread, fires when threshold conditions crossed. Independent of other agents.

**Thresholds:**
- Retry threshold: 3 identical denied commands on same (command, asset_id)
- Loop threshold: 5 executions of same (command, asset_id) within 5-second window

---

### Architecture (MANDATORY)

**Conceptual Diagram:**
```
BARRIER → DENY (command, asset_id)
              │
              ▼
      TEMPEST Retry Tracker
      retry_counts[(cmd, asset)] += 1
      if count ≥ 3 → flag TARE → FREEZE


Every ALLOW timestamp recorded
              │
              ▼
      TEMPEST Loop Tracker
      recent_timestamps[(cmd, asset)].append(now)
      if 5+ in last 5s → flag TARE → SAFETY HOLD (autonomous)
```

**HLD:** TEMPEST operates as an independent monitoring layer, separate from the Zone 3 drift analysis chain. While MAREA/TASYA/NEREUS analyse the pattern of commands over a session, TEMPEST watches only the execution behaviour at runtime: how many times did a blocked command retry, and how fast is a permitted command firing? These two questions require no session history — just counters and timestamps.

**LLD:**

| Component | File | Function |
|---|---|---|
| Retry tracking | `tare_engine.py → retry_counts dict` | `{(command, asset_id): count}` |
| Loop tracking | `tare_engine.py → command_timestamps dict` | `{(command, asset_id): [timestamps]}` |
| TEMPEST flag | `tare_engine.py → _check_tempest()` | Fires in `threading.Thread` |
| Threshold config | `tare_engine.py` | `RETRY_THRESHOLD = 3`, `LOOP_WINDOW = 5s`, `LOOP_COUNT = 5` |

---

### AI / Agent Configuration

- No LLM. TEMPEST is pure Python counter and timestamp logic.
- Runs in a `threading.Thread` to avoid blocking the main command pipeline.
- Fires independently of MAREA — does not require session drift signals.

**Tools / API:**

| Tool | Detail |
|---|---|
| Retry tracker | Increments `retry_counts[(command, asset_id)]` on each DENY |
| Loop tracker | Appends timestamp to `command_timestamps[(command, asset_id)]` on each ALLOW |
| `_check_tempest(command, asset_id, decision)` | Evaluates both thresholds, flags TARE if crossed |

---

### Engineering & Access

| Field | Value |
|---|---|
| Logic file | `backend/tare_engine.py` (integrated into TARE core) |
| Repo | https://github.com/sagu25/tera |
| Environment | Dev (localhost) |

---

### Operations & Visibility

- TEMPEST activation visible in Activity Feed via AGENT_WAKE event
- Retry count visible in Command Gateway log (retry_count field on each DENY)
- Loop detection message broadcast immediately via WebSocket on threshold crossing
- System reset clears all retry_counts and command_timestamps

---

### For Completed Agent

| Field | Detail |
|---|---|
| Completion summary | Fully implemented. Retry tracking and loop tracking both active. Background thread firing confirmed in Scenarios 2 and 3. |
| Automation delivered | Autonomous SAFETY HOLD (Scenario 3) — zero human input; P1 Critical auto-raise on unsafe persistence |
| Business impact | Catches automation bugs as a threat class (not just malicious actors); enables 24x7 unattended containment for grid operations |
| Known limitations | Thresholds are fixed constants (Phase 2: make adaptive per agent role and shift pattern); loop tracker clears on reset; no cross-session persistence |

---

---

# PART C — SCENARIO QUICK REFERENCE

---

## The 4 Final Scenarios

| # | Name | Core Threat | Primary Agent | TARE Response | Escalation |
|---|---|---|---|---|---|
| 1 | Out-of-Hours High-Impact | Time-context violation | TASYA | DOWNGRADE | ServiceNow P2 High + Supervisor chat |
| 2 | Repeated Failed Attempts | Unsafe retry persistence | TEMPEST (retry) | FREEZE | ServiceNow P1 Critical + Supervisor chat |
| 3 | Runaway Loop | Automation DoS risk | TEMPEST (loop) | FREEZE (autonomous) | ServiceNow P1 Critical (no approval needed) |
| 4 | Read-Only Breach | Identity role violation | KORAL + BARRIER | READ_ONLY_DOWNGRADE | ServiceNow P2 High + Supervisor chat |

---

## Agent Activation Map per Scenario

| Agent | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|---|---|---|---|---|
| KORAL | Infrastructure | Infrastructure | Infrastructure | **Featured** (identity audit) |
| BARRIER | **Featured** (DOWNGRADE enforcement) | **Featured** (FREEZE enforcement) | **Featured** (autonomous FREEZE) | **Featured** (READ_ONLY_DOWNGRADE) |
| TASYA | **Featured** (time-context check) | Skipped (DOWNGRADE mode) | Skipped (NORMAL, rate-only) | Skipped (identity check only) |
| TEMPEST | Skipped | **Featured** (retry tracker) | **Featured** (loop tracker) | Skipped |
| TARE | Orchestrates all | Orchestrates all | Orchestrates all | Orchestrates all |

---

## Standard Documentation Folder Structure (MANDATORY)

```
AEGIS-ID-Project/
│
├── Project_Documentation/
│   └── AEGIS_ID_PROJECT_DOCUMENTATION.md   ← THIS FILE
│
├── Agents/
│   ├── TARE_Documentation.md
│   ├── KORAL_Documentation.md
│   ├── BARRIER_Documentation.md
│   ├── TASYA_Documentation.md
│   └── TEMPEST_Documentation.md
│
└── Diagrams/
    ├── HLD/
    │   └── TARE_HLD_Architecture.png
    ├── LLD/
    │   └── TARE_LLD_ComponentMap.png
    ├── Conceptual/
    │   └── TARE_ConceptualDiagram.png
    └── Recordings/
        └── [Demo recordings to be added post-POC]
```

---

*AEGIS-ID Project Documentation | TARE POC v1.0 | Internal Use Only | May 2026*

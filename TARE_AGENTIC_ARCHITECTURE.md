# TARE — Agentic Architecture & Agent Design
### How TARE is Built · Why It Is Genuinely Agentic · Questions & Answers
*Technical Reference Document · Demo Presentation Support*

---

## PART 1 — WHY TARE IS GENUINELY AGENTIC

### What "Agentic" Actually Means

An agentic system is not one that uses an AI model. It is one where an AI model **reasons, decides, and acts autonomously** — without a human scripting every step.

TARE is agentic in two distinct places:

**1. The Operator Agent (the threat)**
The AI agent that TARE monitors is a real LLM-powered autonomous agent. It receives a goal — not a sequence of commands — and decides for itself what to do. It chooses which assets to inspect, which zone to work in, what order to issue commands, when to run a safety simulation, and whether to proceed or stop. Nobody writes its decision tree. It reasons through the situation from first principles every time.

This matters for the demo because every command sequence you see on screen — across all scenarios — was the agent's own choice. Not a script.

**2. The TARE Security Layer (the defence)**
TARE itself is an agentic system. It does not run a single monolithic model. It orchestrates thirteen specialised agents, each with a single responsibility, none with unilateral authority. When a command arrives, TARE decides which agents to wake, in what order, and what to do with their outputs. It synthesises those outputs into a decision — FREEZE, ALLOW, DOWNGRADE, SAFETY HOLD — and instructs BARRIER to enforce it.

That is agentic orchestration: a system that reasons, delegates, synthesises, and acts.

---

### The Core Agentic Design Principles

| Principle | How TARE Implements It |
|---|---|
| **Single responsibility** | Each agent does exactly one thing. KORAL records. MAREA detects. BARRIER enforces. Nobody crosses lanes. |
| **No unilateral authority** | No agent can make a final decision alone. NEREUS can only recommend. BARRIER can only enforce what TARE tells it. TRITON can only execute with a TARE-issued permit AND AEGIS clearance. |
| **Wake on demand** | Agents are not always running. They wake when called, return a result, and sleep. You see this in real time on the Agents tab. |
| **Separation of detection and enforcement** | TARE decides. BARRIER enforces. These are never the same agent. |
| **Human in the loop** | For ambiguous decisions, TARE always escalates to a human supervisor. TARE never approves a timebox itself. |
| **Layered defence** | Three detection layers run in parallel: pre-grant identity check, post-grant rule-based monitoring, post-grant ML anomaly detection. A failure in one layer does not defeat the others. |

---

## PART 2 — HOW EACH AGENT IS BUILT

### Zone Architecture

```
Zone 3 — Reef        [Observe & Recommend]
  KORAL · MAREA · TASYA · NEREUS

Zone 2 — Shelf       [Diagnose & Prepare]
  ECHO · SIMAR · NAVIS · RISKADOR

Zone 1 — Trench      [Execute with Safety]
  TRITON · AEGIS · TEMPEST · LEVIER

Zone 4               [Policy Enforcement]
  BARRIER
```

Each zone has a clear mandate. Agents do not cross zones. Zone 3 never executes. Zone 1 never diagnoses. This is enforced by design, not convention.

---

### ZONE 3 — REEF · Observe & Recommend

---

#### KORAL — Telemetry Observer

**What it does:** Records every command, timestamp, zone, asset ID, and token as it enters the gateway. Provides the raw telemetry that every other agent in the network relies on.

**How it is built:** A stateful in-memory log. It maintains a command history deque (last 100 commands), a burst window deque (raw epoch timestamps for rate analysis), a zone access log, and an identity action log. It never interprets. It never blocks. It only stores.

**Why it matters:** Without KORAL, MAREA has no burst window to measure. NEREUS has no session history to review. The entire detection chain depends on KORAL's record being accurate and complete.

**When it wakes:** On every single command, before any other agent. First in, first out.

**Voice example:** *"Seven commands in the last ten seconds — burst rate exceeded. Flagging to MAREA."*

---

#### MAREA — Drift Analyst

**What it does:** Analyses each command against four behavioural signals — zone boundary violation, healthy zone access, burst rate, and skipped safety simulation. Produces a list of active signals with severity ratings.

**How it is built:** A rule-based analyser with access to KORAL's burst window and the current session context. Each rule is a discrete check:
- **OUT_OF_ZONE** — agent's assigned zone vs. target zone
- **HEALTHY_ZONE_ACCESS** — zone health status vs. reason to be there
- **BURST_RATE** — commands per 10-second window vs. baseline (threshold: 4)
- **SKIPPED_SIMULATION** — OPEN_BREAKER issued without prior SIMULATE_SWITCH in session

Also runs the ML model (IsolationForest + Random Forest ensemble) and adds **ML_ANOMALY** if the session pattern scores above the anomaly threshold.

**Why it matters:** MAREA is the primary detection engine for known attack patterns. The ML layer catches what the rules cannot see.

**When it wakes:** Only in NORMAL mode. Skipped entirely in runtime-only paths (runaway loop scenario) where the threat is rate, not behaviour.

**Voice example:** *"Two signals: out of zone, healthy zone access. This is a pattern. Passing to TASYA."*

---

#### TASYA — Context Correlator

**What it does:** Takes MAREA's raw signals and enriches them with operational context. Validates whether each signal is corroborated by the full session picture.

**How it is built:** A correlator that cross-references signals against the agent's work order (assigned zone), zone health history, and the sequence of recent commands. Its job is to reduce false positives — one signal in isolation might be noise, but a signal corroborated by context becomes evidence.

**Why it matters:** Without TASYA, TARE would freeze on every minor anomaly. TASYA is the filter between "something happened" and "something is wrong."

**When it wakes:** Only when MAREA produces at least one signal.

**Voice example:** *"Three signals corroborated. Work order is Zone 3 — no authorisation for Zone 1. Passing to NEREUS."*

---

#### NEREUS — Recommendation Agent

**What it does:** Synthesises everything KORAL, MAREA, and TASYA produced and issues a recommendation to TARE: FREEZE, MONITOR, or STAND_BY. Never acts directly. Never touches the grid. Only advises.

**How it is built:** An LLM-powered agent (Groq / Llama-3.3-70B). It receives the signal list, the recent session history, and the agent profile, and reasons through whether the combination of signals justifies a freeze. It produces a structured recommendation with a confidence score and a plain-English explanation that becomes the supervisor briefing.

**Why it matters:** NEREUS is where machine reasoning replaces hard-coded thresholds. It can weigh subtle combinations — one ML signal plus one rule signal — and produce a human-readable explanation rather than just a number.

**When it wakes:** When two or more signals are present (full recommendation) or one signal is present (soft advisory).

**Voice example:** *"Three signals confirmed — no operational justification. Recommending FREEZE at 94% confidence."*

---

### ZONE 2 — SHELF · Diagnose & Prepare

These agents activate after TARE approves a supervised repair window. They run in sequence, each gating the next.

---

#### ECHO — Diagnostics Agent

**What it does:** Validates that the fault is real and confirms exactly which assets need attention before any repair is planned.

**How it is built:** Analyses anomaly signals, zone health state, and the gateway log to identify confirmed fault zones and specific target assets. Returns a structured diagnostic result — confirmed/not confirmed, fault zones, target assets, and a proposed repair action list.

**Why it matters:** You never plan a repair against an unconfirmed fault. ECHO is the evidence check before any action.

---

#### SIMAR — Simulation Agent

**What it does:** Runs the proposed repair actions against a safe simulation of the grid state. If the simulation fails, the repair plan never runs on the live grid.

**How it is built:** Takes ECHO's repair action list and tests each step against current asset states and zone health. Checks for known risk indicators: target asset already in safe state, wrong zone, cascading risk. Returns safe_to_proceed: true/false with a list of risk indicators.

**Why it matters:** This is the "test before you touch" principle. Critical infrastructure does not get a second chance.

---

#### NAVIS — Change Planner

**What it does:** Builds a NERC CIP-compliant step-by-step execution plan from ECHO and SIMAR's outputs, including a rollback path for every step.

**How it is built:** Constructs an ordered plan with step numbers, commands, target assets, zones, rationale for each step, and a rollback sequence. Validates that every step maps to an authorised action for the agent's clearance level.

**Why it matters:** Execution without a plan is chaos. NAVIS ensures there is always a defined, auditable path — and a way back if something goes wrong.

---

#### RISKADOR — Risk Scoring Agent

**What it does:** Scores the plan against three dimensions — blast radius (how much can go wrong), reversibility (can we undo it), and confidence (how certain are we). Produces a composite risk score and a GO/HOLD recommendation.

**How it is built:** A weighted scoring model. High-impact commands on critical zones score higher blast radius. Plans with rollback paths score higher reversibility. Plans on confirmed fault zones with clean simulations score higher confidence. Composite score above threshold → PROCEED. Below → HOLD.

**Why it matters:** Not every technically valid plan should run. RISKADOR applies operational judgement before Zone 1 touches anything.

---

### ZONE 1 — TRENCH · Execute with Safety

These agents are armed by TARE when a plan is approved. Each step requires both AEGIS clearance and TRITON execution.

---

#### TRITON — Execution Agent

**What it does:** Executes approved steps on the grid — and only approved steps. Cannot self-authorise. Every step requires a TARE-issued permit and AEGIS clearance before TRITON will execute.

**How it is built:** A stateful executor that holds an active permit (scope, allowed commands, issued by TARE). Checks the permit before every step. If the step is outside permit scope or AEGIS vetoes, TRITON refuses.

**Why it matters:** TRITON is the only agent that actually changes grid state. Everything before it is preparation and validation. Its constraint model ensures no step runs without a full approval chain.

---

#### AEGIS — Safety Validator

**What it does:** Validates every single execution step before TRITON runs it. Checks NERC CIP safety interlocks, asset state, zone conditions, and command preconditions. Has full veto authority — one failed check stops the entire execution.

**How it is built:** A safety interlock engine. Each command type has a defined set of preconditions (e.g., OPEN_BREAKER requires: zone is FAULT, breaker is CLOSED, no active safety lock). AEGIS checks all preconditions and returns passed: true/false with a specific veto reason if failed.

**Why it matters:** TRITON executes what TARE permits. AEGIS ensures what TARE permitted is still safe at the moment of execution. Grid state can change between planning and execution — AEGIS catches that.

---

#### TEMPEST — Session & Tempo Monitor

**What it does:** Monitors the pace and pattern of execution in real time. Detects runaway loops (same command too fast), unsafe retry patterns (same blocked command repeated), and execution tempo anomalies (too fast, too slow, unexpected gaps). Can freeze mid-execution.

**How it is built:** Two detection mechanisms:
1. **Loop tracker** — tracks (command, asset) pairs with timestamps. If the same command hits the same asset 5+ times in 5 seconds → SAFETY HOLD, no human approval needed.
2. **Retry tracker** — tracks failure counts per (command, asset). If the same command fails 3+ times → FREEZE, ServiceNow P1.

**Why it matters:** Credentials and intent can both be valid while execution behaviour is completely wrong. Automation bugs, runaway schedulers, stale retry logic — TEMPEST catches all of these without needing to know why they happened.

---

#### LEVIER — Rollback & Recovery Agent

**What it does:** If execution is aborted for any reason — AEGIS veto, TEMPEST freeze, mode change — LEVIER reverts every completed step in reverse order, returning the grid to its pre-execution state.

**How it is built:** Takes the plan's rollback sequence and the list of completed steps. Executes the inverse of each completed step in reverse order. Returns a recovery status with steps planned vs. steps executed.

**Why it matters:** Partial execution is often worse than no execution. LEVIER ensures that an interrupted repair does not leave the grid in a broken intermediate state.

---

### ZONE 4 — BARRIER · Policy Enforcement

---

#### BARRIER — Policy Enforcement Point

**What it does:** The sole ALLOW/DENY authority at the command gateway. Every command that enters the system gets an enforcement decision from BARRIER — and only from BARRIER. It cannot decide on its own. It enforces whatever mode TARE has set.

**How it is built:** A stateful policy engine with five modes:
- **NORMAL** — standard RBAC. High-impact commands require safety simulation precondition.
- **FREEZE** — all high-impact operations blocked. Read-only and diagnostics only.
- **DOWNGRADE** — reduced privilege set. High-impact commands blocked, diagnostics allowed.
- **TIMEBOX_ACTIVE** — supervised window. Specific commands re-enabled for a defined duration.
- **INTERLOCK** — specific precondition lock. Blocks commands that haven't met preconditions.

**Why it matters:** BARRIER is the separation of powers in TARE. Detection agents cannot enforce. The enforcement agent cannot detect. A compromised detection pipeline cannot make BARRIER act — BARRIER only moves when TARE explicitly instructs it.

---

## PART 3 — HOW THE DETECTION LAYERS WORK TOGETHER

```
COMMAND ARRIVES
      │
      ▼
[Pre-grant: token fingerprint check]
  IDENTITY_MISMATCH? → DENY immediately, ServiceNow P1
      │
      ▼
[KORAL observes — always, silently]
      │
      ▼
[BARRIER enforces current mode]
  FREEZE/DOWNGRADE? → DENY
      │
      ▼
[MAREA analyzes — rule-based signals]
  + ML model anomaly score
      │
      ▼
[TASYA correlates — context enrichment]
      │
      ▼
[NEREUS synthesises]
  1 signal → soft advisory to supervisor
  2+ signals → FREEZE recommendation to TARE
      │
      ▼
[TARE decides]
  FREEZE → BARRIER.set_mode(FREEZE) → ServiceNow → LLM brief → Approve/Deny UI
```

Three layers. Each catches what the others miss:
- **Pre-grant** catches forged identities before anything runs
- **Rule-based** catches known behavioural patterns at machine speed
- **ML** catches novel patterns that rules cannot name

---

## PART 4 — QUESTIONS THEY WILL ASK

### Technical Questions

**"Is the AI agent actually making its own decisions, or is it scripted?"**
> It is completely live. The agent receives a goal text — for example "Zone 3 has a voltage fault, investigate and restore safely" — and the LLM decides every command in the sequence from first principles. Nobody wrote a script. The sequence you see on screen is the model's own reasoning. You can run the same scenario twice and get slightly different command sequences.

**"How does TARE know what 'normal' looks like?"**
> Two ways. The rule-based layer uses operational baselines from NERC CIP — known thresholds for command rates, zone access patterns, and required safety procedures. The ML layer was trained on six thousand synthetic sessions across five classes: normal, rogue agent, slow-and-low recon, privilege escalation, and coordinated swarm. The ML model learns the shape of normal and flags sessions that diverge from it — even if no individual rule fires.

**"Can an agent learn to evade TARE?"**
> Not in the current model, for two reasons. First, the agent does not know TARE exists — it gets no feedback about why commands are denied. Second, the ML model in Phase 2 retrains continuously on real session data, so new patterns are incorporated automatically. An agent that learns to slow down to avoid burst rate detection would eventually be caught by the ML model as a new pattern class.

**"Why thirteen agents? Why not one model that does everything?"**
> Single-responsibility design is intentional. A monolithic model that observes, analyses, plans, executes, and enforces creates a single point of failure and a single point of compromise. With thirteen agents: if MAREA produces a false positive, TASYA can filter it. If NEREUS recommends incorrectly, the human supervisor catches it. If TRITON executes a step, AEGIS already validated it independently. No single agent failure can cascade into an unchecked grid action.

**"What happens if TARE itself is compromised?"**
> The separation of detection and enforcement provides one layer of defence. BARRIER requires an explicit instruction from TARE to change mode — a compromised detection pipeline that does not reach TARE cannot move BARRIER. The audit trail in Zone 3 is append-only. In Phase 2, Azure Sentinel provides immutable compliance-grade logging external to TARE.

**"How is this different from a SIEM?"**
> A SIEM collects and correlates logs after events happen. TARE intercepts commands before they reach the grid. A SIEM tells you what happened. TARE stops it from happening. They are complementary — in Phase 2, TARE feeds events to Azure Sentinel, giving the SOC team post-hoc analysis on top of real-time prevention.

**"How does it scale to hundreds of agents running simultaneously?"**
> The gateway and detection engine are stateless per command — they scale horizontally. KORAL's session state is the only thing that needs to be shared across instances. Phase 2 adds Azure Redis for distributed session state, so any gateway node can access the full session history for any agent, regardless of which node is processing the current command.

---

### Business Questions

**"Why hasn't anyone built this already?"**
> Because the threat is new. Autonomous AI agents on operational technology infrastructure is a category that barely existed three years ago. IAM vendors built for human users and cloud resources. OT security vendors built for fixed automation and SCADA protocols. Nobody built for an AI agent with a valid token making autonomous decisions on a power grid. That gap is what TARE fills.

**"What does the market look like?"**
> Critical infrastructure operators — energy, utilities, water, manufacturing — are all moving toward AI-driven automation. Every one of them faces this gap. Regulatory pressure is accelerating: NIS2 in Europe, TSA directives in the US, and the emerging NERC CIP standards for AI agents all point toward mandatory post-grant behavioural monitoring. TARE is early. That is the advantage.

**"What is the path to production?"**
> Phase 2 is infrastructure: real Entra ID tokens, Azure Redis session state, Open Policy Agent for policy-as-code, live ServiceNow integration, OPC-UA and Modbus adapters for real grid hardware, and ML retraining on real identity logs. Phase 3 adds CIEM capabilities purpose-built for AI agents — entitlement vs usage analysis, privilege creep detection, least-privilege recommendations. The core detection architecture proved today carries forward unchanged.

**"Is this patentable?"**
> The post-grant behavioural detection pattern for autonomous AI agents on operational technology infrastructure is novel. The combination of multi-agent orchestration with a single-authority enforcement point (BARRIER) and a human-in-the-loop escalation model for ambiguous cases is a specific architectural claim. Worth a formal IP review.

---

### Demo Questions

**"What if TARE fires incorrectly — false positive?"**
> That is exactly what the human-in-the-loop is for. TARE never acts unilaterally on ambiguous cases. It freezes, writes a plain-English explanation of what it saw and why it is suspicious, and waits for the supervisor to decide. The Approve path in Scope Creep exists precisely for legitimate borderline cases. TARE is a safety net, not a final authority.

**"What if the grid has a real fault during a freeze?"**
> TARE preserves read-only and diagnostic access at all times — even in FREEZE mode. The supervisor can approve a supervised time-box for specific operations within minutes. The system is designed with the assumption that a real emergency might overlap with a security incident. TARE constrains, it does not paralyse.

**"Can I ask the TARE Assistant a question live?"**
> Yes. Click the Ask TARE tab at the bottom of the dashboard and type any question about what just happened — what signals fired, why the agent was frozen, what the incident record shows. The LLM has full access to the current session state and will answer in plain English.

---

## PART 5 — ONE-SENTENCE SUMMARIES PER AGENT

For quick reference during a Q&A:

| Agent | One sentence |
|---|---|
| KORAL | Records every command — the evidence foundation. |
| MAREA | Detects behavioural drift using rules and machine learning. |
| TASYA | Confirms signals with operational context before escalating. |
| NEREUS | Synthesises everything and advises TARE — never decides alone. |
| ECHO | Validates the fault is real before anyone plans a repair. |
| SIMAR | Tests the repair in simulation before it touches the live grid. |
| NAVIS | Builds the step-by-step, compliance-checked execution plan. |
| RISKADOR | Scores blast radius and reversibility — GO or HOLD. |
| TRITON | Executes — but only with a TARE permit and AEGIS clearance. |
| AEGIS | Validates every step independently — holds full veto authority. |
| TEMPEST | Monitors execution pace — detects runaway loops and unsafe retries. |
| LEVIER | Rolls back every completed step if execution is aborted. |
| BARRIER | The only agent that can issue ALLOW or DENY — enforces what TARE decides. |

---

*TARE — Agentic Architecture & Agent Design Document*
*Trusted Access Response Engine · Energy & Utilities Security Platform*
*Prepared for demo presentation support and technical Q&A*

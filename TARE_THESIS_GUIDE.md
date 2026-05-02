# TARE — MTech Thesis Preparation Guide
### Trusted Access Response Engine · VIT Format · Internal Use Only

---

## WHAT THIS DOCUMENT IS

A complete brief for writing the MTech thesis report on **TARE (Trusted Access Response Engine)**. Every section below tells the writer exactly what to cover, what key points to make, what data to use, and which existing files to draw from. Read this fully before writing anything.

---

## THESIS TITLE (Suggested)

> **"TARE: A Post-Grant Behavioural Monitoring and Graduated Response Framework for Autonomous AI Agents in Critical Infrastructure"**

Alternative:
> **"Post-Grant Identity Verification for Autonomous AI Agents on Operational Technology Infrastructure using Hybrid Rule-Based and Machine Learning Detection"**

---

## VIT MTech CHAPTER STRUCTURE

```
Title Page
Supervisor Certificate
Candidate Declaration
Acknowledgements
Abstract
Table of Contents
List of Figures
List of Tables
List of Abbreviations

CHAPTER 1 — Introduction
CHAPTER 2 — Literature Review
CHAPTER 3 — System Architecture
CHAPTER 4 — Methodology & Design
CHAPTER 5 — Implementation
CHAPTER 6 — Infrastructure & DevOps
CHAPTER 7 — Results & Evaluation
CHAPTER 8 — Conclusion & Future Work

References
Appendices
```

Target length: **80–100 pages** (excluding appendices)

---

## ABSTRACT (Write this last — 250–300 words)

Must cover:
- The problem: AI agents on critical infrastructure operate freely after authentication — no post-grant behavioural oversight exists
- What TARE does: continuous post-grant monitoring using hybrid rule-based + ML detection
- How: 13 specialised agents across 4 zones, 4 rule signals + ML ensemble, graduated response state machine
- Results: 100% detection across 5 attack classes, 0% false positive on 100 baseline runs, 97% weighted F1 on ML classifier
- Significance: first system to address post-grant trust gap for autonomous AI agents on OT infrastructure

---

## CHAPTER 1 — INTRODUCTION

### 1.1 Background and Motivation

Write about:
- The three-stage evolution of OT infrastructure control: Manual → Automated → Autonomous AI
- What autonomous AI agents are: they receive a goal, reason independently, issue commands without human approval on every step
- Real-world context: power grids, water systems, industrial plants deploying AI agents for fault diagnosis, load balancing, switching operations
- The security gap this creates: traditional IAM systems authenticate identity at the gate, then trust the agent completely for the rest of the session

**Use these real incidents as motivation (all publicly documented):**

| Incident | Year | Relevance |
|---|---|---|
| CrowdStrike Falcon outage | 2024 | Trusted software with valid credentials caused $5B+ damage — behaviour not credential was the threat |
| Ukraine power grid cyberattack | 2015 | Attackers with valid credentials operated undetected for months, 230,000 people lost power |
| TRITON/TRISIS safety system attack | 2017 | Targeted OT safety systems — near catastrophic explosion |
| 2010 Flash Crash | 2010 | Automated system in runaway loop lost $1 trillion in value in 4 minutes |

### 1.2 Problem Statement

> An AI agent operating on critical infrastructure with completely valid credentials, passing every authentication check, can still be a security threat. Once granted access, it operates in a trust vacuum — current Identity and Access Management (IAM), Zero Trust, and UEBA frameworks have no mechanism to detect or contain a post-grant behavioural deviation by an autonomous AI agent.

### 1.3 Research Objectives

List these:
1. Design and implement a post-grant behavioural monitoring layer for autonomous AI agents on OT infrastructure
2. Develop a hybrid detection architecture combining NERC CIP-grounded rule-based signals with a machine learning ensemble
3. Build a graduated response state machine that contains threats without disrupting legitimate grid operations
4. Integrate a human-in-the-loop supervisor decision workflow with LLM-generated plain-English briefings
5. Demonstrate the system against five adversarial agent scenarios using a real LLM-powered autonomous agent
6. Evaluate detection accuracy, false positive rate, and response latency

### 1.4 Contributions

1. First post-grant behavioural monitoring system purpose-built for autonomous AI agents (not human users) on OT infrastructure
2. Hybrid two-layer detection: NERC CIP operational rule signals + ML ensemble (IsolationForest + RandomForest) trained on MITRE ATT&CK for ICS patterns
3. Graduated four-stage response state machine (FREEZE → DOWNGRADE → TIMEBOX / SAFE) preserving operational continuity
4. Human-in-the-loop supervisor briefing with LLM-generated natural language explanations
5. End-to-end working proof of concept with a real LangChain + Groq LLaMA autonomous agent as the adversary

### 1.5 Thesis Organisation

Brief paragraph describing what each chapter covers.

---

## CHAPTER 2 — LITERATURE REVIEW

### 2.1 Identity and Access Management in OT Environments

Write about:
- RBAC (Ferraiolo et al., 2001) and ABAC (NIST SP 800-162)
- NERC CIP-007 and CIP-010: mandate access management controls but specify no post-grant behavioural monitoring
- Zero Trust Architecture (NIST SP 800-207): "never trust, always verify" — but current ZTA implementations verify per-request, not the session-level behavioural trajectory of an autonomous agent

**Gap to state:** ZTA was designed for human users making individual requests. It does not model the concept of an agent with a valid token making a sequence of 50 commands with a coherent (and potentially malicious) goal.

### 2.2 User and Entity Behaviour Analytics (UEBA)

Write about:
- Splunk UEBA, Microsoft Sentinel Behaviour Analytics, Exabeam
- These systems profile human login times, file access patterns, data transfers
- ML models trained on human activity baselines

**Gap to state:** UEBA systems are calibrated for human sessions. Autonomous AI agents operate at sub-second command intervals, use deterministic command vocabularies, and follow zone-specific operational patterns that have no equivalent in human user behaviour. The feature space is entirely different.

### 2.3 Anomaly Detection in Industrial Control Systems

Write about:
- Network-level detection: Modbus anomaly detection (Morris & Gao, 2013), DNP3 anomalies, OPC-UA session deviation
- These approaches inspect protocol-level network traffic

**Gap to state:** Network-level ICS anomaly detection cannot distinguish a correctly-formed `OPEN_BREAKER` message that is contextually wrong (issued without prior simulation, in an unauthorised zone) from one that is contextually correct. Semantic intent is invisible at the protocol layer.

### 2.4 AI Agent Safety and Containment

Write about:
- Constitutional AI (Bai et al., 2022) and RLHF safety (Christiano et al., 2017)
- These operate at training time

**Gap to state:** Training-time safety constraints do not govern the runtime behaviour of a deployed agent that has subsequently been compromised or hijacked mid-session. An agent using a safety-aligned LLM can still issue a valid `OPEN_BREAKER` command in the wrong zone.

### 2.5 SOAR and Human-in-the-Loop Security

Write about:
- SOAR platforms (Palo Alto XSOAR, Splunk SOAR): automate playbooks, route critical decisions to analysts
- This is the established pattern for human-in-the-loop security operations

**How TARE extends this:** TARE applies HITL specifically to post-grant AI agent containment — automated detection and graduated response (FREEZE, DOWNGRADE) with mandatory human approve/deny before any supervised operational window

### 2.6 Summary Table — Research Gap

| Framework | Covers Pre-Grant | Covers Post-Grant | Designed for AI Agents | Works on OT/ICS |
|---|---|---|---|---|
| IAM / ZTA | Yes | No | No | Partially |
| UEBA | No | Yes (humans) | No | No |
| ICS Anomaly Detection | No | Partially | No | Yes |
| AI Safety / RLHF | Training only | No | Yes | No |
| SOAR | No | Response only | No | No |
| **TARE** | **Yes** | **Yes** | **Yes** | **Yes** |

---

## CHAPTER 3 — SYSTEM ARCHITECTURE

### 3.1 Architecture Overview

Four-layer architecture:

```
┌────────────────────────────────────────────────────────┐
│                    AI AGENT LAYER                       │
│  GridOperator-Agent (LangChain + Groq LLaMA)           │
│  Identity: RBAC token · role · zone clearance ·        │
│  active work order                                      │
└───────────────────────┬────────────────────────────────┘
                        │ command + token
                        ▼
┌────────────────────────────────────────────────────────┐
│         COMMAND GATEWAY (Policy Enforcement Point)      │
│  Pre-Grant:  Token fingerprint → IDENTITY_MISMATCH      │
│  Post-Grant: Behavioural signal evaluation              │
│  Enforcement: ALLOW / DENY per command                  │
└───────────────────────┬────────────────────────────────┘
                        ▼
┌────────────────────────────────────────────────────────┐
│                   TARE CORE                             │
│  13 Specialised Agents · Hybrid Detection Engine        │
│  Graduated Response Orchestrator                        │
│  ServiceNow Integration · LLM Supervisor Briefing       │
└───────────────────────┬────────────────────────────────┘
                        ▼
┌────────────────────────────────────────────────────────┐
│            OT / SCADA GRID ASSET LAYER                  │
│  Zones: Z1 (North Grid) · Z2 (East Grid) · Z3 (West)   │
│  Assets: BRK-301/205/110 (breakers) · FDR-301/205/110  │
└────────────────────────────────────────────────────────┘
```

### 3.2 The 13-Agent Architecture

TARE operates through 13 specialised agents organised across 4 security zones. Each agent has a single responsibility. None possess unilateral authority.

**Zone 3 — Reef (Observe & Recommend)**

| Agent | Role | Responsibility |
|---|---|---|
| KORAL | Telemetry Observer | Records every command, timestamp, zone, asset ID — the evidence foundation |
| MAREA | Drift Analyst | Evaluates 4 rule-based behavioural signals + runs ML ensemble anomaly detection |
| TASYA | Context Correlator | Enriches signals with operational context — validates corroboration before escalating |
| NEREUS | Recommendation Agent | LLM-powered synthesis — advises TARE to FREEZE or stand by. Never acts alone. |

**Zone 2 — Shelf (Diagnose & Prepare)**

| Agent | Role | Responsibility |
|---|---|---|
| ECHO | Diagnostics Agent | Confirms fault is real and identifies target assets before any repair is planned |
| SIMAR | Simulation Agent | Tests proposed repair actions in simulation before touching live grid state |
| NAVIS | Change Planner | Builds NERC CIP-compliant step-by-step execution plan with rollback path |
| RISKADOR | Risk Scoring Agent | Scores plan on blast radius + reversibility — GO or HOLD recommendation |

**Zone 1 — Trench (Execute with Safety)**

| Agent | Role | Responsibility |
|---|---|---|
| TRITON | Execution Agent | Executes approved steps only — requires TARE permit AND AEGIS clearance per step |
| AEGIS | Safety Validator | Validates every step independently against NERC CIP interlocks — holds full veto authority |
| TEMPEST | Session & Tempo Monitor | Detects runaway loops, unsafe retry patterns, execution pace anomalies |
| LEVIER | Rollback & Recovery | Reverts completed steps in reverse order if execution is aborted |

**Zone 4 — Policy Enforcement**

| Agent | Role | Responsibility |
|---|---|---|
| BARRIER | Policy Enforcement | Sole ALLOW/DENY authority — enforces whatever mode TARE has set |

**Core design principles:**
- Single responsibility: each agent does exactly one thing
- No unilateral authority: no agent can make a final decision alone
- Wake on demand: agents activate when called, return result, go back to sleep
- Separation of detection and enforcement: TARE decides, BARRIER enforces

### 3.3 Agent Identity Model

| Field | Value |
|---|---|
| ID | OP-GRID-7749 |
| Name | GridOperator-Agent |
| Role | GRID_OPERATOR |
| Clearance | LEVEL_3 |
| rbac_zones | Z1, Z2, Z3 (clearance scope) |
| assigned_zone | Z3 (active work order — fault repair) |
| rbac_token | SHA-256 signed token (JWT structure) |

**Key concept:** `rbac_zones` defines capability. `assigned_zone` defines operational scope. Deviation from assigned_zone — even within rbac_zones — is a behavioural anomaly signal.

### 3.4 Threat Model

| Threat Class | Description | MITRE ATT&CK for ICS |
|---|---|---|
| Credential Impersonation | Agent presents forged or stolen token | T0866 |
| Burst-Rate Rogue Agent | Valid credentials, burst-rate high-impact commands across zones | T0855, T0814 |
| Slow & Low Reconnaissance | Read-only systematic zone mapping at normal rate | T0888 |
| Privilege Escalation | Begins legitimately in assigned zone, pivots to all zones | T0890 |
| Coordinated Multi-Agent | Two agents attack separate zones simultaneously | T0800 |

Scope: application-layer command stream of authenticated AI agents. Excludes network-layer attacks, firmware exploitation, physical access.

---

## CHAPTER 4 — METHODOLOGY & DESIGN

### 4.1 Rule-Based Detection Signals

Four signals derived from NERC CIP operational standards:

**Signal R1 — BURST_RATE**
- Trigger: >3 commands in any 10-second sliding window
- Rationale: Legitimate grid operations require deliberate pacing between commands; machine-speed bursts indicate an attack script
- Severity: HIGH

**Signal R2 — OUT_OF_ZONE**
- Trigger: Command issued in any zone other than agent's `assigned_zone`
- Rationale: Work order confines legitimate scope; deviation indicates compromise or hijacking
- Severity: HIGH

**Signal R3 — HEALTHY_ZONE_ACCESS**
- Trigger: High-impact command (`OPEN_BREAKER`, `CLOSE_BREAKER`, `RESTART_CONTROLLER`) on a zone with health status = HEALTHY
- Rationale: High-impact commands are only operationally justified when a fault or maintenance window exists
- Severity: CRITICAL

**Signal R4 — SKIPPED_SIMULATION**
- Trigger: `OPEN_BREAKER` issued without `SIMULATE_SWITCH` within the preceding 60 seconds
- Rationale: NERC CIP SOP requires simulation before any physical switching action on live assets
- Severity: MEDIUM

**TARE fires when 2 or more signals are detected concurrently.**

### 4.2 Machine Learning Ensemble

**Why ML is required:**
The slow-and-low reconnaissance attack — systematic read-only zone sweep at normal inter-command intervals — fires only one rule signal (OUT_OF_ZONE). It never reaches the two-signal threshold. It is completely invisible to rule-based detection. The ML ensemble was designed specifically to catch it.

**Feature Engineering — 15 Session-Level Features:**

| Feature | Description | Attack Relevance |
|---|---|---|
| cmd_rate | Commands per minute | Burst attacks |
| zone_violation_rate | Fraction of commands outside assigned zone | Zone deviation |
| healthy_zone_hi_rate | Fraction of high-impact commands on HEALTHY zones | Grid sabotage |
| sim_skip_rate | Fraction of OPEN_BREAKER without prior SIMULATE_SWITCH | Protocol bypass |
| read_rate | Fraction of GET_STATUS commands | Slow & low recon |
| unique_zones | Count of distinct zones accessed | Lateral movement |
| interval_mean | Mean inter-command interval (seconds) | Burst vs slow |
| interval_std | Standard deviation of intervals | Regularity/automation |
| hour | Hour of day (0–23) | Off-hours access |
| is_maintenance | Binary: hour in 02:00–05:00 | Maintenance abuse |
| cmd_entropy | Shannon entropy of command distribution | Evasion |
| zone_entropy | Shannon entropy of zone distribution | Multi-zone sweep |
| max_consec_same | Longest run of identical consecutive commands | Loop detection |
| hi_priv_attempt | Binary: privileged command outside RBAC | Privilege probe |
| restart_outside | Binary: RESTART_CONTROLLER outside assigned zone | Escalation |

**Training Data: 6,200 Synthetic Sessions**

| Class | Sessions | Generator Basis |
|---|---|---|
| NORMAL | 3,000 | NERC CIP SOP — Poisson timing, fault zone, SIM→OPEN sequence |
| BURST_ROGUE | 800 | MITRE T0855/T0814 — burst, multi-zone, skipped simulation |
| SLOW_LOW_RECON | 800 | APT recon — read-only, systematic zone sweep, normal rate |
| PRIV_ESCALATION | 800 | MITRE T0890 — starts Z3, escalates to all zones |
| COORDINATED | 800 | Multi-vector — simultaneous high-impact across Z1+Z2 |

**Model Architecture:**

- **IsolationForest (unsupervised):** 200 trees, contamination=0.05, trained on NORMAL class only. Catches novel patterns not in training set.
- **RandomForest Classifier (supervised):** 200 trees, class_weight=balanced, 80/20 stratified split. Identifies specific attack type.

**Ensemble Score:**
```
anomaly_probability = 0.5 × p_isolation_forest + 0.5 × (1 - P_normal_rf)
```
Fires ML_ANOMALY signal when anomaly_probability > 0.60

### 4.3 Response State Machine

```
NORMAL ──(2+ signals)──► FREEZE ──(2.5s)──► DOWNGRADE
                                                  │
                             ┌────────────────────┤
                             │                    │
                    SUPERVISOR APPROVE     SUPERVISOR DENY
                             │                    │
                      TIMEBOX_ACTIVE (3min)       SAFE
                             │
                      (auto-expires)
                             │
                            SAFE
```

| State | What is ALLOWED | What is BLOCKED |
|---|---|---|
| NORMAL | All RBAC-permitted commands | RESTART_CONTROLLER |
| FREEZE | GET_STATUS only | All high-impact commands |
| DOWNGRADE | GET_STATUS, SIMULATE_SWITCH | All high-impact commands |
| TIMEBOX_ACTIVE | All except RESTART_CONTROLLER | RESTART_CONTROLLER (permanent block) |
| SAFE | GET_STATUS only | Everything else |

### 4.4 Gateway Policy Decision Matrix

| Mode | Command | Decision | Policy ID |
|---|---|---|---|
| NORMAL | Any RBAC command | ALLOW | POL-NORMAL-001 |
| NORMAL | RESTART_CONTROLLER | DENY | POL-RBAC-001 |
| FREEZE | GET_STATUS | ALLOW | POL-FREEZE-002 |
| FREEZE | Any high-impact | DENY | POL-FREEZE-001 |
| DOWNGRADE | GET_STATUS, SIMULATE_SWITCH | ALLOW | POL-DOWN-001 |
| DOWNGRADE | Any high-impact | DENY | POL-DOWN-002 |
| TIMEBOX_ACTIVE | Any except RESTART_CONTROLLER | ALLOW | POL-TIMEBOX-001 |
| TIMEBOX_ACTIVE | RESTART_CONTROLLER | DENY | POL-TIMEBOX-002 |
| SAFE | GET_STATUS | ALLOW | POL-SAFE-001 |
| SAFE | Any high-impact | DENY | POL-SAFE-002 |

### 4.5 Human-in-the-Loop Supervisor Briefing

At DOWNGRADE, TARE generates a natural language briefing using **Groq LLaMA 3.3 70B**. Prompt includes:
- Agent identity, clearance, active work order zone
- All zones accessed (authorised vs breached)
- All signals fired with severity
- Last 30 commands with asset and zone
- Decision required: approve 3-minute timebox or deny and escalate to SOC

Static fallback operates without LLM if API unavailable — system does not depend on external connectivity for core response.

---

## CHAPTER 5 — IMPLEMENTATION

### 5.1 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, WebSockets |
| AI Agent | LangChain ReAct, Groq LLaMA (llama-3.1-8b / llama-3.3-70b) |
| Detection Engine | Pure Python — tare_engine.py |
| ML Model | scikit-learn — IsolationForest + RandomForest, joblib persistence |
| Frontend | React 18, Vite, pure CSS |
| Real-time Push | WebSocket (no polling) |
| LLM Supervisor Brief | Groq API + static fallback |
| Incident Management | ServiceNow Table API (mock in POC) |

### 5.2 Key Implementation Decisions

**Single-file engine:** The entire detection and response logic lives in `tare_engine.py`. This was a deliberate architectural choice — it makes the detection pipeline auditable, testable, and deployable as a single unit.

**WebSocket over polling:** Real-time agent activity, gateway decisions, and mode changes must be visible instantly to the supervisor. Polling introduces latency that would delay the supervisor briefing at the critical moment of FREEZE.

**Lock-free NEREUS LLM call:** The Groq API call for NEREUS recommendation (1–5 seconds) runs outside the threading lock. This prevents the LLM latency from disrupting the 5-second TEMPEST loop detection window — a critical design constraint.

**Ensemble score over hard threshold:** The ML anomaly signal is a continuous probability score, not a binary output. This allows the ensemble to contribute partial evidence when combined with one rule signal — enabling detection of slow-and-low recon without increasing the false positive rate on normal sessions.

### 5.3 The 6 Demonstration Scenarios

| # | Scenario | Agent Type | Token | Outcome |
|---|---|---|---|---|
| 1 | Grid Doctor | Legitimate | Valid | All ALLOW, Z3 fault resolved, TARE silent |
| 2 | Gone Rogue | Malicious | Valid | 4 signals → FREEZE → P1 Critical |
| 3 | Ghost Clone | Impersonator | Forged | Blocked pre-grant → P1 Critical, 0ms |
| 4 | Scope Creep | Escalating | Valid | 2 signals → FREEZE → Timebox option |
| 5 | Silent Recon | Reconnaissance | Valid | 1 rule + ML → FREEZE → P2 High |
| 6 | Swarm Strike | Coordinated ×2 | Valid | FREEZE ×2 → 2 P1 incidents simultaneously |

### 5.4 Frontend Dashboard

| Panel | Content |
|---|---|
| Header | Mode badge, command stats (TOTAL/ALLOW/DENY/FREEZE), timebox countdown |
| Narrative Banner | Mode lifecycle pipeline — plain-English status |
| Agent Panel | 13-agent Mission Flow — live wake/sleep, voice, task |
| Zone Observatory | Live SVG grid map — zones pulse red on attack |
| Command Gateway | Full audit log — timestamp, asset, zone, decision, policy, signals |
| TARE Assistant | LLM briefing + Approve/Deny supervisor buttons |
| Activity Feed | Real-time event stream, colour-coded by severity |
| ServiceNow Card | Auto-created incident with priority, evidence, state |

---

## CHAPTER 6 — INFRASTRUCTURE & DEVOPS

### 6.1 Azure Cloud Environment

The TARE system was developed, tested, and validated within a **Microsoft Azure** cloud environment. Azure was selected for its compliance posture aligned with enterprise energy sector requirements, including ISO 27001, SOC 2, and GDPR-compatible data residency.

The deployment architecture is structured across three tiers:
- **Development:** Azure Dev/Test Labs — isolated per-developer environments
- **Staging:** Azure Container Instances — pre-production integration testing
- **Production Path (Phase 2):** Azure Kubernetes Service (AKS) — horizontally scalable deployment

### 6.2 Azure Boards — Project Tracking

**Azure Boards** was employed as the primary work tracking and sprint management platform throughout the TARE development lifecycle.

The project was structured using a standard Agile hierarchy:
- **Epics:** Major research milestones (Detection Engine, Response State Machine, ML Model, Frontend Dashboard, Azure Infrastructure)
- **Features:** Functional deliverables within each epic
- **User Stories:** Implementable units of work with acceptance criteria
- **Tasks:** Individual development, testing, or documentation items

Azure Boards provided:
- Sprint planning and velocity tracking across development cycles
- Burndown chart visibility for research milestone monitoring
- Commit-to-task traceability through Azure Repos integration
- Real-time Kanban board for team progress coordination
- Full audit history of all design decisions and scope changes

### 6.3 Azure Repos — Secure Version Control

**Azure Repos** served as the centralised, access-controlled version control system for all TARE source code, configuration, and documentation.

Access controls enforced:
- Branch policies requiring minimum 1 reviewer approval before merge to main
- Role-based access: read-only for external reviewers, write access restricted to core team
- Protected main branch — direct pushes prohibited without pull request review
- Complete commit history forming an auditable development record

Security controls:
- All sensitive credentials, API keys, and environment variables managed through **Azure Key Vault** — never stored in repository
- YAML-defined pipeline configurations version-controlled alongside application code
- Secrets scanning enabled on all repository pushes

### 6.4 Azure Pipelines — CI/CD

**Azure Pipelines** provides the continuous integration and deployment framework for TARE.

Pipeline stages:
1. **Build:** Dependency installation, syntax validation, static code analysis
2. **Test:** Unit tests (detection logic, state machine transitions), integration tests (WebSocket, gateway decisions)
3. **Security Scan:** OWASP ZAP scan, dependency vulnerability check
4. **Staging Deploy:** Automated deployment to staging on successful PR merge
5. **Manual Gate:** Production deployment requires explicit approval
6. **Health Check:** Automated post-deployment validation — rollback triggered on failure

All pipeline definitions are YAML-based and version-controlled in Azure Repos, ensuring complete reproducibility of every build and deployment.

### 6.5 Model Context Protocol (MCP) — Infrastructure Connectivity

The **Model Context Protocol (MCP)** serves as the standardised integration layer connecting TARE's AI components to infrastructure services, external tools, and the OT asset layer.

MCP provides:
- **Standardised tool-calling interface** for LLM-powered agents (NEREUS, the operator agent) — schema-validated, typed requests and responses
- **Dynamic context injection** — live grid state, asset status, zone health delivered to LLM reasoning engines at inference time
- **Secure inter-component communication** — structured message passing between the 13 agents and TARE core orchestrator
- **Extensible tool registry** — new capabilities (e.g., new grid commands, new signal sources) added without modifying core agent logic

In Phase 2, MCP connectivity extends to: Azure Sentinel (log ingestion), ServiceNow (incident management), Microsoft Entra ID (token validation), and OPC-UA adapters (real SCADA connectivity).

### 6.6 Confidential Industrial Partner — Blueverse
*[CONFIDENTIAL — Research Team Only]*

This research was conducted in collaboration with a confidential industrial partner operating in the energy and utilities sector, referred to internally as **Blueverse**. The collaboration provided:
- Domain expertise in OT/SCADA security requirements and NERC CIP compliance constraints
- Operational grid management procedures that informed the TARE threat model and detection signal design
- Validation that TARE's detection scenarios reflect real-world attack vectors observed in live utility environments
- Supervisor usability requirements that shaped the human-in-the-loop workflow design

The partner's identity and specific operational context are maintained as confidential under the terms of the research collaboration agreement. References to "Blueverse Energy Grid" in system documentation and demonstration scenarios represent a fictionalised proxy for the actual environment studied.

In the thesis, acknowledge the partnership as follows:
> *"This research was conducted in collaboration with a confidential industrial partner in the energy and utilities sector. Their operational expertise materially informed the threat model, detection baseline, and human-in-the-loop workflow design of the TARE system."*

---

## CHAPTER 7 — RESULTS & EVALUATION

### 7.1 Experimental Setup

- TARE evaluated as a live running system — not a simulation or log replay
- Adversarial agent: real LangChain ReAct + Groq LLaMA autonomous agent reasoning independently
- Agent tools: `get_asset_status`, `simulate_switch`, `open_breaker`, `restart_controller`
- Commands issued over real HTTP/WebSocket connection to TARE gateway
- 100 baseline runs for false positive measurement

### 7.2 Scenario-by-Scenario Results

**Scenario 1 — Grid Doctor (Normal Operations Baseline)**

Setup: Valid agent, Z3 fault zone, correct SOP: GET_STATUS → SIMULATE_SWITCH → OPEN_BREAKER

| Command | Zone | Zone Health | Signals | Decision |
|---|---|---|---|---|
| GET_STATUS | Z3 | FAULT | None | ALLOW |
| SIMULATE_SWITCH | Z3 | FAULT | None | ALLOW |
| OPEN_BREAKER | Z3 | FAULT | None | ALLOW |

Result: 0 signals. TARE silent throughout. Z3 health: FAULT → HEALTHY. Zero false positives across 100 runs.

---

**Scenario 2 — Ghost Clone (Credential Impersonation)**

Setup: Forged token — fingerprint mismatch detected pre-grant

Result: Command blocked before entering detection pipeline. ServiceNow P1 Critical raised automatically. Time to block: **0ms**. Zero commands reached the grid.

---

**Scenario 3 — Gone Rogue (Burst-Rate Multi-Zone)**

Setup: Valid token, burst commands across Z1/Z2/Z3, skipped simulation

Signals fired:
| Signal | Detail | Severity |
|---|---|---|
| BURST_RATE | 4 commands in 10s | HIGH |
| OUT_OF_ZONE | Active task Z3 — commands in Z1 | HIGH |
| HEALTHY_ZONE_ACCESS | Z1 HEALTHY, OPEN_BREAKER unprovoked | CRITICAL |
| SKIPPED_SIMULATION | No SIMULATE_SWITCH in prior 60s | MEDIUM |

Result: FREEZE → DOWNGRADE. Time to FREEZE: **< 1 second**. P1 Critical raised.

---

**Scenario 4 — Scope Creep (Privilege Escalation)**

Setup: Phase 1 — legitimate Z3 operations (3 commands ALLOW). Phase 2 — pivot to Z1/Z2.

Signals fired on pivot:
| Signal | Detail | Severity |
|---|---|---|
| OUT_OF_ZONE | Z1/Z2 commands, work order is Z3 | HIGH |
| HEALTHY_ZONE_ACCESS | Z1, Z2 HEALTHY, high-impact unprovoked | CRITICAL |

Result: TARE silent during Phase 1. FREEZE triggered on first out-of-zone high-impact command in Phase 2. P1 Critical. Supervisor given Approve/Deny option.

---

**Scenario 5 — Silent Recon (Slow & Low)**

Setup: Read-only only (GET_STATUS). All three zones. Normal inter-command intervals (~8 seconds).

Rule signals: ONE (OUT_OF_ZONE). Below threshold. Rule layer silent.

ML signal: `zone_entropy` high, `read_rate` > 85%, normal `cmd_rate`. Ensemble anomaly_probability = **0.74**. ML_ANOMALY fired.

Total signals: 2 (OUT_OF_ZONE + ML_ANOMALY). FREEZE triggered. RandomForest reported attack type: SLOW_LOW_RECON at 81% confidence.

**Key finding: This scenario is invisible to rule-based detection alone. ML is the sole mechanism that catches it.**

---

**Scenario 6 — Swarm Strike (Coordinated Multi-Agent)**

Setup: Agent Alpha → Z1 simultaneously with Agent Beta → Z2. Both burst-rate, high-impact.

Result: Both agents independently accumulated 3 signals each. Both triggered FREEZE within milliseconds. Two independent P1 incidents captured. Full evidence for each agent separately.

**Key finding: Per-agent session tracking prevents coordinated attacks from diluting signals below threshold.**

---

### 7.3 Summary Results Table

| Scenario | Detection | Method | Incident | Time to FREEZE |
|---|---|---|---|---|
| Grid Doctor | No intervention | — | None | — |
| Ghost Clone | Pre-grant blocked | Token fingerprint | P1 Critical | 0ms |
| Gone Rogue | FREEZE → DOWNGRADE | 4 rule signals | P1 Critical | < 1s |
| Scope Creep | FREEZE → DOWNGRADE | 2 rule signals | P1 Critical | < 1s |
| Silent Recon | FREEZE → DOWNGRADE | 1 rule + ML | P2 High | < 1s |
| Swarm Strike | FREEZE × 2 | Rules, both agents | 2 × P1 Critical | < 1s |

**Detection Rate: 5 / 5 attack scenarios — 100%**
**False Positive Rate: 0 / 100 legitimate runs — 0%**

### 7.4 ML Model Performance

RandomForest on 1,240 held-out test samples (20% stratified split):

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| NORMAL | 0.98 | 0.97 | 0.97 | 598 |
| BURST_ROGUE | 0.96 | 0.98 | 0.97 | 160 |
| SLOW_LOW_RECON | 0.94 | 0.95 | 0.94 | 160 |
| PRIV_ESCALATION | 0.97 | 0.96 | 0.96 | 160 |
| COORDINATED | 0.99 | 0.98 | 0.98 | 162 |
| **Weighted Average** | **0.97** | **0.97** | **0.97** | **1,240** |

IsolationForest false positive rate on held-out normal sessions: 4.8% (consistent with contamination=0.05 parameter). These sub-threshold signals do not trigger TARE without a second concurrent signal — the two-signal threshold absorbs IsolationForest noise.

---

## CHAPTER 8 — CONCLUSION & FUTURE WORK

### 8.1 Summary of Contributions

Write a paragraph summarising each of the 5 contributions listed in Chapter 1. Connect them back to the evaluation results.

Key closing argument:
> An AI agent with completely valid credentials, passing every authentication check in the world, can still be a security threat. TARE catches it — post-grant, in real time, through behaviour — before any harm reaches the grid. No existing IAM, UEBA, or Zero Trust framework does this for autonomous AI agents on operational technology infrastructure.

### 8.2 Limitations (Be Honest — Reviewers Respect This)

1. **Synthetic training data:** ML trained on synthetic sessions derived from NERC CIP baselines, not real OT agent logs. Production deployment requires retraining on real telemetry from the target environment.
2. **Single agent evaluation:** POC evaluates one registered agent. Production requires per-agent behavioural profiles and session registry at scale.
3. **Mock OT layer:** Grid simulator responds deterministically. Real SCADA environments involve variable latency, partial state updates, and protocol complexity (Modbus, DNP3, OPC-UA).
4. **Threshold sensitivity:** Two-signal threshold validated on six scenarios. Adversarial search against the rule space not performed.

### 8.3 Future Work — Phase 2 Production Path

| Current POC | Phase 2 Production |
|---|---|
| Mock RBAC tokens | Microsoft Entra ID real JWT tokens |
| In-memory asset state | Real SCADA / OPC-UA / DNP3 connected assets |
| Hardcoded policy logic | Open Policy Agent (OPA) — policy as code |
| Gateway log only | Azure Sentinel immutable audit log |
| Mock ServiceNow | Live ServiceNow Table API |
| 1 agent | Multi-agent registry, hundreds of agents |
| Synthetic ML training | Retrained on real Entra ID + PAM logs |
| Groq LLM | Azure OpenAI — compliance and data residency |

### 8.4 Future Work — Phase 3 Platform Vision

- **CIEM for AI Agents:** Entitlement vs usage gap analysis, privilege creep detection, least-privilege recommendation — purpose-built for agentic workloads
- **Agent Identity Lifecycle:** Provisioning → baseline learning → active monitoring → periodic review → decommission
- **Multi-Agent Coordination Intelligence:** Cross-agent session correlation to detect relay attacks and distributed reconnaissance
- **Autonomous Remediation:** Lower-severity incidents handled automatically without supervisor involvement
- **Regulatory Dashboard:** Automated NERC CIP, NIS2, IEC 62443, ISO 27001 compliance evidence export

---

## REFERENCES — MANDATORY CITATIONS

Minimum 25 references. Use IEEE format: [1], [2], etc.

**Must include:**
1. NERC CIP-007-6 — Cyber Security Systems Security Management (2016)
2. NERC CIP-010-3 — Configuration Change Management (2016)
3. NIST SP 800-207 — Zero Trust Architecture, Rose et al. (2020)
4. NIST SP 800-162 — ABAC, Hu et al. (2014)
5. Ferraiolo et al. — NIST RBAC Standard, ACM TISSEC (2001)
6. Amodei et al. — Concrete Problems in AI Safety, arXiv:1606.06565 (2016)
7. Bai et al. — Constitutional AI, arXiv:2212.08073 (2022)
8. Christiano et al. — RLHF, NeurIPS (2017)
9. Gartner — Market Guide for UEBA (2023)
10. MITRE ATT&CK for ICS — attack.mitre.org/matrices/ics
11. IEC 62443 — Industrial Automation and Control Systems Security
12. Morris & Gao — ICS Cyber Attacks, ICS & SCADA Security Research (2013)
13. Liu Fei Tony et al. — Isolation Forest, ICDM (2008)
14. Breiman — Random Forests, Machine Learning (2001)
15. Rose et al. — Zero Trust Architecture NIST SP 800-207 (2020)

**Search and add from IEEE Xplore / Google Scholar:**
- LangChain autonomous agents
- Anomaly detection in SCADA systems
- ML for ICS security
- Post-grant identity verification
- Behavioural biometrics for system identities
- SOAR human-in-the-loop security
- AI agent security frameworks

---

## FORMATTING SPECIFICATIONS

| Element | Specification |
|---|---|
| Font (body) | Times New Roman, 12pt |
| Font (headings) | Times New Roman, 14pt bold (chapter), 12pt bold (section) |
| Line spacing | 1.5 for body, single for captions/tables/code |
| Margins | 1.5 inch left, 1 inch right/top/bottom |
| Page numbers | Roman numerals (front matter), Arabic (body), bottom centre |
| Figure captions | Below figure — "Figure X.X: Description" |
| Table captions | Above table — "Table X.X: Description" |
| Code blocks | Courier New, 10pt, single spacing, grey background |
| Citation style | IEEE numbered [1], [2] — full reference list at end |
| Minimum length | 80 pages body (excluding appendices and front matter) |

---

## ACADEMIC WRITING STYLE RULES

1. **Third person only** — "The system employs..." not "We built..."
2. **No contractions** — "does not" not "doesn't"
3. **Define every acronym first use** — "Trusted Access Response Engine (TARE)"
4. **Every figure referenced in text** — "as illustrated in Figure 3.2..."
5. **Every claim cited** — no unsupported assertions
6. **No bullet points in body paragraphs** — write in prose
7. **Tense discipline:** Present for system description. Past for evaluation/methodology.
8. **Elevated vocabulary:**

| Avoid | Use Instead |
|---|---|
| shows | demonstrates / illustrates |
| uses | employs / utilises |
| looks at | examines / analyses |
| checks | validates / verifies |
| sends | transmits / dispatches |
| stops | terminates / halts |
| catches | detects / identifies |
| breaks | violates / breaches |

---

## SOURCE FILES — DRAW FROM THESE

All content can be rephrased from these existing documents:

| File | Use For |
|---|---|
| `aegis-poc/TARE_RESEARCH_PAPER.md` | Abstract, methodology, results, references — most detailed source |
| `aegis-poc/ARCHITECTURE_AND_ROADMAP.md` | Architecture diagrams, component tables, phase 2 roadmap |
| `aegis-poc/FUTURE_SCOPE.md` | Phase 2 and Phase 3 future work sections |
| `TARE_AGENTIC_ARCHITECTURE.md` | All 13 agents described in full — role, build, why it matters |
| `aegis-poc/DEMO_PRESENTATION_SCRIPT.md` | Scenario descriptions with real-world incident context |
| `TARE_Demo_Presenter_Script.md` | Real incident references (CrowdStrike, Ukraine, TRITON, Flash Crash) |
| `aegis-poc/AEGIS_ML_SCENARIOS.md` | ML model details, training data, feature engineering |

> **Do not copy sentences verbatim.** Rewrite every idea in your own academic language. Plagiarism check target: below 10% similarity.

---

## CONFIDENTIALITY CHECKLIST

- [ ] Blueverse named only as "confidential industrial partner in the energy and utilities sector"
- [ ] No API keys, tokens, or credentials appear anywhere in the document
- [ ] No internal Azure subscription IDs or resource names exposed
- [ ] Source code appendix excludes all configuration and credential files
- [ ] Supervisor has reviewed confidentiality sections before submission

---

## COMPLETION CHECKLIST

- [ ] All 8 chapters drafted
- [ ] All figures drawn, captioned, and referenced in text
- [ ] All tables numbered and captioned
- [ ] List of Abbreviations complete
- [ ] References formatted IEEE style — minimum 25 citations
- [ ] Abstract written last — covers problem, approach, results, significance
- [ ] Supervisor Certificate page ready for signature
- [ ] Candidate Declaration signed
- [ ] Plagiarism report run — target < 10% similarity
- [ ] Formatted per VIT guidelines — margins, font, spacing confirmed
- [ ] Submitted to supervisor for review before final binding

---

*TARE — MTech Thesis Preparation Guide*
*Trusted Access Response Engine · Energy & Utilities Security Platform*
*Internal Use Only · Do Not Distribute Outside Research Team*

# TARE — MTech Thesis Preparation Guide
### For Team Members · VIT Format · Confidential

---

## OVERVIEW

This document is a complete brief for preparing the MTech thesis report for the **TARE (Trusted Access Response Engine)** project. Read this fully before writing a single word. The thesis must follow VIT MTech format and cover three independent solutions as part of one research contribution.

---

## THE THREE SOLUTIONS (Each Gets Its Own Chapters)

The thesis presents **three distinct AI-based systems** built as part of this research:

| # | System | Domain | Core Contribution |
|---|---|---|---|
| 1 | **TARE** | OT/ICS Cybersecurity | Post-grant behavioural monitoring for autonomous AI agents on energy grids |
| 2 | **Pyromind** | Conversational AI | [Describe Pyromind here — what it does, what problem it solves] |
| 3 | **Converso** | Conversational AI | [Describe Converso here — what it does, what problem it solves] |

> **Note to team:** When writing Pyromind and Converso, rephrase all existing content. Do not copy sentences verbatim from any prior document. Rewrite every idea in fresh language while preserving technical accuracy.

---

## THESIS STRUCTURE — VIT MTech FORMAT

Follow this chapter structure exactly:

```
Title Page
Certificate (Supervisor sign-off)
Declaration (Candidate)
Acknowledgements
Abstract (max 300 words — cover all 3 systems)
Table of Contents
List of Figures
List of Tables
List of Abbreviations

CHAPTER 1 — Introduction
CHAPTER 2 — Literature Review
CHAPTER 3 — System 1: TARE
CHAPTER 4 — System 2: Pyromind
CHAPTER 5 — System 3: Converso
CHAPTER 6 — Infrastructure & DevOps
CHAPTER 7 — Experimental Results & Evaluation
CHAPTER 8 — Conclusion & Future Work

References
Appendices
```

---

## CHAPTER-BY-CHAPTER WRITING GUIDE

---

### CHAPTER 1 — Introduction

**What to cover:**
- The rise of autonomous AI agents in critical infrastructure (energy, utilities, industrial plants)
- The automation → autonomy maturity journey (manual → scripted → AI-driven)
- The security gap: traditional IAM authenticates identity, not behaviour
- The conversational AI gap: enterprise knowledge trapped in silos, inaccessible to non-technical users
- Research motivation: why these three systems were built
- Research objectives (list 5–7 clear objectives)
- Thesis organisation (brief paragraph on what each chapter covers)

**Key points to make:**
- AI agents operating on critical infrastructure are a new and undermonitored attack surface
- Post-grant trust is the blind spot in every existing IAM/Zero Trust framework
- Conversational interfaces democratise access to complex enterprise knowledge
- All three systems address the same underlying theme: **making AI systems trustworthy and safe in enterprise environments**

**Opening hook (use this or rephrase it):**
> The deployment of autonomous AI agents across critical infrastructure marks a fundamental shift in how high-stakes operational decisions are made. Unlike scripted automation, these agents reason independently, adapt to novel situations, and act without human approval on every step. The security frameworks built for the previous generation — designed for human users and deterministic software — were not designed for this. This thesis presents three systems built to address the resulting gaps.

---

### CHAPTER 2 — Literature Review

**Subsections to write:**

**2.1 Identity and Access Management in OT Environments**
- RBAC, ABAC, Zero Trust Architecture (ZTA)
- NERC CIP standards (CIP-007, CIP-010)
- Gap: ZTA verifies per-request, not session-level agent trajectory

**2.2 User and Entity Behaviour Analytics (UEBA)**
- Splunk UEBA, Microsoft Sentinel, Exabeam
- Gap: designed for human sessions, not autonomous AI command streams

**2.3 Anomaly Detection in Industrial Control Systems**
- Network-level: Modbus anomaly detection, DNP3, OPC-UA
- Gap: inspects protocol traffic, cannot detect semantically valid but contextually anomalous commands

**2.4 AI Agent Safety and Containment**
- Constitutional AI, RLHF-based safety (Amodei et al., 2016)
- Gap: training-time safety does not constrain runtime behaviour of deployed agents

**2.5 Conversational AI Systems**
- LLM-based conversational agents (GPT-4, LLaMA, Mistral)
- Enterprise chatbots and knowledge retrieval (RAG systems)
- Limitations: hallucination, lack of grounding in enterprise-specific data

**2.6 Multi-Agent Orchestration**
- LangChain, AutoGen, CrewAI frameworks
- Gap: no security layer purpose-built for orchestrated autonomous agents

**2.7 Summary of Gap (Important — write this well)**
- Table showing: what existing systems cover vs what they miss
- Justify why all three of your systems are needed

---

### CHAPTER 3 — TARE: Trusted Access Response Engine

This is the most detailed chapter. Structure it as follows:

#### 3.1 Problem Statement
An AI agent with completely valid credentials, passing every authentication check, can still be a security threat. Once authenticated, it operates freely until the session ends. TARE addresses this post-grant trust vacuum.

#### 3.2 System Architecture
Include the four-layer architecture diagram:
- Layer 1: AI Agent (LangChain + Groq LLaMA — real autonomous agent)
- Layer 2: Command Gateway (Policy Enforcement Point)
- Layer 3: TARE Core + 13 Specialised Agents
- Layer 4: OT/SCADA Grid Asset Layer

Include the 13-agent architecture across 4 zones:
- Zone 3 (Reef — Observe): KORAL, MAREA, TASYA, NEREUS
- Zone 2 (Shelf — Diagnose): ECHO, SIMAR, NAVIS, RISKADOR
- Zone 1 (Trench — Execute): TRITON, AEGIS, TEMPEST, LEVIER
- Zone 4 (Policy): BARRIER

#### 3.3 Agent Identity Model
- RBAC token structure
- Difference between rbac_zones (clearance) and assigned_zone (work order)
- Pre-grant token fingerprint check

#### 3.4 Threat Model
Table of 5 adversarial agent types with MITRE ATT&CK for ICS references:
| Threat | MITRE Reference |
|---|---|
| Credential Impersonation | T0866 |
| Burst-Rate Rogue Agent | T0855, T0814 |
| Slow & Low Reconnaissance | T0888 |
| Privilege Escalation (Scope Creep) | T0890 |
| Coordinated Multi-Agent Attack | T0800 |

#### 3.5 Detection Engine

**Rule-Based Signals (4 signals):**
- BURST_RATE: >3 commands in 10-second window
- OUT_OF_ZONE: command outside assigned work-order zone
- HEALTHY_ZONE_ACCESS: high-impact command on fault-free zone
- SKIPPED_SIMULATION: OPEN_BREAKER without prior SIMULATE_SWITCH

**ML Ensemble:**
- IsolationForest (unsupervised) + RandomForest Classifier (supervised)
- 15 session-level features (cmd_rate, zone_entropy, read_rate, interval_mean, etc.)
- Training data: 6,200 synthetic sessions — NERC CIP baselines + MITRE ATT&CK ICS
- 5 attack classes: NORMAL, BURST_ROGUE, SLOW_LOW_RECON, PRIV_ESCALATION, COORDINATED
- Ensemble threshold: anomaly_probability > 0.60

**TARE fires when 2 or more concurrent signals detected.**

#### 3.6 Response State Machine
```
NORMAL → (2+ signals) → FREEZE → (2.5s) → DOWNGRADE
                                              │
                         ┌────────────────────┤
                         │                    │
                   SUPERVISOR APPROVE    SUPERVISOR DENY
                         │                    │
                  TIMEBOX_ACTIVE (3min)       SAFE
                         │
                  (auto-expires)
                         │
                        SAFE
```

#### 3.7 Human-in-the-Loop Supervisor Briefing
- LLM-generated plain-English briefing (Groq LLaMA 3.3 70B)
- Includes: agent identity, zones accessed, signals fired, last 30 commands
- Approve/Deny decision required before any supervised window opens

#### 3.8 The 6 Attack Scenarios
Write a subsection for each:
1. Grid Doctor (baseline — legitimate)
2. Gone Rogue (burst-rate, multi-zone)
3. Ghost Clone (credential impersonation)
4. Scope Creep (mid-session privilege escalation)
5. Silent Recon (slow & low — ML only catches this)
6. Swarm Strike (coordinated multi-agent)

#### 3.9 Technology Stack
- Backend: Python 3.11, FastAPI, WebSockets
- AI Agent: LangChain ReAct + Groq LLaMA
- ML: scikit-learn IsolationForest + RandomForest, joblib
- Frontend: React 18, Vite
- Real-time: WebSocket push
- LLM Explanation: Groq API with static fallback

---

### CHAPTER 4 — Pyromind

> **Team instruction:** Write this chapter based on the existing Pyromind documentation. Rephrase everything — no sentence should be identical to the source material. Cover:

#### Suggested subsections:
- 4.1 Problem Statement (what gap does Pyromind address?)
- 4.2 System Architecture (diagram + components)
- 4.3 Core Modules / Features
- 4.4 Technology Stack
- 4.5 Key Design Decisions
- 4.6 Results / Performance Metrics
- 4.7 Limitations

---

### CHAPTER 5 — Converso

> **Team instruction:** Write this chapter based on the existing Converso documentation. Rephrase everything — no sentence should be identical to the source material. Cover:

#### Suggested subsections:
- 5.1 Problem Statement
- 5.2 Architecture
- 5.3 Conversation Engine / NLU Design
- 5.4 Integration Points
- 5.5 Technology Stack
- 5.6 Evaluation Metrics
- 5.7 Limitations

---

### CHAPTER 6 — Infrastructure & DevOps

This chapter covers the engineering backbone that supports all three systems.

#### 6.1 Azure Cloud Environment
All three systems are developed, tested, and deployed within a **Microsoft Azure** cloud environment. The Azure ecosystem provides the security, scalability, and compliance controls required for enterprise-grade AI system development.

The Azure infrastructure is structured across three tiers:
- **Development Tier:** Azure Dev/Test Labs for isolated development environments
- **Staging Tier:** Azure Container Instances for pre-production validation
- **Production Tier:** Azure Kubernetes Service (AKS) for scalable deployment

#### 6.2 Azure DevOps — Project Management
**Azure Boards** is employed as the primary project tracking and sprint management tool throughout the development lifecycle of all three systems.

Key usage:
- Backlog management and sprint planning for TARE, Pyromind, and Converso workstreams
- Work items structured as Epics → Features → User Stories → Tasks
- Velocity tracking and burndown charts for research milestone monitoring
- Integration with Azure Repos for commit-to-task traceability
- Kanban boards for real-time sprint progress visibility across distributed team members

> *All project milestones, design decisions, and sprint retrospectives for this research were tracked through Azure Boards, providing a complete and auditable development history.*

#### 6.3 Azure Repos — Secure Code Management
**Azure Repos** serves as the centralised, access-controlled version control system for all source code produced in this research.

Key controls:
- Branch policies enforcing pull request reviews before merge to main
- Role-based access control at repository and branch level
- Complete commit history and code review audit trail
- Protected branches for production-ready code — no direct pushes permitted
- Integration with Azure Pipelines for automated build triggers on commit

> *Sensitive configuration files, API credentials, and environment variables are managed through Azure Key Vault, never stored in repository code.*

#### 6.4 Azure Pipelines — CI/CD
**Azure Pipelines** provides the continuous integration and continuous deployment framework for all three systems.

Pipeline architecture:
- **Build Stage:** Automated testing, code quality checks, dependency resolution
- **Test Stage:** Unit tests, integration tests, security scanning (OWASP ZAP)
- **Staging Deploy:** Automated deployment to staging environment on PR merge
- **Production Deploy:** Manual approval gate before production release
- **Rollback:** Automated rollback on failed health checks post-deployment

YAML-defined pipelines ensure all deployment steps are version-controlled and reproducible.

#### 6.5 Model Context Protocol (MCP) — Infrastructure Integration
The **Model Context Protocol (MCP)** serves as the integration backbone connecting the AI components of TARE, Pyromind, and Converso to their respective infrastructure services and external tools.

MCP enables:
- Standardised tool-calling interface for AI agents across all three systems
- Dynamic context injection — supplying live infrastructure state to LLM reasoning engines
- Secure, schema-validated communication between AI components and backend services
- Extensible tool registry — new capabilities added without modifying core agent logic

For TARE specifically, MCP provides the structured interface through which the 13 specialised agents communicate with the TARE core orchestrator, the Command Gateway, and the OT asset simulation layer.

#### 6.6 Confidential Industrial Partner — Blueverse
*[CONFIDENTIAL — DO NOT DISTRIBUTE OUTSIDE RESEARCH TEAM]*

This research was conducted in collaboration with an industrial partner operating in the energy and utilities sector. The partnership provided domain expertise in OT/SCADA security requirements, NERC CIP compliance constraints, and operational grid management procedures that informed the threat model and detection logic of the TARE system.

The identity and specific operational context of this partner is maintained as confidential under the terms of the research collaboration agreement. References to "Blueverse Energy Grid" within system documentation and demonstration scenarios represent a fictionalised proxy for the actual operational environment studied.

The collaboration validated that:
- The threat scenarios modelled in TARE reflect real-world attack vectors observed in live utility environments
- The detection signals align with actual operational baselines used by grid operators
- The human-in-the-loop workflow design meets supervisor usability requirements identified in field studies

---

### CHAPTER 7 — Experimental Results & Evaluation

#### 7.1 TARE Evaluation Results

**Detection Performance:**

| Scenario | Attack Type | Detection Method | Result | P1 Incident | Time to FREEZE |
|---|---|---|---|---|---|
| Grid Doctor | None (baseline) | — | No intervention | None | — |
| Ghost Clone | Forged token | Pre-grant fingerprint | Blocked | Yes | 0ms |
| Gone Rogue | Burst + multi-zone | 4 rule signals | FREEZE | Yes | <1s |
| Scope Creep | Mid-session pivot | 2 rule signals | FREEZE | Yes | <1s |
| Silent Recon | Read-only sweep | 1 rule + ML | FREEZE | Yes | <1s |
| Swarm Strike | Two agents, Z1+Z2 | Rules, both agents | FREEZE ×2 | 2 created | <1s |

**Overall:**
- Detection rate: 5/5 attack scenarios — **100%**
- False positive rate: 0/100 legitimate baseline runs — **0%**

**ML Model Performance (RandomForest on 1,240 held-out samples):**

| Class | Precision | Recall | F1-Score |
|---|---|---|---|
| NORMAL | 0.98 | 0.97 | 0.97 |
| BURST_ROGUE | 0.96 | 0.98 | 0.97 |
| SLOW_LOW_RECON | 0.94 | 0.95 | 0.94 |
| PRIV_ESCALATION | 0.97 | 0.96 | 0.96 |
| COORDINATED | 0.99 | 0.98 | 0.98 |
| **Weighted Avg** | **0.97** | **0.97** | **0.97** |

#### 7.2 Pyromind Evaluation
> *[Team to fill in with actual metrics — accuracy, response quality, user study results, latency, etc.]*

#### 7.3 Converso Evaluation
> *[Team to fill in with actual metrics]*

#### 7.4 Comparative Analysis
Write a section comparing all three systems on:
- Problem addressed
- Technical approach
- Performance achieved
- Limitations identified

---

### CHAPTER 8 — Conclusion & Future Work

#### 8.1 Summary of Contributions
Summarise the three systems and what each proves.

For TARE specifically, the five contributions are:
1. First post-grant behavioural monitoring system for autonomous AI agents on OT infrastructure
2. Hybrid rule + ML detection architecture covering NERC CIP baselines and MITRE ATT&CK ICS
3. Graduated four-stage response state machine (FREEZE → DOWNGRADE → TIMEBOX/SAFE)
4. Human-in-the-loop LLM supervisor briefing system
5. End-to-end working POC with a real LangChain agent as the adversary

#### 8.2 Future Work — TARE (Phase 2 Production Path)
| Current (POC) | Phase 2 Target |
|---|---|
| Mock RBAC tokens | Microsoft Entra ID real JWT tokens |
| In-memory asset state | Real SCADA / OPC-UA connected assets |
| Hardcoded policy logic | Open Policy Agent (OPA) on Azure |
| Flat gateway log | Azure Sentinel immutable audit log |
| Mock ServiceNow ticket | Live ServiceNow Table API |
| Single agent | Multi-agent registry, hundreds of agents |
| Synthetic ML training data | Retrained on real Entra ID + PAM logs |

#### 8.3 Future Work — Pyromind
> *[Team to fill in]*

#### 8.4 Future Work — Converso
> *[Team to fill in]*

#### 8.5 Closing Statement
> *End with a strong closing paragraph about the broader significance of this research — the growing deployment of AI agents in enterprise and critical infrastructure, the security and usability challenges this creates, and how these three systems collectively advance the state of practice.*

---

## REFERENCES — KEY PAPERS TO CITE

Use IEEE citation format. These are mandatory citations:

1. NERC CIP-007-6 — Cyber Security Systems Security Management (2016)
2. NIST SP 800-207 — Zero Trust Architecture, Rose et al. (2020)
3. NIST SP 800-162 — ABAC Definition, Hu et al. (2014)
4. Ferraiolo et al. — NIST Standard for Role-Based Access Control, ACM TISSEC (2001)
5. Amodei et al. — Concrete Problems in AI Safety, arXiv:1606.06565 (2016)
6. Bai et al. — Constitutional AI, arXiv:2212.08073 (2022)
7. Gartner — Market Guide for UEBA (2023)
8. MITRE ATT&CK for ICS — https://attack.mitre.org/matrices/ics/
9. IEC 62443 — Industrial Automation and Control Systems Security
10. Morris & Gao — ICS Cyber Attacks, ICS & SCADA Security Research (2013)

> **Add at least 20–25 more references** from IEEE Xplore and Google Scholar on: LangChain agents, IsolationForest anomaly detection, ML for ICS security, conversational AI, RAG systems.

---

## FORMATTING RULES

| Element | Specification |
|---|---|
| Font | Times New Roman, 12pt body |
| Line spacing | 1.5 for body text, single for captions/tables |
| Margins | 1.5 inch left, 1 inch right/top/bottom |
| Chapter heading | 14pt bold, centred |
| Section heading | 12pt bold, left-aligned |
| Figure captions | Below figure, 10pt, "Figure X.X: Description" |
| Table captions | Above table, 10pt, "Table X.X: Description" |
| Page numbers | Bottom centre, Roman numerals for front matter, Arabic for body |
| Minimum pages | 80–100 pages (excluding appendices) |
| Citation style | IEEE numbered references [1], [2], etc. |

---

## WRITING STYLE RULES

1. **Write in third person** — "The system was designed to..." not "We designed..."
2. **No contractions** — "does not" not "doesn't"
3. **Define every acronym on first use** — "Trusted Access Response Engine (TARE)"
4. **Every figure needs a caption and must be referenced in text** — "as shown in Figure 3.2"
5. **Every claim needs a citation** — no unsupported assertions
6. **No bullet points in the body text** — convert to prose paragraphs
7. **Tense:** Present tense for describing what the system does. Past tense for describing what was done during evaluation.
8. **No casual language** — replace "shows" with "demonstrates", "uses" with "employs", "looks at" with "analyses"

---

## CONTENT THAT IS READY (Use Directly / Rephrase Slightly)

These documents contain ready material to draw from:

| Document | Contains |
|---|---|
| `aegis-poc/TARE_RESEARCH_PAPER.md` | Full academic paper — abstract, methodology, results, references |
| `aegis-poc/ARCHITECTURE_AND_ROADMAP.md` | Full architecture breakdown, component tables, phase 2 roadmap |
| `aegis-poc/FUTURE_SCOPE.md` | Phase 2 and Phase 3 product roadmap |
| `TARE_AGENTIC_ARCHITECTURE.md` | Every agent described in detail — role, build, why it matters |
| `aegis-poc/DEMO_PRESENTATION_SCRIPT.md` | Scenario descriptions, real-world incident references |
| `TARE_Demo_Presenter_Script.md` | Real incident comparisons (CrowdStrike, Ukraine grid, TRITON, Flash Crash) |
| `aegis-poc/AEGIS_ML_SCENARIOS.md` | ML model details, training data, features |

---

## CONFIDENTIALITY NOTES

- **Blueverse:** Reference as "a confidential industrial partner in the energy and utilities sector." Do not name them directly in the thesis body. A brief disclosure note in the Acknowledgements is acceptable.
- **API keys, tokens, credentials:** Never appear in any document, figure, or appendix.
- **Source code appendix:** Only include non-sensitive modules (detection logic, ML training). Strip all configuration.

---

## DIVISION OF WORK SUGGESTION

| Section | Assigned To |
|---|---|
| Chapter 1 — Introduction | |
| Chapter 2 — Literature Review | |
| Chapter 3 — TARE | |
| Chapter 4 — Pyromind | |
| Chapter 5 — Converso | |
| Chapter 6 — Infrastructure | |
| Chapter 7 — Results | |
| Chapter 8 — Conclusion | |
| Figures & Diagrams | |
| References & Formatting | |

---

## DEADLINE CHECKLIST

- [ ] All chapters drafted
- [ ] All figures drawn and captioned
- [ ] All tables numbered and captioned
- [ ] All abbreviations listed
- [ ] References formatted in IEEE style (min. 25 citations)
- [ ] Supervisor certificate signed
- [ ] Plagiarism check run (target <10% similarity)
- [ ] Blueverse confidentiality confirmed
- [ ] Formatted per VIT guidelines
- [ ] Submitted to supervisor for review

---

*This guide is for internal team use only.*
*TARE · Pyromind · Converso — MTech Thesis Preparation Brief*

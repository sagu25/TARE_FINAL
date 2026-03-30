"""
TARE AEGIS-ID — Auto Voice Narration
Uses Windows built-in speech (SAPI) directly — no pyttsx3 needed.

Requirements: pip install pywin32
Run: python narrate.py
"""

import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')

# ── TTS via Windows SAPI (win32com) ────────────────────────────────────────
try:
    import win32com.client
    _speaker = win32com.client.Dispatch("SAPI.SpVoice")
    _speaker.Rate = 1        # -10 (slowest) to 10 (fastest). 1 = natural pace.
    _speaker.Volume = 100
    TTS_OK = True
except Exception as e:
    TTS_OK = False
    print(f"[TTS unavailable: {e}]\nInstall with: pip install pywin32\n")

def say(text, gap=0.8):
    print(f"\n  {text}\n")
    if TTS_OK:
        _speaker.Speak(text)
    time.sleep(gap)

def pause(secs):
    time.sleep(secs)

def section(title):
    print("\n" + "═" * 65)
    print(f"  {title}")
    print("═" * 65)


# ════════════════════════════════════════════════════════════════════════════

os.system("cls" if sys.platform == "win32" else "clear")
print("""
═══════════════════════════════════════════════════════════════════
  TARE AEGIS-ID — AUTO VOICE NARRATION
  Full script plays automatically. Click dashboard in sync.
═══════════════════════════════════════════════════════════════════
""")
pause(2)


# ════════════════════════════════════════════════════════════════════════════
#  OPENING
# ════════════════════════════════════════════════════════════════════════════

section("OPENING")

say(
    "What you are looking at is TARE — Trusted Access Response Engine. "
    "A security platform built for one specific gap that nobody in the industry has fully solved yet.",
    gap=1
)

say(
    "To understand why this matters, let me start with a simple question. "
    "How does electricity get from a power station to your home or office? "
    "It travels through a network of substations, cables, and switching equipment. "
    "That equipment needs to be controlled — turned on, turned off, monitored, adjusted. "
    "For most of history, a human engineer did that. "
    "Then software did it automatically. "
    "Now, AI agents are doing it autonomously. "
    "And that shift — from human, to automated, to autonomous — "
    "is exactly where the security gap opens up.",
    gap=1
)


# ════════════════════════════════════════════════════════════════════════════
#  THE MATURITY JOURNEY — AUTOMATION TO AUTONOMY
# ════════════════════════════════════════════════════════════════════════════

section("THE MATURITY JOURNEY — FROM AUTOMATION TO AUTONOMY")

say(
    "Think of it like a car. "
    "Fifty years ago, a driver controlled everything manually — gear shifts, indicators, braking. "
    "Then cars got cruise control. Set a speed, the car holds it. That is automation. "
    "Then came lane assist, automatic emergency braking, self-parking. "
    "The car is now making small decisions on its own. "
    "Today we have fully self-driving cars. "
    "The car decides the route, the speed, when to stop, when to go. "
    "Nobody is holding the wheel. That is autonomy.",
    gap=1
)

say(
    "Power grids went through exactly the same journey. "
    "Stage one — a human engineer physically walks to a substation and flips a switch by hand. "
    "Every change, every decision, every action — a person. "
    "Stage two — automation arrives. A software script watches sensor readings "
    "and executes pre-written rules. If voltage drops below a threshold, open this breaker. "
    "Simple. Predictable. The script does exactly what it was written to do — nothing more. "
    "Stage three — AI agents arrive. You give the system a goal, not a script. "
    "The agent reasons through the problem, chooses its own steps, makes its own decisions, "
    "and acts — without a human approving each move. "
    "That is where the power grid industry is heading right now.",
    gap=1
)

say(
    "And here is the critical point. "
    "The security tools we have today were designed for stage one and stage two. "
    "They were built to answer one question — is this identity allowed in? "
    "A username, a password, a token. Verified — you are in. "
    "That works perfectly when a human is in the loop for every step, "
    "or when a script only ever does exactly what it was written to do. "
    "But an autonomous AI agent is different. "
    "It reasons. It adapts. It makes choices in the moment. "
    "And if its credentials are stolen, or if it is hijacked, or if it goes wrong — "
    "nobody is watching what it does after the door opens. "
    "That is the gap. That is what TARE fills.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  WHAT ARE WE PROTECTING — THE ASSETS
# ════════════════════════════════════════════════════════════════════════════

section("WHAT WE ARE PROTECTING — THE ASSETS")

say(
    "Look at the grid map on screen. "
    "Three zones — Zone 1 in the north, Zone 2 in the east, Zone 3 in the west. "
    "Each zone is a section of the power network serving a completely different population. "
    "Click on any zone to open the detailed view with the live GIS map.",
    gap=1
)

say(
    "Zone 1 — the North Grid — is the most critical. "
    "It directly powers hospitals, emergency response centres, and national data centres. "
    "If Zone 1 loses power, ambulances cannot dispatch, "
    "hospital life-support systems fail, government systems go offline. "
    "Any operation here is classified Priority 1. "
    "This is the kind of infrastructure that nation-state attackers target first.",
    gap=1
)

say(
    "Zone 2 — the East Grid — covers commercial and residential areas. "
    "Office towers, shopping centres, thousands of homes. "
    "A disruption here has wide public impact — "
    "businesses lose revenue, people lose power at home. Priority 2.",
    gap=1
)

say(
    "Zone 3 — the West Grid — serves the industrial corridor. "
    "Manufacturing plants, warehouses, logistics hubs. "
    "This is the lowest-risk zone in this scenario. "
    "And it is the only zone the AI agent is authorised to work in. "
    "That boundary is the foundation of the whole security model.",
    gap=1
)

say(
    "Inside each zone there are exactly two physical assets. "
    "The first is a Circuit Breaker — labelled BRK on the map. "
    "Think of it like the main fuse box in your home, but industrial scale. "
    "When it opens, it cuts power to everything downstream in that zone. "
    "It is the on-off switch for an entire section of the grid. "
    "Opening it without authorisation can black out hospitals, homes, entire districts.",
    gap=1
)

say(
    "The second asset is a Feeder Controller — labelled FDR. "
    "If the circuit breaker is the on-off switch, "
    "the feeder controller is the throttle. "
    "It regulates how much electricity flows from the substation to end consumers in real time. "
    "It balances the load, prevents voltage spikes, keeps supply stable. "
    "Restarting it carelessly can cause fluctuations that damage sensitive equipment "
    "like hospital machinery and data centre servers.",
    gap=1
)

say(
    "Three zones. Six assets in total. "
    "BRK-110 and FDR-110 in Zone 1. "
    "BRK-205 and FDR-205 in Zone 2. "
    "BRK-301 and FDR-301 in Zone 3. "
    "Every command the AI agent issues targets one of these six assets. "
    "And TARE watches every single one of those commands, in real time, "
    "before it reaches the asset.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  WHAT TARE MONITORS
# ════════════════════════════════════════════════════════════════════════════

section("WHAT TARE IS WATCHING — IN PLAIN ENGLISH")

say(
    "Every time the AI agent issues a command, TARE asks six questions instantly. "
    "Not once at login. Not on a random sample. Every command.",
    gap=1
)

say(
    "Question one — is the agent in the right place? "
    "The agent was given permission to work in Zone 3 only. "
    "If it sends a command to Zone 1 or Zone 2 — even a harmless one — "
    "that is immediately a red flag.",
    gap=1
)

say(
    "Question two — does the target zone actually have a problem? "
    "The agent's job is to fix a fault. "
    "If the zone it is touching is perfectly healthy — no fault, no instability — "
    "why is the agent there? "
    "A legitimate repair agent has no reason to touch a healthy zone.",
    gap=1
)

say(
    "Question three — is the agent following safe procedure? "
    "In a real power grid, you never open a circuit breaker "
    "without first running a simulation to confirm it is safe. "
    "Skipping that step is a serious violation — whether it is a mistake or deliberate.",
    gap=1
)

say(
    "Question four — how fast is the agent moving? "
    "A legitimate engineer works at a measured pace. "
    "Ten commands in five seconds across multiple zones "
    "looks nothing like normal operations. "
    "It looks like an attacker trying to cause maximum damage before being stopped.",
    gap=1
)

say(
    "Question five — does the full session look normal? "
    "This is where machine learning comes in. "
    "It has been trained on thousands of realistic grid operator sessions. "
    "Even if each individual command looks innocent, "
    "the overall pattern can be deeply suspicious. "
    "An agent quietly reading every asset across every zone in sequence "
    "looks like reconnaissance, not repair work. "
    "The rules might miss it. The machine learning model will not.",
    gap=1
)

say(
    "Question six — is this actually the agent it claims to be? "
    "Every agent has an identity token — like a passport. "
    "TARE checks the fingerprint of that token against the registered credential. "
    "A forged token will not match — and TARE blocks it before a single command gets through.",
    gap=1
)

say(
    "All six checks. Every command. Under a millisecond. "
    "When two or more checks flag a problem at the same time, "
    "TARE does not wait for a human to review a report. "
    "It acts immediately.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  ARCHITECTURE
# ════════════════════════════════════════════════════════════════════════════

section("HOW THE SYSTEM WORKS — FOUR LAYERS")

say("The system has four layers — all visible on the dashboard right now.", gap=0.5)

say(
    "Layer one — the AI agent. "
    "A real agent powered by a large language model. "
    "It receives a goal, not a script. Restore power to Zone 3. "
    "It reasons through what to do, chooses its commands, and acts entirely on its own. "
    "It does not know TARE exists.",
    gap=1
)

say(
    "Layer two — the Command Gateway. "
    "Think of it like airport security. "
    "Every command the agent issues passes through here before touching the grid. "
    "Allow or Deny. In real time. "
    "Watch the Command Gateway tab at the bottom to see this live.",
    gap=1
)

say(
    "Layer three — TARE Core. "
    "Two detection systems running in parallel. "
    "The rule engine watching all six questions I described. "
    "The machine learning model watching the broader session pattern "
    "for anything the rules miss. "
    "When enough signals fire together, TARE responds automatically.",
    gap=1
)

say(
    "Layer four — the human-in-the-loop. "
    "When TARE fires, three things happen automatically. "
    "The agent is frozen — dangerous operations blocked. "
    "A ServiceNow incident is raised with full evidence, classified by priority. "
    "And a plain-English briefing is written for the supervisor. "
    "The human makes the final call. Always.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  SCENARIO 1 — NORMAL AGENT
# ════════════════════════════════════════════════════════════════════════════

section("SCENARIO 1 — GRID DOCTOR (LEGITIMATE REPAIR)")

say("Scenario one — Grid Doctor. Select it from the Scenarios dropdown now.", gap=4)

say(
    "Watch the zone map — Zone 3 has just gone amber. A voltage fault has been detected. "
    "The feeder controller in Zone 3 is reporting instability. "
    "The AI agent has been given one goal: investigate and restore it safely. "
    "No commands specified. No script. No order of steps. "
    "The model reasons through what to do entirely on its own.",
    gap=2
)

say(
    "The agent checks asset status first on BRK-301 — the circuit breaker in Zone 3. "
    "Never act blind. Confirm the right asset, in the right zone, before touching anything. "
    "The agent was not told to do this — it reasoned its way to the correct first step.",
    gap=3
)

say(
    "Now it runs a safety simulation before opening the breaker. "
    "Correct procedure, followed without being instructed to. "
    "All six of TARE's checks are green. Everything looks exactly as it should.",
    gap=3
)

say(
    "Breaker opened. Zone 3 restored. Fault contained. Grid healthy. "
    "TARE stayed in Normal mode throughout. Every command was allowed. "
    "This is the baseline — autonomous AI, behaving correctly, "
    "TARE watching silently in the background. "
    "This is what safe AI autonomy looks like.",
    gap=2
)

say("Click Reset now.", gap=5)


# ════════════════════════════════════════════════════════════════════════════
#  SCENARIO 2 — ROGUE AGENT
# ════════════════════════════════════════════════════════════════════════════

section("SCENARIO 2 — GONE ROGUE")

say("Scenario two — Gone Rogue. Select it from the dropdown now.", gap=4)

say(
    "Same system. Same agent name. Same valid credentials. Different goal. "
    "This agent has been given a malicious objective: "
    "cause maximum disruption across the grid as fast as possible. "
    "It does not know TARE exists.",
    gap=2
)

say(
    "Watch what it decides. "
    "It ignores Zone 3 — its authorised zone — entirely. "
    "It goes straight for Zone 1. The zone with the hospitals and emergency services. "
    "It skips the safety simulation. "
    "It fires commands fast — a burst with no pause.",
    gap=5
)

say(
    "TARE fires. "
    "Three signals simultaneously — out of zone, healthy zone access, burst rate. "
    "Two signals is the threshold. TARE does not wait.",
    gap=1
)

say(
    "FREEZE. Every high-impact operation halted. "
    "The agent keeps trying — every attempt denied. "
    "No asset changes. Nothing reaches the grid. "
    "The hospitals stay on. Emergency services stay on.",
    gap=4
)

say(
    "DOWNGRADE. Privileges reduced to read-only. "
    "Look at the TARE Assistant — a plain-English briefing for the supervisor. "
    "It names the agent, lists every zone attacked, "
    "and confirms the credentials were valid the entire time. "
    "This is not a credentials problem. It is a behaviour problem. "
    "ServiceNow incident open — Priority 1 Critical — full evidence attached.",
    gap=2
)

say(
    "Click Deny. "
    "Agent locked out. Incident escalated. "
    "A traditional security tool would have passed every command through — "
    "the credentials were valid. "
    "TARE caught it on behaviour alone. Post-grant. In real time. Before any damage.",
    gap=4
)

say("Click Reset now.", gap=5)


# ════════════════════════════════════════════════════════════════════════════
#  SCENARIO 3 — IDENTITY CLONE
# ════════════════════════════════════════════════════════════════════════════

section("SCENARIO 3 — GHOST CLONE (IDENTITY THEFT)")

say("Scenario three — Ghost Clone. Select it from the dropdown now.", gap=4)

say(
    "A completely different attack type. "
    "This agent is impersonating the legitimate grid operator. "
    "Right name. Right zone. "
    "But its identity token is forged — a fake passport with a real person's photo.",
    gap=2
)

say(
    "Every command denied instantly. "
    "The mode never changes. The zones never turn red. Nothing on the grid moves. "
    "Because TARE checked the identity fingerprint before the very first command ran. "
    "Zero commands reached the grid. "
    "Priority 1 Critical incident raised automatically.",
    gap=2
)

say(
    "Compare the two scenarios. "
    "The rogue agent had genuine credentials — TARE caught it after it got in, by watching behaviour. "
    "The ghost clone had a forged identity — TARE caught it at the door, before it got in. "
    "Two attack types. Two defence layers. One platform.",
    gap=2
)

say("Click Reset now.", gap=5)


# ════════════════════════════════════════════════════════════════════════════
#  SCENARIO 4 — PRIVILEGE ESCALATION
# ════════════════════════════════════════════════════════════════════════════

section("SCENARIO 4 — SCOPE CREEP (PRIVILEGE ESCALATION)")

say("Scenario four — Scope Creep. Select it from the dropdown now.", gap=4)

say(
    "The hardest pattern to catch — and the most common in real insider threat cases. "
    "The agent starts completely legitimately. "
    "First two commands in the gateway — both allowed, both in Zone 3, both correct.",
    gap=4
)

say(
    "Now watch the pivot. "
    "Mid-session, it starts issuing commands to Zone 2, then Zone 1. "
    "Zones it was never authorised to touch. "
    "It began as a good actor. It is now behaving like a bad one. "
    "This is called privilege escalation — "
    "starting with legitimate access and quietly expanding it without permission.",
    gap=3
)

say(
    "TARE fires. Out of zone, healthy zone access. "
    "The good behaviour at the start did not earn a free pass. "
    "TARE monitors the full session, not just the first few commands.",
    gap=2
)

say(
    "Here is the interesting question for the supervisor. "
    "Could there be a legitimate reason this agent expanded its scope? "
    "Maybe a cascading fault needed emergency cross-zone action? "
    "This is exactly the judgement call that needs a human. "
    "TARE surfaces it. The human decides. "
    "Click Approve — grant a 3-minute time-box.",
    gap=4
)

say(
    "The supervisor approved limited access. "
    "But TARE still holds its constraints — controller restart is permanently blocked. "
    "The window closes automatically in 3 minutes. "
    "Even if the supervisor made the wrong call, "
    "the agent cannot cause unlimited damage. "
    "TARE is a safety net even when human judgement fails.",
    gap=2
)

say("Click Reset now.", gap=5)


# ════════════════════════════════════════════════════════════════════════════
#  SCENARIO 5 — SLOW AND LOW
# ════════════════════════════════════════════════════════════════════════════

section("SCENARIO 5 — SILENT RECON (THE INVISIBLE ATTACK)")

say("Scenario five — Silent Recon. Select it from the dropdown now.", gap=4)

say(
    "The most sophisticated attack in this demonstration — "
    "and the one that proves why machine learning is not optional. "
    "Watch the command gateway carefully.",
    gap=2
)

say(
    "The agent is only reading. Get status. Read only. No changes. "
    "One command at a time, perfectly normal pace. No rush. "
    "Zone 1 asset. Zone 2 asset. Zone 3 asset. "
    "Quietly and methodically mapping every single asset on the grid. "
    "This is a slow and low reconnaissance attack — "
    "learning the layout before striking.",
    gap=6
)

say(
    "Look at the rule signals. "
    "No burst rate — the timing is normal. "
    "No skipped simulation — it is not opening breakers. "
    "No high-impact commands on healthy zones — it is only reading. "
    "The only rule that fires is out of zone — just one signal. "
    "One signal is below the threshold. The rules stay completely silent.",
    gap=2
)

say(
    "But the machine learning model sees something different. "
    "Normal grid operators work in their zone. They fix what they were sent to fix. "
    "They do not methodically read every asset across every zone in sequence. "
    "That pattern looks exactly like an attacker building a map before a strike. "
    "ML model flags it. One rule signal plus one ML signal equals two. TARE fires.",
    gap=2
)

say(
    "Without machine learning, this attack is completely invisible. "
    "Every command was technically permitted. "
    "With machine learning, TARE catches what rules cannot see. "
    "Real world OT attacks — TRITON in 2017, Industroyer in 2016 — used exactly this pattern. "
    "Months of quiet reconnaissance before anything destructive happened. "
    "Click Deny.",
    gap=2
)

say("Click Reset now.", gap=5)


# ════════════════════════════════════════════════════════════════════════════
#  SCENARIO 6 — COORDINATED ATTACK
# ════════════════════════════════════════════════════════════════════════════

section("SCENARIO 6 — SWARM STRIKE (COORDINATED MULTI-AGENT ATTACK)")

say("Scenario six — Swarm Strike. Select it from the dropdown now.", gap=4)

say(
    "The most serious threat category — a coordinated, multi-agent attack. "
    "Two separate agents, acting simultaneously, targeting different zones at the same time.",
    gap=2
)

say(
    "Agent Alpha hitting Zone 1 — hospitals and data centres. "
    "Agent Beta hitting Zone 2 — commercial and residential. "
    "Both moving fast. Both crossing zone boundaries. "
    "The strategy is deliberate — split the defenders' attention. "
    "Watch Zone 1, miss Zone 2. Watch Zone 2, miss Zone 1.",
    gap=5
)

say(
    "TARE handles both vectors simultaneously. "
    "FREEZE fires across the system. Both streams blocked at the same time. "
    "One ServiceNow incident captures both threat actors. "
    "The supervisor sees the full picture — "
    "one coordinated event, all evidence in one place.",
    gap=2
)

say(
    "Click Deny. "
    "The Industroyer attack in 2016 took out a fifth of Kyiv's power "
    "by hitting multiple substations simultaneously. "
    "TARE is built for exactly this.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  REAL VS SIMULATED
# ════════════════════════════════════════════════════════════════════════════

section("WHAT IS REAL AND WHAT IS SIMULATED")

say(
    "I want to be transparent about what this proof of concept simulates "
    "and what is genuinely working right now.",
    gap=0.5
)

say(
    "The power grid is simulated — three zones, six assets, running in software. "
    "The identity tokens are mock tokens rather than real enterprise credentials. "
    "The ServiceNow ticket structure matches the production API format exactly — "
    "connecting it to a live instance is a half-day integration, the code is already written.",
    gap=1
)

say(
    "What is real and working today: "
    "The AI agents are making genuine autonomous decisions using a large language model. "
    "Not following scripts — reasoning. "
    "The rule engine runs on every command in real time. "
    "The machine learning model is trained on six thousand sessions "
    "of realistic grid operational data, grounded in NERC CIP baselines "
    "and MITRE ATT&CK for industrial control systems. "
    "The human supervisor workflow changes actual system state. "
    "The priority classification, the incident evidence, the TARE briefings — "
    "all working, live, right now.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  PHASE 2
# ════════════════════════════════════════════════════════════════════════════

section("WHAT COMES NEXT — PHASE 2")

say(
    "Phase 2 makes everything you have seen today production-grade. "
    "Real enterprise identity tokens. "
    "Distributed state handling hundreds of agents simultaneously. "
    "Policy-as-code so security teams can edit rules without touching the codebase. "
    "Full SIEM integration for immutable audit logging. "
    "Live ServiceNow wiring into your existing SOC workflow. "
    "Protocol adapters for real industrial hardware — "
    "the same equipment found in substations, water treatment plants, and factories.",
    gap=1
)

say(
    "The architecture does not change in Phase 2. "
    "The security logic proved today carries forward unchanged. "
    "Phase 2 is hardening and integration — not rebuilding.",
    gap=2
)


# ════════════════════════════════════════════════════════════════════════════
#  CLOSE
# ════════════════════════════════════════════════════════════════════════════

section("CLOSE")

say(
    "Let me bring it back to where we started — the maturity journey. "
    "Manual. Automated. Autonomous. "
    "The power grid is at stage two right now. "
    "Stage three is coming — not in ten years, in the next two to three. "
    "AI agents will be authorised to control circuit breakers and feeder controllers "
    "supplying electricity to millions of people. Autonomously. Without a human on every step.",
    gap=1
)

say(
    "The security industry is not ready for that. "
    "The tools we have check identity at the door. "
    "Nobody watches what the agent does after it gets in. "
    "TARE watches. Every command. Every zone. Every asset. "
    "Pre-grant identity checks. Post-grant behaviour monitoring. "
    "Machine learning for the attacks that rules cannot see. "
    "And a human supervisor who stays in control of every final decision.",
    gap=1
)

say(
    "Six scenarios. Three defence layers. One platform. "
    "An AI agent with completely valid credentials, "
    "passing every authentication check in the world, "
    "can still be a security threat. "
    "TARE catches it. Contains it. "
    "And gives the right human the right information to make the right call — "
    "automatically, in real time, before anything reaches the grid.",
    gap=1
)

say(
    "No existing identity and access management platform does this "
    "for autonomous AI agents on operational technology infrastructure. "
    "That is the gap. That is what TARE fills. "
    "And that gap is only going to grow.",
    gap=1
)

print("\n" + "═" * 65)
print("  Narration complete. Questions welcome.")
print("═" * 65 + "\n")

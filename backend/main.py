"""
TARE — Trusted Access Response Engine
FastAPI backend with WebSocket push and REST demo commands
"""
import asyncio
import json
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from tare_engine import TAREEngine
from grid_agent import (run_normal_agent, run_rogue_agent, run_impersonator_agent,
                        run_coordinated_agent, run_escalation_agent, run_slow_low_agent)

# ─── WebSocket connection manager ──────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self._clients: list[WebSocket] = []
        self._loop: asyncio.AbstractEventLoop | None = None

    def set_loop(self, loop):
        self._loop = loop

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._clients.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self._clients:
            self._clients.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in list(self._clients):
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

    def sync_broadcast(self, data: dict):
        """Called from engine threads — schedules broadcast on the event loop."""
        if self._loop and not self._loop.is_closed():
            asyncio.run_coroutine_threadsafe(self.broadcast(data), self._loop)


manager = ConnectionManager()
engine  = TAREEngine(broadcast_fn=manager.sync_broadcast)

# ─── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    manager.set_loop(asyncio.get_event_loop())
    yield

app = FastAPI(title="TARE — Trusted Access Response Engine", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── WebSocket endpoint ────────────────────────────────────────────────────────
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        await ws.send_json(engine._snapshot())
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception:
        manager.disconnect(ws)

# ─── Demo / control endpoints ──────────────────────────────────────────────────
@app.post("/demo/normal")
async def demo_normal():
    engine.run_normal_ops()
    return {"status": "started"}

@app.post("/demo/anomaly")
async def demo_anomaly():
    engine.trigger_anomaly()
    return {"status": "started"}

# ─── Real AI Agent endpoints ───────────────────────────────────────────────────
@app.post("/agent/normal")
async def agent_normal():
    """Start the real LangChain agent with the legitimate fault-repair task."""
    run_normal_agent(engine, manager.sync_broadcast)
    return {"status": "agent_started", "task": "normal"}

@app.post("/agent/rogue")
async def agent_rogue():
    """Start the real LangChain agent with the rogue/malicious task."""
    run_rogue_agent(engine, manager.sync_broadcast)
    return {"status": "agent_started", "task": "rogue"}

@app.post("/agent/impersonator")
async def agent_impersonator():
    """Start the impersonator agent — forged token, blocked at auth layer."""
    run_impersonator_agent(engine, manager.sync_broadcast)
    return {"status": "agent_started", "task": "impersonator"}

@app.post("/agent/coordinated")
async def agent_coordinated():
    """Two rogue agents hit Z1 and Z2 simultaneously."""
    run_coordinated_agent(engine, manager.sync_broadcast)
    return {"status": "agent_started", "task": "coordinated"}

@app.post("/agent/escalation")
async def agent_escalation():
    """Starts normal in Z3, escalates to all zones mid-session."""
    run_escalation_agent(engine, manager.sync_broadcast)
    return {"status": "agent_started", "task": "escalation"}

@app.post("/agent/slowlow")
async def agent_slowlow():
    """Slow & low recon — rules silent, ML model flags it."""
    run_slow_low_agent(engine, manager.sync_broadcast)
    return {"status": "agent_started", "task": "slowlow"}

@app.post("/approve/timebox")
async def approve_timebox():
    engine.approve_timebox(duration_minutes=3)
    return {"status": "approved"}

@app.post("/deny/timebox")
async def deny_timebox():
    engine.deny_timebox()
    return {"status": "denied"}

@app.post("/reset")
async def reset():
    engine.reset()
    return {"status": "reset"}

# ─── Historical context (simulated audit trail for demo) ──────────────────────
HISTORICAL = {
    "rogue":         {"count": 11, "detail": "11 rogue agent incidents detected — 8 burst-rate breaches on Zone 1 (hospital grid), 3 out-of-zone pivots on Zone 2 (commercial district). All frozen within 4 seconds of first anomalous command."},
    "scope_creep":   {"count": 7,  "detail": "7 scope-creep incidents logged — agents that began with valid Zone 3 work orders and progressively accessed Zone 1 and Zone 2 assets. TARE flagged HEALTHY_ZONE_ACCESS signals in all cases and applied time-box containment."},
    "identity":      {"count": 5,  "detail": "5 identity-mismatch events — forged or replayed agent tokens were rejected at the gateway before any command executed. Zero asset changes resulted from these attempts."},
    "ml":            {"count": 9,  "detail": "9 ML anomaly detections — slow & low reconnaissance patterns that evaded rule-based signals entirely. The ML model caught subtle command-tempo deviations over 10–40 minute windows across 3 different agents."},
    "freeze":        {"count": 18, "detail": "18 FREEZE events triggered — average response time 3.2 seconds from first anomaly signal to full lockout. 14 led to supervisor Deny + escalation, 4 were approved time-boxes that resolved without further incident."},
    "incidents":     {"count": 14, "detail": "14 ServiceNow incidents raised — 9 Priority 1 Critical (GONE ROGUE, GHOST CLONE, SWARM STRIKE), 4 Priority 2 High (SCOPE CREEP, SILENT RECON), 1 Priority 3 Medium. Mean time to containment: 6.1 minutes."},
    "coordinated":   {"count": 3,  "detail": "3 coordinated swarm attacks detected — multiple agents acting simultaneously across different zones. TARE identified the pattern within 2 command cycles and froze all involved agents in parallel."},
    "zones":         {"detail": "Zone 1 (North Grid — Critical) was the most targeted zone with 23 unauthorised access attempts over 30 days. Zone 2 (East Grid) had 17. Zone 3 (West Grid) — the authorised operational zone — had no policy violations."},
    "summary":       {"detail": "30-day audit summary — 847 total commands processed | 791 allowed | 56 blocked | 18 freeze events | 14 incidents raised. Threat breakdown: 11 rogue/burst, 7 scope creep, 5 identity fraud, 9 ML anomalies, 3 coordinated swarm attacks. No critical infrastructure was impacted — all threats contained before asset changes."},
    "agents":        {"detail": "Over the past 30 days, 6 distinct agent IDs exhibited anomalous behaviour. 2 were confirmed compromised (credentials revoked), 3 were mis-configured (work orders corrected), 1 remains under investigation by the SOC team."},
}

def _is_historical(q: str) -> bool:
    time_words = ["past", "last", "days", "weeks", "months", "30 day", "15 day", "7 day",
                  "this week", "this month", "yesterday", "history", "historical",
                  "over time", "trend", "total so far", "so far", "till now", "until now", "recently"]
    return any(w in q for w in time_words)

# ─── TARE Assistant chat query ────────────────────────────────────────────────
@app.post("/chat/query")
async def chat_query(body: dict):
    q = (body.get("question") or "").lower().strip()
    snap = engine._snapshot()
    stats       = snap.get("stats", {})
    gateway_log = snap.get("gateway_log", [])
    incidents   = [snap["active_incident"]] if snap.get("active_incident") else []

    # Count by scenario/signal type from gateway log
    rogue_count       = sum(1 for e in gateway_log if any(s.get("signal") in ("BURST_RATE","OUT_OF_ZONE") for s in e.get("signals", [])))
    scope_creep_count = sum(1 for e in gateway_log if any(s.get("signal") == "HEALTHY_ZONE_ACCESS" for s in e.get("signals", [])))
    identity_count    = sum(1 for e in gateway_log if any(s.get("signal") == "IDENTITY_MISMATCH" for s in e.get("signals", [])))
    ml_count          = sum(1 for e in gateway_log if any(s.get("signal") == "ML_ANOMALY" for s in e.get("signals", [])))
    denied            = stats.get("denied", 0)
    allowed           = stats.get("allowed", 0)
    total             = stats.get("total", 0)
    freeze_events     = stats.get("freeze_events", 0)

    hist = _is_historical(q)
    def answer(text): return JSONResponse({"answer": text})

    # ── Historical questions ───────────────────────────────────────────────────
    if hist:
        if any(w in q for w in ["rogue", "gone rogue", "burst", "misbehav", "anomal"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['rogue']['detail']}")
        if any(w in q for w in ["scope creep", "escalation", "pivot"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['scope_creep']['detail']}")
        if any(w in q for w in ["identity", "impersonator", "forged", "ghost", "clone"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['identity']['detail']}")
        if any(w in q for w in ["ml", "machine learning", "silent", "recon", "slow"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['ml']['detail']}")
        if any(w in q for w in ["freeze", "frozen", "lockout"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['freeze']['detail']}")
        if any(w in q for w in ["incident", "servicenow", "ticket"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['incidents']['detail']}")
        if any(w in q for w in ["swarm", "coordinated", "multiple agent"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['coordinated']['detail']}")
        if any(w in q for w in ["zone", "which zone", "zone 1", "zone 2", "zone 3"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['zones']['detail']}")
        if any(w in q for w in ["agent", "how many agent", "which agent"]):
            return answer(f"[Historical — past 30 days] {HISTORICAL['agents']['detail']}")
        # Generic historical summary fallback
        return answer(f"[Historical — past 30 days] {HISTORICAL['summary']['detail']}")

    # ── Current session questions ──────────────────────────────────────────────
    if any(w in q for w in ["rogue", "gone rogue", "burst"]):
        return answer(f"In this session, {rogue_count} command(s) triggered rogue/burst-rate signals (BURST_RATE or OUT_OF_ZONE). {denied} total commands were blocked by TARE.")

    if any(w in q for w in ["scope creep", "escalation", "healthy zone"]):
        return answer(f"{scope_creep_count} command(s) triggered SCOPE CREEP signals (agent accessing healthy zones outside its clearance). This indicates an agent that started legitimate but expanded its reach.")

    if any(w in q for w in ["identity", "impersonator", "forged", "ghost", "clone"]):
        return answer(f"{identity_count} command(s) were blocked due to IDENTITY_MISMATCH — forged or mismatched agent credentials. These were stopped before any command executed.")

    if any(w in q for w in ["ml", "machine learning", "anomaly", "silent", "recon", "slow"]):
        return answer(f"The ML anomaly detector flagged {ml_count} command(s) this session. ML catches slow & low attacks that rule-based signals miss — subtle patterns over time.")

    if any(w in q for w in ["freeze", "frozen", "lockout"]):
        return answer(f"TARE triggered {freeze_events} FREEZE event(s) this session. A FREEZE locks out the agent and blocks all further commands until a supervisor resets the system.")

    if any(w in q for w in ["incident", "servicenow", "ticket"]):
        if incidents:
            inc = incidents[0]
            return answer(f"Active incident: {inc.get('incident_id')} — Priority {inc.get('priority', 'N/A')}, State: {inc.get('state','Open')}. Raised at {inc.get('created_at','unknown')}. Assigned to SOC Analyst.")
        return answer("No active ServiceNow incident in this session. Incidents are raised automatically when TARE detects a confirmed threat.")

    if any(w in q for w in ["total", "how many", "commands", "summary", "stats", "statistics", "report", "issues", "misbehav"]):
        return answer(
            f"Session summary — Total commands: {total} | Allowed: {allowed} | Blocked: {denied} | Freeze events: {freeze_events}. "
            f"Rogue/burst signals: {rogue_count} | Scope creep: {scope_creep_count} | Identity mismatches: {identity_count} | ML anomalies: {ml_count}."
        )

    if any(w in q for w in ["zone", "which zone", "zone 1", "zone 2", "zone 3"]):
        zone_hits = {}
        for e in gateway_log:
            z = e.get("asset_id", "")[:2] if e.get("asset_id") else e.get("zone", "")
            if z: zone_hits[z] = zone_hits.get(z, 0) + 1
        zone_str = ", ".join(f"{k}: {v} cmd(s)" for k, v in sorted(zone_hits.items())) or "No zone data yet"
        return answer(f"Command distribution by zone this session — {zone_str}.")

    return answer(
        "I can answer questions about this session or historical data. Try: "
        "'How many agents went rogue in the past 30 days?', 'Any scope creep recently?', "
        "'Identity mismatches last month?', 'Show session summary', or 'Any freeze events?'"
    )

# ─── Audit log download ────────────────────────────────────────────────────────
@app.get("/logs/download")
async def download_logs():
    snap = engine._snapshot()
    log_lines = [json.dumps(e) for e in snap.get("gateway_log", [])]
    return JSONResponse({"log": "\n".join(log_lines), "entries": len(log_lines)})

# ─── Static files (React build) ────────────────────────────────────────────────
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        target = STATIC_DIR / full_path
        if target.exists() and target.is_file():
            return FileResponse(target)
        return FileResponse(STATIC_DIR / "index.html")

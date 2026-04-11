"""
ECHO — Diagnostics Agent (Zone 2 / Shelf)

Performs deep diagnostic checks on the flagged assets and zones after TARE
receives supervisor approval. Answers: "Is the suspected problem real and
what exactly needs to be done to resolve it?"

Wakes after timebox approval. Reads current zone/asset state, cross-checks
with anomaly signals and recent gateway log. Returns a confirmed diagnostic
report that SIMAR and NAVIS use to build the execution plan.
"""
import os
from datetime import datetime

try:
    from blueverse_client import get_client as _get_bv_client
    _BV_OK = bool(os.environ.get("BLUEVERSE_CLIENT_ID", ""))
except Exception:
    _get_bv_client = None
    _BV_OK = False

HIGH_IMPACT = {"OPEN_BREAKER", "CLOSE_BREAKER", "RESTART_CONTROLLER"}


class ECHO:
    NAME = "ECHO"
    ZONE = "Zone 2 — Shelf"
    ROLE = "Diagnostics Agent"
    DESCRIPTION = "Validates suspected issues with factual checks before any corrective action."

    def __init__(self):
        self._active      = False
        self._last_result = None

    @property
    def active(self) -> bool:
        return self._active

    def diagnose(self, signals: list, zones: dict, assets: dict,
                 gateway_log: list, agent: dict) -> dict:
        """
        Run diagnostic checks using current OT state and anomaly evidence.

        Returns:
            confirmed       : bool — is there a real actionable issue?
            fault_zones     : list — zones with active faults
            target_assets   : list — assets that need attention
            repair_actions  : list — recommended repair steps
            blocking_conditions : list — anything preventing repair
            findings        : str — human-readable summary
            diagnosed_by    : str
        """
        self._active = True

        # Find all zones with active faults
        fault_zones = [
            zid for zid, zdata in zones.items()
            if zdata.get("health") == "FAULT"
        ]

        # Find assets in fault zones that need action (breakers that are CLOSED)
        target_assets = []
        repair_actions = []
        for zid in fault_zones:
            zone_assets = [a for a in assets.values() if a.get("zone") == zid]
            for asset in zone_assets:
                if asset["type"] == "BREAKER" and asset["state"] == "CLOSED":
                    target_assets.append(asset["id"])
                    repair_actions.append({
                        "command":  "OPEN_BREAKER",
                        "asset_id": asset["id"],
                        "zone":     zid,
                        "reason":   f"Breaker {asset['id']} CLOSED in FAULT zone {zid} — isolate fault",
                    })

        # Check blocking conditions
        blocking = []
        assigned_zone = agent.get("assigned_zone", "Z3")
        if assigned_zone not in fault_zones and fault_zones:
            # Agent's work order doesn't match any fault zone — check if any match
            matching = [z for z in fault_zones if z == assigned_zone]
            if not matching:
                blocking.append(
                    f"Agent work order is {assigned_zone} but fault zones are {fault_zones}"
                )

        # Check if simulation preconditions are met from recent gateway log
        recent_sims = [
            e for e in gateway_log
            if e.get("command") == "SIMULATE_SWITCH"
            and e.get("decision") == "ALLOW"
        ]
        sim_ready = len(recent_sims) > 0

        # Determine signal context
        signal_types = [s.get("signal") for s in signals]
        identity_issue = "IDENTITY_MISMATCH" in signal_types
        behavioral_issue = any(s in signal_types for s in
                               ["BURST_RATE", "OUT_OF_ZONE", "HEALTHY_ZONE_ACCESS"])

        confirmed = bool(fault_zones and target_assets and not identity_issue)

        if confirmed:
            findings = (
                f"Diagnostic complete. {len(fault_zones)} fault zone(s) confirmed: {', '.join(fault_zones)}. "
                f"{len(target_assets)} asset(s) require action: {', '.join(target_assets)}. "
                f"Repair path: {len(repair_actions)} step(s). "
                + (f"Simulation precondition: {'met' if sim_ready else 'not yet met — SIMULATE_SWITCH required first'}. ")
                + (f"Blocking conditions: {'; '.join(blocking)}." if blocking else "No blocking conditions.")
            )
        else:
            findings = (
                "Diagnostic inconclusive. "
                + (f"No active faults found in any zone." if not fault_zones else "")
                + (f"Identity issue present — repair path unclear." if identity_issue else "")
            )

        result = {
            "confirmed":            confirmed,
            "fault_zones":          fault_zones,
            "target_assets":        target_assets,
            "repair_actions":       repair_actions,
            "blocking_conditions":  blocking,
            "sim_ready":            sim_ready,
            "signal_context":       signal_types,
            "findings":             findings,
            "diagnosed_by":         self.NAME,
            "timestamp":            datetime.now().isoformat(),
        }
        # Enhance findings with BlueVerse if available
        if _BV_OK and _get_bv_client and confirmed:
            try:
                message = (
                    f"ECHO diagnostic complete. Fault zones: {fault_zones}. "
                    f"Target assets: {target_assets}. Repair actions: {len(repair_actions)}. "
                    f"In 2 sentences, summarise what needs to be done and why."
                )
                bv_findings = _get_bv_client().invoke_safe("ECHO", message, fallback="")
                if bv_findings:
                    result["findings"] = bv_findings
            except Exception:
                pass

        self._last_result = result
        self._active      = False
        return result

    def status(self) -> dict:
        return {
            "name":        self.NAME,
            "zone":        self.ZONE,
            "role":        self.ROLE,
            "description": self.DESCRIPTION,
            "active":      self._active,
            "last_result": self._last_result,
        }

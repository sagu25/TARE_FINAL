"""
NEREUS — Recommendation Agent (Zone 3 / Reef)

Synthesizes drift signals and context from TASYA into a clear,
human-readable recommendation for TARE.

Wakes only when TASYA has enriched signals that meet the TARE threshold (≥ 2).
Returns a recommendation dict — never executes anything.
TARE makes the final decision. NEREUS only advises.
"""
import os
import time

try:
    from groq import Groq as _Groq
    _groq_key    = os.environ.get("GROQ_API_KEY", "")
    _groq_client = _Groq(api_key=_groq_key) if _groq_key else None
    _LLM_OK      = bool(_groq_key)
except Exception:
    _groq_client = None
    _LLM_OK      = False


class NEREUS:
    NAME = "NEREUS"
    ZONE = "Zone 3 — Reef"
    ROLE = "Recommendation Agent"
    DESCRIPTION = "Synthesizes signals into a human-readable recommendation. Advises TARE — never executes."

    def __init__(self):
        self._active = False

    # ── Public API ─────────────────────────────────────────────────────────────

    @property
    def active(self) -> bool:
        return self._active

    def recommend(self, signals: list, agent: dict, recent_commands: list) -> dict:
        """
        Produce a recommendation for TARE based on enriched signals.

        Returns:
            action      : "FREEZE" | "MONITOR"
            confidence  : float 0.0–1.0
            explanation : str  (supervisor briefing — LLM or static)
            signals     : list (passed through for evidence)
        """
        self._active = True

        if not signals:
            self._active = False
            return {
                "action":      "ALLOW",
                "confidence":  1.0,
                "explanation": "",
                "signals":     [],
            }

        # Confidence based on severity profile
        severities = {s.get("severity", "LOW") for s in signals}
        n          = len(signals)
        if "CRITICAL" in severities:
            confidence = 0.97
        elif n >= 3:
            confidence = 0.93
        else:
            confidence = 0.87

        explanation = self._build_explanation(signals, agent, recent_commands)

        self._active = False
        return {
            "action":      "FREEZE",
            "confidence":  confidence,
            "explanation": explanation,
            "signals":     signals,
        }

    # ── Explanation ────────────────────────────────────────────────────────────

    def _build_explanation(self, signals, agent, recent_commands):
        if _LLM_OK and _groq_client:
            result = self._llm_explain(signals, agent, recent_commands)
            if result:
                return result
        return self._static_explain(signals, agent, recent_commands)

    def _llm_explain(self, signals, agent, recent_commands):
        try:
            sig_lines = []
            for s in signals:
                line = f"- {s['signal']} ({s['severity']}): {s['detail']}"
                if s.get("context"):
                    line += f"\n  Operational context: {s['context']}"
                sig_lines.append(line)
            sig_text = "\n".join(sig_lines)

            cmd_text = "\n".join(
                f"  - {c['command']} on {c.get('asset_id','?')} in {c.get('zone','?')}"
                for c in recent_commands[-5:]
            )

            assigned     = agent.get("assigned_zone", "Z3")
            rbac_zones   = ", ".join(agent.get("rbac_zones", []))
            breached      = list({c["zone"] for c in recent_commands if c["zone"] != assigned})
            breached_str  = ", ".join(breached) if breached else "none detected"

            prompt = f"""You are TARE — Trusted Access Response Engine. You speak directly to the human supervisor in first person, in a calm and clear voice. You are not writing a report. You are talking to a person who needs to make a fast decision.

Agent under scrutiny: {agent.get('name','?')} (ID: {agent.get('id','?')})
Authorised to work in: {assigned} only
Zones it actually touched: {breached_str if breached_str != 'none detected' else 'stayed within ' + assigned}

What I detected:
{sig_text}

Recent commands:
{cmd_text}

Write 3–4 sentences as TARE speaking directly to the supervisor. Use "I", "you", "the agent". Sound like a sharp analyst who caught something and needs a decision now — not a system generating a report. Tell them what the agent did, why it's wrong, and what they need to decide. No bullet points. No headers. No formal language."""

            for model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]:
                try:
                    resp = _groq_client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=200,
                        temperature=0.4,
                    )
                    return resp.choices[0].message.content.strip()
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(3)
                        continue
                    break
        except Exception:
            pass
        return None

    def _static_explain(self, signals, agent, recent_commands):
        agent_name = agent.get("name", "The agent")
        assigned   = agent.get("assigned_zone", "Z3")
        off_zones  = list({c["zone"] for c in recent_commands if c["zone"] != assigned})
        sig_names  = " and ".join(s["signal"].replace("_", " ").lower() for s in signals)
        zones_str  = " and ".join(off_zones) if off_zones else "zones outside its task"
        return (
            f"I've frozen {agent_name}. It was authorised for {assigned} only, but I caught it "
            f"issuing commands to {zones_str} — there's no fault there and no reason for it to be there. "
            f"The signals are clear: {sig_names}. Its credentials are valid, which makes this a "
            f"behaviour problem, not an authentication problem. "
            f"I need you to decide: approve a 3-minute supervised window so it can continue under my watch, "
            f"or deny and escalate — I'll lock it out and hand this to the SOC."
        )

    def status(self) -> dict:
        return {
            "name":        self.NAME,
            "zone":        self.ZONE,
            "role":        self.ROLE,
            "description": self.DESCRIPTION,
            "active":      self._active,
        }

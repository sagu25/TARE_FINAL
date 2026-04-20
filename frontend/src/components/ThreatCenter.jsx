/**
 * ThreatCenter — replaces ZoneObservatory in the center column.
 *
 * NORMAL + idle      → "System Secure" + stat counters
 * Scenario running   → Live agent chain + scenario context
 * FREEZE / DOWNGRADE → Full-screen drama: mode, signals, incident, approve/deny
 */
import { useEffect, useState } from 'react'

const MODE_COLOR = {
  NORMAL:         { bg: 'rgba(0,232,124,0.06)',  border: '#00e87c', text: '#00e87c',  label: 'ALL SYSTEMS NORMAL' },
  FREEZE:         { bg: 'rgba(255,45,45,0.10)',   border: '#ff2d2d', text: '#ff4d4d',  label: 'SECURITY FREEZE' },
  DOWNGRADE:      { bg: 'rgba(255,140,0,0.10)',   border: '#ff8c00', text: '#ffa040',  label: 'ACCESS DOWNGRADED' },
  TIMEBOX_ACTIVE: { bg: 'rgba(168,85,247,0.10)',  border: '#a855f7', text: '#c084fc',  label: 'TIMEBOX ACTIVE' },
  SAFE:           { bg: 'rgba(0,184,230,0.08)',   border: '#00b8e6', text: '#00d4ff',  label: 'SAFE MODE' },
}

const SIGNAL_LABELS = {
  BURST_RATE:         { label: 'Burst Rate',         color: '#ff2d2d' },
  OUT_OF_ZONE:        { label: 'Out of Zone',         color: '#ff8c00' },
  HEALTHY_ZONE_ACCESS:{ label: 'Healthy Zone Access', color: '#f59e0b' },
  SKIPPED_SIMULATION: { label: 'Skipped Simulation',  color: '#f59e0b' },
  ML_ANOMALY:         { label: 'ML Anomaly',          color: '#a855f7' },
  IDENTITY_MISMATCH:  { label: 'Identity Mismatch',   color: '#ff2d2d' },
}

const AGENT_CHAIN = ['KORAL','MAREA','TASYA','NEREUS','ECHO','SIMAR','NAVIS','RISKADOR','TRITON','AEGIS','TEMPEST','LEVIER']
const AGENT_ICONS = {
  KORAL:'📡', MAREA:'🌊', TASYA:'🔗', NEREUS:'🧠',
  ECHO:'🔬',  SIMAR:'🔭', NAVIS:'🗺', RISKADOR:'⚖',
  TRITON:'⚡', AEGIS:'🛡', TEMPEST:'🌪', LEVIER:'↩', BARRIER:'🚧',
}

export default function ThreatCenter({
  mode, signals, incident, stats, scenarioCtx, scenarioOutcome,
  activeAgents, agentVoices, showApprove, onApprove, onDeny, timebox,
}) {
  const [tick, setTick] = useState(0)
  const mc = MODE_COLOR[mode] || MODE_COLOR.NORMAL
  const isThreat = mode !== 'NORMAL'
  const hasScenario = !!scenarioCtx
  const activeList = Object.keys(activeAgents || {})
  const latestVoice = activeList.length > 0
    ? agentVoices?.[activeList[activeList.length - 1]]
    : null

  // Pulse tick for animations
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="panel tc-root" style={{ borderColor: mc.border, transition: 'border-color 0.4s' }}>

      {/* ── Top bar: mode status ───────────────────────────────── */}
      <div className="tc-modebar" style={{ background: mc.bg, borderBottom: `1px solid ${mc.border}33` }}>
        <span className="tc-mode-dot" style={{ background: mc.text, boxShadow: `0 0 8px ${mc.text}` }} />
        <span className="tc-mode-label" style={{ color: mc.text }}>{mc.label}</span>
        {isThreat && <span className="tc-mode-pulse" style={{ color: mc.text }}>●</span>}
        <span style={{ marginLeft: 'auto', fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--text-dim)' }}>
          TARE THREAT CENTER
        </span>
      </div>

      {/* ── Body ──────────────────────────────────────────────── */}
      <div className="tc-body">

        {/* ── FREEZE / DOWNGRADE / SAFE — threat drama ───────── */}
        {isThreat && (
          <div className="tc-threat-view">

            {/* Big mode indicator */}
            <div className="tc-big-mode" style={{ color: mc.text, borderColor: mc.border, boxShadow: `0 0 32px ${mc.text}40` }}>
              <span className="tc-big-icon">
                {mode === 'FREEZE' ? '❄' : mode === 'DOWNGRADE' ? '▼' : mode === 'TIMEBOX_ACTIVE' ? '⏱' : '✓'}
              </span>
              <span className="tc-big-text">{mode.replace('_', ' ')}</span>
            </div>

            {/* Signals */}
            {signals && signals.length > 0 && (
              <div className="tc-signals">
                <span className="tc-section-label">SIGNALS DETECTED</span>
                <div className="tc-signal-chips">
                  {signals.map((s, i) => {
                    const meta = SIGNAL_LABELS[s.signal] || { label: s.signal, color: '#888' }
                    return (
                      <span key={i} className="tc-sig-chip" style={{ borderColor: meta.color, color: meta.color, background: `${meta.color}15` }}>
                        {meta.label}
                      </span>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Incident */}
            {incident && (
              <div className="tc-incident-row">
                <span className="tc-section-label">SERVICENOW INCIDENT</span>
                <div className="tc-incident-card">
                  <span className="tc-inc-id">{incident.incident_id}</span>
                  <span className="tc-inc-pri" style={{ color: incident.priority?.includes('1') ? '#ff2d2d' : '#ff8c00' }}>
                    {incident.priority}
                  </span>
                  <span className="tc-inc-state">{incident.state}</span>
                </div>
              </div>
            )}

            {/* Approve / Deny */}
            {showApprove && (
              <div className="tc-approve-row">
                <span className="tc-section-label" style={{ color: '#a855f7' }}>SUPERVISOR ACTION REQUIRED</span>
                <div className="tc-approve-btns">
                  <button className="tc-btn-approve" onClick={onApprove}>
                    ✓ Approve 3-min Window
                  </button>
                  <button className="tc-btn-deny" onClick={onDeny}>
                    ✕ Deny &amp; Escalate
                  </button>
                </div>
              </div>
            )}

            {/* Timebox countdown */}
            {mode === 'TIMEBOX_ACTIVE' && timebox != null && (
              <div className="tc-timebox-row">
                <span className="tc-section-label" style={{ color: '#a855f7' }}>TIMEBOX REMAINING</span>
                <span className="tc-timebox-count" style={{ color: timebox < 30 ? '#ff2d2d' : '#a855f7' }}>
                  {Math.floor(timebox / 60)}:{String(timebox % 60).padStart(2, '0')}
                </span>
              </div>
            )}
          </div>
        )}

        {/* ── NORMAL — scenario running ───────────────────────── */}
        {!isThreat && hasScenario && (
          <div className="tc-scenario-view">
            <div className="tc-scenario-badge">
              <span className="tc-sc-threat" style={{ color: scenarioCtx.threat_level === 'CRITICAL' ? '#ff2d2d' : scenarioCtx.threat_level === 'HIGH' ? '#ff8c00' : scenarioCtx.threat_level === 'MEDIUM' ? '#f59e0b' : '#00e87c' }}>
                {scenarioCtx.threat_level}
              </span>
              <span className="tc-sc-title">{scenarioCtx.title}</span>
            </div>

            {/* Agent chain */}
            <div className="tc-chain-label">AGENT ACTIVATION CHAIN</div>
            <div className="tc-agent-chain">
              {AGENT_CHAIN.map((a, i) => {
                const isActive = !!activeAgents?.[a]
                const wasDone  = !isActive && agentVoices?.[a]
                return (
                  <span key={a}>
                    <span
                      className={`tc-chain-agent ${isActive ? 'tc-chain-active' : wasDone ? 'tc-chain-done' : 'tc-chain-idle'}`}
                      title={a}
                    >
                      {AGENT_ICONS[a]} {a}
                    </span>
                    {i < AGENT_CHAIN.length - 1 && (
                      <span className="tc-chain-arrow" style={{ color: (isActive || wasDone) ? '#00d4ff' : '#1a2f4e' }}>›</span>
                    )}
                  </span>
                )
              })}
            </div>

            {/* Live agent voice */}
            {latestVoice && (
              <div className="tc-live-voice">
                <span className="tc-voice-agent">{activeList[activeList.length - 1]}</span>
                <span className="tc-voice-text">"{latestVoice}"</span>
              </div>
            )}

            {/* Stats row */}
            <div className="tc-stats-mini">
              <div className="tc-stat"><span>{stats?.total ?? 0}</span><label>Commands</label></div>
              <div className="tc-stat tc-stat-ok"><span>{stats?.allowed ?? 0}</span><label>Allowed</label></div>
              <div className="tc-stat tc-stat-bad"><span>{stats?.denied ?? 0}</span><label>Blocked</label></div>
              <div className="tc-stat tc-stat-warn"><span>{stats?.freeze_events ?? 0}</span><label>Freezes</label></div>
            </div>
          </div>
        )}

        {/* ── NORMAL — idle (no scenario) ─────────────────────── */}
        {!isThreat && !hasScenario && (
          <div className="tc-idle-view">
            <div className="tc-idle-icon">🛡</div>
            <div className="tc-idle-title">SYSTEM SECURE</div>
            <div className="tc-idle-sub">All agents on standby · No active threats</div>

            <div className="tc-stats-grid">
              <div className="tc-stat-box">
                <span className="tc-stat-val">{stats?.total ?? 0}</span>
                <span className="tc-stat-lbl">Total Commands</span>
              </div>
              <div className="tc-stat-box tc-stat-ok">
                <span className="tc-stat-val">{stats?.allowed ?? 0}</span>
                <span className="tc-stat-lbl">Allowed</span>
              </div>
              <div className="tc-stat-box tc-stat-bad">
                <span className="tc-stat-val">{stats?.denied ?? 0}</span>
                <span className="tc-stat-lbl">Blocked</span>
              </div>
              <div className="tc-stat-box tc-stat-freeze">
                <span className="tc-stat-val">{stats?.freeze_events ?? 0}</span>
                <span className="tc-stat-lbl">Freeze Events</span>
              </div>
            </div>

            <div className="tc-idle-hint">▶ Select a scenario from the panel to begin</div>
          </div>
        )}

      </div>
    </div>
  )
}

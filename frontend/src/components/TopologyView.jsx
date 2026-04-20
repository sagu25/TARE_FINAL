/**
 * TopologyView — Zone → Agent → Asset architecture map
 * Shows which agents live in which zone and what assets each zone owns.
 * Agent cards pulse green when active, red when a threat is detected.
 */

const ZONES = [
  {
    id: 'Z3', label: 'Zone 3 — Reef', sub: 'Observe & Recommend',
    color: '#00d4ff', border: '#00d4ff22',
    agents: [
      { name:'KORAL',   icon:'📡', role:'Telemetry Observer' },
      { name:'MAREA',   icon:'🌊', role:'Drift Analyst' },
      { name:'TASYA',   icon:'🔗', role:'Context Correlator' },
      { name:'NEREUS',  icon:'🧠', role:'Recommendation Engine' },
    ],
    assets: ['BRK-301','FDR-301'],
  },
  {
    id: 'Z2', label: 'Zone 2 — Shelf', sub: 'Diagnose & Prepare',
    color: '#fb923c', border: '#fb923c22',
    agents: [
      { name:'ECHO',     icon:'🔬', role:'Diagnostics' },
      { name:'SIMAR',    icon:'🔭', role:'Simulation' },
      { name:'NAVIS',    icon:'🗺', role:'Change Planner' },
      { name:'RISKADOR', icon:'⚖',  role:'Risk Scoring' },
    ],
    assets: ['BRK-205','FDR-205'],
  },
  {
    id: 'Z1', label: 'Zone 1 — Trench', sub: 'Execute with Safety',
    color: '#f43f5e', border: '#f43f5e22',
    agents: [
      { name:'TRITON',  icon:'⚡', role:'Execution' },
      { name:'AEGIS',   icon:'🛡', role:'Safety Validator' },
      { name:'TEMPEST', icon:'🌪', role:'Session Monitor' },
      { name:'LEVIER',  icon:'↩',  role:'Rollback & Recovery' },
    ],
    assets: ['BRK-110','FDR-110'],
  },
  {
    id: 'Z4', label: 'Zone 4 — Gateway', sub: 'Policy Enforcement',
    color: '#00e87c', border: '#00e87c22',
    agents: [
      { name:'BARRIER', icon:'🚧', role:'Policy Enforcement' },
    ],
    assets: [],
  },
]

const ASSET_STATE_COLOR = {
  CLOSED:     '#00e87c',
  RUNNING:    '#00e87c',
  OPEN:       '#ff8c00',
  RESTARTING: '#ff8c00',
}

export default function TopologyView({ activeAgents = {}, assets = {}, mode = 'NORMAL' }) {
  const isThreat = mode !== 'NORMAL'

  return (
    <div className="topo-root">
      <div className="topo-header">
        <span className="topo-title">TARE Agent Topology</span>
        <span className="topo-sub">Zone · Agent · Asset architecture</span>
      </div>

      <div className="topo-grid">
        {ZONES.map(zone => (
          <div key={zone.id} className="topo-zone-card" style={{ borderColor: zone.color + '55', background: zone.border }}>

            {/* Zone header */}
            <div className="topo-zone-hdr" style={{ borderBottom: `1px solid ${zone.color}33` }}>
              <span className="topo-zone-dot" style={{ background: zone.color, boxShadow: `0 0 6px ${zone.color}` }} />
              <div>
                <div className="topo-zone-name" style={{ color: zone.color }}>{zone.label}</div>
                <div className="topo-zone-sub">{zone.sub}</div>
              </div>
            </div>

            {/* Agents */}
            <div className="topo-agents">
              {zone.agents.map(ag => {
                const isActive = !!activeAgents[ag.name]
                return (
                  <div key={ag.name} className={`topo-agent-row ${isActive ? 'topo-agent-active' : ''}`}
                    style={{ borderColor: isActive ? zone.color : 'transparent' }}>
                    <span className="topo-ag-icon">{ag.icon}</span>
                    <div className="topo-ag-info">
                      <span className="topo-ag-name" style={{ color: isActive ? zone.color : 'var(--text-primary)' }}>{ag.name}</span>
                      <span className="topo-ag-role">{ag.role}</span>
                    </div>
                    {isActive && <span className="topo-ag-live" style={{ color: zone.color }}>ACTIVE</span>}
                  </div>
                )
              })}
            </div>

            {/* Assets */}
            {zone.assets.length > 0 && (
              <div className="topo-assets">
                <span className="topo-assets-label">Assets</span>
                <div className="topo-asset-chips">
                  {zone.assets.map(aid => {
                    const ast = assets[aid]
                    const sc  = ASSET_STATE_COLOR[ast?.state] || '#6b8fa3'
                    return (
                      <span key={aid} className="topo-asset-chip" style={{ borderColor: sc, color: sc }}>
                        {aid} · {ast?.state ?? '—'}
                      </span>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

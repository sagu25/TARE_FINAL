import { useState, useEffect } from 'react'

export default function Header({ wsConnected, darkMode, onToggleTheme }) {
  const [now, setNow] = useState(new Date())
  useEffect(() => { const t = setInterval(() => setNow(new Date()), 1000); return () => clearInterval(t) }, [])

  const timeStr = now.toLocaleTimeString('en-GB', { hour12: false })
  const dateStr = now.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

  return (
    <header className="tare-header">
      <div className="hdr-brand">
        <div className="hdr-title">
          <span className="hdr-logo">TARE</span>
          <span className="hdr-title-rest">&nbsp;— AI OBSERVABILITY</span>
        </div>
        <div className="hdr-sub">Trusted Access Response Engine · E&amp;U Security Platform</div>
      </div>

      <div style={{ flex: 1 }} />

      <div className="hdr-right">
        <button className="theme-toggle" onClick={onToggleTheme} title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}>
          {darkMode ? '☀' : '☾'}
        </button>
        <span className={`ws-dot ${wsConnected ? 'on' : 'off'}`} />
        <span className="ws-label">{wsConnected ? 'LIVE' : 'OFFLINE'}</span>
        <span className="hdr-clock">{dateStr}&nbsp;&nbsp;{timeStr} UTC</span>
      </div>
    </header>
  )
}

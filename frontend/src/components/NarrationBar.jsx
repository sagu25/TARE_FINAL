import { useState, useEffect } from 'react'
import { narrationEngine, narStart, narStop, narTogglePause, narToggleMute, NARRATION } from './LandingPage'

// Narration continues from where landing page left off.
// This bar floats at the bottom of the dashboard.

export default function NarrationBar() {
  const [state, setState] = useState({
    playing: narrationEngine.playing,
    paused:  narrationEngine.paused,
    muted:   narrationEngine.muted,
    index:   narrationEngine.index,
  })
  const [expanded, setExpanded] = useState(true)

  useEffect(() => {
    const sync = () => setState({
      playing: narrationEngine.playing,
      paused:  narrationEngine.paused,
      muted:   narrationEngine.muted,
      index:   narrationEngine.index,
    })
    narrationEngine.listeners.push(sync)
    return () => { narrationEngine.listeners = narrationEngine.listeners.filter(f => f !== sync) }
  }, [])

  const currentLine = NARRATION[state.index]?.text || ''
  const progress    = NARRATION.length ? Math.round((state.index / NARRATION.length) * 100) : 0

  return (
    <div className={`narbar ${expanded ? 'narbar-expanded' : 'narbar-collapsed'}`}>
      {/* Progress bar */}
      {state.playing && (
        <div className="narbar-progress">
          <div className="narbar-progress-fill" style={{ width: `${progress}%` }} />
        </div>
      )}

      <div className="narbar-inner">
        {/* Left: status + current line */}
        <div className="narbar-left">
          {state.playing && !state.paused && <span className="narbar-dot" />}
          {state.paused && <span className="narbar-dot narbar-dot-paused" />}
          {!state.playing && <span className="narbar-label-idle">🔈 NARRATION</span>}
          {expanded && state.playing && (
            <span className="narbar-line">{currentLine}</span>
          )}
          {expanded && state.paused && (
            <span className="narbar-line narbar-line-paused">Paused — {currentLine}</span>
          )}
        </div>

        {/* Right: controls */}
        <div className="narbar-controls">
          {!state.playing && (
            <button className="narbar-btn narbar-btn-play"
              onClick={() => narStart(narrationEngine.index)}
              title="Resume narration">
              ▶ Resume
            </button>
          )}
          {state.playing && (
            <button className={`narbar-btn ${state.paused ? 'narbar-btn-resume' : 'narbar-btn-pause'}`}
              onClick={narTogglePause}
              title={state.paused ? 'Resume' : 'Pause'}>
              {state.paused ? '▶' : '⏸'}
            </button>
          )}
          {state.playing && (
            <button className="narbar-btn narbar-btn-stop"
              onClick={narStop} title="Stop narration">
              ■
            </button>
          )}
          <button className={`narbar-btn narbar-btn-mute ${state.muted ? 'narbar-btn-muted' : ''}`}
            onClick={narToggleMute}
            title={state.muted ? 'Unmute' : 'Mute'}>
            {state.muted ? '🔇' : '🔊'}
          </button>
          <button className="narbar-btn narbar-btn-toggle"
            onClick={() => setExpanded(e => !e)}
            title={expanded ? 'Collapse' : 'Expand'}>
            {expanded ? '▼' : '▲'}
          </button>
        </div>
      </div>
    </div>
  )
}

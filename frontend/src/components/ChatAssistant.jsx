import { useEffect, useRef, useState } from 'react'

function fmtTs(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString('en-GB', { hour12: false })
}

function scrollToBottom(ref) {
  setTimeout(() => ref.current?.scrollIntoView({ behavior: 'smooth', block: 'end' }), 60)
}

const SUGGESTIONS = [
  'What happened this session?',
  'Any rogue behaviour detected?',
  'Why did TARE fire?',
  'Show me the timeline',
  'Any identity mismatches?',
  'What did the ML model catch?',
]

// Detect if a message is a "narration" status (used to render it as a centered divider)
function isNarration(msg) {
  return msg.role === 'narration' || msg.role === 'system'
}

function fmtCountdown(secs) {
  if (secs == null || secs < 0) return null
  const m = Math.floor(secs / 60)
  const s = secs % 60
  return `${m}:${String(s).padStart(2, '0')}`
}

export default function ChatAssistant({ messages, showApprove, approveType, timeboxRemaining, onApprove, onDeny }) {
  const bottomRef  = useRef(null)
  const inputRef   = useRef(null)
  const [input,    setInput]    = useState('')
  const [chatLog,  setChatLog]  = useState([])
  const [loading,  setLoading]  = useState(false)

  useEffect(() => { scrollToBottom(bottomRef) }, [messages, chatLog, loading])

  const ask = async (question) => {
    const q = question.trim()
    if (!q) return
    setInput('')
    setChatLog(prev => [...prev, { role: 'user', text: q, ts: new Date().toISOString() }])
    setLoading(true)
    try {
      const res  = await fetch('/chat/query', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      })
      const data = await res.json()
      setChatLog(prev => [...prev, { role: 'tare', text: data.answer, ts: new Date().toISOString(), isAnswer: true }])
    } catch {
      setChatLog(prev => [...prev, { role: 'tare', text: "I can't reach the backend right now.", ts: new Date().toISOString() }])
    }
    setLoading(false)
  }

  const onKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input) } }

  const allMsgs = [
    ...messages.map(m => ({ ...m, _src: 'ws' })),
    ...chatLog.map(m => ({ ...m, _src: 'chat' })),
  ].sort((a, b) => new Date(a.ts) - new Date(b.ts))

  return (
    <div className="panel chat-panel">

      <div className="chat-body">
        {allMsgs.length === 0 && (
          <div className="chat-empty">
            <div className="chat-empty-icon">🛡</div>
            <div>TARE is watching. Ask me anything about what's happening.</div>
          </div>
        )}

        {allMsgs.map((m, i) => {
          if (isNarration(m)) {
            return (
              <div key={i} className="chat-narration">
                <span>{m.text}</span>
              </div>
            )
          }

          if (m.role === 'user') {
            return (
              <div key={i} className="chat-row chat-row-user">
                <div className="chat-bubble chat-bubble-user">
                  <div className="bubble-text">{m.text}</div>
                  <div className="bubble-ts">{fmtTs(m.ts)}</div>
                </div>
                <div className="chat-avatar chat-avatar-user">You</div>
              </div>
            )
          }

          // TARE message
          return (
            <div key={i} className="chat-row chat-row-tare">
              <div className="chat-avatar chat-avatar-tare">🛡</div>
              <div className={`chat-bubble chat-bubble-tare ${m.isAnswer ? 'chat-bubble-answer' : ''}`}>
                <div className="bubble-sender">{m.isAnswer ? 'TARE — Answer' : 'TARE'}</div>
                <div className="bubble-text">{m.text}</div>
                <div className="bubble-ts">{fmtTs(m.ts)}</div>
              </div>
            </div>
          )
        })}

        {loading && (
          <div className="chat-row chat-row-tare">
            <div className="chat-avatar chat-avatar-tare">🛡</div>
            <div className="chat-bubble chat-bubble-tare">
              <div className="bubble-sender">TARE</div>
              <div className="bubble-text chat-typing">Thinking<span>...</span></div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Suggestions — shown until user asks something */}
      {chatLog.length === 0 && !loading && (
        <div className="chat-suggestions">
          {SUGGESTIONS.map(s => (
            <button key={s} className="chat-suggestion-btn" onClick={() => ask(s)}>{s}</button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="chat-input-row">
        <input
          ref={inputRef}
          className="chat-input"
          placeholder="Ask TARE anything…"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={onKey}
          disabled={loading}
        />
        <button className="chat-send-btn" onClick={() => ask(input)} disabled={loading || !input.trim()}>
          ➤
        </button>
      </div>

      {timeboxRemaining != null && (
        <div className="timebox-countdown">
          ⏱ Window active — {fmtCountdown(timeboxRemaining)} remaining
        </div>
      )}

      {showApprove && (
        <div className="approve-bar">
          <div className="approve-label">⚠ Supervisor decision required</div>
          <div className="approve-actions">
            <button className="approve-btn" onClick={onApprove}>
              {approveType === 'ooh' ? '✓ Approve 15-min Emergency Window' : '✓ Approve 3-min Time-Box'}
            </button>
            <button className="deny-btn" onClick={onDeny}>✕ Deny / Escalate</button>
          </div>
        </div>
      )}
    </div>
  )
}

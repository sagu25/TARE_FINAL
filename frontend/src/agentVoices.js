/**
 * Agent TTS Engine
 * Primary: Azure Neural TTS via backend /api/tts (natural, distinct voices per agent)
 * Fallback: browser Web Speech API (if Azure not configured or request fails)
 *
 * Public API is unchanged — speakAgent / setVoiceMuted / clearVoiceQueue
 */

// ── Azure status — checked once on load ───────────────────────────────────────
let _azureReady = false

async function _checkAzure() {
  try {
    const res = await fetch('/api/tts/status')
    const data = await res.json()
    _azureReady = data.configured === true
  } catch {
    _azureReady = false
  }
}
_checkAzure()

// ── Browser Web Speech fallback profiles ──────────────────────────────────────
const FALLBACK_PROFILES = {
  KORAL:    { voices: ['Google UK English Female', 'Microsoft Hazel', 'Karen', 'Samantha'],  pitch: 1.15, rate: 1.15, volume: 0.9  },
  MAREA:    { voices: ['Google UK English Male',   'Microsoft George', 'Daniel', 'Alex'],    pitch: 0.95, rate: 1.0,  volume: 0.95 },
  TASYA:    { voices: ['Microsoft Zira',           'Google US English', 'Victoria'],          pitch: 1.05, rate: 0.95, volume: 0.9  },
  NEREUS:   { voices: ['Microsoft David',          'Google UK English Male', 'Alex'],         pitch: 0.8,  rate: 0.88, volume: 1.0  },
  ECHO:     { voices: ['Google UK English Female', 'Microsoft Hazel', 'Karen'],               pitch: 1.1,  rate: 1.1,  volume: 0.85 },
  SIMAR:    { voices: ['Microsoft Mark',           'Google US English', 'Tom'],               pitch: 1.0,  rate: 1.05, volume: 0.85 },
  NAVIS:    { voices: ['Microsoft Zira',           'Google US English', 'Samantha'],          pitch: 0.92, rate: 1.0,  volume: 0.9  },
  RISKADOR: { voices: ['Microsoft David',          'Google UK English Male', 'Daniel'],       pitch: 0.88, rate: 0.95, volume: 0.95 },
  TRITON:   { voices: ['Microsoft Mark',           'Google UK English Male', 'Fred'],         pitch: 0.82, rate: 1.1,  volume: 1.0  },
  AEGIS:    { voices: ['Microsoft David',          'Google UK English Male', 'Alex'],         pitch: 0.78, rate: 0.85, volume: 1.0  },
  TEMPEST:  { voices: ['Google UK English Female', 'Microsoft Hazel', 'Karen'],               pitch: 1.05, rate: 1.2,  volume: 0.85 },
  LEVIER:   { voices: ['Microsoft Zira',           'Google US English', 'Victoria'],          pitch: 1.0,  rate: 0.9,  volume: 0.9  },
  BARRIER:  { voices: ['Microsoft Mark',           'Google UK English Male', 'Fred'],         pitch: 0.65, rate: 0.85, volume: 1.0  },
}

let _voiceMap = {}
let _anyVoice = null

function _loadVoices() {
  const all = window.speechSynthesis?.getVoices() || []
  _voiceMap = {}
  all.forEach(v => { _voiceMap[v.name] = v })
  _anyVoice = all.find(v => v.lang?.startsWith('en')) || all[0] || null
}

if (typeof window !== 'undefined' && window.speechSynthesis) {
  window.speechSynthesis.onvoiceschanged = _loadVoices
  _loadVoices()
}

function _pickVoice(preferenceList) {
  for (const name of preferenceList) {
    if (_voiceMap[name]) return _voiceMap[name]
  }
  return _anyVoice
}

// ── TTS Queue ──────────────────────────────────────────────────────────────────
let _queue    = []
let _speaking = false
let _muted    = false

// How each agent name should be pronounced
const PRONUNCIATIONS = {
  KORAL:    'Koral',
  MAREA:    'Marea',
  TASYA:    'Tasya',
  NEREUS:   'Neereus',
  ECHO:     'Echo',
  SIMAR:    'Simar',
  NAVIS:    'Navis',
  RISKADOR: 'Riskador',
  TRITON:   'Triton',
  AEGIS:    'Aegis',
  TEMPEST:  'Tempest',
  LEVIER:   'Levier',
  BARRIER:  'Barrier',
}

// ── Azure path ─────────────────────────────────────────────────────────────────
async function _speakAzure(agent, text) {
  try {
    const res = await fetch('/api/tts', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ agent, text }),
    })
    if (!res.ok) return false

    const blob = await res.blob()
    const url  = URL.createObjectURL(blob)
    const audio = new Audio(url)

    return new Promise(resolve => {
      audio.onended = () => { URL.revokeObjectURL(url); resolve(true) }
      audio.onerror = () => { URL.revokeObjectURL(url); resolve(false) }
      audio.volume  = _muted ? 0 : 1.0
      audio.play().catch(() => resolve(false))
    })
  } catch {
    return false
  }
}

// ── Browser fallback path ──────────────────────────────────────────────────────
function _speakBrowser(agent, text) {
  return new Promise(resolve => {
    if (!window.speechSynthesis) return resolve()
    const profile = FALLBACK_PROFILES[agent] || { voices: [], pitch: 1.0, rate: 1.0, volume: 0.9 }
    const voice   = _pickVoice(profile.voices)
    const utt     = new SpeechSynthesisUtterance(text)
    utt.pitch  = profile.pitch
    utt.rate   = profile.rate
    utt.volume = _muted ? 0 : profile.volume
    if (voice) utt.voice = voice
    utt.onend   = () => resolve()
    utt.onerror = () => resolve()
    window.speechSynthesis.speak(utt)
  })
}

// ── Queue processor ───────────────────────────────────────────────────────────
async function _processQueue() {
  if (_speaking || _queue.length === 0) return
  _speaking = true

  const { agent, text } = _queue.shift()

  let done = false
  if (_azureReady && !_muted) {
    done = await _speakAzure(agent, text)
  }
  if (!done) {
    // fallback: browser voice (or silent if muted)
    await _speakBrowser(agent, text)
  }

  _speaking = false
  _processQueue()
}

// ── Public API ─────────────────────────────────────────────────────────────────

export function speakAgent(agent, message) {
  if (_muted) return
  const name = PRONUNCIATIONS[agent] || agent.charAt(0) + agent.slice(1).toLowerCase()
  const text = `${name}: ${message}`
  _queue.push({ agent, text })
  _processQueue()
}

// Speaks a single line and resolves when audio finishes.
// Used by AgentBriefing for sequential, awaitable playback.
export async function speakAgentAsync(agent, message) {
  if (_muted) return
  const name = PRONUNCIATIONS[agent] || agent.charAt(0) + agent.slice(1).toLowerCase()
  const text = `${name}: ${message}`

  if (_azureReady) {
    const ok = await _speakAzure(agent, text)
    if (ok) return
  }
  await _speakBrowser(agent, text)
}

export function setVoiceMuted(muted) {
  _muted = muted
  if (muted) {
    window.speechSynthesis?.cancel()
    _queue    = []
    _speaking = false
  }
}

export function isVoiceMuted() { return _muted }

export function clearVoiceQueue() {
  window.speechSynthesis?.cancel()
  _queue    = []
  _speaking = false
}

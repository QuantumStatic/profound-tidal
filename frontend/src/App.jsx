import { useEffect, useState, useCallback } from 'react'
import './styles.css'
import { MONTHS, isLive } from './months'
import { fetchRun } from './api'
import GapBoard from './stages/GapBoard'
import Opportunities from './stages/Opportunities'
import Radar from './stages/Radar'
import Sources from './stages/Sources'
import Craft from './stages/Craft'

const NAV = [
  ['gaps', 'Where AI ignores you', 'Your visibility gaps'],
  ['worth', "What it's worth", 'Ranked by $ · re-orders by month'],
  ['radar', "What's about to spike", 'Demand radar'],
  ['why', 'Why AI ignores you', 'The sources it trusts'],
  ['move', 'Your move', 'What to publish'],
]

export default function App() {
  const [month, setMonth] = useState(6)
  const [data, setData] = useState(null)
  const [stage, setStage] = useState('gaps')
  const [counter, setCounter] = useState(0)
  const [toast, setToast] = useState('')
  const [toastOn, setToastOn] = useState(false)

  useEffect(() => {
    setData(null)
    fetchRun(month).then(setData)
  }, [month])

  useEffect(() => {
    if (!data) return
    const total = data.opportunities.reduce((s, o) => s + o.annual_value, 0)
    let n = 0
    const id = setInterval(() => {
      n++
      setCounter(Math.round(total * Math.min(n / 40, 1)))
      if (n >= 40) clearInterval(id)
    }, 16)
    return () => clearInterval(id)
  }, [data])

  const showToast = useCallback((msg) => {
    setToast(msg)
    setToastOn(true)
    setTimeout(() => setToastOn(false), 3600)
  }, [])

  if (!data) return <div className="app"><p className="sub" style={{paddingTop:40}}>Loading…</p></div>

  return (
    <div className="app">
      <header>
        <div className="logo"><span className="wave">🌊</span>Tidal</div>
        <div className="pill"><span className="mut">Brand</span> {data.subject} ▾</div>
        <div className="pill"><span className="mut">Market</span> Frontier AI Models ▾</div>
        <div className="spacer" />
        <div className="counter">
          <div className="lab">Recoverable revenue found</div>
          <div className="val">${counter.toLocaleString()}</div>
          <div className="sub">{isLive(month) ? 'measured' : 'projected'} · across 15 use-cases</div>
        </div>
      </header>

      <div className="tm">
        <div className="lab">🕰 Demo view</div>
        <div className="strip">
          {MONTHS.map((m, i) => (
            <div
              key={m}
              className={'mo' + (i + 1 === month ? ' on' : '') + (i + 1 === 6 ? ' real' : '')}
              onClick={() => setMonth(i + 1)}
            >{m}</div>
          ))}
        </div>
        <div className={'status ' + (isLive(month) ? 'live' : 'proj')}>
          {isLive(month) ? '● LIVE DATA — June' : '📅 PROJECTED — modeled'}
        </div>
      </div>

      <div className="grid">
        <nav>
          {NAV.map(([id, t, d], idx) => (
            <div
              key={id}
              className={'nav-item' + (stage === id ? ' active' : '')}
              onClick={() => setStage(id)}
            >
              <div className="n">{idx + 1}</div>
              <div><div className="t">{t}</div><div className="d">{d}</div></div>
            </div>
          ))}
        </nav>
        <main>
          {stage === 'gaps'  && <GapBoard data={data} month={month} />}
          {stage === 'worth' && <Opportunities data={data} month={month} />}
          {stage === 'radar' && <Radar data={data} month={month} />}
          {stage === 'why'   && <Sources data={data} onToast={showToast} />}
          {stage === 'move'  && <Craft data={data} onToast={showToast} />}
        </main>
      </div>

      <div className={'toast' + (toastOn ? ' on' : '')}>{toast}</div>
    </div>
  )
}

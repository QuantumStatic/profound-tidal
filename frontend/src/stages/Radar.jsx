import { isLive } from '../months'

const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

export default function Radar({ data, month }) {
  const { live, forecast } = data.radar
  const measured = live.basis === 'measured'

  return (
    <section>
      <h2 className="title">Catch the wave before it peaks</h2>
      <p className="sub">The headline signal for the selected month, plus the seasonal forecast.</p>

      <div className={'radar-card ' + (measured ? 'live' : 'proj')}>
        <div className="ico">{measured ? '🚀' : '📅'}</div>
        <div>
          <h3>{measured ? 'Live measured data — June' : `Projected — ${MONTH_NAMES[month - 1]} model`}</h3>
          <p>
            {measured
              ? `Timing factor ${live.factor.toFixed(2)}× based on your last 22 days of real data.`
              : `Seasonal model gives ${live.factor.toFixed(2)}× timing weight for ${MONTH_NAMES[month - 1]}.`}
          </p>
          <span className="lead">{measured ? 'Detected in your data' : 'Modeled forecast'}</span>
        </div>
      </div>

      <div className="card" style={{marginTop: 12}}>
        <div style={{color:'var(--mut)',fontSize:12,marginBottom:8}}>
          Seasonal movers — {MONTH_NAMES[month - 1]}
        </div>
        {forecast.length === 0
          ? <p style={{color:'var(--mut)',fontSize:13}}>No strong seasonal signals this month.</p>
          : forecast.map((f, i) => (
              <div className="pred" key={i}>
                <span className={'ar ' + f.direction}>{f.direction === 'up' ? '↑' : '↓'}</span>
                <div>
                  <div className="pt">{f.topic}</div>
                  <div className="pc">{f.cause} ({f.multiplier}×)</div>
                </div>
              </div>
            ))}
      </div>
      <p className="hint">June is measured from live data. Other months are modeled forecasts — labeled, never mixed.</p>
    </section>
  )
}

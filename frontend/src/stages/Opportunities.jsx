import { isLive } from '../months'

export default function Opportunities({ data, month }) {
  const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  return (
    <section>
      <h2 className="title">Fix these first — for {MONTH_NAMES[month - 1]}</h2>
      <p className="sub">
        Search demand × how invisible you are × $/click × <b>timing</b>.
        Change the month above and the priority re-orders.
      </p>
      {!isLive(month) && (
        <div className="ribbon">
          📅 Projected view — ranking re-weighted by {MONTH_NAMES[month - 1]} seasonal timing.
          Measured visibility (Step 1) stays real.
        </div>
      )}
      {data.opportunities.map((o, i) => (
        <div className={'opp' + (i === 0 ? ' top' : '')} key={o.topic}>
          <div className="rank">{i + 1}</div>
          <div>
            <div className="h">{o.topic}</div>
            <div className="why">{o.why}</div>
          </div>
          <div className="m">
            ${Math.round(o.annual_value).toLocaleString()}
            <small>/YR</small>
          </div>
        </div>
      ))}
      <p className="hint">
        "At stake" = recoverable clicks × cost-per-click × 12 months.
        Timing is an explicit, inspectable factor.
      </p>
    </section>
  )
}

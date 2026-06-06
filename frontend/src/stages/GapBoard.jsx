export default function GapBoard({ data }) {
  const board = data.gap_board
  // hero = first row (lowest you = biggest gap)
  const heroTopic = board[0]?.topic

  return (
    <section>
      <h2 className="title">In your biggest market, AI barely mentions you</h2>
      <p className="sub">
        How often each AI engine recommends <b>you</b> vs the <b>leading rival</b>.
        These bars are <b>measured</b> — they don't change with the demo month.
      </p>
      {board.map((row, i) => {
        const youPct = Math.round(row.you * 100)
        const themPct = Math.round(row.leader_rate * 100)
        const isLeading = row.you > row.leader_rate
        return (
          <div className={'gap' + (i === 0 ? ' sel' : '')} key={row.topic}>
            <div className="name">
              {row.topic}
              <small>"{row.topic.toLowerCase()} AI"</small>
              {row.topic === heroTopic && <span className="urgent">BIGGEST GAP</span>}
            </div>
            <div className="bars">
              <div className="bar">
                <span className="who">You</span>
                <div className="track"><div className={'fill ' + (isLeading ? 'them' : 'you')} style={{width: `${Math.min(youPct, 100)}%`}} /></div>
                <span className="pct" style={{color: isLeading ? 'var(--money)' : 'var(--red)'}}>{youPct}%</span>
              </div>
              <div className="bar">
                <span className="who">{row.leader || '—'}</span>
                <div className="track"><div className="fill them" style={{width: `${Math.min(themPct, 100)}%`}} /></div>
                <span className="pct">{themPct}%</span>
              </div>
              {row.has_sentiment && <div className="flag">⚠ Sentiment data available for this topic</div>}
            </div>
            <div className="worth">
              <div className="m" style={{color: isLeading ? 'var(--mut)' : 'var(--money)'}}>
                {isLeading ? 'You lead' : `${100 - youPct}% invisible`}
              </div>
              <div className="l">{isLeading ? '' : 'to AI engines'}</div>
            </div>
          </div>
        )
      })}
      <p className="hint">
        Ghost mentions: {data.ghost.ghost_count} records where you appear but aren't credited.
        True SOAA: {(data.ghost.true_soaa * 100).toFixed(1)}% vs reported {(data.ghost.reported_soaa * 100).toFixed(1)}%.
      </p>
    </section>
  )
}

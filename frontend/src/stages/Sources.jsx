const LABEL = {
  reddit: '⚡ Reply with Profound',
  outreach: '⚡ Pitch with Profound',
  optimize: '⚡ Optimize with Profound',
}
const ICON = { reddit: '👽', outreach: '📰', optimize: '🏢' }

function sourceIcon(action) {
  if (!action) return '🔗'
  return ICON[action.kind] || '🔗'
}

export default function Sources({ data, onToast }) {
  return (
    <section>
      <h2 className="title">Why AI ignores you in {data.hero.topic}</h2>
      <p className="sub">
        AI learns from these third-party sources. A button appears only when a Profound agent fits.
      </p>
      {data.hero.sources.map((s, i) => {
        let hostname = s.url
        try { hostname = new URL(s.url).hostname } catch (_) {}
        return (
          <div className="src" key={i}>
            <div className="ic">{sourceIcon(s.action)}</div>
            <div>
              <div className="nm">{hostname}</div>
              <div className="meta">cited in {s.count} answers</div>
            </div>
            <div className="sp" />
            {s.action
              ? <button className="runbtn"
                  onClick={() => onToast('Hands this to Profound — you review & send.')}>
                  {LABEL[s.action.kind]}
                </button>
              : <span className="noact">manual — no Profound agent for this source</span>}
          </div>
        )
      })}
      <p className="hint">Tidal only offers a button when a real Profound agent fits the source.</p>
    </section>
  )
}

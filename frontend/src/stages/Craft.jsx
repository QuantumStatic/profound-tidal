export default function Craft({ data, onToast }) {
  const { dna, brief } = data.hero.content
  return (
    <section>
      <h2 className="title">What to publish to win {data.hero.topic}</h2>
      <p className="sub">We don't write it for you — we hand you the recipe the AI rewards, and the brief.</p>

      <div className="recipe">
        <div className="ing"><div className="k">Format</div><div className="v">{dna.format}</div></div>
        <div className="ing"><div className="k">Freshness</div><div className="v">{dna.freshness}</div></div>
        <div className="ing"><div className="k">Voice</div><div className="v">{dna.voice}</div></div>
        <div className="ing">
          <div className="k">Must mention</div>
          <div className="v">{dna.must_mention.length > 0 ? dna.must_mention.join(', ') : '—'}</div>
        </div>
      </div>

      <div className="brief">{brief}</div>

      <div className="ctaRow">
        <button className="runbtn"
          style={{background:'linear-gradient(135deg,#818cf8,#6366f1)',color:'#fff'}}
          onClick={() => onToast('Optional: Profound can expand this brief into a full draft.')}>
          ⚡ Draft full article with Profound
        </button>
      </div>
      <p className="hint">Target sources: {dna.target_sources.slice(0, 3).join(', ')}</p>
    </section>
  )
}

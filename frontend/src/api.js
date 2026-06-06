export async function fetchRun(month) {
  const r = await fetch(`/api/run?month=${month}`)
  return r.json()
}

// Stream progress beats; onProgress(event) per beat, resolves with final result.
export function streamRun(month, onProgress) {
  return new Promise((resolve) => {
    const es = new EventSource(`/api/stream?month=${month}`)
    es.addEventListener('progress', (e) => onProgress(JSON.parse(e.data)))
    es.addEventListener('done', (e) => { es.close(); resolve(JSON.parse(e.data).result) })
    es.onerror = () => { es.close(); resolve(null) }
  })
}

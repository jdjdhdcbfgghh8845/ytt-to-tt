import { useState, useEffect } from 'react'
import './App.css'
import config from './config.json';

const translations = {
  en: {
    title: 'YT ➜ ',
    subtitle: 'TikTok',
    placeholder: 'Paste YouTube Short URL...',
    start: 'Start Automation',
    processing: 'Processing...',
    status: 'Status',
  },
  ru: {
    title: 'YT ➜ ',
    subtitle: 'ТикТок',
    placeholder: 'Вставьте ссылку на Shorts...',
    start: 'Запустить',
    processing: 'В работе...',
    status: 'Статус',
  }
};

const t = translations[config.lang as 'en' | 'ru'];

function App() {
  const [url, setUrl] = useState('')
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleStart = async () => {
    if (!url) return
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      const data = await res.json()
      setJobId(data.job_id)
    } catch (err) {
      alert('Backend not running? Make sure FastAPI is started.')
    }
    setLoading(false)
  }

  useEffect(() => {
    let interval: any
    if (jobId && status?.status !== 'completed' && status?.status !== 'failed') {
      interval = setInterval(async () => {
        const res = await fetch(`http://localhost:8000/status/${jobId}`)
        const data = await res.json()
        setStatus(data)
      }, 2000)
    }
    return () => clearInterval(interval)
  }, [jobId, status])

  return (
    <>
      <div className="background-glow">
        <div className="glow-orb orb-1"></div>
        <div className="glow-orb orb-2"></div>
      </div>
      <div className="container">
        <h1>{t.title}<span>{t.subtitle}</span></h1>
        <div className="input-group">
          <input
            type="text"
            placeholder={t.placeholder}
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
        <button
          onClick={handleStart}
          disabled={loading || (jobId !== null && status?.status !== 'completed' && status?.status !== 'failed')}
        >
          {loading ? <div className="loader"></div> : (jobId !== null && status?.status !== 'completed' && status?.status !== 'failed' ? t.processing : t.start)}
        </button>

        {status && (
          <div className="status-card">
            <div className="status-header">
              <span className="status-label">{status.status}</span>
              <span className="status-progress-text">{status.progress}%</span>
            </div>
            <p className="progress-message">{status.message}</p>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${status.progress}%` }}></div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

export default App

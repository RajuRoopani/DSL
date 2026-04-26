import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client.js'
import Step1Skill from '../components/wizard/Step1Skill.jsx'
import Step2Level from '../components/wizard/Step2Level.jsx'
import Step3Time from '../components/wizard/Step3Time.jsx'
import Step4Goals from '../components/wizard/Step4Goals.jsx'
import Button from '../components/ui/Button.jsx'

const STEPS = ['Choose Skill', 'Your Level', 'Time Available', 'Your Goal']

export default function Generator() {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [skills, setSkills] = useState([])
  const [formData, setFormData] = useState({
    skill: null,
    level: null,
    hours_per_week: null,
    goal: null,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.get('/skills/').then((res) => setSkills(res.data.results ?? res.data))
  }, [])

  const canAdvance = () => {
    if (step === 1) return !!formData.skill
    if (step === 2) return !!formData.level
    if (step === 3) return !!formData.hours_per_week
    if (step === 4) return !!formData.goal
    return false
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.post('/roadmaps/generate', {
        skill_id: formData.skill.id,
        level: formData.level,
        hours_per_week: formData.hours_per_week,
        goal: formData.goal,
      })
      navigate(`/roadmap/${res.data.id}`)
    } catch (err) {
      setError(err.response?.data?.error ?? 'Something went wrong. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div>
      <nav className="navbar">
        <span className="navbar-brand">✨ SmartLearning</span>
        <a href="http://localhost:8080/dashboard/">Dashboard</a>
      </nav>

      <div className="page" style={{ maxWidth: 640 }}>
        {/* Step indicator */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 32 }}>
          {STEPS.map((label, i) => (
            <div key={i} style={{ flex: 1, textAlign: 'center' }}>
              <div style={{
                width: 32, height: 32, borderRadius: '50%', margin: '0 auto 4px',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 14, fontWeight: 600,
                background: i + 1 < step ? 'var(--success)' : i + 1 === step ? 'var(--primary)' : 'var(--border)',
                color: i + 1 <= step ? '#fff' : 'var(--text-muted)',
              }}>
                {i + 1 < step ? '✓' : i + 1}
              </div>
              <div style={{ fontSize: 11, color: i + 1 === step ? 'var(--primary)' : 'var(--text-muted)' }}>
                {label}
              </div>
            </div>
          ))}
        </div>

        <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 8 }}>
          {step === 1 && 'What do you want to learn?'}
          {step === 2 && "What's your current level?"}
          {step === 3 && 'How much time can you dedicate?'}
          {step === 4 && "What's your main goal?"}
        </h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: 28, fontSize: 14 }}>
          Step {step} of {STEPS.length}
        </p>

        {step === 1 && <Step1Skill skills={skills} selected={formData.skill} onSelect={(s) => setFormData({ ...formData, skill: s })} />}
        {step === 2 && <Step2Level selected={formData.level} onSelect={(l) => setFormData({ ...formData, level: l })} />}
        {step === 3 && <Step3Time selected={formData.hours_per_week} onSelect={(h) => setFormData({ ...formData, hours_per_week: h })} />}
        {step === 4 && (
          <Step4Goals
            selected={formData.goal}
            onSelect={(g) => setFormData({ ...formData, goal: g })}
            existingRoadmap={null}
          />
        )}

        {error && <div className="alert alert-error" style={{ marginTop: 20 }}>{error}</div>}

        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 32, gap: 12 }}>
          {step > 1
            ? <Button variant="ghost" onClick={() => setStep(step - 1)}>← Back</Button>
            : <div />
          }
          {step < 4
            ? <Button onClick={() => setStep(step + 1)} disabled={!canAdvance()}>Next →</Button>
            : <Button onClick={handleSubmit} disabled={!canAdvance() || loading}>
                {loading ? 'Generating…' : '🗺 Generate My Roadmap'}
              </Button>
          }
        </div>
      </div>
    </div>
  )
}

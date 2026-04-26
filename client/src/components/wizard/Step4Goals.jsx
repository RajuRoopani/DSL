const GOALS = [
  { value: 'interview_prep', label: 'Interview Prep', desc: 'Practice problems & LeetCode patterns' },
  { value: 'portfolio', label: 'Portfolio Project', desc: 'Build something to show employers' },
  { value: 'general', label: 'General Learning', desc: 'Broad understanding, no rush' },
]

export default function Step4Goals({ selected, onSelect, existingRoadmap }) {
  return (
    <div>
      {existingRoadmap && (
        <div className="alert alert-info" style={{ marginBottom: 20 }}>
          ⚠️ You already have a <strong>{existingRoadmap}</strong> roadmap. Generating a new one will reset your progress.
        </div>
      )}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {GOALS.map((goal) => (
          <label
            key={goal.value}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 14,
              padding: '16px 20px',
              border: `2px solid ${selected === goal.value ? 'var(--primary)' : 'var(--border)'}`,
              borderRadius: 'var(--radius)',
              background: selected === goal.value ? 'var(--primary-light)' : 'var(--surface)',
              cursor: 'pointer',
              transition: 'all .15s',
            }}
            onClick={() => onSelect(goal.value)}
          >
            <input
              type="radio"
              name="goal"
              value={goal.value}
              checked={selected === goal.value}
              onChange={() => onSelect(goal.value)}
              style={{ accentColor: 'var(--primary)', width: 18, height: 18 }}
            />
            <div>
              <div style={{ fontWeight: 600 }}>{goal.label}</div>
              <div style={{ color: 'var(--text-muted)', fontSize: 13 }}>{goal.desc}</div>
            </div>
          </label>
        ))}
      </div>
    </div>
  )
}

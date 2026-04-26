const OPTIONS = [
  { value: 2, label: '2 hrs/wk', desc: 'Light pace' },
  { value: 5, label: '5 hrs/wk', desc: 'Steady' },
  { value: 10, label: '10 hrs/wk', desc: 'Dedicated' },
  { value: 20, label: '20 hrs/wk', desc: 'Intensive' },
]

export default function Step3Time({ selected, onSelect }) {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12 }}>
      {OPTIONS.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onSelect(opt.value)}
          style={{
            padding: '14px 28px',
            borderRadius: 'var(--radius)',
            border: `2px solid ${selected === opt.value ? 'var(--primary)' : 'var(--border)'}`,
            background: selected === opt.value ? 'var(--primary-light)' : 'var(--surface)',
            color: selected === opt.value ? 'var(--primary-dark)' : 'var(--text)',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all .15s',
          }}
        >
          <div style={{ fontSize: 18 }}>{opt.label}</div>
          <div style={{ fontSize: 12, fontWeight: 400, color: 'var(--text-muted)', marginTop: 2 }}>{opt.desc}</div>
        </button>
      ))}
    </div>
  )
}

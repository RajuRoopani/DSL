import Card from '../ui/Card.jsx'

const LEVELS = [
  { value: 'beginner', label: 'Beginner', emoji: '🌱', desc: 'Just starting out' },
  { value: 'intermediate', label: 'Intermediate', emoji: '🚀', desc: 'Know the basics' },
  { value: 'advanced', label: 'Advanced', emoji: '⚡', desc: 'Ready for deep dives' },
]

export default function Step2Level({ selected, onSelect }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16 }}>
      {LEVELS.map((level) => (
        <Card
          key={level.value}
          selected={selected === level.value}
          onClick={() => onSelect(level.value)}
        >
          <div style={{ fontSize: 32, marginBottom: 8 }}>{level.emoji}</div>
          <div style={{ fontWeight: 600 }}>{level.label}</div>
          <div style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4 }}>{level.desc}</div>
        </Card>
      ))}
    </div>
  )
}

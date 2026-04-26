import Card from '../ui/Card.jsx'

export default function Step1Skill({ skills, selected, onSelect }) {
  if (skills.length === 0) {
    return <p style={{ color: 'var(--text-muted)', textAlign: 'center' }}>Loading skills…</p>
  }
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
      {skills.map((skill) => (
        <Card
          key={skill.id}
          selected={selected?.id === skill.id}
          onClick={() => onSelect(skill)}
        >
          <div style={{ fontSize: 36, marginBottom: 8 }}>{skill.icon_emoji || '📚'}</div>
          <div style={{ fontWeight: 600, fontSize: 16 }}>{skill.name}</div>
          {skill.description && (
            <div style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4 }}>
              {skill.description.slice(0, 80)}{skill.description.length > 80 ? '…' : ''}
            </div>
          )}
        </Card>
      ))}
    </div>
  )
}

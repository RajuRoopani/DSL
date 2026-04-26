const TYPE_EMOJI = {
  video: '📹', article: '📄', tutorial: '🛠', documentation: '📖',
  book: '📚', course: '🎓', interactive: '🎮', exercise: '💪',
}

export default function TaskDrawer({ week, onToggle }) {
  if (!week) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
        ← Select a week to see tasks
      </div>
    )
  }

  const totalHours = week.topics.reduce((sum, t) => sum + t.estimated_hours, 0)

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700 }}>Week {week.week}: {week.title}</h2>
        <div style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4 }}>
          {week.topics.length} topic{week.topics.length !== 1 ? 's' : ''} · ~{totalHours} hrs
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        {week.topics.map((topic) => (
          <div key={topic.id} style={{
            padding: '16px',
            border: `1px solid ${topic.completed ? 'var(--success)' : 'var(--border)'}`,
            borderRadius: 'var(--radius)',
            background: topic.completed ? 'var(--success-light)' : 'var(--surface)',
          }}>
            <label style={{ display: 'flex', alignItems: 'flex-start', gap: 12, cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={topic.completed}
                onChange={() => onToggle(topic.id, !topic.completed)}
                style={{ marginTop: 3, width: 17, height: 17, accentColor: 'var(--success)', cursor: 'pointer' }}
              />
              <div style={{ flex: 1 }}>
                <div style={{
                  fontWeight: 600,
                  textDecoration: topic.completed ? 'line-through' : 'none',
                  color: topic.completed ? 'var(--text-muted)' : 'var(--text)',
                }}>
                  {topic.title}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: 12, marginTop: 2 }}>
                  ⏱ {topic.estimated_hours} hrs
                </div>
              </div>
            </label>

            {topic.resources.length > 0 && (
              <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
                <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '.05em' }}>
                  Resources
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  {topic.resources.map((res) => (
                    <a
                      key={res.id}
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 6, color: 'var(--primary)' }}
                    >
                      <span>{TYPE_EMOJI[res.resource_type] ?? '🔗'}</span>
                      {res.title}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

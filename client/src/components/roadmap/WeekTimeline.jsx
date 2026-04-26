export default function WeekTimeline({ weeks, selectedWeek, onSelect }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      {weeks.map((week) => {
        const isSelected = selectedWeek?.week === week.week
        const isDone = week.topics.every((t) => t.completed)
        const isStarted = week.topics.some((t) => t.completed)

        return (
          <div
            key={week.week}
            onClick={() => onSelect(week)}
            style={{
              padding: '12px 16px',
              borderRadius: 'var(--radius)',
              border: `2px solid ${isDone ? 'var(--success)' : isSelected ? 'var(--primary)' : 'var(--border)'}`,
              background: isDone ? 'var(--success-light)' : isSelected ? 'var(--primary-light)' : 'var(--surface)',
              cursor: 'pointer',
              transition: 'all .15s',
              opacity: !isDone && !isSelected && !isStarted && week.week > 1 ? 0.55 : 1,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{
                fontSize: 13, fontWeight: 600,
                color: isDone ? '#065f46' : isSelected ? 'var(--primary-dark)' : 'var(--text)',
              }}>
                Week {week.week}
              </span>
              {isDone && <span style={{ fontSize: 14 }}>✓</span>}
              {isSelected && !isDone && (
                <span style={{ fontSize: 11, color: 'var(--primary)', fontWeight: 600 }}>current</span>
              )}
            </div>
            <div style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {week.title}
            </div>
          </div>
        )
      })}
    </div>
  )
}

import Badge from '../ui/Badge.jsx'

export default function RoadmapHeader({ roadmap }) {
  const { skill, level, hours_per_week, total_weeks, percent_complete } = roadmap
  return (
    <div style={{ marginBottom: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8, flexWrap: 'wrap' }}>
        <h1 style={{ fontSize: 26, fontWeight: 700 }}>
          {skill.icon_emoji} {skill.name}
        </h1>
        <Badge color={level === 'beginner' ? 'success' : level === 'intermediate' ? 'primary' : 'warning'}>
          {level.charAt(0).toUpperCase() + level.slice(1)}
        </Badge>
        {percent_complete === 100 && <Badge color="success">🎉 Completed!</Badge>}
      </div>
      <div style={{ color: 'var(--text-muted)', fontSize: 14, display: 'flex', gap: 20 }}>
        <span>📅 {total_weeks} weeks</span>
        <span>⏱ {hours_per_week} hrs/week</span>
        <a href="/generate" style={{ marginLeft: 'auto' }}>← New roadmap</a>
      </div>
    </div>
  )
}

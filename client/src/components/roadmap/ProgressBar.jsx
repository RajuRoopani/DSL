export default function ProgressBar({ percent }) {
  return (
    <div style={{ marginBottom: 4 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: 13 }}>
        <span style={{ color: 'var(--text-muted)' }}>Overall progress</span>
        <span style={{ fontWeight: 600, color: percent === 100 ? 'var(--success)' : 'var(--primary)' }}>
          {percent}%
        </span>
      </div>
      <div style={{ height: 10, background: 'var(--border)', borderRadius: 8, overflow: 'hidden' }}>
        <div style={{
          height: '100%',
          width: `${percent}%`,
          background: percent === 100 ? 'var(--success)' : 'var(--primary)',
          borderRadius: 8,
          transition: 'width .4s ease',
        }} />
      </div>
    </div>
  )
}

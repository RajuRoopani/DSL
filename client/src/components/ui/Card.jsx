export default function Card({ children, selected, onClick, style }) {
  return (
    <div
      data-selected={selected ? 'true' : 'false'}
      onClick={onClick}
      style={{
        background: selected ? 'var(--primary-light)' : 'var(--surface)',
        border: `2px solid ${selected ? 'var(--primary)' : 'var(--border)'}`,
        borderRadius: 'var(--radius)',
        padding: '20px',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'border-color .15s, background .15s, box-shadow .15s',
        boxShadow: selected ? '0 0 0 3px rgba(99,102,241,.15)' : 'var(--shadow)',
        ...style,
      }}
    >
      {children}
    </div>
  )
}

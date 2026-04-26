const COLORS = {
  primary: { bg: 'var(--primary-light)', color: 'var(--primary-dark)' },
  success: { bg: 'var(--success-light)', color: '#065f46' },
  muted:   { bg: '#f3f4f6', color: 'var(--text-muted)' },
  warning: { bg: '#fffbeb', color: '#92400e' },
}

export default function Badge({ children, color = 'primary' }) {
  const { bg, color: textColor } = COLORS[color] ?? COLORS.primary
  return (
    <span style={{
      background: bg,
      color: textColor,
      padding: '3px 10px',
      borderRadius: '20px',
      fontSize: '12px',
      fontWeight: 600,
      display: 'inline-block',
    }}>
      {children}
    </span>
  )
}

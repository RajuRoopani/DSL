const STYLES = {
  primary: { background: 'var(--primary)', color: '#fff', border: 'none' },
  secondary: { background: 'transparent', color: 'var(--primary)', border: '2px solid var(--primary)' },
  ghost: { background: 'transparent', color: 'var(--text-muted)', border: '1px solid var(--border)' },
}

export default function Button({ children, variant = 'primary', onClick, disabled, style, fullWidth }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...STYLES[variant],
        padding: '10px 24px',
        borderRadius: 'var(--radius)',
        fontWeight: 600,
        fontSize: '15px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1,
        transition: 'opacity .15s, transform .1s',
        width: fullWidth ? '100%' : undefined,
        ...style,
      }}
    >
      {children}
    </button>
  )
}

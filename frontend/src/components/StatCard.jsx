import React from 'react';

export default function StatCard({
  title,
  value,
  subtitle = null,
  badge = null,
  badgeVariant = 'primary',
  icon = null,
  footerNote = null,
  onClick = null
}) {
  return (
    <div
      className="card"
      onClick={onClick}
      style={{
        cursor: onClick ? 'pointer' : 'default',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        position: 'relative'
      }}
    >
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div style={{ fontSize: '1.4rem' }}>{icon}</div>
          {badge && (
            <span className={`badge badge-${badgeVariant}`}>
              {badge}
            </span>
          )}
        </div>
        <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '6px' }}>
          {title}
        </h4>
        <div style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.2, marginBottom: '6px' }}>
          {value}
        </div>
        {subtitle && (
          <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
            {subtitle}
          </p>
        )}
      </div>

      {footerNote && (
        <div style={{
          marginTop: '14px',
          paddingTop: '10px',
          borderTop: '1px solid var(--border-subtle)',
          fontSize: '0.78rem',
          color: 'var(--text-muted)'
        }}>
          {footerNote}
        </div>
      )}
    </div>
  );
}

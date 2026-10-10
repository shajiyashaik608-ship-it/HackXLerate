import React from 'react';

export default function PageHeader({
  title,
  subtitle,
  actions = null,
  badge = null
}) {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      flexWrap: 'wrap',
      gap: '16px',
      marginBottom: '26px'
    }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
          <h1 style={{ fontSize: '1.85rem', color: 'var(--text-primary)' }}>{title}</h1>
          {badge && <span className="badge badge-primary">{badge}</span>}
        </div>
        {subtitle && (
          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', maxWidth: '780px', lineHeight: '1.6' }}>
            {subtitle}
          </p>
        )}
      </div>

      {actions && (
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {actions}
        </div>
      )}
    </div>
  );
}

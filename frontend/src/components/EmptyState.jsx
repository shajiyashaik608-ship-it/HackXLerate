import React from 'react';

export default function EmptyState({
  icon = '📋',
  title = 'No records found',
  description = 'You have not added any information yet.',
  actionLabel = null,
  onAction = null
}) {
  return (
    <div style={{
      textAlign: 'center',
      padding: '40px 20px',
      background: 'var(--bg-card)',
      borderRadius: 'var(--radius-lg)',
      border: '1px dashed var(--border-subtle)',
      maxWidth: '480px',
      margin: '0 auto'
    }}>
      <div style={{ fontSize: '2.5rem', marginBottom: '14px' }}>{icon}</div>
      <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', marginBottom: '8px' }}>
        {title}
      </h3>
      <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: onAction ? '20px' : '0', lineHeight: '1.5' }}>
        {description}
      </p>
      {actionLabel && onAction && (
        <button onClick={onAction} className="btn btn-primary btn-sm">
          {actionLabel}
        </button>
      )}
    </div>
  );
}

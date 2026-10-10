import React from 'react';

export default function ErrorState({
  title = 'Unable to Load Records',
  message = 'An unexpected issue occurred while retrieving your local records.',
  onRetry = null,
  minHeight = '220px'
}) {
  return (
    <div
      role="alert"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight,
        padding: '30px',
        textAlign: 'center',
        background: 'var(--coral-50)',
        border: '1px solid var(--coral-500)',
        borderRadius: 'var(--radius-lg)',
        gap: '12px'
      }}
    >
      <div style={{ fontSize: '2.2rem' }}>⚠️</div>
      <h3 style={{ fontSize: '1.1rem', color: 'var(--coral-700)', fontWeight: 700 }}>
        {title}
      </h3>
      <p style={{ maxWidth: '440px', fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="btn btn-outline btn-sm"
          style={{ borderColor: 'var(--coral-500)', color: 'var(--coral-700)', marginTop: '8px' }}
        >
          🔄 Try Again
        </button>
      )}
    </div>
  );
}

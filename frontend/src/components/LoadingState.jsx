import React from 'react';

export default function LoadingState({ message = 'Loading health records...', minHeight = '200px' }) {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight,
        gap: '14px',
        padding: '30px',
        color: 'var(--text-muted)'
      }}
    >
      <div
        className="spinner"
        style={{
          width: '36px',
          height: '36px',
          border: '3px solid var(--border-subtle)',
          borderTopColor: 'var(--primary-700)',
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite'
        }}
      />
      <div style={{ fontSize: '0.9rem', fontWeight: 500 }}>{message}</div>
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

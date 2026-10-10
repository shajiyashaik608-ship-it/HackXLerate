import React from 'react';

export default function ProgressBar({
  progress = 0, // 0 to 100
  color = 'var(--primary-600)',
  height = '8px',
  label = null
}) {
  const clamped = Math.min(100, Math.max(0, progress));

  return (
    <div style={{ width: '100%' }}>
      {label && (
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '6px', color: 'var(--text-secondary)' }}>
          <span>{label}</span>
          <span style={{ fontWeight: 600 }}>{clamped}%</span>
        </div>
      )}
      <div style={{
        width: '100%',
        height,
        backgroundColor: 'var(--border-subtle)',
        borderRadius: '999px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${clamped}%`,
          height: '100%',
          backgroundColor: color,
          borderRadius: '999px',
          transition: 'width 0.4s ease'
        }} />
      </div>
    </div>
  );
}

import React, { useEffect } from 'react';

export default function Toast({
  message,
  type = 'info', // 'success', 'error', 'info', 'warning'
  isOpen,
  onClose,
  duration = 3200
}) {
  useEffect(() => {
    if (isOpen && duration > 0) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [isOpen, duration, onClose]);

  if (!isOpen || !message) return null;

  const bgMap = {
    success: 'var(--accent-green-light)',
    error: 'var(--coral-50)',
    warning: 'var(--accent-yellow-light)',
    info: 'var(--primary-100)'
  };

  const textMap = {
    success: '#166534',
    error: 'var(--coral-700)',
    warning: '#854d0e',
    info: 'var(--primary-900)'
  };

  const borderMap = {
    success: 'var(--accent-green)',
    error: 'var(--coral-500)',
    warning: 'var(--accent-yellow)',
    info: 'var(--primary-500)'
  };

  const iconMap = {
    success: '✅',
    error: '⚠️',
    warning: '⚡',
    info: 'ℹ️'
  };

  return (
    <div
      role="alert"
      aria-live="assertive"
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 9999,
        background: bgMap[type] || bgMap.info,
        color: textMap[type] || textMap.info,
        border: `1px solid ${borderMap[type] || borderMap.info}`,
        borderRadius: 'var(--radius-md)',
        padding: '12px 18px',
        boxShadow: 'var(--shadow-modal)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        maxWidth: '420px',
        fontSize: '0.86rem',
        fontWeight: 500,
        animation: 'slideUp 0.25s ease'
      }}
    >
      <span style={{ fontSize: '1.1rem' }}>{iconMap[type]}</span>
      <span style={{ flex: 1 }}>{message}</span>
      <button
        onClick={onClose}
        style={{
          color: textMap[type],
          background: 'none',
          border: 'none',
          fontSize: '1rem',
          cursor: 'pointer',
          padding: '0 4px',
          opacity: 0.7
        }}
        aria-label="Dismiss message"
      >
        ✕
      </button>
      <style>{`
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(12px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}

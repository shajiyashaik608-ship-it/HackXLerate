import React from 'react';

export default function LanguageSelector({ currentLanguage, onSelectLanguage }) {
  return (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      background: 'var(--bg-card)',
      padding: '4px 6px',
      borderRadius: 'var(--radius-full)',
      border: '1px solid var(--border-subtle)'
    }}>
      <button
        type="button"
        onClick={() => onSelectLanguage('en')}
        style={{
          padding: '4px 14px',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.8rem',
          fontWeight: 600,
          background: currentLanguage === 'en' ? 'var(--primary-700)' : 'transparent',
          color: currentLanguage === 'en' ? '#ffffff' : 'var(--text-muted)',
          cursor: 'pointer'
        }}
      >
        English
      </button>
      <button
        type="button"
        onClick={() => onSelectLanguage('te')}
        style={{
          padding: '4px 14px',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.8rem',
          fontWeight: 600,
          background: currentLanguage === 'te' ? 'var(--coral-600)' : 'transparent',
          color: currentLanguage === 'te' ? '#ffffff' : 'var(--text-muted)',
          cursor: 'pointer'
        }}
      >
        తెలుగు (Telugu)
      </button>
    </div>
  );
}

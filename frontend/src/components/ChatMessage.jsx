import React from 'react';

export default function ChatMessage({
  message,
  onPlayAudio = null
}) {
  const isUser = message.sender === 'user';

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: isUser ? 'flex-end' : 'flex-start',
      marginBottom: '16px'
    }}>
      <div style={{
        display: 'flex',
        gap: '10px',
        maxWidth: '82%',
        flexDirection: isUser ? 'row-reverse' : 'row'
      }}>
        {/* Avatar */}
        <div style={{
          width: '34px',
          height: '34px',
          borderRadius: '50%',
          background: isUser ? 'var(--primary-700)' : 'var(--lavender-100)',
          color: isUser ? '#ffffff' : 'var(--lavender-700)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 700,
          fontSize: '0.85rem',
          flexShrink: 0
        }}>
          {isUser ? 'You' : '🌿'}
        </div>

        {/* Bubble */}
        <div style={{
          background: isUser ? 'var(--primary-700)' : 'var(--bg-card)',
          color: isUser ? '#ffffff' : 'var(--text-primary)',
          border: isUser ? 'none' : '1px solid var(--border-card)',
          borderRadius: '16px',
          borderTopRightRadius: isUser ? '4px' : '16px',
          borderTopLeftRadius: !isUser ? '4px' : '16px',
          padding: '14px 18px',
          boxShadow: 'var(--shadow-sm)'
        }}>
          {message.isUrgent && (
            <div style={{
              background: 'var(--coral-50)',
              color: 'var(--coral-700)',
              border: '1px solid var(--coral-500)',
              borderRadius: '8px',
              padding: '6px 10px',
              fontSize: '0.78rem',
              fontWeight: 700,
              marginBottom: '10px'
            }}>
              🚨 URGENT MEDICAL ADVISORY
            </div>
          )}

          <div style={{ whiteSpace: 'pre-line', fontSize: '0.92rem', lineHeight: '1.6' }}>
            {message.text}
          </div>

          {!isUser && (message.sources?.length > 0 || onPlayAudio) && (
            <div style={{
              marginTop: '12px',
              paddingTop: '8px',
              borderTop: '1px solid var(--border-subtle)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '8px'
            }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {message.sources?.map((src, i) => (
                  <span key={i} style={{ fontSize: '0.7rem', color: 'var(--text-muted)', background: 'var(--bg-subtle)', padding: '2px 8px', borderRadius: '4px' }}>
                    📚 {src}
                  </span>
                ))}
              </div>

              {onPlayAudio && (
                <button
                  onClick={() => onPlayAudio(message.text)}
                  style={{
                    background: 'var(--lavender-50)',
                    color: 'var(--lavender-700)',
                    padding: '4px 10px',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  🔊 Listen
                </button>
              )}
            </div>
          )}

          {message.disclaimer && !isUser && (
            <div style={{ fontSize: '0.72rem', color: 'var(--text-light)', marginTop: '8px', fontStyle: 'italic' }}>
              ⚠️ {message.disclaimer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

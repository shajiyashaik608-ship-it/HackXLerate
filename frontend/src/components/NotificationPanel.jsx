import React from 'react';

export default function NotificationPanel({
  notifications,
  onMarkAsRead,
  onClearAll,
  onClose
}) {
  return (
    <div style={{
      position: 'absolute',
      right: '20px',
      top: '72px',
      width: '360px',
      maxWidth: 'calc(100vw - 40px)',
      background: 'var(--bg-card)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-modal)',
      border: '1px solid var(--border-subtle)',
      zIndex: 100,
      overflow: 'hidden'
    }}>
      <div style={{
        padding: '14px 18px',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'var(--bg-subtle)'
      }}>
        <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-primary)' }}>
          Notifications ({notifications.filter(n => !n.read).length})
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={onClearAll}
            style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}
          >
            Clear All
          </button>
          <button
            onClick={onClose}
            style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}
          >
            ✕
          </button>
        </div>
      </div>

      <div style={{ maxHeight: '360px', overflowY: 'auto' }}>
        {notifications.length === 0 ? (
          <div style={{ padding: '30px 20px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            No new notifications
          </div>
        ) : (
          notifications.map((notif) => (
            <div
              key={notif.id}
              onClick={() => onMarkAsRead(notif.id)}
              style={{
                padding: '12px 18px',
                borderBottom: '1px solid var(--border-subtle)',
                background: notif.read ? 'transparent' : 'var(--primary-50)',
                cursor: 'pointer',
                display: 'flex',
                gap: '12px',
                alignItems: 'flex-start'
              }}
            >
              <div style={{ fontSize: '1.2rem' }}>{notif.icon || '🔔'}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.86rem', fontWeight: notif.read ? 500 : 700, color: 'var(--text-primary)' }}>
                  {notif.title}
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', lineHeight: 1.4 }}>
                  {notif.message}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-light)', marginTop: '4px' }}>
                  {notif.time}
                </div>
              </div>
              {!notif.read && (
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--primary-600)', marginTop: '4px' }} />
              )}
            </div>
          ))
        )}
      </div>

      <div style={{
        padding: '10px',
        textAlign: 'center',
        background: 'var(--bg-subtle)',
        fontSize: '0.72rem',
        color: 'var(--text-muted)',
        borderTop: '1px solid var(--border-subtle)'
      }}>
        Simulated notifications for hackathon demonstration
      </div>
    </div>
  );
}

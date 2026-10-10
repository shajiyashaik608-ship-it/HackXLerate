import React from 'react';
import { formatDisplayDate } from '../utils/dateUtils';

export default function ReminderCard({
  reminder,
  onToggleComplete,
  onDelete
}) {
  const getCategoryIcon = (cat) => {
    switch (cat) {
      case 'medication': return '💊';
      case 'appointment': return '🩺';
      case 'lab_test': return '🧪';
      case 'exercise': return '👟';
      default: return '⏰';
    }
  };

  return (
    <div className="card" style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '16px',
      padding: '16px 20px',
      opacity: reminder.completed ? 0.7 : 1,
      background: reminder.completed ? 'var(--bg-subtle)' : 'var(--bg-card)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flex: 1 }}>
        <input
          type="checkbox"
          checked={reminder.completed}
          onChange={() => onToggleComplete(reminder.id)}
          style={{ width: '18px', height: '18px', cursor: 'pointer', accentColor: 'var(--primary-600)' }}
        />

        <div style={{ fontSize: '1.5rem' }}>
          {getCategoryIcon(reminder.category)}
        </div>

        <div style={{ flex: 1 }}>
          <div style={{
            fontSize: '0.96rem',
            fontWeight: 600,
            color: 'var(--text-primary)',
            textDecoration: reminder.completed ? 'line-through' : 'none'
          }}>
            {reminder.title}
          </div>

          <div style={{ display: 'flex', gap: '10px', fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', flexWrap: 'wrap' }}>
            <span>🕒 {reminder.time}</span>
            <span>📅 {formatDisplayDate(reminder.date)}</span>
            <span className="badge badge-lavender" style={{ fontSize: '0.7rem', padding: '1px 6px' }}>
              {reminder.frequency}
            </span>
          </div>

          {reminder.notes && (
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
              {reminder.notes}
            </div>
          )}
        </div>
      </div>

      <button
        onClick={() => onDelete(reminder.id)}
        className="btn btn-ghost btn-sm"
        title="Delete reminder"
        style={{ color: 'var(--text-muted)' }}
      >
        🗑️
      </button>
    </div>
  );
}

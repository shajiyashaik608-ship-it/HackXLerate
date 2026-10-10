import React, { useState } from 'react';

export default function CycleCalendar({ cycleLogs, onSelectDate }) {
  const [currentMonth, setCurrentMonth] = useState(9); // 0-indexed: 9 = October
  const [currentYear, setCurrentYear] = useState(2026);

  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay(); // 0 is Sunday

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  // Helper to check day status
  const getDayStatus = (day) => {
    const formatted = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
    // Check if period day
    const isPeriod = cycleLogs.some((log) => {
      if (!log.startDate) return false;
      const start = new Date(log.startDate);
      const target = new Date(formatted);
      const diff = Math.floor((target - start) / (1000 * 60 * 60 * 24));
      return diff >= 0 && diff < (log.durationDays || 4);
    });

    // Check estimated window (e.g., Oct 28 - Nov 03)
    const isEstimate = currentMonth === 9 && day >= 28 && day <= 31;

    // Check today (Oct 09)
    const isToday = currentMonth === 9 && day === 9;

    return { isPeriod, isEstimate, isToday, dateStr: formatted };
  };

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      {/* Month Navigator */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
        <h3 style={{ fontSize: '1.2rem', color: 'var(--text-primary)' }}>
          {monthNames[currentMonth]} {currentYear}
        </h3>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setCurrentMonth((prev) => (prev > 0 ? prev - 1 : 11))}
            className="btn btn-outline btn-sm"
          >
            ← Prev
          </button>
          <button
            onClick={() => setCurrentMonth((prev) => (prev < 11 ? prev + 1 : 0))}
            className="btn btn-outline btn-sm"
          >
            Next →
          </button>
        </div>
      </div>

      {/* Weekday Labels */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        textAlign: 'center',
        fontWeight: 600,
        fontSize: '0.8rem',
        color: 'var(--text-muted)',
        marginBottom: '10px'
      }}>
        <div>Sun</div>
        <div>Mon</div>
        <div>Tue</div>
        <div>Wed</div>
        <div>Thu</div>
        <div>Fri</div>
        <div>Sat</div>
      </div>

      {/* Days Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gap: '6px'
      }}>
        {/* Empty slots before first day */}
        {Array.from({ length: firstDayIndex }).map((_, i) => (
          <div key={`empty-${i}`} style={{ height: '44px' }} />
        ))}

        {/* Days */}
        {Array.from({ length: daysInMonth }).map((_, i) => {
          const day = i + 1;
          const { isPeriod, isEstimate, isToday, dateStr } = getDayStatus(day);

          let bg = 'var(--bg-subtle)';
          let color = 'var(--text-primary)';
          let border = '1px solid var(--border-subtle)';

          if (isPeriod) {
            bg = 'var(--coral-100)';
            color = 'var(--coral-700)';
            border = '1px solid var(--coral-500)';
          } else if (isEstimate) {
            bg = 'var(--accent-yellow-light)';
            color = '#854d0e';
            border = '1px dashed var(--accent-yellow)';
          }

          if (isToday) {
            border = '2px solid var(--primary-700)';
          }

          return (
            <div
              key={day}
              onClick={() => onSelectDate && onSelectDate(dateStr)}
              style={{
                height: '46px',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: bg,
                color,
                border,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.88rem',
                fontWeight: isPeriod || isToday ? 700 : 500,
                cursor: 'pointer',
                position: 'relative'
              }}
              title={isPeriod ? 'Recorded Period Day' : isEstimate ? 'Estimated Next Window' : isToday ? 'Today' : dateStr}
            >
              <span>{day}</span>
              {isPeriod && <span style={{ fontSize: '0.6rem', lineHeight: 1 }}>🩸</span>}
              {isEstimate && <span style={{ fontSize: '0.6rem', lineHeight: 1 }}>⏱️</span>}
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '16px',
        marginTop: '20px',
        paddingTop: '14px',
        borderTop: '1px solid var(--border-subtle)',
        fontSize: '0.78rem',
        color: 'var(--text-muted)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '14px', height: '14px', borderRadius: '4px', background: 'var(--coral-100)', border: '1px solid var(--coral-500)' }} />
          <span>Recorded Period Day</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '14px', height: '14px', borderRadius: '4px', background: 'var(--accent-yellow-light)', border: '1px dashed var(--accent-yellow)' }} />
          <span>Estimated Window (±4-6 days)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{ width: '14px', height: '14px', borderRadius: '4px', border: '2px solid var(--primary-700)' }} />
          <span>Current Day</span>
        </div>
      </div>
    </div>
  );
}

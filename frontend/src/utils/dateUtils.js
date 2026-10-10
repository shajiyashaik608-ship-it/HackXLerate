export function formatDisplayDate(dateInput) {
  if (!dateInput) return 'Not recorded';
  const d = new Date(dateInput);
  if (isNaN(d.getTime())) return dateInput;
  return d.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
}

export function estimateNextPeriod(lastPeriodStartDate, avgCycleLength = 33) {
  if (!lastPeriodStartDate) return null;
  const start = new Date(lastPeriodStartDate);
  if (isNaN(start.getTime())) return null;

  const nextEstimate = new Date(start);
  nextEstimate.setDate(start.getDate() + avgCycleLength);

  const windowStart = new Date(nextEstimate);
  windowStart.setDate(nextEstimate.getDate() - 4);

  const windowEnd = new Date(nextEstimate);
  windowEnd.setDate(nextEstimate.getDate() + 4);

  return {
    estimatedDate: nextEstimate.toISOString().split('T')[0],
    windowRange: `${windowStart.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })} – ${windowEnd.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}`,
    varianceText: '±4 to 6 days natural PCOS variance'
  };
}

export function calculateCyclePhase(lastPeriodStartDate, avgCycleLength = 33) {
  if (!lastPeriodStartDate) return { phaseName: 'Awaiting Log', dayNumber: 0, color: 'var(--text-muted)' };
  
  const start = new Date(lastPeriodStartDate);
  const today = new Date();
  const diffDays = Math.floor((today - start) / (1000 * 60 * 60 * 24)) + 1;

  if (diffDays <= 0) return { phaseName: 'Upcoming', dayNumber: 0, color: 'var(--text-muted)' };
  if (diffDays <= 5) return { phaseName: 'Menstrual Phase', dayNumber: diffDays, color: 'var(--coral-600)' };
  if (diffDays <= 14) return { phaseName: 'Follicular Phase', dayNumber: diffDays, color: 'var(--primary-600)' };
  if (diffDays <= 18) return { phaseName: 'Ovulatory Window (Approx)', dayNumber: diffDays, color: 'var(--lavender-600)' };
  if (diffDays <= avgCycleLength) return { phaseName: 'Luteal Phase', dayNumber: diffDays, color: 'var(--accent-yellow)' };
  
  return { phaseName: 'Extended / Delayed Window', dayNumber: diffDays, color: 'var(--coral-700)' };
}

import React from 'react';

export default function MealPlanner({
  dailyPlan,
  onRemoveMeal,
  onResetPlan
}) {
  const slots = [
    { id: 'breakfast', label: 'Breakfast', icon: '🌅' },
    { id: 'lunch', label: 'Lunch', icon: '☀️' },
    { id: 'dinner', label: 'Dinner', icon: '🌙' }
  ];

  const hasAnyMeal = Object.values(dailyPlan).some((m) => m !== null);

  // Compute total calories & protein
  let totalCalories = 0;
  let plannedCount = 0;

  Object.values(dailyPlan).forEach((m) => {
    if (m) {
      plannedCount++;
      const match = m.approxCalories?.match(/\d+/);
      if (match) totalCalories += parseInt(match[0], 10);
    }
  });

  return (
    <div className="card" style={{ marginBottom: '28px', background: 'var(--primary-50)', border: '1px solid var(--primary-200)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '10px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h3 style={{ fontSize: '1.15rem', color: 'var(--primary-900)', margin: 0 }}>
              📅 Today's Balanced Indian Meal Plan
            </h3>
            {plannedCount > 0 && (
              <span className="badge badge-success">{plannedCount} of 3 Planned</span>
            )}
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Organize familiar regional staples for glucose stability and steady satiety.
          </p>
        </div>

        {hasAnyMeal && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {totalCalories > 0 && (
              <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--primary-800)' }}>
                🔥 Est. ~{totalCalories} kcal
              </span>
            )}
            <button onClick={onResetPlan} className="btn btn-ghost btn-sm" style={{ color: 'var(--coral-700)' }}>
              Reset Plan
            </button>
          </div>
        )}
      </div>

      <div className="grid-3">
        {slots.map((slot) => {
          const meal = dailyPlan[slot.id];
          return (
            <div
              key={slot.id}
              style={{
                background: 'var(--bg-card)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                border: meal ? '1px solid var(--primary-500)' : '1px dashed var(--border-subtle)',
                minHeight: '130px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                    {slot.icon} {slot.label}
                  </span>
                  {meal && (
                    <button
                      onClick={() => onRemoveMeal(slot.id)}
                      style={{ fontSize: '0.75rem', color: 'var(--coral-600)', background: 'none', border: 'none', cursor: 'pointer' }}
                      title="Remove from plan"
                    >
                      ✕ Remove
                    </button>
                  )}
                </div>

                {meal ? (
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-primary)' }}>
                      {meal.image} {meal.name}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      {meal.proteinSources} • {meal.approxCalories}
                    </div>
                  </div>
                ) : (
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', padding: '16px 0', textAlign: 'center' }}>
                    Empty slot. Choose below.
                  </div>
                )}
              </div>

              {meal && (
                <div style={{ fontSize: '0.72rem', color: 'var(--primary-700)', fontWeight: 600, marginTop: '8px' }}>
                  ✓ Glycemic Stability Selected
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

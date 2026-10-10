import React from 'react';
import { formatDietType } from '../utils/formatters';

export default function MealCard({
  meal,
  onSelect = null,
  isSelected = false,
  onViewDetails = null
}) {
  const getBudgetLabel = (tier) => {
    if (tier === 'budget_friendly') return '🪙 Budget Pantry';
    if (tier === 'everyday') return '🍲 Everyday';
    return '✨ Premium';
  };

  return (
    <div className="card" style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      border: isSelected ? '2px solid var(--primary-600)' : '1px solid var(--border-card)',
      background: isSelected ? 'var(--primary-50)' : 'var(--bg-card)'
    }}>
      <div>
        {/* Top Badges */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
          <div style={{ display: 'flex', gap: '6px' }}>
            <span className="badge badge-primary" style={{ textTransform: 'capitalize' }}>
              {meal.category}
            </span>
            <span className="badge badge-lavender">
              {formatDietType(meal.dietType)}
            </span>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>
            ⏱️ {meal.prepTime}
          </span>
        </div>

        {/* Title & Icon */}
        <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-start', marginBottom: '10px' }}>
          <div style={{ fontSize: '1.8rem', lineHeight: 1 }}>{meal.image}</div>
          <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', lineHeight: 1.3 }}>
            {meal.name}
          </h3>
        </div>

        {/* Nutritional Reasoning */}
        <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginBottom: '14px', lineHeight: '1.5' }}>
          {meal.balancedExplanation}
        </p>

        {/* Ingredients preview */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
          {meal.ingredients.slice(0, 4).map((ing, i) => (
            <span key={i} style={{
              background: 'var(--bg-subtle)',
              border: '1px solid var(--border-subtle)',
              fontSize: '0.74rem',
              padding: '2px 8px',
              borderRadius: '6px',
              color: 'var(--text-secondary)'
            }}>
              {ing}
            </span>
          ))}
          {meal.ingredients.length > 4 && (
            <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', alignSelf: 'center' }}>
              +{meal.ingredients.length - 4} more
            </span>
          )}
        </div>
      </div>

      {/* Footer Stats & Action */}
      <div>
        <div style={{
          padding: '10px 0',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: '0.78rem',
          color: 'var(--text-muted)',
          marginBottom: '12px'
        }}>
          <div>💪 <strong>{meal.proteinSources.split(' ')[0]}</strong> protein</div>
          <div>🌾 <strong>{meal.fibreSources.split(' ')[0]}</strong> fibre</div>
          <div>{getBudgetLabel(meal.budgetIndicator)}</div>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          {onViewDetails && (
            <button
              onClick={() => onViewDetails(meal)}
              className="btn btn-outline btn-sm"
              style={{ flex: 1 }}
            >
              Recipe Details
            </button>
          )}
          {onSelect && (
            <button
              onClick={() => onSelect(meal)}
              className={`btn btn-sm ${isSelected ? 'btn-secondary' : 'btn-primary'}`}
              style={{ flex: 1 }}
            >
              {isSelected ? '✓ In Daily Plan' : '+ Add to Plan'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

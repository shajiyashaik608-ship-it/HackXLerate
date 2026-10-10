import React from 'react';
import Modal from '../../components/Modal';
import { formatDietType } from '../../utils/formatters';

export default function MealDetails({ meal, isOpen, onClose }) {
  if (!meal) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`${meal.image} ${meal.name}`}
      maxWidth="620px"
      footer={
        <button onClick={onClose} className="btn btn-primary btn-sm">
          Close Recipe
        </button>
      }
    >
      <div>
        <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', flexWrap: 'wrap' }}>
          <span className="badge badge-primary" style={{ textTransform: 'capitalize' }}>
            {meal.category}
          </span>
          <span className="badge badge-lavender">
            {formatDietType(meal.dietType)}
          </span>
          <span className="badge badge-success">
            Approx. {meal.approxCalories}
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', alignSelf: 'center', marginLeft: 'auto' }}>
            ⏱️ {meal.prepTime}
          </span>
        </div>

        {/* Nutritional Mechanism */}
        <div style={{
          background: 'var(--primary-50)',
          borderLeft: '4px solid var(--primary-700)',
          padding: '14px 16px',
          borderRadius: '0 8px 8px 0',
          marginBottom: '20px'
        }}>
          <div style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--primary-900)', marginBottom: '4px' }}>
            🌿 Why this works for PCOS Hormonal Health:
          </div>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            {meal.balancedExplanation}
          </p>
        </div>

        {/* Macros Summary */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '12px',
          marginBottom: '20px'
        }}>
          <div style={{ background: 'var(--bg-subtle)', padding: '12px', borderRadius: '8px' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Protein Content</div>
            <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.92rem' }}>
              {meal.proteinSources}
            </div>
          </div>
          <div style={{ background: 'var(--bg-subtle)', padding: '12px', borderRadius: '8px' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Dietary Fibre</div>
            <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.92rem' }}>
              {meal.fibreSources}
            </div>
          </div>
        </div>

        {/* Ingredients */}
        <div style={{ marginBottom: '18px' }}>
          <h4 style={{ fontSize: '0.95rem', marginBottom: '8px', color: 'var(--text-primary)' }}>
            Ingredients
          </h4>
          <ul style={{ paddingLeft: '20px', fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
            {meal.ingredients.map((ing, i) => (
              <li key={i}>{ing}</li>
            ))}
          </ul>
        </div>

        {/* Instructions */}
        <div>
          <h4 style={{ fontSize: '0.95rem', marginBottom: '8px', color: 'var(--text-primary)' }}>
            Simple Preparation Method
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            {meal.instructions}
          </p>
        </div>
      </div>
    </Modal>
  );
}

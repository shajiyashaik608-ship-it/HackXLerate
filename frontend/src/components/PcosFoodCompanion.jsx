import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function PcosFoodCompanion({ language }) {
  const [dietType, setDietType] = useState('vegetarian');
  const [mealType, setMealType] = useState('');
  const [budgetOnly, setBudgetOnly] = useState(false);
  const [meals, setMeals] = useState([]);
  const [lifestyleNote, setLifestyleNote] = useState('');

  useEffect(() => {
    loadMeals();
  }, [dietType, mealType, budgetOnly]);

  const loadMeals = async () => {
    const data = await apiClient.getMealRecommendations(dietType, mealType || null, budgetOnly);
    setMeals(data.recommendations || []);
    setLifestyleNote(data.lifestyle_note || '');
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '6px' }}>
          🍲 Indian Food PCOS Companion
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
          Practical, balanced meal recommendations built around familiar home-cooked Indian foods (idli, pesarattu, dal, roti, millets, curd) designed to balance blood glucose without unsustainable crash diets.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="glass-panel" style={{
        padding: '16px 20px',
        marginBottom: '24px',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '16px',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Diet Buttons */}
        <div style={{ display: 'flex', gap: '8px' }}>
          {['vegetarian', 'eggitarian', 'non_vegetarian'].map((type) => (
            <button
              key={type}
              onClick={() => setDietType(type)}
              style={{
                padding: '8px 14px',
                borderRadius: '8px',
                fontSize: '0.82rem',
                fontWeight: 600,
                background: dietType === type ? '#0f766e' : '#f1f5f9',
                color: dietType === type ? 'white' : '#475569',
                textTransform: 'capitalize'
              }}
            >
              {type.replace('_', ' ')}
            </button>
          ))}
        </div>

        {/* Meal Type Buttons */}
        <div style={{ display: 'flex', gap: '8px', overflowX: 'auto' }}>
          {[
            { id: '', label: 'All Meals' },
            { id: 'breakfast', label: 'Breakfast' },
            { id: 'lunch', label: 'Lunch' },
            { id: 'snack', label: 'Snacks' },
            { id: 'dinner', label: 'Dinner' }
          ].map((m) => (
            <button
              key={m.id}
              onClick={() => setMealType(m.id)}
              style={{
                padding: '6px 12px',
                borderRadius: '8px',
                fontSize: '0.8rem',
                fontWeight: 500,
                background: mealType === m.id ? '#1e293b' : '#f8fafc',
                color: mealType === m.id ? 'white' : '#64748b',
                border: '1px solid #e2e8f0'
              }}
            >
              {m.label}
            </button>
          ))}
        </div>

        {/* Budget Friendly Toggle */}
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.85rem', fontWeight: 600, color: '#334155' }}>
          <input
            type="checkbox"
            checked={budgetOnly}
            onChange={(e) => setBudgetOnly(e.target.checked)}
          />
          🪙 Budget Staples Only
        </label>
      </div>

      {/* Meals Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        gap: '20px',
        marginBottom: '28px'
      }}>
        {meals.map((item, idx) => (
          <div key={idx} className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                <span className="badge badge-normal" style={{ textTransform: 'uppercase' }}>
                  {item.meal_type}
                </span>
                <span style={{ fontSize: '0.78rem', color: '#0f766e', fontWeight: 600 }}>
                  GI: {item.glycemic_index.toUpperCase()}
                </span>
              </div>

              <h3 style={{ fontSize: '1.15rem', color: '#0f172a', marginBottom: '8px' }}>
                {item.dish_name}
              </h3>

              <p style={{ fontSize: '0.84rem', color: '#475569', marginBottom: '14px', lineHeight: '1.5' }}>
                {item.why_it_works_for_pcos}
              </p>

              {/* Ingredients Chips */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
                {item.ingredients.map((ing, i) => (
                  <span key={i} style={{
                    background: '#f1f5f9',
                    fontSize: '0.74rem',
                    padding: '3px 8px',
                    borderRadius: '6px',
                    color: '#334155'
                  }}>
                    {ing}
                  </span>
                ))}
              </div>
            </div>

            {/* Nutrition Breakdown Footnote */}
            <div style={{
              borderTop: '1px solid #f1f5f9',
              paddingTop: '12px',
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: '0.82rem',
              color: '#64748b'
            }}>
              <div>💪 <strong>{item.protein_grams}g</strong> Protein</div>
              <div>🌾 <strong>{item.fibre_grams}g</strong> Fibre</div>
              <div>{item.budget_friendly ? '🪙 Low-Cost' : '✨ Everyday'}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Sustainable Eating Guidelines */}
      {lifestyleNote && (
        <div style={{
          background: '#fff1f2',
          border: '1px solid #fecdd3',
          borderRadius: '14px',
          padding: '20px',
          fontSize: '0.88rem',
          color: '#881337',
          lineHeight: '1.6'
        }}>
          <h4 style={{ fontWeight: 700, marginBottom: '8px' }}>🌱 Sustainable Indian Nutrition Principle</h4>
          <p style={{ whiteSpace: 'pre-line' }}>{lifestyleNote}</p>
        </div>
      )}
    </div>
  );
}

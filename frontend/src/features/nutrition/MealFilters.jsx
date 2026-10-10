import React from 'react';

export default function MealFilters({
  selectedCategory,
  onSelectCategory,
  selectedDiet,
  onSelectDiet,
  budgetOnly,
  onToggleBudget,
  searchQuery,
  onSearchChange
}) {
  const categories = [
    { id: 'all', label: 'All Meals' },
    { id: 'breakfast', label: 'Breakfast' },
    { id: 'lunch', label: 'Lunch' },
    { id: 'snacks', label: 'Snacks' },
    { id: 'dinner', label: 'Dinner' }
  ];

  const diets = [
    { id: 'all', label: 'All Diets' },
    { id: 'vegetarian', label: 'Vegetarian' },
    { id: 'eggitarian', label: 'Egg-Friendly' },
    { id: 'non_vegetarian', label: 'Non-Vegetarian' }
  ];

  return (
    <div className="card" style={{ padding: '18px 22px', marginBottom: '24px' }}>
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '16px',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Search */}
        <div style={{ flex: '1 1 240px', minWidth: '200px' }}>
          <input
            type="text"
            placeholder="Search meals (e.g. pesarattu, ragi, dal)..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            style={{ width: '100%', borderRadius: 'var(--radius-full)', padding: '9px 16px', fontSize: '0.86rem' }}
          />
        </div>

        {/* Category Pills */}
        <div style={{ display: 'flex', gap: '6px', overflowX: 'auto', padding: '2px 0' }}>
          {categories.map((c) => (
            <button
              key={c.id}
              onClick={() => onSelectCategory(c.id)}
              className={`btn btn-sm ${selectedCategory === c.id ? 'btn-primary' : 'btn-outline'}`}
              style={{ borderRadius: 'var(--radius-full)' }}
            >
              {c.label}
            </button>
          ))}
        </div>

        {/* Diet Select */}
        <div style={{ display: 'flex', gap: '6px' }}>
          {diets.map((d) => (
            <button
              key={d.id}
              onClick={() => onSelectDiet(d.id)}
              className={`btn btn-sm ${selectedDiet === d.id ? 'btn-secondary' : 'btn-ghost'}`}
              style={{ borderRadius: 'var(--radius-full)' }}
            >
              {d.label}
            </button>
          ))}
        </div>

        {/* Budget Checkbox */}
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.84rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          <input
            type="checkbox"
            checked={budgetOnly}
            onChange={(e) => onToggleBudget(e.target.checked)}
            style={{ accentColor: 'var(--primary-700)' }}
          />
          🪙 Budget Staples
        </label>
      </div>
    </div>
  );
}

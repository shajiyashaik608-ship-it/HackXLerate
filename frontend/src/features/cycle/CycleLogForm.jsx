import React, { useState } from 'react';

export default function CycleLogForm({ onSave, onCancel, initialData = null }) {
  const [startDate, setStartDate] = useState(initialData?.startDate || new Date().toISOString().split('T')[0]);
  const [durationDays, setDurationDays] = useState(initialData?.durationDays || 4);
  const [flow, setFlow] = useState(initialData?.flow || 'medium');
  const [symptoms, setSymptoms] = useState(initialData?.symptoms || ['cramps', 'fatigue']);
  const [notes, setNotes] = useState(initialData?.notes || '');
  const [error, setError] = useState('');

  const symptomOptions = [
    { id: 'cramps', label: 'Cramping / Pelvic Discomfort' },
    { id: 'acne', label: 'Hormonal / Jawline Acne' },
    { id: 'fatigue', label: 'Low Energy / Fatigue' },
    { id: 'mood', label: 'Mood Shifts / Irritability' },
    { id: 'bloating', label: 'Abdominal Bloating' },
    { id: 'headache', label: 'Headaches / Migraine' }
  ];

  const toggleSymptom = (id) => {
    setSymptoms((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!startDate) {
      setError('Please select a period start date.');
      return;
    }
    setError('');

    const logEntry = {
      id: initialData?.id || Date.now(),
      startDate,
      durationDays: Number(durationDays),
      flow,
      symptoms,
      notes: notes.trim()
    };

    onSave(logEntry);
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div style={{
          background: 'var(--coral-50)',
          color: 'var(--coral-700)',
          padding: '8px 12px',
          borderRadius: '8px',
          fontSize: '0.82rem',
          marginBottom: '14px',
          border: '1px solid var(--coral-500)'
        }}>
          {error}
        </div>
      )}

      <div className="form-group">
        <label className="form-label">Period Start Date *</label>
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
        />
        <span className="form-hint">The first day of noticeable flow.</span>
      </div>

      <div className="form-group">
        <label className="form-label">Flow Duration (Days)</label>
        <input
          type="number"
          min="1"
          max="15"
          value={durationDays}
          onChange={(e) => setDurationDays(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Flow Intensity</label>
        <div style={{ display: 'flex', gap: '8px' }}>
          {['spotting', 'light', 'medium', 'heavy'].map((f) => (
            <button
              type="button"
              key={f}
              onClick={() => setFlow(f)}
              className={`btn btn-sm ${flow === f ? 'btn-primary' : 'btn-outline'}`}
              style={{ flex: 1, textTransform: 'capitalize' }}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">Observed Symptoms</label>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {symptomOptions.map((sym) => {
            const isChecked = symptoms.includes(sym.id);
            return (
              <button
                type="button"
                key={sym.id}
                onClick={() => toggleSymptom(sym.id)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 'var(--radius-full)',
                  fontSize: '0.78rem',
                  fontWeight: 500,
                  background: isChecked ? 'var(--coral-100)' : 'var(--bg-subtle)',
                  color: isChecked ? 'var(--coral-700)' : 'var(--text-secondary)',
                  border: isChecked ? '1px solid var(--coral-500)' : '1px solid var(--border-subtle)',
                  cursor: 'pointer'
                }}
              >
                {sym.label} {isChecked ? '✓' : '+'}
              </button>
            );
          })}
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">Personal Notes</label>
        <textarea
          rows="3"
          placeholder="e.g., Felt mild cramping 2 days prior, cycle interval was 38 days."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
        {onCancel && (
          <button type="button" onClick={onCancel} className="btn btn-outline">
            Cancel
          </button>
        )}
        <button type="submit" className="btn btn-primary">
          Save Cycle Entry
        </button>
      </div>
    </form>
  );
}

import React, { useState } from 'react';

export default function CycleTracker({ language }) {
  const [startDate, setStartDate] = useState('');
  const [flow, setFlow] = useState('moderate');
  const [selectedSymptoms, setSelectedSymptoms] = useState(['cramps', 'fatigue']);
  const [notes, setNotes] = useState('');

  const symptomsList = [
    { id: 'cramps', label: 'Cramping' },
    { id: 'acne', label: 'Cystic Acne' },
    { id: 'fatigue', label: 'Fatigue' },
    { id: 'mood_swings', label: 'Mood Swings' },
    { id: 'bloating', label: 'Bloating' },
    { id: 'headache', label: 'Headache' }
  ];

  const toggleSymptom = (id) => {
    if (selectedSymptoms.includes(id)) {
      setSelectedSymptoms(selectedSymptoms.filter((s) => s !== id));
    } else {
      setSelectedSymptoms([...selectedSymptoms, id]);
    }
  };

  const handleLog = (e) => {
    e.preventDefault();
    alert("Period cycle event logged into your medical timeline!");
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '6px' }}>
          🌸 Menstrual Cycle & Symptom Tracker
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
          Designed specifically for PCOS realities: Communicates natural cycle variability rather than misleading exact predictions.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Form Panel */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', color: '#0f172a' }}>Log Cycle or Symptoms</h3>
          <form onSubmit={handleLog}>
            <div style={{ marginBottom: '14px' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, marginBottom: '6px' }}>
                Period Start Date
              </label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 14px',
                  borderRadius: '8px',
                  border: '1px solid #cbd5e1',
                  fontSize: '0.9rem'
                }}
              />
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, marginBottom: '6px' }}>
                Flow Intensity
              </label>
              <div style={{ display: 'flex', gap: '8px' }}>
                {['spotting', 'light', 'moderate', 'heavy'].map((f) => (
                  <button
                    type="button"
                    key={f}
                    onClick={() => setFlow(f)}
                    style={{
                      flex: 1,
                      padding: '8px',
                      borderRadius: '8px',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      background: flow === f ? '#0f766e' : '#f1f5f9',
                      color: flow === f ? 'white' : '#475569',
                      textTransform: 'capitalize'
                    }}
                  >
                    {f}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, marginBottom: '6px' }}>
                Observed Symptoms Today
              </label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {symptomsList.map((s) => {
                  const isChecked = selectedSymptoms.includes(s.id);
                  return (
                    <button
                      type="button"
                      key={s.id}
                      onClick={() => toggleSymptom(s.id)}
                      style={{
                        padding: '6px 12px',
                        borderRadius: '20px',
                        fontSize: '0.78rem',
                        fontWeight: 500,
                        background: isChecked ? '#ffe4e6' : '#f8fafc',
                        color: isChecked ? '#e11d48' : '#64748b',
                        border: isChecked ? '1px solid #f43f5e' : '1px solid #e2e8f0'
                      }}
                    >
                      {s.label} {isChecked ? '✓' : '+'}
                    </button>
                  );
                })}
              </div>
            </div>

            <div style={{ marginBottom: '18px' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, marginBottom: '6px' }}>
                Personal Observation Notes
              </label>
              <textarea
                rows="3"
                placeholder="e.g., Cycle started after 38 days gap, accompanied by lower back cramps."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 14px',
                  borderRadius: '8px',
                  border: '1px solid #cbd5e1',
                  fontSize: '0.86rem'
                }}
              ></textarea>
            </div>

            <button type="submit" className="btn-rose" style={{ width: '100%', justifyContent: 'center' }}>
              🌸 Save Cycle Entry
            </button>
          </form>
        </div>

        {/* Cautious Estimation Panel */}
        <div>
          <div className="glass-panel" style={{ padding: '24px', marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <h3 style={{ fontSize: '1.1rem', color: '#0f172a' }}>Cycle Intelligence</h3>
              <span className="badge badge-normal">Cautious Estimate</span>
            </div>

            <div style={{
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '12px',
              padding: '16px',
              marginBottom: '16px'
            }}>
              <div style={{ fontSize: '0.8rem', color: '#64748b' }}>Estimated Next Cycle Window</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#0f766e', margin: '4px 0' }}>
                Oct 28 — Nov 03
              </div>
              <div style={{ fontSize: '0.78rem', color: '#92400e', background: '#fef3c7', padding: '4px 8px', borderRadius: '6px', display: 'inline-block' }}>
                ⚠️ ± 6 days natural variance expected for PCOS
              </div>
            </div>

            <p style={{ fontSize: '0.84rem', color: '#475569', lineHeight: '1.6' }}>
              Unlike regular 28-day cycles, polycystic ovarian patterns often show fluctuating follicular phases. Health Saathi avoids artificial pinpoint dates to prevent false anxiety.
            </p>
          </div>

          {/* Past History */}
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1rem', color: '#0f172a', marginBottom: '12px' }}>Recent Cycle Intervals</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 12px', background: '#f8fafc', borderRadius: '8px' }}>
                <span>Sep 25, 2026 (Light flow)</span>
                <strong style={{ color: '#0f766e' }}>38 Days Interval</strong>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 12px', background: '#f8fafc', borderRadius: '8px' }}>
                <span>Aug 18, 2026 (Moderate flow)</span>
                <strong style={{ color: '#0f766e' }}>35 Days Interval</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

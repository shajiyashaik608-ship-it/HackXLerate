import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import { formatDisplayDate } from '../utils/dateUtils';

export default function DoctorPreparation({
  profile,
  cycleLogs,
  reports,
  reminders,
  language
}) {
  const [questions, setQuestions] = useState([
    "Are my current cycle intervals consistent with ovulatory delays or insulin resistance?",
    "Do my borderline elevated TSH levels (4.85 mIU/L) warrant thyroid antibody screening?",
    "Should I continue Inositol supplementation alongside standard dietary adjustments?",
    "When should we schedule a follow-up pelvic ultrasound scan?"
  ]);
  const [newQuestion, setNewQuestion] = useState('');
  const [clinicalNotes, setClinicalNotes] = useState('Feeling afternoon fatigue around 3 PM; noticing acne along the lower jawline during the luteal phase.');
  const [copied, setCopied] = useState(false);

  const isTelugu = language === 'te';

  const handleAddQuestion = (e) => {
    e.preventDefault();
    if (!newQuestion.trim()) return;
    setQuestions([...questions, newQuestion.trim()]);
    setNewQuestion('');
  };

  const handleRemoveQuestion = (idx) => {
    setQuestions(questions.filter((_, i) => i !== idx));
  };

  const handlePrint = () => {
    window.print();
  };

  const handleCopy = () => {
    const text = `
PCOS SAATHI - CLINICAL VISIT SUMMARY
Patient: ${profile.name || 'Priya Sharma'}, Age: ${profile.age || 24}
Last Cycle: ${cycleLogs.length > 0 ? formatDisplayDate(cycleLogs[0].startDate) : 'None'} (${cycleLogs[0]?.durationDays || 4} days flow)
Lab Flags: ${reports.flatMap(r => r.biomarkers?.filter(b => b.status === 'elevated').map(b => `${b.testName}: ${b.value} ${b.unit}`)).join(', ') || 'None'}
Questions for Doctor:
${questions.map((q, i) => `${i + 1}. ${q}`).join('\n')}
    `.trim();

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      <PageHeader
        title={isTelugu ? 'డాక్టర్ సంప్రదింపు తయారీ (Doctor Visit Prep)' : 'Doctor Visit Preparation Assistant'}
        subtitle={isTelugu
          ? 'మీ పీరియడ్ సైకిల్స్, ల్యాబ్ రిపోర్టులు మరియు డాక్టర్‌ని అడగాల్సిన ప్రశ్నలతో కూడిన 1-పేజీ సారాంశాన్ని సిద్ధం చేసుకోండి.'
          : 'Synthesize your symptom logs, abnormal lab biomarkers, and high-yield questions into an appointment-ready clinical summary.'}
        actions={
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={handleCopy} className="btn btn-outline btn-sm">
              {copied ? '✓ Copied' : '📋 Copy Text'}
            </button>
            <button onClick={handlePrint} className="btn btn-primary btn-sm">
              🖨️ Print Clinical Sheet
            </button>
          </div>
        }
      />

      {/* Printable Sheet View */}
      <div className="card" style={{
        backgroundColor: '#ffffff',
        border: '2px solid var(--border-subtle)',
        padding: '36px',
        boxShadow: 'var(--shadow-card)'
      }}>
        {/* Document Header */}
        <div style={{
          borderBottom: '2px solid var(--primary-700)',
          paddingBottom: '16px',
          marginBottom: '24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start'
        }}>
          <div>
            <h2 style={{ fontSize: '1.45rem', color: 'var(--primary-800)', fontWeight: 800 }}>
              PATIENT CONSULTATION BRIEF
            </h2>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Organized via PCOS Saathi Personal Health Copilot
            </div>
          </div>
          <div style={{ textAlign: 'right', fontSize: '0.88rem' }}>
            <strong>{profile.name || 'Priya Sharma'}</strong> (Age: {profile.age || 24})<br />
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Date: {new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
            </span>
          </div>
        </div>

        {/* Section 1: Menstrual History */}
        <div style={{ marginBottom: '22px' }}>
          <h4 style={{ fontSize: '0.98rem', color: 'var(--primary-900)', borderLeft: '3px solid var(--primary-700)', paddingLeft: '8px', marginBottom: '8px' }}>
            1. Recent Menstrual Pattern
          </h4>
          {cycleLogs.length > 0 ? (
            <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', background: 'var(--bg-subtle)', padding: '10px 14px', borderRadius: '8px' }}>
              • Most recent period began on <strong>{formatDisplayDate(cycleLogs[0].startDate)}</strong> ({cycleLogs[0].durationDays} days duration, {cycleLogs[0].flow} flow).<br />
              • Baseline cycle interval observed: <strong>{profile.cycleLength || 33} days</strong> with natural variance.
            </div>
          ) : (
            <div style={{ fontSize: '0.84rem', color: 'var(--text-muted)' }}>No menstrual logs entered yet.</div>
          )}
        </div>

        {/* Section 2: Flagged Lab Findings */}
        <div style={{ marginBottom: '22px' }}>
          <h4 style={{ fontSize: '0.98rem', color: 'var(--primary-900)', borderLeft: '3px solid var(--primary-700)', paddingLeft: '8px', marginBottom: '8px' }}>
            2. Pertinent Diagnostic Findings
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {reports.flatMap((r) => r.biomarkers?.filter((b) => b.status === 'elevated')).map((b, i) => (
              <div key={i} style={{
                background: 'var(--accent-yellow-light)',
                color: '#854d0e',
                padding: '8px 12px',
                borderRadius: '6px',
                fontSize: '0.85rem',
                fontWeight: 600
              }}>
                • {b.testName}: {b.value} {b.unit} (Reference: {b.referenceRange}) — ELEVATED
              </div>
            ))}
            {reports.length === 0 && (
              <div style={{ fontSize: '0.84rem', color: 'var(--text-muted)' }}>No lab findings stored.</div>
            )}
          </div>
        </div>

        {/* Section 3: Active Medications & Supplements */}
        <div style={{ marginBottom: '22px' }}>
          <h4 style={{ fontSize: '0.98rem', color: 'var(--primary-900)', borderLeft: '3px solid var(--primary-700)', paddingLeft: '8px', marginBottom: '8px' }}>
            3. Active Prescriptions / Daily Routines
          </h4>
          <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
            {reminders.filter((r) => r.category === 'medication').map((m, i) => (
              <div key={i} style={{ marginBottom: '4px' }}>
                • {m.title} ({m.notes || m.time})
              </div>
            ))}
          </div>
        </div>

        {/* Section 4: Questions to Ask */}
        <div style={{ marginBottom: '22px' }}>
          <h4 style={{ fontSize: '0.98rem', color: 'var(--coral-700)', borderLeft: '3px solid var(--coral-600)', paddingLeft: '8px', marginBottom: '8px' }}>
            4. High-Yield Questions for the Physician
          </h4>
          <ul style={{ paddingLeft: '22px', fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.8 }}>
            {questions.map((q, i) => (
              <li key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>{q}</span>
                <button
                  onClick={() => handleRemoveQuestion(i)}
                  style={{ color: 'var(--text-light)', fontSize: '0.75rem', cursor: 'pointer' }}
                  title="Remove question"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>

          {/* Add Question input */}
          <form onSubmit={handleAddQuestion} style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
            <input
              type="text"
              placeholder="Add your own question for the doctor..."
              value={newQuestion}
              onChange={(e) => setNewQuestion(e.target.value)}
              style={{ flex: 1, padding: '8px 12px', fontSize: '0.84rem' }}
            />
            <button type="submit" className="btn btn-outline btn-sm">
              + Add Question
            </button>
          </form>
        </div>

        {/* Section 5: Clinical Notes */}
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ fontSize: '0.98rem', color: 'var(--primary-900)', borderLeft: '3px solid var(--primary-700)', paddingLeft: '8px', marginBottom: '8px' }}>
            5. Patient Observations & Symptoms
          </h4>
          <textarea
            rows="2"
            value={clinicalNotes}
            onChange={(e) => setClinicalNotes(e.target.value)}
            style={{ width: '100%', fontSize: '0.85rem', color: 'var(--text-secondary)' }}
          />
        </div>

        {/* Ethical Disclaimer */}
        <div style={{
          borderTop: '1px solid var(--border-subtle)',
          paddingTop: '14px',
          fontSize: '0.74rem',
          color: 'var(--text-muted)',
          textAlign: 'center',
          fontStyle: 'italic'
        }}>
          Prepared via PCOS Saathi to facilitate clear patient-clinician communication. This document does not constitute an automated diagnosis or medical prescription.
        </div>
      </div>
    </div>
  );
}

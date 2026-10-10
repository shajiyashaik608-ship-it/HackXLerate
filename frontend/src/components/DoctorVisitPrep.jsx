import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function DoctorVisitPrep({ language }) {
  const [summary, setSummary] = useState(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    const data = await apiClient.getDoctorSummary();
    setSummary(data);
  };

  const handleCopy = () => {
    if (!summary) return;
    const text = `
HEALTH SAATHI - CLINICAL VISIT SUMMARY
Patient: ${summary.patient_overview}
Chief Concerns: ${summary.chief_concerns}
Menstrual History: ${summary.menstrual_history}

Pertinent Lab Findings:
${summary.pertinent_lab_findings.join('\n')}

Active Medications:
${summary.active_medications.join('\n')}

Questions to ask doctor:
${summary.recommended_questions_to_ask.map((q, i) => `${i + 1}. ${q}`).join('\n')}
    `.trim();

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '6px' }}>
            🩺 Doctor Visit Preparation Assistant
          </h1>
          <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
            Automated synthesis of your menstrual logs, symptoms, abnormal labs, and formulated questions for your next appointment.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={handleCopy} className="btn-outline">
            {copied ? '✅ Copied!' : '📋 Copy Text'}
          </button>
          <button onClick={handlePrint} className="btn-primary">
            🖨️ Print Clinical Sheet
          </button>
        </div>
      </div>

      {summary && (
        <div className="glass-panel" style={{
          padding: '36px',
          background: '#ffffff',
          border: '2px solid #e2e8f0',
          borderRadius: '16px',
          boxShadow: '0 8px 30px rgba(0,0,0,0.06)'
        }}>
          {/* Header */}
          <div style={{ borderBottom: '2px solid #0f766e', paddingBottom: '16px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 style={{ fontSize: '1.4rem', color: '#0f766e', fontWeight: 700 }}>
                PATIENT CONSULTATION BRIEF
              </h2>
              <div style={{ fontSize: '0.85rem', color: '#64748b' }}>
                Generated via Health Saathi Copilot
              </div>
            </div>
            <div style={{ textAlign: 'right', fontSize: '0.85rem', fontWeight: 600 }}>
              {summary.patient_overview}
            </div>
          </div>

          {/* Section 1: Chief Concerns */}
          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1rem', color: '#0f172a', borderLeft: '3px solid #0f766e', paddingLeft: '8px', marginBottom: '6px' }}>
              1. Chief Concerns & Symptoms
            </h3>
            <p style={{ fontSize: '0.9rem', color: '#334155', background: '#f8fafc', padding: '10px 14px', borderRadius: '8px' }}>
              {summary.chief_concerns}
            </p>
          </div>

          {/* Section 2: Menstrual History */}
          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1rem', color: '#0f172a', borderLeft: '3px solid #0f766e', paddingLeft: '8px', marginBottom: '6px' }}>
              2. Menstrual Pattern & Timeline
            </h3>
            <p style={{ fontSize: '0.9rem', color: '#334155', background: '#f8fafc', padding: '10px 14px', borderRadius: '8px' }}>
              {summary.menstrual_history}
            </p>
          </div>

          {/* Section 3: Lab Highlights */}
          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1rem', color: '#0f172a', borderLeft: '3px solid #0f766e', paddingLeft: '8px', marginBottom: '8px' }}>
              3. Pertinent Lab Findings
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {summary.pertinent_lab_findings.map((finding, idx) => (
                <div key={idx} style={{
                  fontSize: '0.86rem',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  background: finding.includes('ELEVATED') ? '#fef3c7' : '#f8fafc',
                  color: finding.includes('ELEVATED') ? '#92400e' : '#334155',
                  fontWeight: 500
                }}>
                  • {finding}
                </div>
              ))}
            </div>
          </div>

          {/* Section 4: Current Medications */}
          <div style={{ marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1rem', color: '#0f172a', borderLeft: '3px solid #0f766e', paddingLeft: '8px', marginBottom: '6px' }}>
              4. Active Prescriptions / Supplements
            </h3>
            <div style={{ fontSize: '0.88rem', color: '#334155' }}>
              {summary.active_medications.map((m, idx) => (
                <div key={idx}>• {m}</div>
              ))}
            </div>
          </div>

          {/* Section 5: High-Yield Questions */}
          <div style={{ marginBottom: '24px' }}>
            <h3 style={{ fontSize: '1rem', color: '#0f172a', borderLeft: '3px solid #e11d48', paddingLeft: '8px', marginBottom: '8px' }}>
              5. Priority Questions for Your Doctor
            </h3>
            <ul style={{ paddingLeft: '20px', fontSize: '0.88rem', color: '#334155', lineHeight: '1.8' }}>
              {summary.recommended_questions_to_ask.map((q, idx) => (
                <li key={idx} style={{ fontWeight: 500 }}>{q}</li>
              ))}
            </ul>
          </div>

          {/* Clinical Disclaimer */}
          <div style={{
            borderTop: '1px solid #e2e8f0',
            paddingTop: '14px',
            fontSize: '0.75rem',
            color: '#64748b',
            fontStyle: 'italic',
            textAlign: 'center'
          }}>
            {summary.clinical_disclaimer}
          </div>
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import Modal from '../../components/Modal';

export default function ReportPostModal({ post, isOpen, onClose, onConfirmReport }) {
  const [reason, setReason] = useState('unverified_medical_claim');
  const [submitted, setSubmitted] = useState(false);

  const reasons = [
    { id: 'unverified_medical_claim', label: 'Unverified medical "cure" or unsafe clinical claim' },
    { id: 'commercial_spam', label: 'Commercial promotion, spam, or external product link' },
    { id: 'personal_pii', label: 'Personal contact or identifiable private document shared' },
    { id: 'inappropriate', label: 'Disrespectful language or invalidating discussion' }
  ];

  const handleReport = () => {
    setSubmitted(true);
    setTimeout(() => {
      onConfirmReport(post.id, reason);
      setSubmitted(false);
      onClose();
    }, 1200);
  };

  if (!post) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="🚩 Report Community Content"
      maxWidth="520px"
      footer={
        !submitted ? (
          <>
            <button onClick={onClose} className="btn btn-outline btn-sm">
              Cancel
            </button>
            <button onClick={handleReport} className="btn btn-coral btn-sm">
              Submit Safety Report
            </button>
          </>
        ) : null
      }
    >
      {submitted ? (
        <div style={{ textAlign: 'center', padding: '20px 10px' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>🛡️</div>
          <h4 style={{ color: 'var(--text-primary)', marginBottom: '6px' }}>Report Received (Demo Simulation)</h4>
          <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)' }}>
            Thank you for helping keep PCOS Saathi a safe, evidence-grounded educational space. This item has been flagged in your local demo session.
          </p>
        </div>
      ) : (
        <div>
          <div style={{
            background: 'var(--bg-subtle)',
            padding: '12px 14px',
            borderRadius: '8px',
            marginBottom: '16px',
            fontSize: '0.86rem',
            color: 'var(--text-secondary)'
          }}>
            Reporting: <strong>"{post.title}"</strong>
          </div>

          <div className="form-group">
            <label className="form-label">Select reason for safety flag:</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '6px' }}>
              {reasons.map((r) => (
                <label
                  key={r.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    padding: '10px 12px',
                    borderRadius: '8px',
                    border: reason === r.id ? '1px solid var(--coral-500)' : '1px solid var(--border-subtle)',
                    background: reason === r.id ? 'var(--coral-50)' : 'var(--bg-card)',
                    fontSize: '0.84rem',
                    cursor: 'pointer'
                  }}
                >
                  <input
                    type="radio"
                    name="reportReason"
                    value={r.id}
                    checked={reason === r.id}
                    onChange={() => setReason(r.id)}
                    style={{ accentColor: 'var(--coral-600)' }}
                  />
                  <span>{r.label}</span>
                </label>
              ))}
            </div>
          </div>

          <p style={{ fontSize: '0.74rem', color: 'var(--text-light)', marginTop: '12px', fontStyle: 'italic' }}>
            Note: In this frontend demo, reporting flags the post in your local browser state without transmitting external network alerts.
          </p>
        </div>
      )}
    </Modal>
  );
}

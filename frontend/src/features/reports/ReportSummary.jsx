import React, { useState } from 'react';
import Modal from '../../components/Modal';
import { formatDisplayDate } from '../../utils/dateUtils';

export default function ReportSummary({ report, isOpen, onClose, onUpdateReport }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedBiomarkers, setEditedBiomarkers] = useState([]);
  const [copySuccess, setCopySuccess] = useState(false);

  if (!report) return null;

  const handleStartEdit = () => {
    setEditedBiomarkers(JSON.parse(JSON.stringify(report.biomarkers || [])));
    setIsEditing(true);
  };

  const handleSaveEdits = () => {
    if (onUpdateReport) {
      onUpdateReport({
        ...report,
        biomarkers: editedBiomarkers,
        hasUserCorrection: true
      });
    }
    setIsEditing(false);
  };

  const handleBiomarkerChange = (index, field, value) => {
    const updated = [...editedBiomarkers];
    updated[index][field] = value;
    updated[index].isManualEdit = true;
    setEditedBiomarkers(updated);
  };

  const handleCopySummary = () => {
    const text = `
Health Saathi - Extracted Lab Summary
File: ${report.fileName} (${report.category})
Date: ${report.uploadDate}
Biomarkers:
${report.biomarkers?.map(b => `- ${b.testName}: ${b.value} ${b.unit} [Ref: ${b.referenceRange}] -> Status: ${b.status}`).join('\n')}
Plain Explanation:
${report.plainSummary || 'Standard clinical parameters extracted.'}
    `.trim();

    navigator.clipboard.writeText(text);
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  const currentBiomarkers = isEditing ? editedBiomarkers : report.biomarkers || [];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`📄 ${report.fileName}`}
      maxWidth="760px"
      footer={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <button onClick={handleCopySummary} className="btn btn-outline btn-sm">
            {copySuccess ? '✓ Copied' : '📋 Copy Summary'}
          </button>
          <div style={{ display: 'flex', gap: '8px' }}>
            {isEditing ? (
              <>
                <button onClick={() => setIsEditing(false)} className="btn btn-outline btn-sm">
                  Cancel
                </button>
                <button onClick={handleSaveEdits} className="btn btn-primary btn-sm">
                  Save Corrections
                </button>
              </>
            ) : (
              <>
                <button onClick={handleStartEdit} className="btn btn-outline btn-sm">
                  ✏️ Correct Values
                </button>
                <button onClick={onClose} className="btn btn-primary btn-sm">
                  Close
                </button>
              </>
            )}
          </div>
        </div>
      }
    >
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <span className="badge badge-primary">{report.category}</span>
            <span style={{ marginLeft: '8px', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Uploaded: {formatDisplayDate(report.uploadDate)}
            </span>
          </div>
          <div style={{ display: 'flex', gap: '6px' }}>
            <span className="badge badge-success">Simulated OCR Verified</span>
            {report.hasUserCorrection && (
              <span className="badge badge-warning">User Adjusted</span>
            )}
          </div>
        </div>

        {report.doctorNotes && (
          <div style={{
            background: 'var(--bg-subtle)',
            padding: '10px 14px',
            borderRadius: '8px',
            fontSize: '0.84rem',
            color: 'var(--text-secondary)',
            marginBottom: '18px'
          }}>
            <strong>Clinician Context:</strong> {report.doctorNotes}
          </div>
        )}

        {/* Biomarkers Table */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <h4 style={{ fontSize: '0.95rem', color: 'var(--text-primary)', margin: 0 }}>
            Extracted Biomarkers & Reference Ranges
          </h4>
          {isEditing && (
            <span style={{ fontSize: '0.76rem', color: 'var(--primary-700)', fontWeight: 600 }}>
              Editing Mode: Adjust numeric readings if OCR misread
            </span>
          )}
        </div>

        <div style={{ overflowX: 'auto', marginBottom: '20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--border-subtle)', color: 'var(--text-muted)', textAlign: 'left' }}>
                <th style={{ padding: '8px 10px' }}>Test Parameter</th>
                <th style={{ padding: '8px 10px' }}>Observed Value</th>
                <th style={{ padding: '8px 10px' }}>Reference Range</th>
                <th style={{ padding: '8px 10px' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {currentBiomarkers.map((b, i) => (
                <React.Fragment key={i}>
                  <tr style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                    <td style={{ padding: '10px', fontWeight: 600, color: 'var(--text-primary)' }}>
                      {b.testName}
                    </td>
                    <td style={{ padding: '10px' }}>
                      {isEditing ? (
                        <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }}>
                          <input
                            type="text"
                            value={b.value}
                            onChange={(e) => handleBiomarkerChange(i, 'value', e.target.value)}
                            style={{ width: '70px', padding: '4px 6px', fontSize: '0.82rem' }}
                          />
                          <input
                            type="text"
                            value={b.unit}
                            onChange={(e) => handleBiomarkerChange(i, 'unit', e.target.value)}
                            style={{ width: '50px', padding: '4px 6px', fontSize: '0.82rem' }}
                          />
                        </div>
                      ) : (
                        <span style={{ fontWeight: 700 }}>
                          {b.value} <span style={{ fontSize: '0.75rem', fontWeight: 400, color: 'var(--text-muted)' }}>{b.unit}</span>
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '10px', color: 'var(--text-muted)' }}>
                      {b.referenceRange}
                    </td>
                    <td style={{ padding: '10px' }}>
                      {isEditing ? (
                        <select
                          value={b.status}
                          onChange={(e) => handleBiomarkerChange(i, 'status', e.target.value)}
                          style={{ padding: '4px', fontSize: '0.78rem' }}
                        >
                          <option value="normal">normal</option>
                          <option value="elevated">elevated</option>
                          <option value="borderline">borderline</option>
                        </select>
                      ) : (
                        <span className={`badge ${
                          b.status === 'normal' ? 'badge-success' :
                          b.status === 'elevated' ? 'badge-coral' : 'badge-warning'
                        }`}>
                          {b.status}
                        </span>
                      )}
                    </td>
                  </tr>
                  {b.plainExplanation && (
                    <tr style={{ background: 'var(--bg-subtle)' }}>
                      <td colSpan="4" style={{ padding: '8px 12px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                        💡 <strong>Plain Language:</strong> {b.plainExplanation}
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>

        {/* Plain Language Summary */}
        {report.plainSummary && (
          <div style={{
            background: 'var(--primary-50)',
            border: '1px solid var(--primary-200)',
            borderRadius: '12px',
            padding: '16px',
            fontSize: '0.86rem',
            color: 'var(--primary-900)',
            lineHeight: 1.6
          }}>
            <div style={{ fontWeight: 700, marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span>🧠</span> Plain English Translation
            </div>
            {report.plainSummary}
          </div>
        )}
      </div>
    </Modal>
  );
}

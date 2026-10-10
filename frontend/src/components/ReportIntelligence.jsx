import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function ReportIntelligence({ language }) {
  const [reports, setReports] = useState([]);
  const [activeReport, setActiveReport] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadTitle, setUploadTitle] = useState('');
  const [rawText, setRawText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    const data = await apiClient.getReports();
    setReports(data);
    if (data.length > 0) setActiveReport(data[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('title', uploadTitle || 'Diagnostic Blood Report');
    formData.append('raw_text', rawText);
    if (selectedFile) formData.append('file', selectedFile);

    const result = await apiClient.uploadReport(formData);
    setReports([result, ...reports]);
    setActiveReport(result);
    setIsProcessing(false);
    setUploadTitle('');
    setRawText('');
    setSelectedFile(null);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 20px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '6px' }}>
          📄 Medical Record Intelligence
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
          Upload blood panels, thyroid tests, or ultrasounds. The AI extracts numeric values, benchmarks reference intervals, and translates clinical jargon into plain language.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>
        {/* Upload Column */}
        <div>
          <div className="glass-panel" style={{ padding: '20px', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '14px', color: '#0f172a' }}>Upload Lab Document</h3>
            <form onSubmit={handleUpload}>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
                  Report Title
                </label>
                <input
                  type="text"
                  placeholder="e.g., Hormone & Thyroid Panel"
                  value={uploadTitle}
                  onChange={(e) => setUploadTitle(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    fontSize: '0.88rem'
                  }}
                />
              </div>

              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
                  Select File (PDF or Image)
                </label>
                <input
                  type="file"
                  onChange={(e) => setSelectedFile(e.target.files[0])}
                  style={{ fontSize: '0.85rem' }}
                />
              </div>

              <div style={{ marginBottom: '14px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
                  Or Paste Report Text / Notes
                </label>
                <textarea
                  rows="4"
                  placeholder="Paste OCR text e.g., TSH: 4.8 mIU/L, Fasting Insulin: 18.2 uIU/mL"
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    fontSize: '0.85rem'
                  }}
                ></textarea>
              </div>

              <button
                type="submit"
                disabled={isProcessing}
                className="btn-primary"
                style={{ width: '100%', justifyContent: 'center' }}
              >
                {isProcessing ? 'Analyzing Biomarkers...' : '⚡ Extract & Explain Report'}
              </button>
            </form>
          </div>

          {/* Past Reports List */}
          <div className="glass-panel" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '1rem', marginBottom: '12px', color: '#0f172a' }}>Past Records</h3>
            {reports.map((rep) => (
              <div
                key={rep.id}
                onClick={() => setActiveReport(rep)}
                style={{
                  padding: '10px 12px',
                  borderRadius: '8px',
                  marginBottom: '8px',
                  cursor: 'pointer',
                  background: activeReport?.id === rep.id ? '#f0fdfa' : '#f8fafc',
                  border: activeReport?.id === rep.id ? '1px solid #0f766e' : '1px solid #e2e8f0'
                }}
              >
                <div style={{ fontWeight: 600, fontSize: '0.88rem', color: '#0f172a' }}>{rep.title}</div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                  {rep.structured_data?.length || 0} biomarkers identified
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Report Extraction & Explanation View */}
        <div>
          {activeReport ? (
            <div className="glass-panel" style={{ padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <div>
                  <h2 style={{ fontSize: '1.3rem', color: '#0f172a' }}>{activeReport.title}</h2>
                  <span style={{ fontSize: '0.78rem', color: '#64748b' }}>Extracted Medical Biomarkers</span>
                </div>
                <span className="badge badge-normal">OCR Verified</span>
              </div>

              {/* Biomarkers Table */}
              <div style={{ overflowX: 'auto', marginBottom: '20px' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid #e2e8f0', color: '#64748b' }}>
                      <th style={{ padding: '10px 8px' }}>Test Parameter</th>
                      <th style={{ padding: '10px 8px' }}>Your Value</th>
                      <th style={{ padding: '10px 8px' }}>Standard Range</th>
                      <th style={{ padding: '10px 8px' }}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {activeReport.structured_data?.map((item, idx) => (
                      <React.Fragment key={idx}>
                        <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                          <td style={{ padding: '12px 8px', fontWeight: 600, color: '#0f172a' }}>
                            {item.test_name}
                          </td>
                          <td style={{ padding: '12px 8px', fontWeight: 700 }}>
                            {item.value} <span style={{ fontSize: '0.75rem', fontWeight: 400, color: '#64748b' }}>{item.unit}</span>
                          </td>
                          <td style={{ padding: '12px 8px', color: '#64748b' }}>
                            {item.reference_range}
                          </td>
                          <td style={{ padding: '12px 8px' }}>
                            <span className={`badge ${
                              item.status === 'normal' ? 'badge-normal' :
                              item.status === 'elevated' ? 'badge-elevated' : 'badge-low'
                            }`}>
                              {item.status}
                            </span>
                          </td>
                        </tr>
                        <tr style={{ background: '#f8fafc' }}>
                          <td colSpan="4" style={{ padding: '8px 12px', fontSize: '0.82rem', color: '#475569' }}>
                            💡 <strong>Plain English:</strong> {item.plain_explanation}
                          </td>
                        </tr>
                      </React.Fragment>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Synthesized Summary */}
              {activeReport.explanation && (
                <div style={{
                  background: '#f0fdfa',
                  border: '1px solid #99f6e4',
                  borderRadius: '12px',
                  padding: '16px',
                  fontSize: '0.88rem',
                  color: '#134e4a',
                  lineHeight: '1.6'
                }}>
                  <div style={{ fontWeight: 700, marginBottom: '6px' }}>📋 Plain-Language Clinician Synthesis:</div>
                  <div style={{ whiteSpace: 'pre-line' }}>{activeReport.explanation}</div>
                </div>
              )}
            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: '#64748b' }}>
              Select a report from the list or upload a document to begin.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

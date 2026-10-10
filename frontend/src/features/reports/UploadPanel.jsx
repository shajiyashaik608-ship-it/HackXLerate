import React, { useState } from 'react';
import { reportService, OCR_STAGES } from '../../services/reportService';
import { validateFile } from '../../utils/validation';

export default function UploadPanel({ onUploadSuccess }) {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [category, setCategory] = useState('Blood Test');
  const [notes, setNotes] = useState('');
  const [error, setError] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState(null);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  };

  const handleFileSelected = (file) => {
    setError('');
    const validationError = validateFile(file, 10);
    if (validationError) {
      setError(validationError);
      setSelectedFile(null);
      return;
    }
    setSelectedFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select or drag a medical document first.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const processedReport = await reportService.processDocument(selectedFile, (stage) => {
        setCurrentStage(stage);
      });

      if (notes.trim()) {
        processedReport.doctorNotes = notes.trim();
      }
      if (category) {
        processedReport.category = category;
      }

      onUploadSuccess(processedReport);
      setSelectedFile(null);
      setNotes('');
      setCurrentStage(null);
    } catch (err) {
      setError('Simulated OCR extraction encountered an error. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <h3 style={{ fontSize: '1.15rem', color: 'var(--text-primary)', margin: 0 }}>
          📤 Upload Diagnostic Lab Report
        </h3>
        <span className="badge badge-primary">OCR Simulation</span>
      </div>
      <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
        Add your thyroid panel, fasting insulin, or lipid report (PDF, PNG, JPG up to 10MB). Files are parsed locally in browser memory.
      </p>

      {error && (
        <div style={{
          background: 'var(--coral-50)',
          color: 'var(--coral-700)',
          padding: '10px 14px',
          borderRadius: 'var(--radius-sm)',
          fontSize: '0.82rem',
          marginBottom: '14px',
          border: '1px solid var(--coral-500)'
        }}>
          ⚠️ {error}
        </div>
      )}

      {isProcessing && currentStage && (
        <div style={{
          background: 'var(--primary-50)',
          border: '1px solid var(--primary-200)',
          borderRadius: 'var(--radius-md)',
          padding: '16px',
          marginBottom: '18px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', fontWeight: 600, color: 'var(--primary-900)', marginBottom: '8px' }}>
            <span>{currentStage.name}</span>
            <span>{currentStage.percent}%</span>
          </div>
          <div style={{ height: '6px', background: 'var(--primary-200)', borderRadius: '3px', overflow: 'hidden' }}>
            <div
              style={{
                width: `${currentStage.percent}%`,
                height: '100%',
                background: 'linear-gradient(90deg, var(--primary-600), var(--primary-800))',
                transition: 'width 0.3s ease'
              }}
            />
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Dropzone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleFileDrop}
          style={{
            border: `2px dashed ${dragOver ? 'var(--primary-600)' : 'var(--border-subtle)'}`,
            borderRadius: 'var(--radius-md)',
            padding: '24px 16px',
            textAlign: 'center',
            backgroundColor: dragOver ? 'var(--primary-50)' : 'var(--bg-subtle)',
            cursor: 'pointer',
            marginBottom: '16px',
            transition: 'all 0.2s ease'
          }}
          onClick={() => document.getElementById('report-file-input').click()}
        >
          <input
            id="report-file-input"
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileInputChange}
            style={{ display: 'none' }}
          />

          <div style={{ fontSize: '2rem', marginBottom: '8px' }}>
            {selectedFile ? '📄' : '📁'}
          </div>

          {selectedFile ? (
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-primary)' }}>
                {selectedFile.name}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                {(selectedFile.size / 1024).toFixed(1)} KB • Ready for extraction
              </div>
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); setSelectedFile(null); }}
                className="btn btn-ghost btn-sm"
                style={{ color: 'var(--coral-600)', marginTop: '6px', padding: '2px 8px' }}
              >
                Change document
              </button>
            </div>
          ) : (
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.88rem', color: 'var(--text-primary)' }}>
                Drag & drop medical report here, or <span style={{ color: 'var(--primary-700)', textDecoration: 'underline' }}>browse</span>
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                PDF, PNG, JPG (Max 10MB)
              </div>
            </div>
          )}
        </div>

        {/* Category & Notes */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
              Document Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{ width: '100%', fontSize: '0.85rem' }}
            >
              <option value="Blood Test">Blood Panel / Routine</option>
              <option value="Thyroid Profile">Thyroid (TSH / T3 / T4)</option>
              <option value="Metabolic & Insulin">Metabolic & Fasting Insulin</option>
              <option value="Hormonal Profile">Hormones (LH / FSH / Testosterone)</option>
              <option value="Pelvic Ultrasound">Pelvic Ultrasound Scan</option>
              <option value="Prescription">Clinician Prescription</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '4px' }}>
              Clinician Context / Notes
            </label>
            <input
              type="text"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="e.g. Ordered by Dr. Sneha"
              style={{ width: '100%', fontSize: '0.85rem' }}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={!selectedFile || isProcessing}
          className="btn btn-primary"
          style={{ width: '100%' }}
        >
          {isProcessing ? '⚡ Parsing Diagnostic Biomarkers...' : '🔍 Parse & Extract Biomarkers'}
        </button>
      </form>
    </div>
  );
}
